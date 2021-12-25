package com.example.mysocket;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

public class MyTransProcess {
    public static void TS(String IP, int PORT, FileInputStream isFile, FileOutputStream osFile) throws IOException, InterruptedException {
        myTCP client = new myTCP(IP, PORT);
        client.setAsClient();

        //client.getModel(osFile, isFile);
        //client.sendFile("isFile", 1, 1024*8);
        //int maxBufSize = client.recvMSG(1);
        //client.sendFile(isFile,1, maxBufSize);
        //client.recvFile(osFile, 1);
        //client.sendFile(isFile, 1, 8000);

    }
    public static void FS(int PORT) throws IOException {

    }
}
