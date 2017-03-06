package com.mdpgrp4.mdp.adapter;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import com.mdpgrp4.mdp.R;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GridAdapter extends BaseAdapter {
    private String robot_direction = "S";
    private Context context;
    private int[] map;
    public final String STATE_UNEXPLORED = "unexplored";
    public final String STATE_OBSTACLE = "obstacle";
    public final String STATE_FREE = "free";
    private final String DIRECTION_NORTH = "N";
    private final String DIRECTION_SOUTH = "S";
    private final String DIRECTION_EAST = "E";
    private final String DIRECTION_WEST = "W";
    private final String FORWARD = "f";
    private final String REVERSE = "r";
    private final String TURN_RIGHT = "tr";
    private final String TURN_LEFT = "tl";
    private int robot_curr_x;
    private int robot_curr_y;
    private List<Integer> obstacles = new ArrayList<>();

    public GridAdapter(Context c, int location_x, int location_y) {
        context = c;
        map = new int[300];
        for (int i=0; i<15; i++) {
            for (int j=0; j<20; j++) {
                updateMap(i, j, STATE_UNEXPLORED);
            }
        }
        robot_curr_x = location_x;
        robot_curr_y = location_y;
        updateRobot(location_x, location_y);
    }

    public void updateMap(int x, int y, String state) {
        if (isValidMapIndex(x, y)){
            if (x<3 && y<3) {
                map[x*20+y] = R.drawable.start;
            }
            else if (x>11 && y>16) {
                map[x*20+y] = R.drawable.goal;
            }
            else if (state.equals(STATE_FREE)) {
                if(!obstacles.contains(x*20+y)) {
                    map[x * 20 + y] = R.drawable.blue;
                }
            }
            else if (state.equals(STATE_OBSTACLE)) {
                map[x*20+y] = R.drawable.block;
                obstacles.add(x*20+y);
            }
            else if (state.equals(STATE_UNEXPLORED)) {
                map[x*20+y] = R.drawable.gray;
            }
            else {
                Log.e("Map", "Invalid state: " + state);
            }
        }
    }

    public void updateRobot(int y, int x ) {
        if (isValidMapIndex(x, y)) {
            int image = R.drawable.robot_s_01;
            for(int i = 0; i<3; i++) {
                for(int j=0; j<3; j++) {
                    updateMap( robot_curr_y + j, robot_curr_x + i, STATE_FREE);
                }
            }
            if (robot_direction.equals(DIRECTION_EAST))
                image = R.drawable.robot_e_01;
            else if (robot_direction.equals(DIRECTION_WEST))
                image = R.drawable.robot_w_01;
            else if (robot_direction.equals(DIRECTION_NORTH))
                image = R.drawable.robot_n_01;
            else if (robot_direction.equals(DIRECTION_SOUTH))
                image = R.drawable.robot_s_01;
            for (int i=0; i<3; i++) {
                for (int j=0; j<3; j++) {
                    map[(x+i)*20+(y+j)] = image+i*3+j;
                }
            }

            robot_curr_x = y;
            robot_curr_y = x;

            if(robot_direction.equals(DIRECTION_EAST)) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 3; j++) {
                        updateMap(robot_curr_y + j, robot_curr_x + 3 + i, STATE_FREE);
                    }
                }
                for (int j = 0; j < 2; j++) {
                    updateMap(robot_curr_y + 3 + j, robot_curr_x + 2, STATE_FREE);
                    updateMap(robot_curr_y - 1 - j, robot_curr_x + 2, STATE_FREE);
                }
            }else if(robot_direction.equals(DIRECTION_WEST)) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 3; j++) {
                        updateMap(robot_curr_y + j, robot_curr_x - 1 - i, STATE_FREE);
                    }
                }
                for (int j = 0; j < 2; j++) {
                    updateMap(robot_curr_y + 3 + j, robot_curr_x, STATE_FREE);
                    updateMap(robot_curr_y - 1 - j, robot_curr_x, STATE_FREE);
                }
            }else if(robot_direction.equals(DIRECTION_SOUTH)) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 3; j++) {
                        updateMap(robot_curr_y  + 3 + i, robot_curr_x + j, STATE_FREE);
                    }
                }
                for (int j = 0; j < 2; j++) {
                    updateMap(robot_curr_y + 2, robot_curr_x + 3 + j, STATE_FREE);
                    updateMap(robot_curr_y + 2, robot_curr_x - 1 - j, STATE_FREE);
                }
            }else if(robot_direction.equals(DIRECTION_NORTH)) {
                for (int i = 0; i < 2; i++) {
                    for (int j = 0; j < 3; j++) {
                        updateMap(robot_curr_y - 1 - i, robot_curr_x + j, STATE_FREE);
                    }
                }
                for (int j = 0; j < 2; j++) {
                    updateMap(robot_curr_y, robot_curr_x + 3 + j, STATE_FREE);
                    updateMap(robot_curr_y, robot_curr_x - 1 - j, STATE_FREE);
                }
            }
            notifyDataSetChanged();
        }

    }

    public boolean isValidMapIndex(int x, int y) {
        return (x>=0 && x<15 && y>=0 && y<20);
    }

    public int getCount() {
        return map.length;
    }

    public Object getItem(int position) {
        return map[position];
    }

    public void setItem(int position, String state) {
        List<Integer> positions = new ArrayList<>(Arrays.asList(0, 1, 2, 20, 21, 22, 40, 41, 42, 257, 258, 259, 277, 278, 279, 297, 298, 299));
        if(!positions.contains(position)) {
            int label = R.drawable.gray;
            if (state.equals(STATE_FREE)) {
                label = R.drawable.blue;
            } else if (state.equals(STATE_OBSTACLE)) {
                label = R.drawable.block;
            }
            // map[position] = label;
            updateMap(position%15, position/15, state);
            notifyDataSetChanged();
        }
    }

    public long getItemId(int position) {
        return 0;
    }

    // create a new ImageView for each item referenced by the Adapter
    public View getView(int position, View convertView, ViewGroup parent) {
        ImageView imageView;
        if (convertView == null) {
            imageView = new ImageView(context);
            imageView.setAdjustViewBounds(true);
        } else {
            imageView = (ImageView) convertView;
        }
        imageView.setImageResource(map[position]);
        return imageView;
    }

    public void moveRobot(String command){
        if(command.equals(FORWARD)){
            if (robot_direction.equals(DIRECTION_NORTH)) {
                if (isValidMapIndex(robot_curr_y - 1, robot_curr_x))
                    updateRobot(robot_curr_x, robot_curr_y - 1);
            }
            else if (robot_direction.equals(DIRECTION_SOUTH)) {
                if (isValidMapIndex(robot_curr_y + 3, robot_curr_x))
                    updateRobot(robot_curr_x, robot_curr_y + 1);
            }
            else if (robot_direction.equals(DIRECTION_EAST)) {
                if (isValidMapIndex(robot_curr_y, robot_curr_x + 3))
                    updateRobot(robot_curr_x + 1, robot_curr_y);
            }
            else if (robot_direction.equals(DIRECTION_WEST)) {
                if (isValidMapIndex(robot_curr_y, robot_curr_x - 1))
                    updateRobot(robot_curr_x - 1, robot_curr_y);
            }
        }
        else if(command.equals(REVERSE)){
            if (robot_direction.equals(DIRECTION_NORTH))
                updateRobot(robot_curr_x, robot_curr_y+1);
            else if (robot_direction.equals(DIRECTION_SOUTH))
                updateRobot(robot_curr_x, robot_curr_y-1);
            else if (robot_direction.equals(DIRECTION_EAST))
                updateRobot(robot_curr_x-1, robot_curr_y);
            else if (robot_direction.equals(DIRECTION_WEST))
                updateRobot(robot_curr_x+1, robot_curr_y);
        }
        else if(command.equals(TURN_RIGHT)){
            if (robot_direction.equals(DIRECTION_NORTH))
                robot_direction = DIRECTION_EAST;
            else if (robot_direction.equals(DIRECTION_SOUTH))
                robot_direction = DIRECTION_WEST;
            else if (robot_direction.equals(DIRECTION_EAST))
                robot_direction = DIRECTION_SOUTH;
            else if (robot_direction.equals(DIRECTION_WEST))
                robot_direction = DIRECTION_NORTH;
            updateRobot(robot_curr_x, robot_curr_y);
        }
        else if(command.equals(TURN_LEFT)){
            if (robot_direction.equals(DIRECTION_NORTH))
                robot_direction = DIRECTION_WEST;
            else if (robot_direction.equals(DIRECTION_SOUTH))
                robot_direction = DIRECTION_EAST;
            else if (robot_direction.equals(DIRECTION_EAST))
                robot_direction = DIRECTION_NORTH;
            else if (robot_direction.equals(DIRECTION_WEST))
                robot_direction = DIRECTION_SOUTH;
            updateRobot(robot_curr_x, robot_curr_y);
        }
    }
}