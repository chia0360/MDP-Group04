package com.mdpgrp4.mdp;

/**
 * Created by Cherr on 9/3/2017.
 */

public class Sensor {
    public int x_coor;
    public int y_coor;

    public Sensor(int x, int y){
        this.y_coor = y;
        this.x_coor = x;
    }

    public void setX(int x){
        this.x_coor = x;
    }

    public void setY(int y){
        this.y_coor = y;
    }

    public int getX(){
        return this.x_coor;
    }

    public int getY(){
        return this.y_coor;
    }
}
