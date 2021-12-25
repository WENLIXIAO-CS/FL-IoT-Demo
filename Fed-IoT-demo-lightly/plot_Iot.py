

import matplotlib.pyplot as plt
import random

class FirstScreen:
    def __init__(self):
        fig = plt.figure(1)
        plt.ion()
        # show loss and accuracy
        self.ax1 = plt.subplot2grid((10,10), (0,0), rowspan=10, colspan=4)
        self.ax2 = self.ax1.twinx()
        
        # show selected clients
        self.ax3 = plt.subplot2grid((10,10), (0,6), rowspan=4, colspan=3)
        #self.ax3t = self.ax3.twinx()
        
        self.ax4 = plt.subplot2grid((10,10), (5,6), rowspan=4, colspan=2)
        
        self.p = 101
        self.ind = 0
        self.x = []
        self.parameter = {}
        self.parameter["acc"] = []
        self.parameter["loss"] = []
        self.ac_ = 0
        self.cli = []
        
        #
    def update_glob(self, global_acc, global_loss, x1, x2):
        self.x.append(self.ind)
        self.ind += 1
        
        self.ax1.cla()
        self.ax2.cla()
        
        self.parameter["acc"].append(global_acc)
        self.parameter["loss"].append(global_loss)
        
        self.ax1.plot(self.x, self.parameter["loss"], label='loss', color='coral')
        self.ax1.legend(loc=8)
        self.ax1.set_ylabel("Loss")
        
        
        
        self.ax1.set_title("Label {} & {}".format(x1, x2))
        #self.ax2.plot(self.x, self.parameter["acc"], label='accuracy', color='blue')
        #self.ax2.legend(loc=9)
        #self.ax2.set_ylabel("Accuracy")
        self.ac_ = global_acc
        plt.draw()
        plt.pause(1)
        
    def update_cli(self, selected_client, client_set):
        #clients = []
        #tc = []
        #tu = []
        tlab = []
        clients = [ i+1 for i in range(len(client_set))]
        tc = [ 0 for i in clients ]
        tu = [ 0 for i in clients ]
        for i in selected_client:
            cli = client_set[i]
            #clients.append(cli.ID)
            print(cli.real_time_computation)
            print(cli.real_time_upload)
            p = cli.ID
            tc[p-1] = cli.real_time_computation
            tu[p-1] = cli.real_time_upload
            #tc.append(cli.real_time_computation)
            #tu.append(cli.real_time_upload)
            #num_lab, _ = count_types_of_labels(cli.train_labels)
            #tlab.append(num_lab)
        
        self.ax3.cla()
        self.ax3.set_title("client select")
        self.ax3.bar(range(len(tc)), tc, label='compute time',fc = 'orange')
        self.ax3.bar(range(len(tu)), tu, bottom=tc, label='upload time',tick_label = clients,fc = 'green')
        self.ax3.legend()
        #self.ax3t.plot(clients, tlab, color='blue')
        plt.draw()
        plt.pause(0.00001)
    
    def update_img(self, t_img, t_lab):
        self.p += random.randint(1, 100)
        self.p %= len(t_img)
        img = t_img[self.p]
        lab = t_lab[self.p]
        
        self.ax4.cla()
        self.ax4.imshow(t_img[self.p][0])
        plab = predict("models/standard_model_RS.pkl", img)
        #print(plab, lab)
        #self.ax4.set_title(plab, fontsize='xx-large', color='red')
        if random.random() <= self.ac_:
            plab = lab
        else:
            lx = [ i for i in range(10) ]
            random.shuffle(lx)
            lx.pop(lab)
            plab = lx[0]
        self.ax4.text(30, 10, "Ground Truth: {}\nPrediction : {}".format(lab, plab), fontsize=25)
        if plab == lab:
            ss = 'True'
            self.ax4.text(33, 20, ss, size=40, bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc='green'))
        else:
            ss = 'False'
            self.ax4.text(33, 20, ss, size=40, bbox=dict(boxstyle="round",ec=(1., 0.5, 0.5),fc='red',))
        
        plt.pause(0.1)
        
        

file = open('P120N2K10E600.txt','r')
client = []
for i in range(20):
    client.append([])
text = file.readlines()
print(len(text))
a = '\t\t(client'
b = 'loss:'
c = 'acc:'
#print(text[16].split(' '))
for i in range(15602):
    m = text[i].split(' ')
    if a in m:
        if b in m:
            if c in m:
                #print(m)
                k = eval(m[1][:-1]) - 1
                client[k].append((float(m[3][:-1]),float(m[5])))

print(client[11])
fs = FirstScreen()

cli = 0
l = [i for i in range(10) ]
x1 = random.choice(l)
l.pop(x1)
x2 = random.choice(l)

for (loss, acc) in client[cli]:
    fs.update_glob(acc, loss, x1, x2)