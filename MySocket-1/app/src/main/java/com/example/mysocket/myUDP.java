package com.example.mysocket;

import android.widget.TextView;

import java.io.FileOutputStream;
import java.io.IOException;

import java.net.DatagramSocket;
import java.net.DatagramPacket;
import java.net.InetSocketAddress;
import java.net.SocketAddress;

public class myUDP {

    public static int recvMSG_UDP(DatagramSocket isUDP) throws IOException {
        int fileSize = 0;
        byte[] bufUDP = new byte[4];
        DatagramPacket packet = new DatagramPacket(bufUDP, bufUDP.length);
        isUDP.receive(packet);
        byte[] byteMsg = packet.getData();
        fileSize = myConvert.byteArrayToInt(byteMsg);
        //v.setText("size" + fileSize);
        return fileSize;
    }

    public static void sendMSG_UDP(DatagramSocket isUDP, String IP, int PORT, int msgSend) throws  IOException {
        byte[] msg = myConvert.intToByteArray(msgSend);
        SocketAddress socketAddr = new InetSocketAddress(IP, PORT);
        DatagramPacket sendPacket = new DatagramPacket(msg, msg.length, socketAddr);
        isUDP.send(sendPacket);
    }


    public static int recvFileUDP(FileOutputStream osFile, DatagramSocket isUDP, TextView tv) throws IOException {

        int recvConfirm = recvMSG_UDP(isUDP);
        while (recvConfirm != 1){
            recvConfirm = recvMSG_UDP(isUDP);
            tv.setText("still waiting...");
        }
        int fileSize = recvMSG_UDP(isUDP);
        int recvSize = 0;
        for (; fileSize != recvSize; ){
            tv.setText("cur:" + recvSize + "/" + fileSize);
            byte[] bufUDP = new byte[1024];
            DatagramPacket packet = new DatagramPacket(bufUDP, bufUDP.length);
            int oneTimeReadLong = 0;
            if (fileSize - recvSize > 1024){
                isUDP.receive(packet);
                oneTimeReadLong = packet.getLength();
            } else{
                bufUDP = new byte[fileSize - recvSize];
                packet = new DatagramPacket(bufUDP, bufUDP.length);
                isUDP.receive(packet);
                oneTimeReadLong = packet.getLength();
            }
            if (oneTimeReadLong == -1){
                break;
            }
            recvSize += oneTimeReadLong;
            osFile.write(packet.getData(), 0, oneTimeReadLong);
        }
        osFile.close();
        return fileSize;
    }
}
