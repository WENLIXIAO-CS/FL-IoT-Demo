#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 08:28:07 2020

@author: randyxiao
"""

import copy
#import cplex
import random
import numpy as np
#from tensorflow.keras import datasets
#from cplex.exceptions import CplexErro

"""
create data
"""
"""
Client stuff
"""
class Client:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.compute_speed_info = 0
        self.upload_time_info = 0
        self.real_time_computation = 0
        self.real_time_upload = 0
        self.log_compute_t = 0
        self.log_upload_t = 0
        self.log_download_t = 0
        self.download_time_add = 0
        self.compute_time_add = 0
        self.upload_time_add = 0
        self.num_traindata = 0
        self.train_images = 0
        self.train_labels = 0
        self.test_images = 0
        self.test_labels = 0
        self.train_img_pool = []
        self.train_lab_pool = []
        self.num_pack = 0
        self.local_acc = 0
        self.local_loss = 0
    
    def get_log_time(self, t_download, t_compute, t_upload):
        #self.log_download_t = t_download
        self.log_compute_t = t_compute
        self.log_upload_t = t_upload

    def get_local_accuracy(self, local_loss, local_acc):
        self.local_loss = local_loss
        self.local_acc = local_acc
    
    def get_single_train_data(self, train_img, train_lab):
        self.train_images = train_img
        self.train_labels = train_lab
        self.train_img_pool.append(train_img)
        self.train_lab_pool.append(train_lab)

    def get_train_data_pool(self, train_img, train_lab):
        self.train_img_pool.append(train_img)
        self.train_lab_pool.append(train_lab)
        
    def modify_client(self, num_pack, add_download_time, add_compute_time, add_upload_time):
        try:
            self.num_pack = num_pack
            self.train_images = self.train_img_pool[num_pack]
            self.train_labels = self.train_lab_pool[num_pack]
            self.num_traindata = len(self.train_labels)
            self.real_time_computation = self.compute_speed_info + add_compute_time + random.random()
            self.real_time_upload = self.upload_time_info + add_upload_time
            self.download_time_add = add_download_time
            self.compute_time_add = add_compute_time
            self.upload_time_add = add_upload_time
        except:
            pass
        
    def get_time_info(self, compute_speed, upload_time):
        self.compute_speed_info = compute_speed
        self.upload_time_info = upload_time
    
def init_clients_with_data_pack(numOfClients, packOfDataEachClient):
    client_set = []
    # init client
    for i in range(numOfClients):
        client_set.append(Client("client{}".format(i+1), i+1))
    
    (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
    for i in range(packOfDataEachClient):
        create_one_pack_train_data_for_all_client(client_set, train_images, train_labels)
    # get data
    return client_set

def generate_variation_clients(client_set, packOfDataEachClient, var_compute_speed, var_upload_time):
    for client in client_set:
        num_pack = random.randint(0, packOfDataEachClient-1)
        add_compute_speed = random.randint(0, var_compute_speed)
        add_upload_time = random.randint(0, var_upload_time)
        client.modify_client(num_pack, add_compute_speed, add_upload_time)

def generate_constant_clients(client_set, l_add_download_time, l_add_compute_time, l_add_upload_time):
    for i in range(len(client_set)):
        client = client_set[i]
        client.modify_client(0, l_add_download_time[i], l_add_compute_time[i], l_add_upload_time[i])


# RS

def randomly_select(client_fraction_selected, K):
    client_selected = copy.deepcopy(client_fraction_selected)
    random.shuffle(client_selected)
    return client_selected[:K]

"""
Algorithm: TDD
"""
def sort_computation_time(Client_selected, Client_set):
    client_sort = copy.deepcopy(Client_selected)
    num_client_selected = np.size(client_sort)
    
    for i in range(num_client_selected):
        for j in range(i + 1, num_client_selected):
            if Client_set[client_sort[i]].real_time_computation > Client_set[client_sort[j]].real_time_computation:
                client_sort[i], client_sort[j] = client_sort[j], client_sort[i]
                
    return client_sort

def Cplex_client_selection_emnist_nocover(Client_fraction_selected, Client_set, T_round):
    client_selected_real = []
    
    my_obj = []
    my_ub = []
    my_lb = []
    my_ctype = []
    my_colnames = []
    my_rhs = []
    my_rownames = []
    my_sense =[]
    
    client_selected_sort = sort_computation_time(Client_fraction_selected, Client_set)
    num_clients_round = np.size(client_selected_sort)
    
    for i in range(num_clients_round):
        my_obj.append(Client_set[client_selected_sort[i]].num_traindata)
        my_ub.append(1)
        my_lb.append(0)
        my_ctype.append("I")
        my_colnames.append("x" + str(i))
        
        my_obj.append(0)
        my_ub.append(1)
        my_lb.append(0)
        my_ctype.append("I")
        my_colnames.append("z" + str(i))
        
        my_obj.append(0)
        my_ub.append(T_round)
        my_lb.append(0)
        my_ctype.append("C")
        my_colnames.append("Y" + str(i))
        
        my_obj.append(0)
        my_ub.append(T_round)
        my_lb.append(0)
        my_ctype.append("C")
        my_colnames.append("T" + str(i))
        
        my_rhs.append(0)
        my_rownames.append("r" + str(i))
        my_sense.append('E')
        my_sense.append('L')
        my_sense.append('L')
        
    for i in range(3):
        for j in range(num_clients_round):
            my_rhs.append(0)
            my_rownames.append("r" + str(j + (i+1)*num_clients_round))
            
            
    for i in range(num_clients_round):
        my_rhs.append(T_round)
        my_rownames.append("r" + str(i + 4*num_clients_round))
        my_sense.append('L')
        my_sense.append('L')
    
    
    my_ctype = ''.join(my_ctype)
    my_sense = ''.join(my_sense)  
        
    try:
        my_prob = cplex.Cplex()
        my_prob.objective.set_sense(my_prob.objective.sense.maximize)
        my_prob.variables.add(obj=my_obj, lb=my_lb, ub=my_ub, types=my_ctype, names=my_colnames)
        
        rows = []
        
        for i in range(num_clients_round):
            rows.append([[my_colnames[3 + 4*i],
                          my_colnames[2 + 4*i],
                          my_colnames[4*i]],
                         [1, -1, -Client_set[client_selected_sort[i]].real_time_upload]])
        
            rows.append([[my_colnames[4*i],
                          my_colnames[2 + 4*i]],
                         [Client_set[client_selected_sort[i]].real_time_computation, -1]])
            
            rows.append([[my_colnames[2 + 4*i],
                          my_colnames[4*i],
                          my_colnames[1 + 4*i]],
                         [1, -Client_set[client_selected_sort[i]].real_time_computation, -T_round]])
        
        rows.append([[my_colnames[2]],[-1]])
        for i in range(num_clients_round - 1):
            rows.append([[my_colnames[3 + 4*i],
                          my_colnames[6 + 4*i]],
                         [1, -1]])
        
        rows.append([[my_colnames[2],my_colnames[1]],[1, T_round]])
        for i in range(num_clients_round - 1):
            rows.append([[my_colnames[6 + 4*i],
                          my_colnames[3 + 4*i],
                          my_colnames[5 + 4*i]],
                         [1, -1, T_round]])
        
        my_prob.linear_constraints.add(lin_expr=rows, senses=my_sense,
                                       rhs=my_rhs, names=my_rownames)
        my_prob.solve()

    except CplexError as exc:
        print(exc)
        
    solution = my_prob.solution.get_values()
    print("solution:", solution)
    for i in range(num_clients_round):
        if solution[4*i] > 0.9:
            client_selected_real.append(client_selected_sort[i])
    # print(x)
    #return client_selected_real
    return client_selected_real

"""
Algorithm CS
"""
def time_cost_uu(Client_selected, Client_set):
    num_clients = np.size(Client_selected)
    time_cost = 0
    for i in range(num_clients):
        if Client_set[Client_selected[i]].real_time_computation > time_cost:
            time_cost = Client_set[Client_selected[i]].real_time_computation + Client_set[Client_selected[i]].real_time_upload
        else:
            time_cost = time_cost + Client_set[Client_selected[i]].real_time_upload
            
    return time_cost

def CS_client_selection(Client_fraction_selected, Client_set, T_round):
    client_selected_real = []
    
    T_dis_real = 0
    
    while True:
        client_selected_real = sort_computation_time(client_selected_real, Client_set)
        T_uu_before = time_cost_uu(client_selected_real, Client_set)

        for i in range(np.size(Client_fraction_selected)):
            tmp_client_selected = copy.deepcopy(client_selected_real)
            tmp_client_selected.append(Client_fraction_selected[i])
                
            tmp_client_selected = sort_computation_time(tmp_client_selected, Client_set)
            T_uu_after = time_cost_uu(tmp_client_selected, Client_set)
            
            client_priority = T_uu_after - T_uu_before
            
            if i == 0:
                add_time = T_uu_after - T_uu_before
                priority_level = client_priority
                flag_add_client = 0
            elif priority_level > client_priority:
                add_time = T_uu_after - T_uu_before
                priority_level = client_priority
                flag_add_client = i
            
        if np.size(Client_fraction_selected) == 0:
            break
        else:
            if T_round >= (T_uu_before + add_time):
                client_selected_real.append(Client_fraction_selected[flag_add_client])
                T_uu_real = T_uu_before + add_time
                Client_fraction_selected = np.delete(Client_fraction_selected, flag_add_client)
            else:
                break

    if np.size(Client_fraction_selected) == 0:
        T_round_real = T_uu_real + T_dis_real
    else:
        T_round_real = T_round

    return client_selected_real

"""
Algorithm LIM

