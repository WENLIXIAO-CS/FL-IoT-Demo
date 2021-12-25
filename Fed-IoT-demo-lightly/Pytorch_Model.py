import numpy as np
import torch
import time
from torch.autograd import Variable
import torchvision.transforms as transforms
import torchvision.datasets as dsets
import collections
import torch.utils.data as data



class Model(torch.nn.Module):
    def __init__(self, input_dim=784, output_dim=10):
        super(Model, self).__init__()
        self.linear = torch.nn.Linear(input_dim, output_dim)
        self.input_dim = input_dim
        self.output_dim = output_dim
    
    def forward(self, x):
        outputs = self.linear(x)
        return outputs

class MyDataset(data.Dataset):
    def __init__(self, images, labels):
        self.images = images
        self.labels = labels

    def __getitem__(self, index): # return tensor type
        img, target = self.images[index], self.labels[index]
        return img, target

    def __len__(self):
        return len(self.images)

def get_mnist_train_list():
    # build-in mnist dataset
    train_dataset = dsets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=False)
    img_list = [ x for x, y in train_dataset ]
    lab_list = [ y for x, y in train_dataset ]
    return img_list, lab_list

def exp_data():
    train_dataset = dsets.MNIST(root='./data', train=True, transform=transforms.ToTensor(), download=False)
    for (x, y) in train_dataset:
        print( type(x), type(y) )

#exp_data()
     
def transform_train_list(images_list, labels_list, bt_size):
    train_images = [ img for img in images_list ]
    train_labels = [ lab for lab in labels_list ]
    #print("type", type(train_images[0]))
    new_dataset = MyDataset(train_images, train_labels)
    train_loader = torch.utils.data.DataLoader(dataset=new_dataset, batch_size=bt_size, shuffle=False)
    return train_loader


def evaluate(model_name, test_images, test_labels, l_rate=0.001):
    test_model = load_model(model_name) 
    test_loader = transform_train_list(test_images, test_labels, 1)
    
    # init
    correct = 0
    total = 0
    loss = 0
    #optimizer = torch.optim.SGD(test_model.parameters(), lr=l_rate)
    criterion = torch.nn.CrossEntropyLoss() 
    
    # get acc & loss
    for i, (img, lab) in enumerate(test_loader):
        img = Variable(img.view(-1, 28 * 28))
        lab = Variable(lab)
        #optimizer.zero_grad()
        outputs = test_model(img)
        loss += criterion(outputs, lab)
        #optimizer.step()
        _, predicted = torch.max(outputs.data, 1)
        total+= lab.size(0)
        correct+= (predicted == lab).sum()
        
    # get average
    loss /= len(test_labels)
    accuracy = int(correct)/total  
    
    return loss, accuracy

#训练函数
def train(train_model, train_raw_img, train_raw_lab, E, bt_size=100, epochs=1, lr_rate=0.001): # E means iteration
    # get train loader
    train_loader = transform_train_list(train_raw_img, train_raw_lab, bt_size)
    # 计算 softmax 分布之上的交叉熵损失
    criterion = torch.nn.CrossEntropyLoss() 
    #SGD
    optimizer = torch.optim.SGD(train_model.parameters(), lr=lr_rate)
    # train
    tms = []
    #tic = time.time()
    for epoch in range(epochs):
        print('epoch {}:'.format(epoch + 1))
        for i in range(E):
            print("--\titeration {}".format(i+1))
            img, lab = next(iter(train_loader))
            img = Variable(img.view(-1, 28 * 28))
            lab = Variable(lab)
            optimizer.zero_grad()
            tic = time.time()
            outputs = train_model(img)
            #print(lab)
            loss = criterion(outputs, lab)
            loss.backward()
            optimizer.step()
            toc = time.time()
            tms.append(toc-tic)
            #print(loss)
    #toc = time.time()
    return np.sum(tms)

def save_model(model,path):
    # torch.save(model, path, _use_new_zipfile_serialization=False)
    torch.save(model, path)
    
def load_model(model_name):
    model = torch.load(model_name)
    return model

def aggregate(client_select, client_set, model_name): 

    models_list = []
    for i in client_select:
        client = client_set[i]
        name = 'models/model{}.pkl'.format(client.ID)
        model = torch.load(name)
        models_list.append(model)     
    models_dict = [i.state_dict() for i in models_list]
    weight_keys = list(models_dict[0].keys())
    server_model_dict = collections.OrderedDict() 
    for key in weight_keys:
        key_sum = 0
        sumation = 0
        for i in range(len(models_list)):
            client = client_set[ client_select[i] ]
            key_sum += models_dict[i][key] * client.num_traindata
            sumation += client.num_traindata
        server_model_dict[key] = key_sum / sumation
    server_model = torch.load(model_name)
    server_model.load_state_dict(server_model_dict)
    torch.save(server_model, model_name, _use_new_zipfile_serialization=False)
    #print('aggregation done!')
 
def predict(model_name, img):
    img = Variable(img.view(-1, 28 * 28))
    model = torch.load(model_name)
    lab = model(img)
    x = -100
    p = 0
    #print(lab[0])
    print("hh", lab)
    for i in range(len(lab[0])):
        if lab[0][i].double() > x:
            print(lab[0][i].double(), i)
            x = lab[0][i].double()
            p = i
    #print("hhhhhh", lab, p)
    return p


