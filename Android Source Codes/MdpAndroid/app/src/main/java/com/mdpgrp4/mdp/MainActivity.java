package com.mdpgrp4.mdp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.GridView;

import com.mdpgrp4.mdp.adapter.GridAdapter;

public class MainActivity extends AppCompatActivity {

    GridView arena;
    Button exploreBtn, runBtn, manualBtn;
    GridAdapter adapter;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        assignInterfaceVariables();

        adapter = new GridAdapter(this);
        arena.setAdapter(adapter);


    }

    public void assignInterfaceVariables(){
        arena = (GridView) findViewById(R.id.arena_grid_view);
        exploreBtn = (Button) findViewById(R.id.explore_btn);
        runBtn = (Button) findViewById(R.id.run_btn);
        manualBtn = (Button) findViewById(R.id.manual_btn);

    }

    @Override
    public boolean onPrepareOptionsMenu(Menu menu) {
        MenuItem item = menu.findItem(R.id.action_bluetooth);
        item.setVisible(true);
        super.onPrepareOptionsMenu(menu);
        return true;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.action_bluetooth, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {

            case R.id.action_bluetooth:

                return true;

            default:
                return super.onOptionsItemSelected(item);

        }
    }

}
