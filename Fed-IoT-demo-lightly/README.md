# Fed-IoT Demonstration Platform
**This code is used for Adaptive Sampling Federated Learning demonstration**

## Important

fix server ip: `192.168.43.156`

fix server port: `8240`


## Setup network for experiment
1. Turn on Wifi router
2. Connect to Wifi

    name: `FL-network`

    pwd: 88888888

3. Config Wifi

    3.1. Open browser, and enter URL: 192.168.43.1 

    3.2. user: admin pwd: admin

    3.3. PORT Management -> DHCP Setting

        3.3.1. Scan devices under this wifi

        3.3.2. Check device's connect by identity

    3.4. VLAN: address binding
        
        3.4.1. Bind address of server to a fix ip (`192.168.43.156` in this program)

        3.4.2. Tips: fix ip of devices and note them

4.  Connect Android phone to wifi

## do experiment

### Overview
on server
```
python FL_ServerMain.py
```

on client
```
python FL_ClientMain.py -ip 192.168.43.156`
```
### Platform usage workflow

1. Preparation
    1.1. add ssh-key, remove existing files, send latest code 
    ```
    sh prepare.sh
    ```
 

2. activate server `python FL_ServerMain.py`
   
3. execute code on clients

    3.1.   `sh run.sh`

4. Launch app `MySocket` on Android phone one by one



## Server prerequirement
```
pytorch 1.4
matplotlib
```
