//FRONT CALIBRATION CHECK AGAIN
#include "PinChangeInt.h"
#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;
#define arraySize 10

//----------------------Sensors------------------------------------------------------------
int RightSensorPin = A3;
int frontCentreSensorPin = A0;
int frontLeftSensorPin = A2; 
int leftSensorPin = A5;
int frontRightSensorPin = A4;
int NewRightSensorPin = A1;

//----------------------Variables------------------------------------------------------------

double leftSensorArray[arraySize], rightSensorArray[arraySize], frontRightSensorArray[arraySize], frontLeftSensorArray[arraySize], NewRightSensorArray[arraySize], frontCentreSensorArray[arraySize];
double leftSensorMedian = 0.0, rightSensorMedian = 0.0,  frontRightSensorMedian = 0.0, frontLeftSensorMedian = 0.0, NewRightSensorMedian = 0.0;
double frontCentreSensorMedian = 0.0;

int x = 0;
int left = 1, right = 1;
int counterF=0;
int MovementCountAvg;
double calibratedFrontCentreDist = 13.5 ;//9.6

double LeftSensorValue = 0, rightSensorValue = 0, frontRightSensorValue = 0, frontLeftSensorValue = 0, frontCentreSensorValue = 0;
int commands = 'z';

double leftSensorAvg = 0.0, rightSensorAvg = 0.0,  frontRightSensorAvg = 0.0, frontLeftSensorAvg = 0.0, frontCentreSensorAvg = 0.0;
double NewRightSensorValue = 0.0, NewRightSensorAvg = 0.0;
//----------------Motor movement---------------------------------------------------------
//Measuring movement counts and ticks of m1 and m2
volatile int m1Ticks = 0, m2Ticks = 0;
volatile int m1MovementCount = 0, m2MovementCount = 0,  m1 = 0, m2 = 0;


//PID Parameters
double curError = 0.0;
double prevError = 0.0;
int totalgrid;
double kP = -6.9;
double Adjust = 0;

boolean error=true;
boolean repo = true;
boolean cornerrepositioning=true;

unsigned long prev_ms = 0;
unsigned long interval = 0;
double m1Speed = 0, m2Speed = 0;
int objPos[5] = {'\0', '\0', '\0', '\0', '\0'};
String fastestpath;
int count=0;

//---------------Movement Parameter---------------------------------------------------------
//int gridcompensation=5;
boolean TurningLeftTest=false,TurningRightTest=false;
boolean movingTest=false;
int leftmotorspeed=208,rightmotorspeed=242;//212 //242 //left inc -->right
int test=false;
boolean Astar=false;
int leftAngleTarget=370,rightAngleTarget=367;
int movement=240; //245
boolean fastestpathspeed=false;
void setup() {
  Serial.begin(115200);
  PCintPort::attachInterrupt(3, &compute_m1_ticks, RISING); //Attached to Pin 3
  PCintPort::attachInterrupt(5, &compute_m2_ticks, RISING); //Attached to Pin 5
  md.init();
//moveOneGrid(1);
}


void loop() {
  //objScan();
  //Serial.println(leftSensorMedian);

  if(fastestpathspeed==true){
    while(1){
    moveForward(355,300); //left inc-->left //right //left
    FindFrontSensorAvg();
    if(frontLeftSensorAvg<=15 ||frontRightSensorAvg<=15 ||frontCentreSensorAvg<=15){
    fastestpathspeed=false;
    md.setBrakes(400,400);

    break;
    }
    
    }
  }
   if(TurningLeftTest==true){
   delay(400);
   TurnLeftAngle();
   }

   if(TurningRightTest==true){
   delay(400);
   TurnRightAngle();
   }

   if(movingTest==true){
    delay(500);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);
    moveOneGrid(1);

  }
   
  
 //check if algo is sending any values to arduino
  if (Serial.available() > 0) 
    commands = (char)Serial.read();
    
  if (commands == 'o') { //if fastest path, send command
        Astar=true;

     rightmotorspeed=355;
        leftmotorspeed=300;
        
     
        while(Serial.available() > 0|| commands!='\n'){ 
           commands = (char)Serial.read();

                 switch(commands){
                     case 'f':
                       counterF = counterF+1;
                     //  Serial.println(counterF);
                      // Serial.println('\n');
                       break;
  
                    case 'r':
                      totalgrid = counterF;
                      moveOneGrid(totalgrid);
                       TurnRightAngle();
                      counterF = 0;
                      break;
                      
                    case 'l':
                      totalgrid = counterF;
                      moveOneGrid(totalgrid);
                      TurnLeftAngle();
                      counterF = 0;
                      break;

                    case '\n':
                      if(counterF>0){
                             totalgrid=counterF;
                             moveOneGrid(totalgrid);
                             counterF=0;
                      }  
                      break;
                    default:
                      // bye
                      break;   
                 }
               
            
          }
      }
  else
     action();
}

