#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 09:10:03 2020

@author: randyxiao
"""
import numpy as np
import sys
import matplotlib.pyplot as plt

class Round:
    def __init__(self,):
        self.client_size = None
        self.client_set = None
        self.total_time = None
        self.client_pos = []
        self.client_times = []
        self.total_loss = None
        self.total_acc = None
        self.client_loss_acc = []
        self.td = 0 
        self.tc = 0
        self.tu = 0
        #self.get_time_loss_acc(client_selected, client_set)
    

    def get_time(self, td, tc, tu):
        self.td = td
        self.tc = tc
        self.tu = tu

    def get_time_loss_acc(self, client_selected, client_set):
        for i in client_selected:
            client = client_set[i]
            pos = client.ID 
            self.client_pos.append(pos)
            self.client_times.append((client.log_compute_t, client.log_upload_t))
            self.client_loss_acc.append((client.local_loss, client.local_acc))

def count_types_of_labels(label_list, numOfLabels=10):
    num_of_each_label = [ 0 for i in range(numOfLabels)]
    num_of_total_label = 0
    for label in label_list:
        x = int(label)
        num_of_each_label[x] += 1
    
    for i in range(10):
        if num_of_each_label[i]:
            num_of_total_label += 1
            
    return num_of_total_label, num_of_each_label
    
def log_round_time(round_num, algr, client_selected, client_set, total_acc, total_time, fileName):
    f = open(fileName, "a")
    f.write("\n")
    # Round info
    num_of_client = len(client_selected)
    f.write("Round {} ({} clients)\n".format(round_num, num_of_client))

    f.write("\n")
    # Time info 
    f.write("\tTime-> Total: {:.5}s\n".format(total_time))
    for i in client_selected:
        client = client_set[i]
        pos = client.ID 
        tc = client.log_compute_t
        tu = client.log_upload_t
        td = client.log_download_t
        f.write("\t\t(client {}) download: {:.5}s, compute: {:.5}s, upload: {:.5}s\n".format(pos, td, tc, tu))
    
    f.write("\n")
    # acc
    f.write("\tACC -> Total loss: {:.5}, acc: {:.5}\n".format(total_acc[0], total_acc[1]))
    for i in client_selected:
        client = client_set[i]
        pos = client.ID
        local_loss = client.local_loss
        local_accy = client.local_acc
        f.write("\t\t(client {}) loss: {:.5}, acc: {:.5}\n".format(pos, local_loss, local_accy))
    f.close()
    
def read_log_round_time(file_name):
    round_log = []
    round_index = 0
    client_num = 0
    total_loss = 0
    total_time = 0
    td = 0
    tc = 0
    tu = 0
    with open(file_name, "r") as f:
        for line in f:
            if line.find('Round') != -1:
                sp = line.split()
                round_index = eval(sp[1]) - 1
                round_log.append(Round())
            
            # get loss and acc
            if line.find('ACC') != -1:
                sp = line.split()
                total_loss = eval(sp[4][:-1]) # delete ','
                total_acc = eval(sp[6])
                round_log[round_index].total_loss = total_loss
                round_log[round_index].total_acc = total_acc

            # get time
            if line.find('download') != -1:
                sp = line.split()
                td = eval(sp[3][:-2])
                tc = eval(sp[5][:-2])
                tu = eval(sp[7][:-1])
                #print(td, tc, tu)
                round_log[round_index].get_time(td,tc,tu)                

    return round_log

def output_log_data(file_name, postfix='.loss'):
    round_log = read_log_round_time(file_name)
    
    # print loss to loss.txt
    loss_list = []
    f = open(file_name + postfix, 'w')
    for round in round_log:
        loss_list.append(round.total_acc)
        f.write("{}\n".format(round.total_acc))
    print(loss_list)
    f.close()

def output_time(file_name):
    round_log = read_log_round_time(file_name)
    
    # print loss to loss.txt
    acc_list = []
    f = open(file_name + '.acc', 'w')
    for round in round_log:
        acc_list.append(round.total_acc)
        f.write("{}\n".format(round.total_acc))
    print(acc_list)
    f.close() 

def get_avg_time(file_name):
    round_log = read_log_round_time(file_name)
    td = []
    tc = []
    tu = []
    for round in round_log:
        td.append(round.td)
        tc.append(round.tc)
        tu.append(round.tu)
    tda = np.sum(td) / np.size(td)
    tca = np.sum(tc) / np.size(tc)
    tua = np.sum(tu) / np.size(tu)
    return tda, tca, tua


def show_client_data_pack(client_set):
    index = 1
    for client in client_set:
        print("client ", index, "---"*10)
        for i in range(10):
            train_lab = client.train_lab_pool[i]
            num_of_label, labels = count_types_of_labels(train_lab)
            #print("data_num:", len(train_lab), ", label_type:", num_of_label, " ", labels)
        index += 1
    
def print_without_trace(content):
    sys.stdout.write(content)
    sys.stdout.write("\r")
    sys.stdout.flush()

def clear_local_line():
    content = ' '* 100
    print_without_trace(content)

# plot

def plot_X_Y(X, Y):
    plt.plot(X, Y)
    

#output_log_data('round_time_log.txt')

#print(output_time('round_time_log.txt'))


