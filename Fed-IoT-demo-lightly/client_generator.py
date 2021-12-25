import random
import numpy as np
from client_control_algorithm import *
# from Log_Tools import *
from Pytorch_Model import *

def shuffle_data(images, labels):
    l = list(zip(images, labels))
    random.shuffle(l)
    l_img = [ i for (i,j) in l ]
    l_lab = [ j for (i,j) in l ]
    return l_img, l_lab

# Non-iid
def generate_data_non_iid(client_set, n, ti, d_f, train_image, train_label): # n clients, ti iid type[1,2,4,8]
    # make packs
    data_pool_img = [ [] for i in range(10) ]
    data_pool_lab = [ [] for i in range(10) ]
    
    train_img_shuf, train_lab_shuf = shuffle_data(train_image, train_label)
    
    #print(p2_count_types_of_labels(train_lab_shuf))
    for i in range(len(train_lab_shuf)):
        lab = train_lab_shuf[i]
        data_pool_img[lab].append(train_img_shuf[i])
        data_pool_lab[lab].append(train_lab_shuf[i])
    
    d0 = int(5416 * d_f)# init size of every label
    
    D = len(train_label) # D num of data
    d =  int(d0 // (n * ti / 10)) # every label pack
    h = int(n * ti / 10) # num of layer
    d1 = d * h 
    print(D, d0, d, h, d1)
    
    ret_t_img = []
    ret_t_lab = []

    for i in range(10):
        data_pool_img[i] = data_pool_img[i][:d1]
        data_pool_lab[i] = data_pool_lab[i][:d1]
        ret_t_img += data_pool_img[i]
        ret_t_lab += data_pool_lab[i]
    
    ret_img, ret_lab = shuffle_data(ret_t_img, ret_t_lab)

    cli_index = 0

    #print(client_set)
    if ti == 1 or ti == 2:
        for i in range(h):
            label_pool = [ x for x in range(10) ]
            random.shuffle(label_pool)
            #print(label_pool)
            cli_num = int(10 / ti)
            for j in range(cli_num):
                cli_img = []
                cli_lab = []
                for k in range(ti):
                    lab = label_pool[0]
                    label_pool.pop(0)
                    #print("lab", lab)
                    #print(len(data_pool_img[lab]))
                    cli_img += data_pool_img[lab][:d]
                    cli_lab += data_pool_lab[lab][:d]
                    data_pool_img[lab] = data_pool_img[lab][d:]
                    data_pool_lab[lab] = data_pool_lab[lab][d:]
                client = client_set[cli_index]
                #p2_count_types_of_labels(cli_lab)
                client.get_single_train_data(cli_img, cli_lab)
                cli_index += 1
    
    if ti == 4:
        for i in range(h//2):
            plug_label_pool = [ x for x in range(10) ]
            random.shuffle(plug_label_pool)
            plug_label = plug_label_pool[:4]
            for j in range(2):
                label_pool = [ x for x in range(10) ]
                label_pool.remove( plug_label[j*2] ) 
                label_pool.remove( plug_label[j*2+1] )
                #print(plug_label, label_pool)
                random.shuffle(label_pool)
                for cli in range(2):
                    cli_img = []
                    cli_lab = []
                    for e in range(4):
                        lab = label_pool[e]
                        cli_img += data_pool_img[lab][:d]
                        cli_lab += data_pool_lab[lab][:d]
                        data_pool_img[lab] = data_pool_img[lab][d:]
                        data_pool_lab[lab] = data_pool_lab[lab][d:]
                    label_pool = label_pool[4:]
                    client = client_set[cli_index]
                    client.get_single_train_data(cli_img, cli_lab)
                    cli_index += 1
            # add 5 th client
            cli_img = []
            cli_lab = []
            for e in range(4):
                lab = plug_label[e]
                cli_img += data_pool_img[lab][:d]
                cli_lab += data_pool_lab[lab][:d]
                data_pool_img[lab] = data_pool_img[lab][d:]
                data_pool_lab[lab] = data_pool_lab[lab][d:] 
            client = client_set[cli_index]
            client.get_single_train_data(cli_img, cli_lab)
            cli_index += 1
    
    if ti == 8:
        for i in range(h//4):
            plug_label_pool = [ x for x in range(10) ]
            random.shuffle(plug_label_pool)
            plug_label = plug_label_pool[:8]
            for j in range(4):
                label_pool = [ x for x in range(10) ]
                label_pool.remove( plug_label[j*2] ) 
                label_pool.remove( plug_label[j*2+1] )
                cli_img = []
                cli_lab = []
                for e in range(8):
                    lab = label_pool[e]
                    cli_img += data_pool_img[lab][:d]
                    cli_lab += data_pool_lab[lab][:d]
                    data_pool_img[lab] = data_pool_img[lab][d:]
                    data_pool_lab[lab] = data_pool_lab[lab][d:]
                client = client_set[cli_index]
                client.get_single_train_data(cli_img, cli_lab)
                cli_index += 1
            # add 5 th client
            cli_img = []
            cli_lab = []
            for e in range(8):
                lab = plug_label[e]
                cli_img += data_pool_img[lab][:d]
                cli_lab += data_pool_lab[lab][:d]
                data_pool_img[lab] = data_pool_img[lab][d:]
                data_pool_lab[lab] = data_pool_lab[lab][d:] 
            client = client_set[cli_index]
            client.get_single_train_data(cli_img, cli_lab)
            cli_index += 1
    
    print("total data usage:", len(ret_lab))
    return ret_img, ret_lab

def p2_count_types_of_labels(train_lab):
    num_of_each_label = [ 0 for i in range(10)]
    num_of_total_label = 0
    for i in range( len(train_lab) ):
        x = train_lab[i]
        try:
            num_of_each_label[x] += 1
        except :
            print("x", x)
    for i in range(10):
        if num_of_each_label[i]:
            num_of_total_label += 1
            
    return num_of_total_label, num_of_each_label

def p2_show_client_with_data(client_set):
    print("\n", "---"*10, "client data distribution", "---"*10, "\n")

    # print info    
    cli = client_set[0]
    train_lab = cli.train_labels
    lab_size, labels = p2_count_types_of_labels(train_lab) 
    print("total {} clients".format(len(client_set)))
    print("unit data size:  {}".format(len(train_lab)))
    print("unit label size: {}".format(lab_size))
    print("cli\lab", end="")
    for i in range(10):
        print("\t{}".format(i), end="")
    print()
    for client in client_set:
        train_lab = client.train_labels
        lab_size, labels = p2_count_types_of_labels(train_lab)
        print("  {}".format(client.ID), end="")
        for i in range(10):
            print("\t{}".format(labels[i]), end='')
        print()
    print()
    

def p2_init_client_with_data(n, ti, d_f):
    client_set = []
    for i in range(n):
        client_set.append(Client("{}".format(i), i+1))
    train_img, train_lab = get_mnist_train_list()
    ret_img, ret_lab = generate_data_non_iid(client_set, n, ti, d_f, train_img, train_lab)
    for client in client_set:
        img, lab = shuffle_data(client.train_images, client.train_labels)
        client.train_images, client.train_labels = img, lab
    
    return client_set, ret_img, ret_lab