void action() {
  switch (commands) {
      case 'm':
      //check if repositioning was being sent by algo
      //  if(error==true){ //to prevent double repositioning
        
         FindLeftRightSensorsAvg() ;
         FindFrontSensorAvg();
      
      //if the robot is not straight
          if (rightSensorAvg<=14 && NewRightSensorAvg<= 14) 
          RightReposition();


       if(frontLeftSensorAvg<=16.5 &&frontRightSensorAvg<=16.5 &&frontCentreSensorAvg<=17){
         repositionRobotFront();
         realignRobotCentre() ;
          repositionRobotFront();
          count=0;
       }

    //  else if (frontLeftSensorAvg<=15 &&frontRightSensorAvg<=15)
      //         repositionRobotFront();

      else if(frontLeftSensorAvg<=15 &&frontCentreSensorAvg<=14){
              realignRobotCentre() ;
              repositionRobotFrontLeft();
               realignRobotCentre() ;
           //    count=0;

      }

      else if(frontRightSensorAvg<=15 &&frontCentreSensorAvg<=14){
              realignRobotCentre() ;
              repositionRobotFrontRight();
               realignRobotCentre() ;
               count=0;

      }
  
      
       //if right sides is a wall, and robot is too far from the wall
        if (rightSensorAvg<=15 && NewRightSensorAvg<= 15) {
            int pos = realignRideSide();
              if (pos == 1) {
                  TurnRightAngle();
                  FindFrontSensorAvg();
                  FindFrontSensorAvg();
                    
                  if (frontLeftSensorAvg <= 16.5&&frontRightSensorAvg <=16.5 &&frontCentreSensorAvg<=17){ //if front sensor has sth
                  repositionRobotFront() ;
                  realignRobotCentre() ;
                  repositionRobotFront() ;
                  }
          
              TurnLeftAngle();
         }
       }

       
      objScan();
      delay(500);
      commands = 'z';
      break;

    case 'f':
      moveOneGrid(1);
      error = true;
      cornerrepositioning=true;
      commands = 'm';
      break;

    case 'l':
      TurnLeftAngle();
      error= true;
      cornerrepositioning=true;
      commands = 'm';
      break;

    case 'r':
      TurnRightAngle();
      error = true;
      cornerrepositioning=true;
      commands = 'm';
      break;
      
    case'e': //front wall calibration
      for (long startTime = millis(); (millis() - startTime) < 50;) 
        FindFrontSensorAvg();
            
      //check 2 conditions
      //3 blocks in front

      if(cornerrepositioning==true){
              if (frontLeftSensorAvg <= 15 && frontRightSensorAvg <= 15 && frontCentreSensorAvg <= 16){ 
                repositionRobotFront();
                realignRobotCentre() ;
                repositionRobotFront();
                count=0;
              }
              
              //2 blocks left and right in front
              if (frontLeftSensorAvg <= 14 && frontRightSensorAvg <= 14)
                repositionRobotFront();
      }        
        
        commands = 'z';
        error = false;
        cornerrepositioning=false;
        break;
        
    case 'd':
    //corner calibration
        TurnRightAngle();
        repositionRobotFront() ;
        realignRobotCentre() ;
        TurnLeftAngle();
        realignRobotCentre();
        repositionRobotFront() ;
        commands = 'm';
        error = false;
        cornerrepositioning=false;
        count=0;
       break;

    case 'g':
    RightReposition();
    break;
    
    case 48:
      moveOneGrid(totalgrid);
      break;
  }
}

//-------------Motor Interrupt----------------------------
void compute_m1_ticks() {
  m1Ticks++;
  m1MovementCount++;
}

void compute_m2_ticks() {
  m2Ticks++;
  m2MovementCount++;
}

//-------------PID----------------------------

void Alignment() {
  Adjust = 0;
  curError = m2Ticks - m1Ticks;
  Adjust = kP * curError;

}

