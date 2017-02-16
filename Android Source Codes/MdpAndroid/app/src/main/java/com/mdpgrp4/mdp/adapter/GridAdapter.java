package com.mdpgrp4.mdp.adapter;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import com.mdpgrp4.mdp.R;

import java.util.InputMismatchException;

public class GridAdapter extends BaseAdapter {
    private String robot_direction = "S";
    private int[] robot_location = {1, 1};
    private Context mContext;
    private int[] map;

    public GridAdapter(Context c) {
        mContext = c;
        map = new int[300];
        for (int i=0; i<15; i++) {
            for (int j=0; j<20; j++) {
                put_map(i, j, "unexplored");
            }
        }
        put_robot(robot_location[0], robot_location[1]);
    }

    public void put_map(int x, int y, String state) {
        if (valid_index(x, y)){
            if (x<3 && y<3) {
                map[x*20+y] = R.drawable.s_yellow;
            }
            else if (x>11 && y>16) {
                map[x*20+y] = R.drawable.g_yellow;
            }
            else if (state.equals("free")) {
                map[x*20+y] = R.drawable.blue;
            }
            else if (state.equals("obstacle")) {
                map[x*20+y] = R.drawable.red;
            }
            else if (state.equals("unexplored")) {
                map[x*20+y] = R.drawable.gray;
            }
            else {
                Log.e("Map", "Invalid state: " + state);
            }
        }
        Log.e("Map", "Invalid index: ("+Integer.toString(x)+","+ Integer.toString(y)+")");
    }

    public void put_robot(int x, int y) {
        if (valid_index(x-1, y-1) && valid_index(x+1, y+1)) {
            if (robot_direction.equals("E")) {
                int image = R.drawable.robot_e_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals("W")) {
                int image = R.drawable.robot_w_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals("N")) {
                int image = R.drawable.robot_n_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
            else if (robot_direction.equals("S")) {
                int image = R.drawable.robot_s_01;
                for (int i=0; i<3; i++) {
                    for (int j=0; j<3; j++) {
                        map[(x-1+i)*20+(y-1+j)] = image+i*3+j;
                    }
                }
            }
        }

    }

    public boolean valid_index(int x, int y) {
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
        if (state.equals("free")) {
            label = R.drawable.blue;
        }
        else if (state.equals("obstacle")) {
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
        if (convertView == null) {  // if it's not recycled, initialize some attributes
            imageView = new ImageView(mContext);

            imageView.setAdjustViewBounds(true);
//            imageView.setScaleType(ImageView.ScaleType.CENTER_CROP);
//            imageView.setPadding(1, 0, 1, 0);
        } else {
            imageView = (ImageView) convertView;
        }

        imageView.setImageResource(map[position]);

        return imageView;
    }

}