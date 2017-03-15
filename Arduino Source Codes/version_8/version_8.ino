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
int MovementCountAvg;
double calibratedFrontCentreDist = 13.5 ;//9.6
boolean error=true;
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
boolean repo = true;
unsigned long prev_ms = 0;
unsigned long interval = 0;
double m1Speed = 0, m2Speed = 0;
int objPos[5] = {'\0', '\0', '\0', '\0', '\0'};
String fastestpath;

//---------------Movement Parameter---------------------------------------------------------

boolean TurningLeftTest=false,TurningRightTest=false;
boolean movingTest=false;

int leftmotorspeed=185,rightmotorspeed=200;

double kdl=6.07, kdr=5.86;
void setup() {
  Serial.begin(115200);
  PCintPort::attachInterrupt(3, &compute_m1_ticks, RISING); //Attached to Pin 3
  PCintPort::attachInterrupt(5, &compute_m2_ticks, RISING); //Attached to Pin 5
  md.init();
}


void loop() {
  if(TurningLeftTest==true){
   delay(400);
   TurnAngle(90);
   }

   if(TurningRightTest==true){
   delay(400);
   TurnAngle(-90);
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
    }
  
  //check if algo is sending any values to arduino
  if (Serial.available() > 0) {
    commands = (char)Serial.read();
    if (commands == 'o') { //if fastest path, send command
        while(Serial.available() > 0){
            fastestpath.concat(commands);
            if (commands == '\n')
            break;
        }
     }
  }

  //fastest path 
  if (fastestpath.length()>0) {

    for (int i = 0; i < fastestpath.length(); i++) {
      if (fastestpath[i] >= 48 && fastestpath[i] <= 57 && fastestpath[i + 1] >= 48 && fastestpath[i + 1] <= 57) {
          totalgrid = (fastestpath[i] - 48) * 10 + (fastestpath[i + 1] - 48);
          commands = 48;
          i++;

      }

      else if (fastestpath[i] >= 48 && fastestpath[i] <= 57) {
          totalgrid = fastestpath[i] - 48;
          commands = 48;
      }
      
      else 
        commands = fastestpath[i];
        
      action();

    }
  }
  
  else
    action();
}

