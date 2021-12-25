import socket, os, time, sys, torch
import numpy as np
from plotO import *

class myTCP:
    def __init__(self, IP, PORT):
        self.IP = IP
        self.PORT = PORT
        self.cliList = []
        print("\tIP:{}\n\tPORT:{}\n".format(IP,PORT))
        self.numBUFSIZE = 4
        self.f_buf_size = 256

    def connectAsServer(self):
        self.Socket = socket.socket()
        self.Socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try:
            self.Socket.bind((self.IP, self.PORT))
        except socket.error as e:
            print(str(e)) 

    def connectAsClient(self, posClient):
        self.Socket = socket.socket()
        try:
            self.Socket.connect((self.IP, self.PORT))
            self.cliList = [0]*posClient + [self.Socket]
        except socket.error as e:
            print(str(e))
            
    def disConnect(self):
        self.Socket.close()

    def lisClient(self, numTotal):
        self.Socket.listen(numTotal)   
        self.cliList = [0] * (numTotal+1)

    def getClient(self, posClient):
        Client, Addr = self.Socket.accept()
        self.cliList[posClient] = Client
        return Client

    def send_msg(self, posClient, msgSend): # msg: int
        conn = self.cliList[posClient]
        msg = msgSend.to_bytes(self.numBUFSIZE, "big") 
        conn.send(msg)
        #print('sent :', msgSend)
    
    def recv_msg(self, posClient=1):
        conn = self.cliList[posClient]
        msg = conn.recv(self.numBUFSIZE)
        msgRecv = int.from_bytes(msg, byteorder="big") 
        #print("revieved :", msgRecv)
        return msgRecv
    
    def sendMSG(self, posClient, msgSend):
        if type(msgSend) == int:
            self.send_msg(posClient, 0)
            self.send_msg(posClient, msgSend)
        else:
            self.send_msg(posClient, 1)
            msg = int(msgSend*1e8)
            self.send_msg(posClient, msg)
    
    def send_raw_msg(self, posClient, msg):
        msgSend = int(msg*1e5)
        self.send_msg(posClient, msgSend)
        
        
    def recvMSG(self, posClient=1):
        opt = self.recv_msg(posClient)
        if opt == 0:
            msg = self.recv_msg(posClient)
        else:
            msgRecv = self.recv_msg(posClient)
            msg = msgRecv / 1e8
        return msg

            
    def sendFile(self, posClient, file_name):
        self.sendMSG(posClient, 1)
        self.recvMSG(posClient)
        st_ = time.time()
        conn = self.cliList[posClient]
        f = open(file_name, "rb")
        file_msg = []
        file_size = 0
        buf_size = self.f_buf_size
        while True:
            data = f.read(buf_size)
            if not data:
                break
            file_msg.append(data)
            file_size += len(data)
        f.close()
        self.sendMSG(posClient, file_size)
        for msg in file_msg:
            conn.send(msg)
        self.recvMSG(posClient)
        #tm_s = time.time() - st_
        self.sendMSG(posClient, 1)
        return time.time() - st_

    def recvFile(self, posClient, file_name):
        self.recvMSG(posClient)
        self.sendMSG(posClient, 1)
        st_ = time.time()
        conn = self.cliList[posClient]
        file_size = self.recvMSG(posClient)
        buf_size = self.f_buf_size
        recv_size = 0
        file_msg = []
        while recv_size != file_size:
            if file_size - recv_size > buf_size:
                data = conn.recv(buf_size)
            else:
                data = conn.recv(file_size-recv_size)
            recv_size += len(data)
            #clear_local_line()
            #print_without_trace(" recieved {}/{}".format(recv_size, file_size))
            file_msg.append(data)
        f = open(file_name, "wb")
        for msg in file_msg:
            f.write(msg)
        f.close()
        #tm_r = time.time() - st_
        self.sendMSG(posClient, 1)
        self.recvMSG(posClient)
        return time.time() - st_
         
        
    def server_get_recv_speed(self, posClient, interval=3):
        #print("Pre process: test average upload speed ")
        self.sendFile(posClient, "models/test_speed.pkl")
        tm_ = 0
        for i in range(interval):
            #print("*")
            tm_ += self.recvFile(posClient, "models/ser_testSpeed.pkl")
        #ed_time = time.time()
        avg_time = tm_ / interval
        #print(avg_time, "s")
        return avg_time
        
    def client_get_send_speed(self, posClient=1, interval=3):
        print("Pre process: test upload speed!")
        self.recvFile(posClient, "models/cli_testSpeed.pkl")
        for i in range(interval):
            self.sendFile(posClient, "models/cli_testSpeed.pkl")
            
    def client_submit_compute_time(self, posClient=1, filePath="compute_speed.txt"):
        f = open("compute_speed.txt", "r")
        compute_speed = eval(f.read())
        f.close()
        self.sendMSG(posClient, compute_speed)
    