"""
def LIM_client_selection_share(Client_fraction_selected, Client_set, T_round):
    
    num_clients_round = np.size(Client_fraction_selected)
    client_selected_real = []
    
    T_uu_real_tmp = 0#初始化更新及上传时间
    T_dis_real = 0
    # for i in range(num_clients_round):#实际下发时间（取决于通信质量最差的用户）
    #     if i == 0:
    #         T_dis_real = Client_set[Client_fraction_selected[i]].real_time_distribution
    #     elif T_dis_real < Client_set[Client_fraction_selected[i]].real_time_distribution:
    #         T_dis_real = Client_set[Client_fraction_selected[i]].real_time_distribution
    
    client_computation_sort = sort_computation_time(Client_fraction_selected,Client_set)
    for i in range(num_clients_round):
        if Client_set[client_computation_sort[i]].real_time_computation > T_uu_real_tmp:
            T_uu_real_tmp = Client_set[client_computation_sort[i]].real_time_computation + Client_set[client_computation_sort[i]].real_time_upload
        else:
            T_uu_real_tmp = T_uu_real_tmp + Client_set[client_computation_sort[i]].real_time_upload
        
        if T_round > T_uu_real_tmp:
            client_selected_real.append(client_computation_sort[i])
            T_uu_real = T_uu_real_tmp
        else:
            break
    
    if np.size(client_selected_real) == num_clients_round:
        T_round_real = T_dis_real + T_uu_real
    else:
        T_round_real = T_round

    return client_selected_real