void moveForward(double m1Speed, double m2Speed) {
  unsigned long current_ms = millis() ;
  
    if ((current_ms - prev_ms) > 50) {
      Alignment();
      m1Speed = m1Speed - Adjust;
      md.setM1Speed(m1Speed * left);
      md.setM2Speed(m2Speed * right);
      prev_ms = current_ms;
    }
}


//-------------Movements----------------------------

void moveOneGrid(int grid) {
  left = 1;
  right = 1;
  
  m1MovementCount = 0;
  m2MovementCount = 0;

  MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  
  if(Astar==true)
  grid=296.165*grid-68.0271;
  
  else
  grid = grid * (movement);
  
  //grid=movement;
  //if(count>3){ //grid compensation
  //grid=grid+gridcompensation;   
  //count=0;
  //}
  while (MovementCountAvg < grid) {
    if(Astar==true){ //e-brake
    FindFrontSensorAvg();
       if(frontLeftSensorAvg<=15 || frontRightSensorAvg<=15||frontCentreSensorAvg<=15)
       break;
    }
    moveForward(rightmotorspeed,leftmotorspeed ); //175//220
    MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  }

    md.setBrakes(312,327); // swing left > increase left //2nd value left from back //313
    delay(350);
    m1Ticks = 0;
    m2Ticks = 0;
}

void TurnAngle(int degree){
  int tick = 0;
  unsigned long current_ms = millis();
 
  if (degree > 0) {
    left = 1;
    right = -1;
  }
 
  else if (degree < 0) {
    left = -1;
    right = 1;
  }
  tick=5.30*abs(degree);
   
  while (tick > 0){
      moveForward(50, 40);
      delay(2);
      tick--;
  }

  left = 1;
  right = 1;
  md.setBrakes(330, 300);
  delay(100);
  m1Ticks = 0;
  m2Ticks = 0;
}

//-------------Sensor Readings---------------------------
void FindLeftRightSensorsAvg() {
  int sum = 0;
  rightSensorAvg = 0;
  leftSensorAvg = 0;

  for (sum = 0; sum < 25; sum++) {
    rightSensorValue = analogRead(RightSensorPin);
    NewRightSensorValue = analogRead(NewRightSensorPin);
    LeftSensorValue = analogRead(leftSensorPin);
    leftSensorAvg = leftSensorAvg + LeftSensorValue,
    rightSensorAvg = rightSensorValue + rightSensorAvg;
    NewRightSensorAvg = NewRightSensorValue + NewRightSensorAvg;
  }

  leftSensorAvg = leftSensorAvg / 25;
  rightSensorAvg = rightSensorAvg / 25;
  NewRightSensorAvg = NewRightSensorAvg / 25;
  leftSensorAvg = -1.2293 * (pow(10, -6)) * pow(leftSensorAvg, 3) + 0.00157807 * pow(leftSensorAvg, 2) - 0.756313 * leftSensorAvg + 158.344;
  rightSensorAvg = -6.71123 * pow(10, -7) * pow(rightSensorAvg, 3) + 0.000965316 * pow(rightSensorAvg, 2) - 0.482634 * rightSensorAvg + 93.7447;
  NewRightSensorAvg = -5.84716 * pow(10, -7) * pow(NewRightSensorAvg, 3) + 0.00088273 * pow(NewRightSensorAvg, 2) - 0.458497 * NewRightSensorAvg + 91.5766;

}

void FindFrontSensorAvg() {
  int sum = 0;

  frontRightSensorAvg = 0;
  frontLeftSensorAvg = 0;
  frontCentreSensorAvg = 0;

  for (sum = 0; sum < 25; sum++) {
    frontRightSensorValue = analogRead(frontRightSensorPin);
    frontRightSensorAvg = frontRightSensorValue + frontRightSensorAvg;

    frontLeftSensorValue = analogRead(frontLeftSensorPin);
    frontLeftSensorAvg = frontLeftSensorValue + frontLeftSensorAvg;

    frontCentreSensorValue = analogRead(frontCentreSensorPin);
    frontCentreSensorAvg = frontCentreSensorAvg + frontCentreSensorValue;
  }

  frontRightSensorAvg = frontRightSensorAvg / 25;
  frontLeftSensorAvg = frontLeftSensorAvg / 25;
  frontCentreSensorAvg = frontCentreSensorAvg / 25;
  frontRightSensorAvg = -2.90778 * pow(10, -7) * pow(frontRightSensorAvg, 3) + 0.000476141 * pow(frontRightSensorAvg, 2) - 0.276684 * frontRightSensorAvg + 65.1692;
  frontLeftSensorAvg = -3.97168 * pow(10, -7) * pow(frontLeftSensorAvg, 3) + 0.000595119 * frontLeftSensorAvg * frontLeftSensorAvg - 0.314918 * frontLeftSensorAvg + 68.1434;
  frontCentreSensorAvg = -9.85343 * pow(10, -7) * pow(frontCentreSensorAvg, 3) + 0.00121121 * pow(frontCentreSensorAvg, 2) - 0.525592 * frontCentreSensorAvg + 92.371;

}