def get_IP():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 8009))
        IP = s.getsockname()[0]
    finally:
        s.close()
    return IP
    
def get_IP_2():
    pass

def create_socket_server(numOfClient, PORT=8240):
    #host = socket.gethostname()
    #IP = socket.gethostbyname(host)
    IP = get_IP()
    socketServer = myTCP(IP, PORT)
    socketServer.connectAsServer()
    socketServer.lisClient(numOfClient)
    for i in range(1, numOfClient+1):
        socketServer.getClient(i)
        print("connected to client {}".format(i))
    print("\nConnected to all {} clients!".format(numOfClient))
    return socketServer

def create_socket_server_for_show(numOfClient, numOfPhone=1, PORT=8240):
    IP = get_IP()
    socketServer = myTCP(IP, PORT)
    socketServer.connectAsServer()
    socketServer.lisClient(numOfClient+numOfPhone)
    for i in range(1, numOfClient+1):
        socketServer.getClient(i)
        print("connected to client {}".format(i))
    print("\nConnected to all {} clients!\n".format(numOfClient))
    for i in range(numOfClient+1, numOfClient+numOfPhone+1):
        socketServer.getClient(i)
        print("connected to Phone {}".format(i-numOfClient))
    print("\nConnected to all {} phones!".format(numOfPhone))
    return socketServer

def create_socket_client(IP, PORT=8240):
    # IP = input("Please enter IP addr:")
    socketClient = myTCP(IP,PORT)
    socketClient.connectAsClient(1)
    return socketClient

def save_data_to_file(data_img, data_lab, img_name="data/compute_img.npy", lab_name="data/compute_lab.npy"):
    np.save(img_name, data_img)
    np.save(lab_name, data_lab)

def read_data_from_file(img_name="data/compute_img.npy", lab_name="data/compute_lab.npy"):
    train_img = np.load(img_name)
    train_lab = np.load(lab_name)
    return train_img, train_lab
        
def server_send_each_train_data_pack(socketServer, posClient, packNum, train_raw_img, train_raw_lab):
    train_images_name = "data/train_image_send{}.npy".format(packNum)
    train_labels_name = "data/train_label_send{}.npy".format(packNum)
    train_img = [ np.array(t) for t in train_raw_img ]
    train_lab = np.array(train_raw_lab)
    np.save(train_images_name, train_img)
    np.save(train_labels_name, train_lab)
    socketServer.sendFile(posClient, train_images_name)
    socketServer.sendFile(posClient, train_labels_name)
    #clear_local_line()
    #rint_without_trace("sent training data! pack{}".format(packNum))

def client_recv_each_train_data_pack(socketClient, packNum):
    train_images_name = "data/train_image_recv{}.npy".format(packNum)
    train_labels_name = "data/train_label_recv{}.npy".format(packNum)
    socketClient.recvFile(1, train_images_name)
    #time.sleep(0.1)
    socketClient.recvFile(1, train_labels_name)
    print("recv training data! pack{}".format(packNum))
   


