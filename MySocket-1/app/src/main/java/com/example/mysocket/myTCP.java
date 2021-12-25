package com.example.mysocket;

import android.util.Log;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;


public class myTCP {
    static int PORT;
    static String IP;
    static int maxNumOfClients = 500;
    static Socket[] client = new Socket[maxNumOfClients];

    myTCP(String IP, int PORT){
        this.IP = IP;
        this.PORT = PORT;
    }

    public static void setAsServer(int numOfClients) throws IOException {
        ServerSocket server = new ServerSocket(PORT);
        Log.i("ShowMe","ADDR->"+IP+PORT);
        for (int i=1; i<=numOfClients; i++ ){
            client[i] = server.accept();
        }
    }

    public static void setAsClient() throws IOException {
        // TCP Net
        int showMe = Log.i("ShowMe", "ADDR->" + IP + PORT);
//        new Socket(IP,PORT);
        client[1] = new Socket(IP, PORT);

        Log.i("ShowMe", "connect success");
    }
    public static int recv_msg(int posOfClient) throws IOException {
        DataInputStream is = new DataInputStream(client[posOfClient].getInputStream());
        byte[] byteNum = new byte[4];
        is.read(byteNum);
        int clientNum = myConvert.byteArrayToInt(byteNum);
        return clientNum;
    }

    public static void send_msg(int posOfClient, int msgSend) throws IOException{
        DataOutputStream os = new DataOutputStream(client[posOfClient].getOutputStream());
        byte[] msg = myConvert.intToByteArray(msgSend);
        os.write(msg, 0, 4);
    }

    public static double recvMSG(int posOfClient) throws IOException {
        int opt = recv_msg(posOfClient);
        double msg = opt / 1e5;
        return msg;
    }

    /*
    public static void getModel(FileOutputStream osFile, FileInputStream isFile) throws IOException, InterruptedException {
        recvFile(osFile, 1);
        Log.i("ShowMe", "recieve success!");
        sendFile(isFile, 1, 1024*8);
        //sendMSG(1,0);
    }

    public static void sendFileSize(FileInputStream isFile, int posOfClient) throws IOException {
        int fileSize = isFile.available();
        send_msg(posOfClient, fileSize);
    }


    public static void recvFile(final FileOutputStream osFile, int posOfClient) throws IOException {
        //FileOutputStream osFile = openFileOutput(fileName, Context.MODE_PRIVATE);
        DataInputStream is = new DataInputStream(client[posOfClient].getInputStream());
        int fileSize = recvMSG(posOfClient);
        int maxBufSize = recvMSG(posOfClient);
        byte[] buf = new byte[maxBufSize];
        int recvSize = 0;
        for (; fileSize != recvSize; ){
            Log.d("ShowMe", "Recieve File:"+recvSize+"/"+fileSize);
            int oneTimeReadLong = 0;
            if (fileSize - recvSize > maxBufSize){
                oneTimeReadLong = is.read(buf);
            } else{
                oneTimeReadLong = is.read(buf, 0, (int) (fileSize-recvSize));
            }
            if (oneTimeReadLong == -1){
                break;
            }
            recvSize += oneTimeReadLong;
            osFile.write(buf, 0, oneTimeReadLong);

        }
        osFile.close();
    }

    public static void sendFile(FileInputStream isFile, int posOfClient, int maxBufSize) throws IOException, InterruptedException {
        DataOutputStream os = new DataOutputStream(client[posOfClient].getOutputStream());
        //isFile.reset();
        // send file info
        int fileSize = isFile.available();
        sendMSG(posOfClient, fileSize);
        sendMSG(posOfClient, maxBufSize);
        // send file
        int sendFileSize = 0;
        byte[] buf = new byte[maxBufSize];
        for (; sendFileSize != fileSize; ){

            double st_time = System.currentTimeMillis();
            double seg = st_time % 10;
            if (seg >= 0 && seg < 2){
                continue;
            }
            //Thread.sleep(50);
            Log.i("ShowMe", "send file:"+sendFileSize+"/"+fileSize);
            int oneTimeFileSize = 0;
            if (fileSize - sendFileSize > maxBufSize){
                oneTimeFileSize = isFile.read(buf, 0, maxBufSize);
            }else {
                oneTimeFileSize = isFile.read(buf, 0, (int) (fileSize - sendFileSize));
            }
            sendFileSize += oneTimeFileSize;
            os.write(buf, 0, oneTimeFileSize);
            double ed_time = System.currentTimeMillis();
            double avgTime = ed_time - st_time;
            Log.i("ShowMe", "time is "+avgTime+" st time:"+st_time+", ed time is:"+ed_time);
        }
        isFile.close();
    }
    */

}