//-------------Repositioning----------------------------
//repositioning front robot
void repositionRobotFront() {
  int check = 0;
  
  FindFrontSensorAvg();
  FindFrontSensorAvg();
  md.setBrakes(330, 300);

  while ((abs(frontLeftSensorAvg - frontRightSensorAvg) > 0.73)&&check<15) {
    //if(abs(frontLeftSensorAvg - frontRightSensorAvg) > 0.6&&abs(frontLeftSensorAvg - frontRightSensorAvg) < 0.7)
    //break;
    if (frontLeftSensorAvg > frontRightSensorAvg) 
      TurnAngle(-10);
    
    else if (frontLeftSensorAvg < frontRightSensorAvg) 
      TurnAngle(17);
    

    for (long startTime = millis(); (millis() - startTime) < 100;) {
      FindFrontSensorAvg();
    }
    check++;
  }
  md.setBrakes(330, 300);
  delay(200);
  m1Ticks = 0;
  m2Ticks = 0;
}

//pull the robot near a block
int realignRideSide() {
  FindLeftRightSensorsAvg();
  if (rightSensorAvg <= 9.0  || rightSensorAvg > 11.5 && rightSensorAvg <= 15.0)
    return 1;

  if (NewRightSensorAvg <= 9.5 || NewRightSensorAvg > 11.5 && rightSensorAvg <= 15.0 )
    return 1;

  else return 0;
}

//check centre distance
void realignRobotCentre() {
  FindFrontSensorAvg();
  
  while ((frontCentreSensorAvg - calibratedFrontCentreDist) > 0.1) {
      moveForward(50, 50);
      for (long startTime = millis(); (millis() - startTime) < 50;) {
        FindFrontSensorAvg();
    }
  }

  md.setBrakes(330, 300);
  delay(280);

  while ((frontCentreSensorAvg - calibratedFrontCentreDist) < 0) {
        moveForward(70, 60);
        left = -1;
        right = -1;
        for (long startTime = millis(); (millis() - startTime) < 100;) {
          FindFrontSensorAvg();
        }
  }
 
  left = 1;
  right = 1;
  md.setBrakes(330, 300);
  delay(280);
  m1Ticks = 0;
  m2Ticks = 0;

}

//ensure robot is straight
void RightReposition() {
 
  int check=0;
  for (long startTime = millis(); (millis() - startTime) < 50;)
    FindLeftRightSensorsAvg() ;

  while ((abs(NewRightSensorAvg - rightSensorAvg ) > 0.7)&&(abs(NewRightSensorAvg - rightSensorAvg ) < 10.0)&& check<10){//  && { //&&abs((NewRightSensorAvg+0.4)-rightSensorAvg )>0 ||abs((NewRightSensorAvg+0.4)-rightSensorAvg )<0  ){//||(abs(NewRightSensorAvg +0.8)-rightSensorAvg)>3.5){

      if (rightSensorAvg > NewRightSensorAvg) {
        TurnAngle(-8);
        delay(5);
      }
      
      if (NewRightSensorAvg > rightSensorAvg)
      {
        TurnAngle(9);
        delay(5);
      }

    for (long startTime = millis(); (millis() - startTime) < 50;)
      FindLeftRightSensorsAvg() ;


  }
    check++;
}

