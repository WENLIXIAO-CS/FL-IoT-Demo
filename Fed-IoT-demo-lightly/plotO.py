#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 12:03:49 2020

@author: randyxiao
"""

import random
import matplotlib.pyplot as plt
from Log_Tools import read_log_round_time
from client_control_algorithm import Client
from Pytorch_Model import predict
from Log_Tools import count_types_of_labels


class FirstScreen:
    def __init__(self):
        
        fig = plt.figure(1)
        plt.ion()
        
        # show loss and accuracy
        self.ax1 = plt.subplot2grid((10,10), (0,0), rowspan=7, colspan=10)
        self.ax2 = self.ax1.twinx()
        
        # show selected clients
        self.ax3 = plt.subplot2grid((10,10), (8,0), rowspan=3, colspan=10)
        
        #self.ax3t = self.ax3.twinx()
        #self.ax4 = plt.subplot2grid((10,10), (5,6), rowspan=4, colspan=2)
        self.p = 101
        self.ind = 0
        self.x = []
        self.parameter = {}
        self.parameter["acc"] = []
        self.parameter["loss"] = []
        self.ac_ = 0
        self.cli = []
        
    def update_glob(self, global_acc, global_loss, ):
        self.x.append(self.ind)
        self.ind += 1
        
        self.ax1.cla()
        self.ax2.cla()
        
        self.parameter["acc"].append(global_acc)
        self.parameter["loss"].append(global_loss)
        
        self.ax1.plot(self.x, self.parameter["loss"], label='loss', color='coral')
        self.ax1.legend(loc=8)
        self.ax1.set_ylabel("Loss")
        self.ax1.set_title("Federated Learning Outcome")
        self.ax2.plot(self.x, self.parameter["acc"], label='accuracy', color='blue')
        self.ax2.legend(loc=9)
        self.ax2.set_ylabel("Accuracy")
        self.ac_ = global_acc

        plt.draw()
        plt.pause(0.00001)
        
    def update_cli_1(self, selected_client, client_set):

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
        
        self.ax3.cla()
        self.ax3.set_title("client select")
        self.ax3.bar(range(len(tc)), tc, label='compute time',fc = 'orange')
        self.ax3.bar(range(len(tu)), tu, bottom=tc, label='upload time',tick_label = clients,fc = 'green')
        self.ax3.legend()
        #self.ax3t.plot(clients, tlab, color='blue')
        plt.draw()
        plt.pause(0.00001)
    
    def update_cli(self, clients, tc, tu):

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
        plab = predict("standard_model_RS.pkl", img)
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
'''
        
Screen1 = FirstScreen()

for i in range(10000):
    a = random.random()
    b = random.random()*10
    
    Screen1.update_glob(a, b)
    #plt.pause(2)
    










'''