void action() {
  switch (commands) {
    case 'm':
     //send the sensor values to algo
      objScan();
    
      //check if repositioning was being sent by algo
    if(error==true){
        
      //if the robot is not straight
        if (objPos[4] == 1 && objPos[5] == 1) 
        RightReposition();
       
       //if the robot is too far away from the block
        if (objPos[4] == 1 && objPos[5] == 1) {
          int pos = realignRideSide();
          if (pos == 1) {
              TurnAngle(-90);
              FindFrontSensorAvg();
              FindFrontSensorAvg();
                
                if (frontLeftSensorAvg <= 16.5&&frontRightSensorAvg <=16.5)
                    repositionRobotFront() ;
           
                if (frontCentreSensorAvg<=17)
                  realignRobotCentre() ;
          
              TurnAngle(90);
         }
       }
       
       //if there is a corner
        error=false;
    }

      commands = 'z';
      break;

    case'e': //front wall calibration
      for (long startTime = millis(); (millis() - startTime) < 50;) 
        FindFrontSensorAvg();
            
      //check 2 conditions
      //3 blocks in front
      
      if (frontLeftSensorAvg <= 15 && frontRightSensorAvg <= 15 && frontCentreSensorAvg <= 16){ 
        repositionRobotFront();
        realignRobotCentre() ;
        repositionRobotFront();
      }
      
      //2 blocks left and right in front
      if (frontLeftSensorAvg <= 14 && frontRightSensorAvg <= 14)
        repositionRobotFront();
       
        commands = 'z';
        error = false;
        break;

    case 'f':
      moveOneGrid(1);
      commands = 'z';
      error = true;
      break;

    case 'l':
      TurnAngle(90);
      commands = 'z';
      error= true;
      break;

    case 'r':
      TurnAngle(-90);
      commands = 'z';
      error = true;
      break;

    case 'd':
    //corner calibration
        TurnAngle(-90);
        repositionRobotFront() ;
        realignRobotCentre() ;
        TurnAngle(90);
        realignRobotCentre();
        repositionRobotFront() ;
      
      commands = 'z';
      error = false;
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

  if ((current_ms - prev_ms) > 5) {
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
  int inc = 0;
  m1MovementCount = 0;
  m2MovementCount = 0;

  MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  
  if (grid % 5 == 0) 
    inc = grid / 5;
  
  grid = grid * (218 + inc);

  while (MovementCountAvg < grid) {
    moveForward(leftmotorspeed, rightmotorspeed); //175//220
    MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  }

    md.setBrakes(330, 300);
    delay(380);
    m1Ticks = 0;
    m2Ticks = 0;
}

void TurnAngle(int degree){
  int tick = 0;
  unsigned long current_ms = millis();
 
  if (degree > 0) {
    left = 1;
    right = -1;
   // kd = 6.07;
    tick = kdl * abs(degree);

  }
 
  else if (degree < 0) {
    left = -1;
    right = 1;
    //kd = 5.86;
    tick = kdr * abs(degree);

  }
  
   
  while (tick > 0){
      moveForward(125, 100);
      delay(2);
      tick--;
  }

  left = 1;
  right = 1;
  md.setBrakes(330, 300);
  delay(380);
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

  while ((abs(frontLeftSensorAvg - frontRightSensorAvg) > 0.7)&&check<15) {

    if (frontLeftSensorAvg > frontRightSensorAvg) 
      TurnAngle(-4);
    
    else if (frontLeftSensorAvg < frontRightSensorAvg) 
      TurnAngle(4);
    

    for (long startTime = millis(); (millis() - startTime) < 100;) {
      FindFrontSensorAvg();
    }
    check++;
  }
  md.setBrakes(330, 300);
  delay(350);
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
    moveForward(70, 60);
    for (long startTime = millis(); (millis() - startTime) < 50;) {
      FindFrontSensorAvg();
    }
  }

  md.setBrakes(330, 300);
  delay(300);

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
  delay(300);
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
        TurnAngle(-6);
        delay(5);
      }
      
      if (NewRightSensorAvg > rightSensorAvg)
      {
        TurnAngle(7);
        delay(5);
      }

    for (long startTime = millis(); (millis() - startTime) < 50;)
      FindLeftRightSensorsAvg() ;


  }
    check++;
}


//---------------Send sensor reading to PC---------------------------------------
void objScan() {
  for (long startTime = millis(); (millis() - startTime) < 50;)
  computeMedian();
  

  if (leftSensorMedian <= 18 && leftSensorMedian > 0) 
    objPos[0] = 1;
  else if (leftSensorMedian <= 28 && leftSensorMedian > 18)
   objPos[0] = 2;
  else
    objPos[0] = -2;

  if (frontLeftSensorMedian <= 15.0 && frontLeftSensorMedian > 0)
    objPos[1] = 1;
  else if (frontLeftSensorMedian <= 23 && frontLeftSensorMedian > 15.0)
    objPos[1] = 2;

  else
    objPos[1] = -2;

  if (frontCentreSensorMedian <= 16 && frontCentreSensorMedian > 0)
    objPos[2] = 1;
  else if (frontCentreSensorMedian <= 26.5 && frontCentreSensorMedian > 16)
    objPos[2] = 2;

  else
    objPos[2] = -2;

  if (frontRightSensorMedian <= 15.0 && frontRightSensorMedian > 0)
    objPos[3] = 1;
  else if (frontRightSensorMedian <= 23 && frontRightSensorMedian > 15.0)
    objPos[3] = 2;
  else
    objPos[3] = -2;


  if (rightSensorMedian <= 15.0 && rightSensorMedian > 0)
    objPos[4] = 1;
  else if (rightSensorMedian <= 23 && rightSensorMedian > 12.0)
    objPos[4] = 2;
  else
    objPos[4] = -2;

  if (NewRightSensorMedian <= 15 && NewRightSensorMedian > 0)
    objPos[5] = 1;
  else if (NewRightSensorMedian > 15 && NewRightSensorMedian < 24)
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






