void repositionRobotFrontLeft(){
  int reposCount=0;
        FindFrontSensorAvg();

  while(abs(frontLeftSensorAvg - frontCentreSensorAvg) > 3.40 && reposCount<15||abs(frontLeftSensorAvg - frontCentreSensorAvg)<3.00 && reposCount<15){
   if(abs(frontLeftSensorAvg - frontCentreSensorAvg)>20) break;
    if((frontLeftSensorAvg+3.29)>frontCentreSensorAvg){  
      // set wheels to rotate right
     TurnAngle(-15);
    } else if((frontLeftSensorAvg+3.29)<frontCentreSensorAvg){
      // set wheels to rotate left
      TurnAngle(15);
      }
 md.setBrakes(330,300);
 for(long startTime=millis();(millis()-startTime)<50;){
      FindFrontSensorAvg();
    }
    reposCount++;
  }
}


void repositionRobotFrontRight(){
  int reposCount=0;
          FindFrontSensorAvg();

  while(abs(frontCentreSensorAvg - frontRightSensorAvg) > 4.0 && reposCount<15 ||abs(frontCentreSensorAvg - frontRightSensorAvg) < 3.3 && reposCount<15){
   if(abs(frontRightSensorAvg - frontCentreSensorAvg)>20) break;

  //if(frontCentreSensorAvg
    if(frontCentreSensorAvg>(frontRightSensorAvg+3.83)){  
    TurnAngle(-15);
    } else if(frontCentreSensorAvg<(frontRightSensorAvg+3.84)){
      TurnAngle(15);
      }
    
    // Setting wheels to brake
    md.setBrakes(330,300);
    for(long startTime=millis();(millis()-startTime)<50;){
           FindFrontSensorAvg();

    }
    reposCount++;
  }
}



//---------------Send sensor reading to PC---------------------------------------
void objScan() {
  for (long startTime = millis(); (millis() - startTime) < 50;)
  computeMedian();
  
  if (leftSensorMedian <= 20.5 && leftSensorMedian > 0) 
    objPos[0] = 1;
  else if (leftSensorMedian <= 33.5 && leftSensorMedian > 20.5) //30.5
        objPos[0] = 2;
  // else if (leftSensorMedian <= 39.0 && leftSensorMedian > 33.5) //39
    //       objPos[0] = 3;
  else
    objPos[0] = -2; //-2

  if (frontLeftSensorMedian <= 15.0 && frontLeftSensorMedian > 0)
    objPos[1] = 1;
  else if (frontLeftSensorMedian <= 23 && frontLeftSensorMedian > 15.0)
    objPos[1] = 2;
  else
      objPos[1] = -2;

  if (frontCentreSensorMedian <= 16 && frontCentreSensorMedian > 0)
    objPos[2] = 1;
  else if (frontCentreSensorMedian <= 29.0 && frontCentreSensorMedian > 16) //28.5
  objPos[2] = 2;
  else
  objPos[2] = -2;

  if (frontRightSensorMedian <= 15.0 && frontRightSensorMedian > 0)
    objPos[3] = 1;
  else if (frontRightSensorMedian <= 23.5 && frontRightSensorMedian > 15.0) //25
    objPos[3] = 2;
  else
    objPos[3] = -2;


  if (rightSensorMedian <= 15.0 && rightSensorMedian > 0)
    objPos[4] = 1;
  else if (rightSensorMedian <= 24 && rightSensorMedian > 15.0) //23
    objPos[4] = 2;
  else
    objPos[4] = -2;

  if (NewRightSensorMedian <= 15 && NewRightSensorMedian > 0)
    objPos[5] = 1;
  else if (NewRightSensorMedian > 15 && NewRightSensorMedian <= 24)
    objPos[5] = 2;
  else
    objPos[5] = -2;

//print sensor values to PC
  Serial.print(x);
  Serial.print(',');
  Serial.print(objPos[0]);
  Serial.print(',');
  Serial.print(objPos[1]);
  Serial.print(',');
  Serial.print(objPos[2]);
  Serial.print(',');
  Serial.print(objPos[3]);
  Serial.print(',');
  Serial.print(objPos[4]);
  Serial.print(',');
  Serial.print(objPos[5]);
  Serial.print("\n");
  x++;
}

//-------------Sensors-------------------------------
double frontRightSensorReading() {
  double dist = analogRead(frontRightSensorPin);
  return -2.90778 * pow(10, -7) * pow(dist, 3) + 0.000476141 * pow(dist, 2) - 0.276684 * dist + 65.1692;
}

double frontLeftSensorReading() {
  double dist = analogRead(frontLeftSensorPin);
  return -3.97168 * pow(10, -7) * pow(dist, 3) + 0.000595119 * dist * dist - 0.314918 * dist + 68.1434;
}

