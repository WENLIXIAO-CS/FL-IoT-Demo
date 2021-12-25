#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:42:48 2020

@author: randyxiao
"""

import matplotlib.pyplot as plt
import random
import socket
import time
import numpy as np
from pyTCP import *
from Pytorch_Model import *
import argparse


def FL_client_pre_process(IP):
    
    socketClient = create_socket_client(IP)
    
    socketClient.client_get_send_speed()
    socketClient.client_submit_compute_time()
    
    # recieve training data
    p2_client_recv_data(socketClient)
    
    return socketClient

def train_time_decay(num_of_round, model, t_img, t_lab, E, bt_size, epoch, l_rate, decay_rate):
    #st_ = time.time()
    new_lr = l_rate*(decay_rate**(num_of_round-1))
    print("new learning rate:", new_lr)
    tm = train(model, t_img, t_lab, E, bt_size, epoch, new_lr)
    #ed_ = time.time()
    save_model(model, "models/local_model.pkl")
    return tm

def TS_FL_every_single_train(num_of_round_1, socketClient, E, bt_size, epoch, l_rate, decay_rate):
    num_of_round, num_pack, add_compute_time, add_upload_time, td = recv_standard_model(socketClient)
    print("round", num_of_round)
    train_images, train_labels = client_get_data_from_pool(num_pack)
    
    listen_to_starting_gun(socketClient)
    # train
    print(train_labels[0])
    
    # compute 
    #st_compute_time = time.time()
    new_model = load_model("models/local_model.pkl")
    tc = train_time_decay(num_of_round, new_model, train_images, train_labels, E, bt_size, epoch, l_rate, decay_rate)
    
    time.sleep(add_compute_time)
    compute_time = tc + add_compute_time

    print("compute_finished")
    # upload model
    #st_upload_time = time.time()    
    upload_time = send_local_model(socketClient, add_upload_time)
    #upload_time = time.time() - st_upload_time

    # upload time info
    socketClient.recvMSG()
    socketClient.sendMSG(1, td)
    socketClient.sendMSG(1, compute_time)
    socketClient.sendMSG(1, upload_time)
    

def TS_process_every_round(num_of_round, socketClient, E, bt_size, epoch, l_rate, decay_rate):
   TS_FL_every_single_train(num_of_round, socketClient, E, bt_size, epoch, l_rate, decay_rate)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', help='ip address of server')
    args = parser.parse_args()

    socketClient = FL_client_pre_process(args.ip)
    
    num_of_round = socketClient.recvMSG()
    E = socketClient.recvMSG()
    bt_size = socketClient.recvMSG()
    epoch = socketClient.recvMSG()
    l_rate = socketClient.recvMSG()
    decay_rate = socketClient.recvMSG()

    SEED = socketClient.recvMSG()

    random.seed(SEED)
    
    for i in range(num_of_round):
        TS_process_every_round(
            i+1, 
            socketClient, 
            E,
            bt_size,
            epoch,
            l_rate,
            decay_rate)

        
