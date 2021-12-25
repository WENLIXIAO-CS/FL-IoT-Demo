#!/bin/bash

# USERNAME="nano"
# HOSTS="192.168.43.10 192.168.43.11 192.168.43.12 192.168.43.13 192.168.43.14 192.168.43.15 192.168.43.16 192.168.43.17 192.168.43.18 192.168.43.19"
# # HOSTS="192.168.43.10"
# SCRIPT="pwd; ls"

# # Transfer new version
# # cd ..
# DIR="$( cd "$( dirname "$0" )" && pwd )"
# echo ${DIR}

# # copy ssh-key
# for HOSTNAME in ${HOSTS} ; do
#     echo ${HOSTNAME}
#     # Copy ssh passwd
#     # ssh-copy-id nano@${HOSTNAME}

#     # Remove Old version Code
#     # ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "rm -rf /home/nano/fed-iot/fed-iot-demo-lightly
    
#     # Upload New version Code 
#     rsync -r -avu -e ssh --stats --exclude=.git --exclude=data/synthetic/ --exclude=log/* --exclude=cache/* "${DIR}" nano@${HOSTNAME}:/home/nano/fed-iot-demo-lightly
#     # scp -rp "${DIR}" nano@${HOSTNAME}:/home/nano/fed-iot

#     # Install Necessary Package
#     # ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "python -m pip install pickle5; python -m pip install tensorboardX"

# done


# prepare pi
USERNAME="pi"

# Set ip of available devices
HOSTS="192.168.43.28 192.168.43.29 192.168.43.30 192.168.43.38"
SCRIPT="pwd; ls"

# Transfer new version
# cd ..
DIR="$( cd "$( dirname "$0" )" && pwd )"
echo ${DIR}

# copy ssh-key
for HOSTNAME in ${HOSTS} ; do
    echo ${HOSTNAME}
    # copy ssh key 
    # ssh-copy-id pi@${HOSTNAME}

    # remove old version code 
    ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "rm -rf /home/nano/fed-iot/fed-iot-demo-lightly"

    # Upload new code 
    rsync -r -avu -e ssh --stats --exclude=.git --exclude=data/synthetic --exclude=log/* --exclude=cache/* "${DIR}" pi@${HOSTNAME}:/home/pi/fed-iot-demo-lightly
    # scp -rp "${DIR}" pi@${HOSTNAME}:/home/pi/fed-iot/

    # Install necessary library
    # ssh -o StrictHostKeyChecking=no -l ${USERNAME} ${HOSTNAME} "sudo su - <<'EOF' 
    # python -m pip install pickle5
    # python -m pip install tensorboardX"
    # echo ${HOSTNAME}
done