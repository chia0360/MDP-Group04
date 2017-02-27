package com.example.cherr.bluetooth3;

import android.app.Dialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
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

import com.example.cherr.bluetooth3.adapter.GridAdapter;

import java.math.BigInteger;

public class MainActivity extends AppCompatActivity implements View.OnClickListener, SensorEventListener{

    ExpandableGridView arena;
    Button exploreBtn, runBtn, manualBtn, upBtn, downBtn, leftBtn, rightBtn, setCoorBtn, refreshBtn, f1Btn, f2Btn, configureBtn, save;
    ToggleButton autoUpdateBtn;
    GridAdapter adapter;
    LinearLayout leftLayout, control;
    EditText xCoor, yCoor;
    BluetoothChatFragment bluetoothFragment;
    SensorManager sensorManager;
    Sensor sensor;
    TextView status;
    Boolean update = false;
    Boolean tilt = false;
    Dialog d;
    EditText f1command;
    EditText f2command;
    SharedPreferences sharedPref;

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

        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        bluetoothFragment = new BluetoothChatFragment();
        transaction.replace(R.id.chat_message, bluetoothFragment);
        transaction.commit();

        Display display = getWindowManager().getDefaultDisplay();
        int width = display.getWidth();
        //leftLayout.setLayoutParams(new LinearLayout.LayoutParams((width / 2), ViewGroup.LayoutParams.FILL_PARENT));

        setMapAdapter(0,0);

        sharedPref = this.getPreferences(Context.MODE_PRIVATE);

        //extension for c10
        sensorManager = (SensorManager) getSystemService(MainActivity.SENSOR_SERVICE);
        sensor = sensorManager.getDefaultSensor(Sensor.TYPE_GRAVITY);

    }

    public void assignInterfaceVariables(){
        arena = (ExpandableGridView) findViewById(R.id.arena_grid_view);
        exploreBtn = (Button) findViewById(R.id.explore_btn);
        runBtn = (Button) findViewById(R.id.run_btn);
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
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        return true;
    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        return super.onPrepareOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
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
                    bluetoothFragment.sendMessage("Robot starts at (" + Integer.toString(x_coor_txt) + ", "
                            + Integer.toString(y_coor_txt) + ")");
                    adapter.updateRobot(x_coor_txt, y_coor_txt);
                    text = "Robot Location Reset";
                }
            }

            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
        else if(v == upBtn){
            bluetoothFragment.sendMessage("f");
            adapter.moveRobot("f");
            status.setText("Going Forward");
        }
        else if(v == downBtn){
            bluetoothFragment.sendMessage("r");
            adapter.moveRobot("r");
            status.setText("Going Backward");
        }
        else if(v == leftBtn){
            bluetoothFragment.sendMessage("tl");
            adapter.moveRobot("tl");
            status.setText("Turning Left");
        }
        else if(v == rightBtn){
            bluetoothFragment.sendMessage("tr");
            adapter.moveRobot("tr");
            status.setText("Turning Right");
        }
        else if(v == refreshBtn){
            bluetoothFragment.sendMessage("sendArena");
            update = true;
        }
        else if(v == exploreBtn){
            bluetoothFragment.sendMessage("beginExplore");
        }
        else if(v == f1Btn){
            String defaultValue = "f1old";
            String cmd = sharedPref.getString("C1", defaultValue);
            bluetoothFragment.sendMessage(cmd);
        }
        else if(v == f2Btn){
            String defaultValue = "f2old";
            String cmd = sharedPref.getString("C2", defaultValue);
            bluetoothFragment.sendMessage(cmd);
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
            }else{
                adapter.setItem(index, adapter.STATE_UNEXPLORED);
            }
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
        } else if (msg.contains("turning left")) {
            status.setText("Turning Left");
        } else if (msg.contains("turning right")) {
            status.setText("Turning Right");
        } else if (msg.contains("moving forward")) {
            status.setText("Moving Forward");
        } else if (msg.contains("reversing")) {
            status.setText("Reversing");
        }else if (msg.contains("connected")) {
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
        sensorManager.registerListener(this, sensor, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        float axisX = event.values[0];
        float axisY = event.values[1];
        float axisZ = event.values[2];

        Log.e("Tilting", "X: " + axisX + " Y: " + axisY + " Z: " + axisZ);

        if(tilt == true){
            if(axisY > 5){
                bluetoothFragment.sendMessage("r");
                adapter.moveRobot("r");
                status.setText("Moving Backward");
            }
            else if(axisY < -5){
                bluetoothFragment.sendMessage("f");
                adapter.moveRobot("f");
                status.setText("Moving Forward");
            }
            else if(axisX > 5){
                bluetoothFragment.sendMessage("tl");
                adapter.moveRobot("tl");
                status.setText("Turning Left");
            }
            else if(axisX < -5 ){
                bluetoothFragment.sendMessage("tr");
                adapter.moveRobot("tr");
                status.setText("Turning Right");

            }
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }
}
