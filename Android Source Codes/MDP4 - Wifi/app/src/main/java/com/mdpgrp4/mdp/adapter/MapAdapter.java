package com.mdpgrp4.mdp.adapter;
import android.content.Context;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;

import com.mdpgrp4.mdp.R;
import com.mdpgrp4.mdp.Sensor;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MapAdapter extends BaseAdapter {
    private Context context;
    private int[] map;
    public final String STATE_UNEXPLORED = "unexplored";
    public final String STATE_OBSTACLE = "obstacle";
    public final String STATE_FREE = "free";
    public final String STATE_FREE_MAP = "freefromobs";
    private final char DIRECTION_NORTH = 'N';
    private final char DIRECTION_SOUTH = 'S';
    private final char DIRECTION_EAST = 'E';
    private final char DIRECTION_WEST = 'W';
    private final String FORWARD = "f";
    private final String REVERSE = "r";
    private final String TURN_RIGHT = "tr";
    private final String TURN_LEFT = "tl";
    private int robot_curr_x;
    private int robot_curr_y;
    private int robot_next_x;
    private int robot_next_y;
    private char robot_curr_direction = 'S';
    private char robot_next_direction;
    private List<Integer> obstacles = new ArrayList<>();
    private List<Integer> explored = new ArrayList<>();

    public MapAdapter(Context c, int location_x, int location_y) {
        context = c;
        map = new int[300];
        for (int i=0; i<15; i++) {
            for (int j=0; j<20; j++) {
                replaceMap(i, j, STATE_UNEXPLORED);
            }
        }
        robot_curr_x = location_x;
        robot_curr_y = location_y;
        robot_next_x = robot_curr_x;
        robot_next_y=robot_curr_y;
        robot_next_direction=robot_curr_direction;

        replaceRobot(location_x, location_y, DIRECTION_SOUTH);
    }

    public void updateMap() {
        System.out.println(obstacles.toString());
        System.out.println(explored.toString());
        //if Robot position changed, change the space it was previously occupying back to map
        if (robot_curr_x != robot_next_x || robot_curr_y != robot_next_y) {
            for (int i = robot_curr_x - 1; i < robot_curr_x + 2; i++) {
                for (int j = robot_curr_y - 1; j < robot_curr_y + 2; j++) {
                    if (!(i >= robot_next_x - 1 && i <= robot_next_x + 1 && j >= robot_next_y - 1 && j <= robot_next_y + 1)) {
                        replaceMap(i, j, STATE_FREE);
                    }
                }
            }
        }
        //update non-robot area
        for (int i=0; i<15; i++) {
            for (int j=0; j<20; j++) {
                if (!(i >= robot_next_x - 1 && i <= robot_next_x + 1 && j >= robot_next_y - 1 && j <= robot_next_y + 1)) {
                    if(explored.contains(i*20+j)){
                        if(obstacles.contains(i*20+j)) {
                            replaceMap(i, j, STATE_OBSTACLE);
                        }
                        else{
                            replaceMap(i, j, STATE_FREE);
                        }
                    }
                }
            }
        }

        //Place robot on map
        if(robot_curr_x != robot_next_x || robot_curr_y != robot_next_y || robot_curr_direction != robot_next_direction){
            replaceRobot(robot_next_x,robot_next_y,robot_next_direction);

        }

        robot_curr_direction = robot_next_direction;
        robot_curr_x = robot_next_x;
        robot_curr_y = robot_next_y;
        notifyDataSetChanged();
    }

    public void replaceRobot(int x, int y, char direction){
        int image = R.drawable.robot_s_01;
        if (direction == DIRECTION_EAST)
            image = R.drawable.robot_e_01;
        else if (direction == DIRECTION_WEST)
            image = R.drawable.robot_w_01;
        else if (direction == DIRECTION_NORTH)
            image = R.drawable.robot_n_01;
        else if (robot_curr_direction == DIRECTION_SOUTH)
            image = R.drawable.robot_s_01;
        for (int i=0; i<3; i++) {
            for (int j=0; j<3; j++) {
                map[(x+i-1)*20+(y+j-1)] = image+i*3+j;
            }
        }
    }

    public void replaceMap(int x, int y, String state) {
        if (isValidMapIndex(x, y)){
            // Start & Goal areas
            if (x<3 && y<3) {
                map[x*20+y] = R.drawable.start;
            }
            else if (x>11 && y>16) {
                map[x*20+y] = R.drawable.goal;
            }
            else if (state.equals(STATE_UNEXPLORED)) {
                map[x*20+y] = R.drawable.gray;
            }
            else if (state.equals(STATE_FREE)) {
                map[x*20+y] = R.drawable.blue;
            }
            else if (state.equals(STATE_OBSTACLE)) {
                map[x*20+y] = R.drawable.block;
            }
        }
    }

    public boolean isValidMapIndex(int x, int y) {
        return (x>=0 && x<15 && y>=0 && y<20);
    }

    public boolean isValidRobotIndex(int x, int y) {
        return (x>=1 && x<14 && y>=1 && y<19);
    }

    public int getCount() {
        return map.length;
    }

    public Object getItem(int position) {
        return map[position];
    }

    public void updateSensor(String[] sensor){
        for(int i=1; i<6; i++) {
            int value = Integer.parseInt(sensor[i]);
            System.out.println(value);
            int position1 = -1;
            int position2 = -1;
            Sensor s1 = null;
            Sensor s2 = null;
            switch (i) {
                case 1:
                    s1 = getFirstLeft();
                    s2 = getSecondLeft();
                    break;
                case 2:
                    s1 = getFirstFrontLeft();
                    s2 = getSecondFrontLeft();
                    break;
                case 3:
                    s1 = getFirstFrontMiddle();
                    s2 = getSecondFrontMiddle();
                    break;
                case 4:
                    s1 = getFirstFrontRight();
                    s2 = getSecondFrontRight();
                    break;
                case 5:
                    s1 = getFirstRight();
                    s2 = getSecondRight();
                    break;
            }
            if(s1 != null && s2!= null){
                position1 = s1.getX() * 20 + s1.getY();
                position2 = s2.getX() * 20 + s2.getY();
            }
            switch (value) {
                case 1:
                    if(s1.isValid() && position1 != -1) {
                        if (!obstacles.contains(position1))
                            obstacles.add(position1);
                        if (!explored.contains(position1))
                            explored.add(position1);
                    }
                    break;
                case 2:
                    if (s1.isValid() && position1 != -1 ) {
                        if (obstacles.contains(position1))
                            obstacles.remove(obstacles.indexOf(position1));
                        if (!explored.contains(position1))
                            explored.add(position1);
                    }
                    if(s2.isValid() && position2 != -1) {
                        if (!obstacles.contains(position2))
                            obstacles.add(position2);
                        if (!explored.contains(position2))
                            explored.add(position2);
                    }
                    break;
                default:
                    if(s1.isValid() && position1 != -1){
                        if (!explored.contains(position1))
                            explored.add(position1);
                        if (obstacles.contains(position1))
                            obstacles.remove(obstacles.indexOf(position1));
                    }
                    if(s2.isValid() && position2 != -1) {
                        if (!explored.contains(position2))
                            explored.add(position2);
                        if (obstacles.contains(position2))
                            obstacles.remove(obstacles.indexOf(position2));
                    }
                    break;
            }
        }
        updateMap();
    }


    public void moveRobot(String command){
        if(command.equals(FORWARD)){
            if (robot_curr_direction == DIRECTION_NORTH) {
                if (isValidRobotIndex(robot_curr_x - 1, robot_curr_y)) {
                    robot_next_x = robot_curr_x-1;
                    robot_next_y = robot_curr_y;
                }
            }
            else if (robot_curr_direction == DIRECTION_SOUTH){
                if (isValidRobotIndex(robot_curr_x +1, robot_curr_y)) {
                    robot_next_x = robot_curr_x+1;
                    robot_next_y = robot_curr_y;
                }
            }
            else if (robot_curr_direction == DIRECTION_EAST) {
                if (isValidRobotIndex(robot_curr_x, robot_curr_y+1)) {
                    robot_next_x = robot_curr_x;
                    robot_next_y = robot_curr_y+1;
                }
            }
            else if (robot_curr_direction == DIRECTION_WEST) {
                if (isValidRobotIndex(robot_curr_x, robot_curr_y-1)) {
                    robot_next_x = robot_curr_x;
                    robot_next_y = robot_curr_y-1;
                }
            }
            updateMap();
        }
        else if(command.equals(TURN_RIGHT)){
            if (robot_curr_direction == DIRECTION_NORTH)
                robot_next_direction = DIRECTION_EAST;
            else if (robot_curr_direction == DIRECTION_SOUTH)
                robot_next_direction = DIRECTION_WEST;
            else if (robot_curr_direction == DIRECTION_EAST)
                robot_next_direction = DIRECTION_SOUTH;
            else if (robot_curr_direction == DIRECTION_WEST)
                robot_next_direction = DIRECTION_NORTH;
            //updateRobot(robot_curr_x, robot_curr_y);
            updateMap();
        }
        else if(command.equals(TURN_LEFT)){
            if (robot_curr_direction == DIRECTION_NORTH)
                robot_next_direction = DIRECTION_WEST;
            else if (robot_curr_direction== DIRECTION_SOUTH)
                robot_next_direction = DIRECTION_EAST;
            else if (robot_curr_direction == DIRECTION_EAST)
                robot_next_direction = DIRECTION_NORTH;
            else if (robot_curr_direction == DIRECTION_WEST)
                robot_next_direction = DIRECTION_SOUTH;
            //updateRobot(robot_curr_x, robot_curr_y);
            updateMap();
        }
    }

    public Sensor getFirstFrontMiddle(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x, robot_curr_y+2);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x, robot_curr_y-2);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+2, robot_curr_y);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-2, robot_curr_y);
        }
        return s;
    }

    public Sensor getSecondFrontMiddle(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x, robot_curr_y+3);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x, robot_curr_y-3);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+3, robot_curr_y);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-3, robot_curr_y);
        }
        return s;
    }

    public Sensor getFirstFrontLeft(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x-1, robot_curr_y+2);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x+1, robot_curr_y-2);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+2, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-2, robot_curr_y-1);
        }
        return s;
    }

    public Sensor getSecondFrontLeft(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x-1, robot_curr_y+3);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x+1, robot_curr_y-3);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+3, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-3, robot_curr_y-1);
        }
        return s;
    }

    public Sensor getFirstFrontRight(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x+1, robot_curr_y+2);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x-1, robot_curr_y-2);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+2, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-2, robot_curr_y+1);
        }
        return s;
    }

    public Sensor getSecondFrontRight(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x+1, robot_curr_y+3);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x-1, robot_curr_y-3);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+3, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-3, robot_curr_y+1);
        }
        return s;
    }

    public Sensor getFirstLeft(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x-2, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x+2, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+1, robot_curr_y+2);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-1, robot_curr_y-2);
        }
        return s;
    }

    public Sensor getSecondLeft(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x-3, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x+3, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+1, robot_curr_y+3);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-1, robot_curr_y-3);
        }
        return s;
    }

    public Sensor getFirstRight(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x+2, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x-2, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+1, robot_curr_y-2);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-1, robot_curr_y+2);
        }
        return s;
    }


    public Sensor getSecondRight(){
        Sensor s = null;
        if(robot_curr_direction == DIRECTION_EAST) {
            s = new Sensor(robot_curr_x+3, robot_curr_y+1);
        }
        else if(robot_curr_direction == DIRECTION_WEST) {
            s = new Sensor(robot_curr_x-3, robot_curr_y-1);
        }
        else if(robot_curr_direction == DIRECTION_SOUTH) {
            s = new Sensor(robot_curr_x+1, robot_curr_y-3);
        }
        else if(robot_curr_direction == DIRECTION_NORTH) {
            s = new Sensor(robot_curr_x-1, robot_curr_y+3);
        }
        return s;
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
}