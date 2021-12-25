

# import gc
import time
import random
# import _thread
import datetime
# import threading
import numpy as np
from pyTCP import *
# from Log_Tools import *
from Pytorch_Model import *
from client_generator import *
# import matplotlib.pyplot as plt
from client_control_algorithm import *
#from plotO import FirstScreen

t_img = []
t_lab = []

#fs = FirstScreen()
fs = 0

# from plotO import FirstScreen
# Screen1 = FirstScreen()

# Set number of phones to connect
numOfPhone = 3

# Ignore
numOfConnect = None

def FL_server_pre_process(num_of_client, num_of_client_connect, ti, d_f):
    global t_img, t_lab, numOfConnect
    # create model and network
    # new_model = load_model("models/standard_model.pkl") 
    new_model = Model()
    save_model(new_model, "models/standard_model_RS.pkl")
    # init clients with data 
    client_set, t_img, t_lab = p2_init_client_with_data(num_of_client, ti, d_f)
    # show data distribution
    p2_show_client_with_data(client_set)
    
    #socketServer = create_socket_server(num_of_client_connect)
    socketServer = create_socket_server_for_show(num_of_client_connect, numOfPhone)
    #print(socketServer.cliList)
    
    # assign id to phone
    numOfConnect = num_of_client_connect
    for i in range(num_of_client_connect+1, num_of_client_connect+numOfPhone+1):
        socketServer.send_raw_msg(i, client_set[i-num_of_client_connect-1].ID)
    
    # get upload and compute time 
    
    # create and save a network and use it to test speed
    # save model to test_speed.pkl
    save_model(new_model, "models/test_speed.pkl")
    for i in range(num_of_client_connect):
        client = client_set[i]
        pos = client.ID
        upload_time = socketServer.server_get_recv_speed(pos)
        compute_speed = socketServer.recvMSG(pos)
        compute_speed /= 1000
        client.get_time_info(compute_speed, upload_time)
        print("\nclient {}:".format(pos))
        print("  |_ average upload time: {}s".format(upload_time))
        print("  |_ unit data compute time: {}s".format(compute_speed))
    # hand out train data to all client
    for i in range(num_of_client_connect):
        client = client_set[i]
        p2_server_send_data(socketServer, client)

    # create and save network to local file
    print()
    print("---"*22, "pre process finished", "\n")
    
    return socketServer, client_set

def gen_useful_data(selected_client, client_set):

    tlab = []
    clients = [ i+1 for i in range(len(client_set))]
    tc = [ 0 for i in clients ]
    tu = [ 0 for i in clients ]
    for i in selected_client:
        cli = client_set[i]
        #clients.append(cli.ID)
        #print(cli.real_time_computation)
        #print(cli.real_time_upload)
        p = cli.ID
        tc[p-1] = cli.real_time_computation
        tu[p-1] = cli.real_time_upload
    return clients, tc, tu


def TS_FL_every_algorithm(round_num, socketServer, flg_para, algr, client_selected, client_set, model_name, log_file_name, round_log):
    # get test data
    global t_img, t_lab, fs
    
   
    st_time = time.time()
    
    hand_out_standard_model(round_num, socketServer, client_selected, client_set, model_name)
    fire_starting_gun(socketServer, client_selected, client_set)
    # recieve model one by one
    recv_local_model(socketServer, client_selected, client_set, t_img, t_lab, fs)
    
    # aggregation
    tot_time = time.time() - st_time
    aggregate(client_selected, client_set, model_name)
    
    tot_time_ = 0
    
    for i in client_selected:
        client = client_set[i]
        pos = client.ID
        socketServer.sendMSG(pos, 1)
        t_download = socketServer.recvMSG(pos)
        t_compute = socketServer.recvMSG(pos)
        t_upload = socketServer.recvMSG(pos)
        client.get_log_time(t_download, t_compute, t_upload)
        
    if flg_para:
        tot_time = tot_time_
        
    # show acc
    aggr_loss, aggr_acc = evaluate(model_name, t_img, t_lab)
    print("\tACC -> total loss: {:.5}, acc: {:.5}".format(aggr_loss, aggr_acc))
    for i in client_selected:
        client = client_set[i]
        pos = client.ID
        local_file_name = "models/model{}.pkl".format(pos)
        local_loss, local_acc = evaluate(local_file_name, client.train_images, client.train_labels)
        print("\t\t(client {})  loss: {:.5}, acc: {:.5}".format(pos, local_loss, local_acc))
        client.get_local_accuracy(local_loss, local_acc)
    print()
    # show time 
    print("\tTime-> total time: {:.5}s".format(tot_time))
    for i in client_selected:
        client = client_set[i]
        pos = client.ID 
        print("\t\t(client {}) download: {:.5}s, compute: {:.5}s, upload: {:.5}s".format(pos, client.log_download_t, client.log_compute_t, client.log_upload_t))
    print("\n")
    
    # Log Round/Algorithm/data type( num of data, num of label, label type )/accury(local and total/cost time)
    # log_round_time(round_num, algr, client_selected, client_set, (aggr_loss, aggr_acc), tot_time, log_file_name)
    #plt.clf()
    # Screen1.update_glob(aggr_acc, aggr_loss)
    clients, tc, tu = gen_useful_data(client_selected, client_set)
    # Screen1.update_cli(clients, tc, tu)
    # gc.collect()
    for i in range(numOfConnect+1, numOfConnect+numOfPhone+1):
        #print('send to ', i )
        socketServer.send_raw_msg(i, client_set[i-numOfConnect-1].local_loss)
        

