package com.example.mysocket;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.w3c.dom.Text;

import android.util.Log;

import java.io.FileNotFoundException;
import java.util.logging.Logger;
import android.view.LayoutInflater;
import android.view.View;
import android.view.WindowManager;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;


import java.io.IOException;
import java.net.InetAddress;

import java.io.DataInputStream;

import java.io.DataOutputStream;

import java.net.Socket;
import java.net.UnknownHostException;
import java.io.FileOutputStream;
import java.io.FileInputStream;

import static com.example.mysocket.R.id.green_block;

public class MainActivity extends AppCompatActivity {

    TextView newtextView, staView;

    public void ShowGreen(){
        ImageView green = (ImageView) findViewById(green_block);
        ImageView grey = (ImageView) findViewById(R.id.white_block);
        green.setVisibility(View.VISIBLE);
        grey.setVisibility(View.GONE);
    }

    public void ShowGrey(){
        ImageView green = (ImageView) findViewById(green_block);
        ImageView grey = (ImageView) findViewById(R.id.white_block);
        green.setVisibility(View.INVISIBLE);
        grey.setVisibility(View.VISIBLE);
    }

    public void modify_text(TextView text, String contxt){
        text.setText(contxt);
    }

    public void ChangeBgCol(){
        LayoutInflater layoutInflater = (LayoutInflater) getSystemService(Activity.LAYOUT_INFLATER_SERVICE);

        LinearLayout linearLay = (LinearLayout) layoutInflater.inflate(R.layout.activity_main, null) ;

        linearLay.setBackgroundColor(Color.RED);

        setContentView(linearLay);
    }

    //@Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

//        Init IP and Port
        final String IP = "192.168.43.156";
        final int PORT = 8240;

//        Init View
        setContentView(R.layout.activity_main);

//        KEEP SCREEN ON
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        ImageView w_block = (ImageView) findViewById(R.id.white_block);
        ImageView g_block = (ImageView) findViewById(R.id.green_block);
        final TextView Text_ID = (TextView) findViewById(R.id.title1);
        final TextView Text_Loss = (TextView) findViewById(R.id.loss);
//        g_block.setVisibility(View.INVISIBLE);
//        for (int i=1; i <= 2; ++ i) {
//            w_block.setVisibility(View.VISIBLE);
//            w_block.setVisibility(View.INVISIBLE);
//        }
        final ImageView green = (ImageView) findViewById(green_block);
        final ImageView grey = (ImageView) findViewById(R.id.white_block);


        Text_ID.setText("Init");

        final myTCP client = new myTCP(IP, PORT);

        new Thread(new Runnable(){
//            @Override
            public void run() {
                try {
                    client.setAsClient();
                    double msg = client.recvMSG(1);
                    int ID = (int) msg;
                    Text_ID.setText("Client " + ID);
                    while (true) {
                        double msg1 = client.recvMSG(1);
                        double msg2 = client.recvMSG(1);
                        if ((int) msg1 == 1) {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    green.setVisibility(View.VISIBLE);
                                    grey.setVisibility(View.GONE);
                                    // Stuff that updates the UI

                                }
                            });

                        } else {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    green.setVisibility(View.INVISIBLE);
                                    grey.setVisibility(View.VISIBLE);
                                    // Stuff that updates the UI

                                }
                            });

                        }
                        Text_Loss.setText("" + msg2);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();

    }
}