def client_get_data_from_pool(packNum):
    train_images_name = "data/train_image_recv{}.npy".format(packNum)
    train_labels_name = "data/train_label_recv{}.npy".format(packNum)
    train_raw_img = np.load(train_images_name)
    train_raw_lab = np.load(train_labels_name)
    train_img = [ torch.from_numpy(t) for t in train_raw_img ]
    train_lab = [ int(lab) for lab in train_raw_lab ]
    return train_img, train_lab

def p2_server_send_data(socketServer, client):
    pos = client.ID
    train_img = client.train_images
    train_lab = client.train_labels
    server_send_each_train_data_pack(socketServer, pos, 0, train_img, train_lab)

def p2_client_recv_data(socketClient):
    client_recv_each_train_data_pack(socketClient, 0)

def server_send_packs(socketServer, client): # num from 0
    pos = client.ID
    packOfData = len(client.train_img_pool)
    socketServer.sendMSG(pos, packOfData)
    for i in range(packOfData):
        train_img = client.train_img_pool[i]
        train_lab = client.train_lab_pool[i]
        server_send_each_train_data_pack(socketServer, pos, i, train_img, train_lab)
    
def client_recv_packs(socketClient):
    packOfData = socketClient.recvMSG(1)
    for i in range(packOfData):
        client_recv_each_train_data_pack(socketClient, i)
    return packOfData
    
def hand_out_standard_model(num_of_round, socketServer, client_selected, client_set, modelName="models/standard_model.pkl"):
    for i in client_selected:
        client = client_set[i]
        pos = client.ID
        num_pack = client.num_pack
        add_download_time = client.download_time_add
        add_compute_time = client.compute_time_add
        add_upload_time = client.upload_time_add
        
        socketServer.sendMSG(pos, num_of_round)
        socketServer.sendMSG(pos, num_pack)
        socketServer.sendMSG(pos, add_download_time)
        socketServer.sendMSG(pos, add_compute_time)
        socketServer.sendMSG(pos, add_upload_time)
        
        time.sleep(add_download_time)
        td = socketServer.sendFile(pos, modelName) + add_download_time
        #print("td", td)
        client.log_download_t = td

def recv_standard_model(socketClient):
    num_of_round = socketClient.recvMSG()
    num_pack = socketClient.recvMSG()
    add_download_time = socketClient.recvMSG()
    add_compute_time = socketClient.recvMSG()
    add_upload_time = socketClient.recvMSG()
    time.sleep(add_download_time)
    td = socketClient.recvFile(1, "models/local_model.pkl")
    return num_of_round, num_pack, add_compute_time, add_upload_time, td + add_download_time

def tell_every_client(socketServer, num_of_client, info):
    for i in range(1, num_of_client+1):
        socketServer.sendMSG(i, info)

def fire_starting_gun(socketServer, client_selected, client_set):
    for i in client_selected:
        client = client_set[i]
        socketServer.sendMSG(client.ID, 1)

def listen_to_starting_gun(socketClient):
    socketClient.recvMSG()

def send_local_model(socketClient, add_upload_time, fileName="models/local_model.pkl"):
    listen_to_starting_gun(socketClient)
    #st_ = time.time()
    time.sleep(add_upload_time)
    tu = socketClient.sendFile(1, fileName) + add_upload_time
    #ed_ = time.time()
    return tu
    
def recv_local_model(socketServer, client_selected, client_set, t_img, t_lab, fs):
    for i in client_selected:
        client = client_set[i]
        pos = client.ID
        socketServer.sendMSG(pos, 0)
        st_time = time.time()
        tu = socketServer.recvFile(pos, "models/model{}.pkl".format(pos))
        #fs.update_img(t_img, t_lab)
        #ed_time = time.time()
        #tm_u = ed_time - st_time
        #client.log_upload_t = tm_u

# utils
def print_without_trace(content):
    sys.stdout.write(content)
    sys.stdout.write("\r")
    sys.stdout.flush()

def clear_local_line():
    content = ' '* 100
    print_without_trace(content)

    