def TS_process_every_round(round_num, socketServer, flg_para, round_log, client_set, num_of_client_connect, K, log_file_name="round_time_log.txt"):
    
    print("----{}th round FL\n".format(round_num))
    # select clients using MILP
    num_of_client = len(client_set)
    client_fraction_selected = [ i for i in range(num_of_client_connect) ] # avil 
    
    # Random selection
    model_name_RS = "models/standard_model_RS.pkl"
    client_selected_RS = randomly_select(client_fraction_selected, K)
    #print(client_selected_RS)
    
    # send chosen one
    for i in range(num_of_client_connect+1, num_of_client_connect+numOfPhone+1):
        #print('send to', i)
        if i-1-num_of_client_connect in client_selected_RS:    
            socketServer.send_raw_msg(i, 1)
        else:
            socketServer.send_raw_msg(i, 0)
    
    TS_FL_every_algorithm(round_num, socketServer, flg_para, "RS", client_selected_RS, client_set, model_name_RS, log_file_name, round_log)


def gen_add_list(num_of_client, dis_info, flg_same_type):
    if flg_same_type == True:
        mean = dis_info[0]
        return [ mean for i in range(num_of_client) ]
    else:
        mean = dis_info[0]
        sig = dis_info[1]
        s = np.random.normal(mean, sig, num_of_client)
        l = [ x for x in s ]
        return l

def FL_control(SEED, E, K, bt_size, epoch, l_rate, decay_rate, ti, d_f, num_of_client, num_of_client_connect, num_of_round, download_dis_info, compute_dis_info, upload_dis_info, flg_same_type, flg_para):
    log_file = "round_time_log.txt"
    f = open(log_file, "a")
    the_time = datetime.datetime.now()
    f.write("\n{}\n".format(the_time))
    
    np.random.seed(SEED)
    random.seed(SEED)
    socketServer, client_set = FL_server_pre_process(num_of_client, num_of_client_connect, ti, d_f)
    
    # tell num of round
    tell_every_client(socketServer, num_of_client_connect, num_of_round)
    # tell E
    tell_every_client(socketServer, num_of_client_connect, E)
    tell_every_client(socketServer, num_of_client_connect, bt_size)
    tell_every_client(socketServer, num_of_client_connect, epoch)
    tell_every_client(socketServer, num_of_client_connect, l_rate)
    tell_every_client(socketServer, num_of_client_connect, decay_rate)
    # tell random seed 
    
    tell_every_client(socketServer, num_of_client_connect, SEED)
    
    # create wave
    l_add_download = gen_add_list(num_of_client, download_dis_info, flg_same_type)
    l_add_compute = gen_add_list(num_of_client, compute_dis_info, flg_same_type)
    l_add_upload = gen_add_list(num_of_client, upload_dis_info, flg_same_type)
    generate_constant_clients(client_set, l_add_download, l_add_compute, l_add_upload)

    # Log 
    round_log = []
    # do n rounds federated learning
    for i in range(num_of_round):
        TS_process_every_round(i+1, socketServer, flg_para, round_log, client_set, num_of_client_connect, K)

    # do some plot here using round_log list
    # e.g



if __name__ == "__main__":

    FL_control(
        SEED= 10,
        E= 10, # iteration
        K= 1, # num of choice client
        bt_size=64,
        epoch=1,
        l_rate=0.01,
        decay_rate=0.996,
        ti= 2, # non-iid type 1,2,4,8
        d_f= 0.6, # data fraction
        num_of_client= 10,   
        # set number of devices to connect
        num_of_client_connect= 3,
        num_of_round= 4000000,
        download_dis_info=(0,0.5),
        compute_dis_info=(0,0.5), # (mean, sig)
        upload_dis_info=(0,0.5), 
        flg_same_type=True, # same distribution or not
        flg_para=False # control parallel or serial
    )
    # plt.show()


