package com.example.mysocket;

import android.content.Context;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.util.logging.Logger;
import android.util.Log;

public class MQTTManager {

    public static final String SERVER_HOST = "tcp://192.168.2.100:30042";
    private String clientid = "";
    private static MQTTManager mqttManager=null;
    private MqttClient client;
    private MqttConnectOptions options;

    //private MessageHandlerCallBack callBack;
    private MQTTManager(Context context) {

        clientid += MqttClient.generateClientId();
    }

    /**
     * 获取一个MQTTManager单例
     * @param context
     * @return 返回一个MQTTManager的实例对象
     */
    public static MQTTManager getInstance(Context context) {
        Log.d("mqttManager=",""+mqttManager);
        if (mqttManager==null) {
            mqttManager=new MQTTManager(context);
            synchronized (Object.class) {
                Log.d("synchronized mqttManager",""+mqttManager);
                if (mqttManager!=null) {
                    return mqttManager;
                }
            }
        }
        return mqttManager;
    }
    /**
     * 连接服务器
     */
    public void connect(){
        Log.d("开始连接MQtt","");
        try {
            // host为主机名，clientid即连接MQTT的客户端ID，一般以唯一标识符表示，MemoryPersistence设置clientid的保存形式，默认为以内存保存
            client = new MqttClient(SERVER_HOST, clientid, new MemoryPersistence());
            // MQTT的连接设置
            options = new MqttConnectOptions();
            // 设置是否清空session,这里如果设置为false表示服务器会保留客户端的连接记录，这里设置为true表示每次连接到服务器都以新的身份连接
//              options.setCleanSession(true);
            // 设置连接的用户名
            options.setUserName("admin");
            // 设置连接的密码
            options.setPassword("password".toCharArray());
            // 设置超时时间 单位为秒
//              options.setConnectionTimeout(30);
            // 设置会话心跳时间 单位为秒 服务器会每隔1.5*20秒的时间向客户端发送个消息判断客户端是否在线，但这个方法并没有重连的机制
//              options.setKeepAliveInterval(30);
            // 设置回调
//              MqttTopic topic = client.getTopic(TOPIC);
            //setWill方法，如果项目中需要知道客户端是否掉线可以调用该方法。设置最终端口的通知消息
//              options.setWill(topic, "close".getBytes(), 2, true);
            //client.setCallback(new PushCallback());
            client.connect(options);
            Log.d("ClientId=",""+client.getClientId());
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    /**
     * 订阅消息
     * @param topic 订阅消息的主题
     */
    public void subscribeMsg(String topic,int qos){
        if (client!=null) {
            int[] Qos  = {qos};
            String[] topic1 = {topic};
            try {
                client.subscribe(topic1, Qos);
                Log.d("开始订阅topic=",""+topic);
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }

    /**
     * 发布消息
     * @param topic 发布消息主题
     * @param msg 消息体
     * @param isRetained 是否为保留消息
     */
    public void publish(String topic,String msg,boolean isRetained,int qos) {

        if (client!=null) {
            MqttMessage message = new MqttMessage();
            message.setQos(qos);
            message.setRetained(isRetained);
            message.setPayload(msg.getBytes());
            try{
                client.publish(topic, message);
            } catch (MqttException e) {
                e.printStackTrace();
            }

            //Logger.d("topic="+topic+"--msg="+msg+"--isRetained"+isRetained);
        }

    }
    int count=0;

    public void disconnect(){
        if (client!=null&&client.isConnected()) {
            try {
                client.disconnect();
                mqttManager=null;
            } catch (MqttException e) {
                e.printStackTrace();
            }
        }
    }
    /**
     * 释放资源
     */
    public void release(){
        if (mqttManager!=null) {
            mqttManager=null;
        }
    }
    /**
     *  判断服务是否连接
     * @return
     */
    public boolean isConnected(){
        if (client!=null) {
            return client.isConnected();
        }
        return false;
    }

}
