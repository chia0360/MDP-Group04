package com.example.cherr.bluetooth3.adapter;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import com.example.cherr.bluetooth3.R;

public class GridAdapter extends BaseAdapter {
    private String robot_direction = "S";
    private Context context;
    private int[] map;
    private final String STATE_UNEXPLORED = "unexplored";
    private final String STATE_OBSTACLE = "obstacle";
    private final String STATE_FREE = "free";
    private final String DIRECTION_NORTH = "N";
    private final String DIRECTION_SOUTH = "S";
    private final String DIRECTION_EAST = "E";
    private final String DIRECTION_WEST = "W";


    public GridAdapter(Context c, int location_x, int location_y) {
        context = c;
        map = new int[300];
        for (int i=0; i<15; i++) {
            for (int j=0; j<20; j++) {
                updateMap(i, j, STATE_UNEXPLORED);
            }
        }
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
                map[x*20+y] = R.drawable.blue;
            }
            else if (state.equals(STATE_OBSTACLE)) {
                map[x*20+y] = R.drawable.red;
            }
            else if (state.equals(STATE_UNEXPLORED)) {
                map[x*20+y] = R.drawable.gray;
            }
            else {
                Log.e("Map", "Invalid state: " + state);
            }
        }
        Log.e("Map", "Invalid index: ("+Integer.toString(x)+","+ Integer.toString(y)+")");
    }

    public void updateRobot(int x, int y) {
        if (isValidMapIndex(x-1, y-1) && isValidMapIndex(x+1, y+1)) {
            if (robot_direction.equals(DIRECTION_EAST)) {
                int image = R.drawable.robot_e_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals(DIRECTION_WEST)) {
                int image = R.drawable.robot_w_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals(DIRECTION_NORTH)) {
                int image = R.drawable.robot_n_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals(DIRECTION_SOUTH)) {
                int image = R.drawable.robot_s_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
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
        int label = R.drawable.gray;
        if (state.equals(STATE_FREE)) {
            label = R.drawable.blue;
        }
        else if (state.equals(STATE_OBSTACLE)) {
            label = R.drawable.red;
        }
        map[position] = label;
        notifyDataSetChanged();
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

    public void notifyDataSetChanged(int x, int y)
    {
        notifyDataSetChanged();
        updateRobot(x, y);
    }

}