double frontCentreSensorReading() {
  double dist = analogRead(frontCentreSensorPin);
  return -9.85343 * pow(10, -7) * pow(dist, 3) + 0.00121121 * pow(dist, 2) - 0.525592 * dist + 92.371;
}

double rightSensorReading() {
  double dist = analogRead(RightSensorPin);
  return -6.71123 * pow(10, -7) * pow(dist, 3) + 0.000965316 * pow(dist, 2) - 0.482634 * dist + 93.7447;
}


double leftSensorReading() {
  double dist = analogRead(leftSensorPin);
  return -1.2293 * (pow(10, -6)) * pow(dist, 3) + 0.00157807 * pow(dist, 2) - 0.756313 * dist + 158.344;
}

double backRightSensorReading() {
  double dist = analogRead(NewRightSensorPin);
  return -5.84716 * pow(10, -7) * pow(dist, 3) + 0.00088273 * pow(dist, 2) - 0.458497 * dist + 91.5766;
}

//find the median of the sensor values
void computeMedian() {
  static int index = 0;

  // get reading
  leftSensorArray[index] = leftSensorReading();
  rightSensorArray[index] = rightSensorReading();
  frontRightSensorArray[index] = frontRightSensorReading();
  frontLeftSensorArray[index] = frontLeftSensorReading();
  frontCentreSensorArray[index] = frontCentreSensorReading();
  NewRightSensorArray[index] = backRightSensorReading();
  // sort data
  insertionSort();

  leftSensorMedian = leftSensorArray[arraySize / 2];
  rightSensorMedian = rightSensorArray[arraySize / 2];
  frontRightSensorMedian = frontRightSensorArray[arraySize / 2];
  frontLeftSensorMedian = frontLeftSensorArray[arraySize / 2];
  frontCentreSensorMedian = frontCentreSensorArray[arraySize / 2];
  NewRightSensorMedian = NewRightSensorArray[arraySize / 2];
  index = (index + 1) % arraySize;
}

//sorting
void insertionSort() {
  for (int i = 1; i < arraySize; i++) {
    for (int j = i; j > 0; j--) {
      if (leftSensorArray[j] < leftSensorArray[j - 1]) {
        double temp = leftSensorArray[j];
        leftSensorArray[j] = leftSensorArray[j - 1];
        leftSensorArray[j - 1] = temp;
      }
      if (rightSensorArray[j] < rightSensorArray[j - 1]) {
        double temp = rightSensorArray[j];
        rightSensorArray[j] = rightSensorArray[j - 1];
        rightSensorArray[j - 1] = temp;
      }

      if (frontLeftSensorArray[j] < frontLeftSensorArray[j - 1]) {
        double temp = frontLeftSensorArray[j];
        frontLeftSensorArray[j] = frontLeftSensorArray[j - 1];
        frontLeftSensorArray[j - 1] = temp;
      }
      if (frontCentreSensorArray[j] < frontCentreSensorArray[j - 1]) {
        double temp = frontCentreSensorArray[j];
        frontCentreSensorArray[j] = frontCentreSensorArray[j - 1];
        frontCentreSensorArray[j - 1] = temp;
      }

      if (frontRightSensorArray[j] < frontRightSensorArray[j - 1]) {
        double temp = frontRightSensorArray[j];
        frontRightSensorArray[j] = frontRightSensorArray[j - 1];
        frontRightSensorArray[j - 1] = temp;
      }

      if (NewRightSensorArray[j] < NewRightSensorArray[j - 1]) {
        double temp = NewRightSensorArray[j];
        NewRightSensorArray[j] = NewRightSensorArray[j - 1];
        NewRightSensorArray[j - 1] = temp;
      }
    }
  }
}

void TurnRightAngle(){
  left = -1;
  right = 1;
     
  while (m1Ticks <rightAngleTarget){ //m1 to
  moveForward(150, 142);
  delay(2);
  }
  
  left = 1;
  right = 1;
  md.setBrakes(300, 315);
  delay(350);
  m1Ticks = 0;
  m2Ticks = 0;
}

void TurnLeftAngle(){
    left = 1;
    right = -1;
     while (m1Ticks <leftAngleTarget){ //m1 to be any random to make it 90c
      moveForward(150, 142);
      delay(2);
    }
    
    left = 1;
    right = 1;
    
    md.setBrakes(310, 325); //310//325
    delay(350);
    m1Ticks = 0;
    m2Ticks = 0;
}





















