package com.example.cherr.bluetooth3;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.Display;
import android.view.Menu;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.cherr.bluetooth3.adapter.GridAdapter;

public class MainActivity extends AppCompatActivity implements View.OnClickListener{

    ExpandableGridView arena;
    Button exploreBtn, runBtn, manualBtn, upBtn, downBtn, leftBtn, rightBtn, setCoorBtn;
    GridAdapter adapter;
    LinearLayout leftLayout, control;
    EditText xCoor, yCoor;
    BluetoothChatFragment bluetoothFragment;
    SensorManager sensorManager;
    Sensor sensor;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        assignInterfaceVariables();

        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        bluetoothFragment = new BluetoothChatFragment();
        transaction.replace(R.id.sample_content_fragment, bluetoothFragment);
        transaction.commit();

        Display display = getWindowManager().getDefaultDisplay();
        int width = display.getWidth();
        leftLayout.setLayoutParams(new LinearLayout.LayoutParams((width / 2), ViewGroup.LayoutParams.FILL_PARENT));

        setMapAdapter(1, 1);


        //extension
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
        leftLayout = (LinearLayout) findViewById(R.id.left_layout);
        control = (LinearLayout) findViewById(R.id.control);
        xCoor = (EditText) findViewById(R.id.x_text);
        yCoor = (EditText) findViewById(R.id.y_text);

        exploreBtn.setOnClickListener(this);
        runBtn.setOnClickListener(this);
        manualBtn.setOnClickListener(this);
        upBtn.setOnClickListener(this);
        leftBtn.setOnClickListener(this);
        downBtn.setOnClickListener(this);
        rightBtn.setOnClickListener(this);
        setCoorBtn.setOnClickListener(this);


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
            }else{
                control.setVisibility(View.VISIBLE);
            }
        }
        else if(v == setCoorBtn){
            Context context = getApplicationContext();
            CharSequence text = "Invalid Coordinates";

            if((validateFields(xCoor.getText().toString())) && validateFields(yCoor.getText().toString())){
                int x_coor_txt = Integer.parseInt(xCoor.getText().toString());
                int y_coor_txt = Integer.parseInt(yCoor.getText().toString());
                if(isValidCoor(x_coor_txt, y_coor_txt)){
                    bluetoothFragment.sendMessage("Robot starts at (" + Integer.toString(x_coor_txt) + ", "
                            + Integer.toString(x_coor_txt) + ")");
                    setMapAdapter(x_coor_txt, y_coor_txt);
                    text = "Robot Location Reset";
                }
            }

            int duration = Toast.LENGTH_SHORT;
            Toast toast = Toast.makeText(context, text, duration);
            toast.show();
        }
    }

    public Boolean isValidCoor(int x_coor_txt, int y_coor_txt) {
        if (x_coor_txt > 0 && x_coor_txt <= 15) {
            if (y_coor_txt > 0 && y_coor_txt <= 20) {
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
}