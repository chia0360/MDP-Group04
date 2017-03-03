package com.mdpgrp4.mdp;

import android.app.Activity;
import android.app.Dialog;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.view.Display;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.mdpgrp4.mdp.adapter.GridAdapter;

import java.math.BigInteger;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, SensorEventListener{


    ExpandableGridView arena;
    Button manualBtn, upBtn, downBtn, leftBtn, rightBtn, setCoorBtn, refreshBtn, f1Btn, f2Btn, configureBtn, save;
    ToggleButton autoUpdateBtn, exploreBtn, runBtn;
    GridAdapter adapter;
    LinearLayout leftLayout, control;
    EditText xCoor, yCoor;
    SensorManager sensorManager;
    Sensor sensor;
    TextView status;
    Boolean update = false;
    Boolean tilt = false;
    Dialog d;
    EditText f1command;
    EditText f2command;
    SharedPreferences sharedPref;
    static final int SocketServerPORT = 8765;
    static final String SocketServerADD = "192.168.4.1";

    LinearLayout chatPanel;

    TextView chatMsg;

    EditText editTextSay;
    Button buttonSend;

    String msgLog = "";
    String statusLog = "";
    String mapLog = "";
    boolean mapUpdateLog = false;

    ChatClientThread chatClientThread = null;

    private static final int REQUEST_CONNECT_DEVICE_SECURE = 1;
    private static final int REQUEST_CONNECT_DEVICE_INSECURE = 2;
    private static final int REQUEST_ENABLE_BT = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        assignInterfaceVariables();

        autoUpdateBtn.setOnCheckedChangeListener( new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton toggleButton, boolean isChecked) {
                setRefreshBtn(isChecked) ;
            }
        }) ;


        Display display = getWindowManager().getDefaultDisplay();
        int width = display.getWidth();
        //leftLayout.setLayoutParams(new LinearLayout.LayoutParams((width / 2), ViewGroup.LayoutParams.FILL_PARENT));

        setMapAdapter(0,0);

        exploreBtn.setText("Explore");
        runBtn.setText("Run");

        sharedPref = this.getPreferences(Context.MODE_PRIVATE);

        //extension for c10
        sensorManager = (SensorManager) getSystemService(MainActivity.SENSOR_SERVICE);
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);

    }

    public void assignInterfaceVariables(){
        arena = (ExpandableGridView) findViewById(R.id.arena_grid_view);
        exploreBtn = (ToggleButton) findViewById(R.id.explore_btn);
        runBtn = (ToggleButton) findViewById(R.id.run_btn);
        manualBtn = (Button) findViewById(R.id.manual_btn);
        leftBtn = (Button) findViewById(R.id.left_btn);
        upBtn = (Button) findViewById(R.id.up_btn);
        downBtn = (Button) findViewById(R.id.down_btn);
        rightBtn = (Button) findViewById(R.id.right_btn);
        setCoorBtn = (Button) findViewById(R.id.set_coord_btn);
        refreshBtn = (Button) findViewById(R.id.refresh);
        f1Btn = (Button) findViewById(R.id.f1);
        f2Btn = (Button) findViewById(R.id.f2);
        configureBtn = (Button) findViewById(R.id.configure);
        autoUpdateBtn = (ToggleButton) findViewById(R.id.auto_update_btn);
        leftLayout = (LinearLayout) findViewById(R.id.left_layout);
        control = (LinearLayout) findViewById(R.id.control);
        xCoor = (EditText) findViewById(R.id.x_text);
        yCoor = (EditText) findViewById(R.id.y_text);
        status = (TextView) findViewById(R.id.robotstatus);

        d = new Dialog(MainActivity.this);
        d.setTitle("Command Button Configuration");
        d.setContentView(R.layout.dialog_configure);
        save = (Button) d.findViewById(R.id.save);
        f1command = (EditText) d.findViewById(R.id.f1Command);
        f2command = (EditText) d.findViewById(R.id.f2Command);


        exploreBtn.setOnClickListener(this);
        runBtn.setOnClickListener(this);
        manualBtn.setOnClickListener(this);
        upBtn.setOnClickListener(this);
        leftBtn.setOnClickListener(this);
        downBtn.setOnClickListener(this);
        rightBtn.setOnClickListener(this);
        setCoorBtn.setOnClickListener(this);
        refreshBtn.setOnClickListener(this);
        f1Btn.setOnClickListener(this);
        f2Btn.setOnClickListener(this);
        configureBtn.setOnClickListener(this);
        save.setOnClickListener(this);

        chatPanel = (LinearLayout)findViewById(R.id.chatpanel);
        chatMsg = (TextView) findViewById(R.id.chatmsg);

        editTextSay = (EditText)findViewById(R.id.say);
        buttonSend = (Button)findViewById(R.id.send);

        buttonSend.setOnClickListener(buttonSendOnClickListener);
    }


    @Override
    public boolean  onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.connect_wifi:
                /*Intent intent = new Intent(this, DeviceListActivity.class);
                startActivityForResult(intent, 1);
                return true;*/
                msgLog = "";
                chatMsg.setText(msgLog);

                chatClientThread = new ChatClientThread(
                        "Android Client", SocketServerADD, SocketServerPORT);
                chatClientThread.start();

                Context context = getApplicationContext();
                CharSequence text = "Connected to Server";
                int duration = Toast.LENGTH_SHORT;
                Toast toast = Toast.makeText(context, text, duration);
                toast.show();

                status.setText("Connected");
                return true;
            case R.id.rst_btn:
                setMapAdapter(0,0);
                return true;
            case R.id.disconnect:
                if(chatClientThread!=null){
                    chatClientThread.disconnect();
                }
                return true;
            /*case R.id.insecure_connect_scan: {
                // Launch the DeviceListActivity to see devices and do scan
                Intent serverIntent = new Intent(getActivity(), DeviceListActivity.class);
                startActivityForResult(serverIntent, REQUEST_CONNECT_DEVICE_INSECURE);
                return true;
            }
            case R.id.discoverable: {
                // Ensure this device is discoverable by others
                ensureDiscoverable();
                return true;
            }*/
        }
        return false;
    }


    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public void onClick(View v) {
        if (v == manualBtn){
            if(control.getVisibility() == View.VISIBLE) {
                control.setVisibility(View.INVISIBLE);
                tilt = false;
            }else{
                control.setVisibility(View.VISIBLE);
                tilt = true;
            }
        }
        else if(v == setCoorBtn){
            Context context = getApplicationContext();
            CharSequence text = "Invalid Coordinates";

            if((validateFields(xCoor.getText().toString())) && validateFields(yCoor.getText().toString())){
                int x_coor_txt = Integer.parseInt(xCoor.getText().toString());
                int y_coor_txt = Integer.parseInt(yCoor.getText().toString());
                if(isValidCoor(x_coor_txt, y_coor_txt)){
                    //send msg via bluetooth
                    sendMessage("Robot starts at (" + Integer.toString(x_coor_txt) + ", "
                            + Integer.toString(y_coor_txt) + ")");
                    setMapAdapter(x_coor_txt, y_coor_txt);
                    text = "Robot Location Reset";
                }
            }

            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
        else if(v == upBtn){
            sendMessage("f");
            adapter.moveRobot("f");
            status.setText("Going Forward");
        }
        else if(v == downBtn){
           /* sendMessage("r");
            adapter.moveRobot("r");
            status.setText("Going Backward");*/
        }
        else if(v == leftBtn){
            sendMessage("l");
            adapter.moveRobot("tl");
            status.setText("Turning Left");
        }
        else if(v == rightBtn){
            sendMessage("r");
            adapter.moveRobot("tr");
            status.setText("Turning Right");
        }
        else if(v == refreshBtn){
            sendMessage("sendArena");
            update = true;
        }
        else if(v == exploreBtn){
            if(!runBtn.isChecked()) {
                if (exploreBtn.isChecked()) {
                    exploreBtn.setText("Stop");
                    sendMessage("startexplore");
                    runBtn.setClickable(false);
                } else {
                    exploreBtn.setText("Explore");
                    sendMessage("stop");
                    runBtn.setClickable(true);
                }
            }
        }
        else if(v == runBtn) {
            if(!exploreBtn.isChecked()) {
                if (runBtn.isChecked()) {
                    runBtn.setText("Stop");
                    sendMessage("fastestpath");
                    exploreBtn.setClickable(false);
                } else {
                    runBtn.setText("Run");
                    sendMessage("stop");
                    exploreBtn.setClickable(true);
                }
            }
        }
        else if(v == f1Btn){
            String defaultValue = "f1old";
            String cmd = sharedPref.getString("C1", defaultValue);
            sendMessage(cmd);
        }
        else if(v == f2Btn){
            String defaultValue = "f2old";
            String cmd = sharedPref.getString("C2", defaultValue);
            sendMessage(cmd);
        }
        else if(v == configureBtn){
            d.show();
        }
        else if(v == save){
            if(f1command.getText().toString() != "") {
                saveCommand(f1command.getText().toString(), "C1");
                d.dismiss();
            }
            if(f2command.getText().toString() != "") {
                saveCommand(f2command.getText().toString(), "C2");
                d.dismiss();
            }
        }
    }

    public Boolean isValidCoor(int x_coor_txt, int y_coor_txt) {
        if (x_coor_txt >= 0 && x_coor_txt < 18) {
            if (y_coor_txt >= 0 && y_coor_txt < 13) {
                return true;
            }
        }
        return false;
    }

    public void setMapAdapter(int x, int y){
        adapter = new GridAdapter(this, x, y);
        arena.setAdapter(adapter);

        arena.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                v.getParent().requestDisallowInterceptTouchEvent(true);
                return false;
            }

        });
    }

    public boolean validateFields(String name){
        if (TextUtils.isEmpty(name)) {
            return false;
        } else {
            return true;
        }
    }

    public void setRefreshBtn(Boolean isChecked){
        if (isChecked)
            refreshBtn.setVisibility(View.GONE);
        else
            refreshBtn.setVisibility(View.VISIBLE);
    }

    public void updateMap(String msg){
        String hex = msg.substring(11, msg.length() - 2);
        String obstacles = hexToBinary(hex);
        int index = 0;
        while(index < obstacles.length()){
            if(obstacles.charAt(index) == '1') {
                adapter.setItem(index, adapter.STATE_OBSTACLE);
            }/*else{
                adapter.setItem(index, adapter.STATE_UNEXPLORED);
            }*/
            index++;
        }
    }

    public void saveCommand(String newcmd, String cmd){
        SharedPreferences.Editor editor = sharedPref.edit();
        editor.putString(cmd, newcmd);
        editor.commit();

        Context context = getApplicationContext();
        CharSequence text = "Command saved";
        int duration = Toast.LENGTH_SHORT;
        Toast toast = Toast.makeText(context, text, duration);
        toast.show();
    }

    public void onReceiveMessage(String msg){
        if (msg.contains("grid")) {
            if(autoUpdateBtn.isChecked() || update == true) {
                updateMap(msg);
                update = false;
            }
        } else if (msg.contains("exploring")) {
            status.setText("Exploring");
        } else if (msg.contains("fastest path")) {
            status.setText("Fastest Path");
        } else if (msg.equals("l")) {
            status.setText("Turning Left");
            adapter.moveRobot("tl");
        } else if (msg.equals("r")) {
            status.setText("Turning Right");
            adapter.moveRobot("tr");
        } else if (msg.equals("f")) {
            status.setText("Moving Forward");
            adapter.moveRobot("f");
        } /*else if (msg.contains("reversing")) {
            status.setText("Reversing");
        }*/else if (msg.contains("connected")) {
            status.setText("Bluetooth Connected");
        }else if (msg.contains("disconnect")) {
            status.setText("Bluetooth Disconnected");
        }else if (msg.contains("connecting")) {
            status.setText("Bluetooth Connecting");
        }
    }

    public static String hexToBinary(String hex) {
        int len = hex.length() * 4;
        String bin = new BigInteger(hex, 16).toString(2);

        if(bin.length() < len){
            int diff = len - bin.length();
            String pad = "";
            for(int i = 0; i < diff; ++i){
                pad = pad.concat("0");
            }
            bin = pad.concat(bin);
        }
        return bin;
    }

    @Override
    protected void onResume() {
        super.onResume();
        //sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        float axisX = event.values[0];
        float axisY = event.values[1];
        float axisZ = event.values[2];

        Log.e("Tilting", "X: " + axisX + " Y: " + axisY + " Z: " + axisZ);

        if(tilt == true){
            /*if(axisY > 5){
                sendMessage("r");
                adapter.moveRobot("r");
                status.setText("Moving Backward");
            }
            else */
            if(axisY < -5){
                sendMessage("f");
                adapter.moveRobot("f");
                status.setText("Moving Forward");
            }
            else if(axisX > 5){
                sendMessage("l");
                adapter.moveRobot("tl");
                status.setText("Turning Left");
            }
            else if(axisX < -5 ){
                sendMessage("r");
                adapter.moveRobot("tr");
                status.setText("Turning Right");
            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        switch (requestCode) {
            case REQUEST_CONNECT_DEVICE_SECURE:
                // When DeviceListActivity returns with a device to connect
                if (resultCode == Activity.RESULT_OK) {
                    //bluetoothFragment.connectDevice(data, true);
                }
                break;
            case REQUEST_CONNECT_DEVICE_INSECURE:
                // When DeviceListActivity returns with a device to connect
                if (resultCode == Activity.RESULT_OK) {
                    //bluetoothFragment.connectDevice(data, false);
                }
                break;
            case REQUEST_ENABLE_BT:
                // When the request to enable Bluetooth returns
                if (resultCode == Activity.RESULT_OK) {
                    // Bluetooth is now enabled, so set up a chat session
                    //bluetoothFragment.setupChat();
                } else {
                    // User did not enable Bluetooth or an error occurred
                    Toast.makeText(this, R.string.bt_not_enabled_leaving,
                            Toast.LENGTH_SHORT).show();
                    finish();
                }
        }
    }

    View.OnClickListener buttonSendOnClickListener = new View.OnClickListener() {

        @Override
        public void onClick(View v) {
            if (editTextSay.getText().toString().equals("")) {
                return;
            }
            sendMessage(editTextSay.getText().toString());
        }

    };

    public void sendMessage(String msg){

        if(chatClientThread==null){
            return;
        }

        chatClientThread.sendMsg(msg + "\n");
    }


    private class ChatClientThread extends Thread {

        String name;
        String dstAddress;
        int dstPort;

        String msgToSend = "";
        boolean goOut = false;

        ChatClientThread(String name, String address, int port) {
            this.name = name;
            dstAddress = address;
            dstPort = port;
        }

        @Override
        public void run() {
            Socket socket = null;
            DataOutputStream dataOutputStream = null;
            DataInputStream dataInputStream = null;

            try {
                socket = new Socket(dstAddress, dstPort);
                dataOutputStream = new DataOutputStream(
                        socket.getOutputStream());
                dataInputStream = new DataInputStream(socket.getInputStream());
                //dataOutputStream.writeUTF(name);
                //dataOutputStream.flush();

                while (!goOut) {
                    if (dataInputStream.available() > 0) {
                        int count = dataInputStream.available();
                        byte[] bs = new byte[count];
                        dataInputStream.read(bs);
                        for (byte b:bs) {
                            // convert byte into character
                            char c = (char)b;
                            msgLog+=c;
                            if(c == 'f'){
                                statusLog = "f";
                            }else if(c == 'r'){
                                statusLog = "r";
                            }else if(c == 'l'){
                                statusLog = "l";
                            }else if(c == 'm'){
                                statusLog = "m";
                                mapUpdateLog = true;
                            }
                            if(mapUpdateLog == true){
                                if(c == '1' || c == '0'){
                                    mapLog += c + "";
                                }else{
                                    mapUpdateLog = false;
                                }
                            }
                        }
                        //msgLog += dataInputStream.readUTF();

                        MainActivity.this.runOnUiThread(new Runnable() {

                            @Override
                            public void run() {
                                chatMsg.setText(msgLog);
                                if(statusLog != "") {
                                    onReceiveMessage(statusLog);
                                }
                            }
                        });
                    }

                    if(!msgToSend.equals("")){
                        dataOutputStream.writeBytes(msgToSend);
                        dataOutputStream.flush();
                        msgToSend = "";
                    }
                }

            } catch (UnknownHostException e) {
                e.printStackTrace();
                final String eString = e.toString();
                MainActivity.this.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        Toast.makeText(MainActivity.this, eString, Toast.LENGTH_LONG).show();
                    }

                });
            } catch (IOException e) {
                e.printStackTrace();
                final String eString = e.toString();
                MainActivity.this.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                        Toast.makeText(MainActivity.this, eString, Toast.LENGTH_LONG).show();
                    }

                });
            } finally {
                if (socket != null) {
                    try {
                        socket.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

                if (dataOutputStream != null) {
                    try {
                        dataOutputStream.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

                if (dataInputStream != null) {
                    try {
                        dataInputStream.close();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }

                MainActivity.this.runOnUiThread(new Runnable() {

                    @Override
                    public void run() {
                    }

                });
            }

        }

        private void sendMsg(String msg){
            msgToSend = msg;
        }

        private void disconnect(){
            goOut = true;
        }
    }
}
