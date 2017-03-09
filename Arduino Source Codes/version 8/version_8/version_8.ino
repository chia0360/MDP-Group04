#include "PinChangeInt.h"
#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;
#define arraySize 10

//----------------------Sensors------------------------------------------------------------
int RightSensorPin= A3;
int frontCentreSensorPin = A0;//A5
int frontLeftSensorPin = A2; //A1
int leftSensorPin = A5;
int frontRightSensorPin = A4;
int NewRightSensorPin= A1;

double leftSensorArray[arraySize], rightSensorArray[arraySize], frontRightSensorArray[arraySize], frontLeftSensorArray[arraySize],NewRightSensorArray[arraySize],frontCentreSensorArray[arraySize];
double leftSensorMedian=0.0, rightSensorMedian=0.0,  frontRightSensorMedian=0.0, frontLeftSensorMedian=0.0,NewRightSensorMedian=0.0;
double frontCentreSensorMedian=0.0;

int x=0;
double kd = 0;
int left = 1, right = 1;
int MovementCountAvg;
double calibratedFrontCentreDist = 13.5 ;//9.6

double LeftSensorValue = 0, rightSensorValue = 0, frontRightSensorValue = 0, frontLeftSensorValue = 0, frontCentreSensorValue = 0;
char commands='z';

double leftSensorAvg = 0.0, rightSensorAvg = 0.0,  frontRightSensorAvg = 0.0, frontLeftSensorAvg = 0.0, frontCentreSensorAvg = 0.0;
double NewRightSensorValue=0.0,NewRightSensorAvg=0.0;
//----------------Motor movement---------------------------------------------------------
//Measuring movement counts and ticks of m1 and m2
volatile int m1Ticks = 0, m2Ticks = 0;
volatile int m1MovementCount = 0, m2MovementCount = 0, avgCount = 0, m1 = 0, m2 = 0;

//PID Parameters
double curError = 0.0;
double prevError = 0.0;

double kP = -6.9;
double Adjust = 0;
boolean check=false;
unsigned long prev_ms = 0;
unsigned long interval = 0;
double m1Speed = 0, m2Speed = 0;
int repo;
int objPos[5]={'\0','\0','\0','\0','\0'};
String fastestpath;
//int align;

void setup() {
  Serial.begin(115200);
  PCintPort::attachInterrupt(3, &compute_m1_ticks, RISING); //Attached to Pin 3
  PCintPort::attachInterrupt(5, &compute_m2_ticks, RISING); //Attached to Pin 5
  md.init();
}


void loop(){
//objScan();
//    Serial.print("left");
//    Serial.println(frontLeftSensorAvg);
//    Serial.print("right");
//    Serial.println(frontRightSensorAvg);
  while (Serial.available() > 0){
    commands = (char)Serial.read(); 
    if(commands!='o'){ //if fastest path, send command 
      break;
    } 
    if(commands=='\n')
      break;

    fastestpath.concat(commands);
  }
  
  if(commands=='o'){
    for(int i=0;i<fastestpath.length();i++){
      commands=fastestpath[i];
      action();
    }
    for(int i=0;i<fastestpath.length();i++){
      fastestpath[i]='\0';
    }
  }
  else
    action();   
}


void action(){
  switch(commands){
  case 'm': 
    objScan();
    repo = realignRideSide();
  // Serial.println(repo);
    if(check==false){
      FindLeftRightSensorsAvg();
      double checkdistance=abs(rightSensorAvg-NewRightSensorAvg);
//   Serial.println(checkdistance);

      if( checkdistance>9.0 && checkdistance<=15 ||checkdistance<=8.7){
        if(repo==1){
          TurnAngle(-90);
          for (long startTime = millis(); (millis() - startTime) < 100;) {
            FindFrontSensorAvg();
            FindLeftRightSensorsAvg() ;
          }
            
          if(frontLeftSensorAvg<=13 &&frontRightSensorAvg<=13 && frontCentreSensorAvg<=21 ||frontLeftSensorAvg<=13&& frontLeftSensorAvg<=25&&frontRightSensorAvg<=13 &&frontRightSensorAvg<=25&& frontCentreSensorAvg>=21 &&frontCentreSensorAvg<=31){
            repositionRobotFront();
            realignRobotCentre() ;
            repositionRobotFront();
          }
        //if(frontLeftSensorAvg<=13 &&frontRightSensorAvg<=13||frontLeftSensorAvg<=13 && frontLeftSensorAvg<=25&&frontRightSensorAvg<=13 &&frontRightSensorAvg<=25)
          //  repositionRobotFront();
          TurnAngle(90);    
        
          check=true;
        }
      }
    }
    commands='z';
    break;

  case'e':
    for (long startTime = millis(); (millis() - startTime) < 100;) {
      FindFrontSensorAvg();
    }
  //FindFrontSensorAvg();
    if(frontLeftSensorAvg<=14 &&frontRightSensorAvg<=14 && frontCentreSensorAvg<=16 ||frontLeftSensorAvg>14&& frontLeftSensorAvg<=28&&frontRightSensorAvg>14 &&frontRightSensorAvg<=28&& frontCentreSensorAvg>16 &&frontCentreSensorAvg<=28){
      repositionRobotFront();
      realignRobotCentre() ;
      repositionRobotFront();
    }
      if(frontLeftSensorAvg<=14 &&frontRightSensorAvg<=14||frontLeftSensorAvg>14 && frontLeftSensorAvg<=32&&frontRightSensorAvg>14 &&frontRightSensorAvg<=30)
        repositionRobotFront();
      commands='z';
      check=true;  
      break;

  case 'f':
    moveOneGrid(1);
    commands='z';
    check=false;
    break;

  case 'l': 
    TurnAngle(88);
    commands='z';
    check=true;
    break;                  

  case 'r':
    TurnAngle(-90);
    commands='z';
    check=true;
    break;

  case 'd':
    TurnAngle(-90);
    repositionRobotFront() ;
    realignRobotCentre() ;
    TurnAngle(90);
    realignRobotCentre();
    repositionRobotFront() ;
    commands='z';
    check=true;
    break;

  default:
    if(commands>0 && commands<20)
    moveOneGrid(commands);
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

void Alignment() {
  Adjust = 0;
  curError = m2Ticks - m1Ticks;
  Adjust = kP * curError;

}

void moveForward(double m1Speed, double m2Speed) {
  unsigned long current_ms= millis() ;
 // Serial.println("FORWARD");

   if ((current_ms - prev_ms) > 5) {
    Alignment();
    m1Speed = m1Speed - Adjust;
    md.setM1Speed(m1Speed*left);
    md.setM2Speed(m2Speed*right);
    prev_ms = current_ms;
  }
}



void moveOneGrid(int grid) {
  left=1;
  right=1;
  int inc=0;
  m1MovementCount = 0;
  m2MovementCount = 0;

  MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  if(grid%5==0){
    inc=grid/5;
  }
  grid=grid*(245+inc);
    //Serial.print(MovementCountAvg);
  while (MovementCountAvg < grid) {
    moveForward(173,200);//175//220
    MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;
  }
    
  md.setBrakes(350, 350);
  delay(380);
}

void TurnAngle(int degree)
{

  int tick = 0;
  unsigned long current_ms = millis();
  if (degree > 0) {
    left = 1;
    right = -1;
    kd = 5.90;
  }
  else if (degree < 0) {
    left = -1;
    right = 1;
    kd = 5.55;
  }
  tick = kd * abs(degree);
  //Serial.println(tick);
  while(tick>0)
  {
    moveForward(80, 100); 
        delay(2);
        tick--;
  }
   
  left = 1;
  right = 1;
  md.setBrakes(350, 350);
  delay(380);
}

//Sensors Reading
void FindLeftRightSensorsAvg() {
  int sum = 0;
  rightSensorAvg = 0;
  leftSensorAvg = 0;

  for (sum = 0; sum < 25; sum++) {
    rightSensorValue = analogRead(RightSensorPin);
    NewRightSensorValue=analogRead(NewRightSensorPin);
    LeftSensorValue = analogRead(leftSensorPin);
    leftSensorAvg = leftSensorAvg + LeftSensorValue,
    rightSensorAvg = rightSensorValue + rightSensorAvg;
    NewRightSensorAvg=NewRightSensorValue+NewRightSensorAvg;
  }


//right sensor=centre
  leftSensorAvg = leftSensorAvg / 25;
  rightSensorAvg = rightSensorAvg / 25;
  NewRightSensorAvg=NewRightSensorAvg/25;
  leftSensorAvg = -1.2293*(pow(10,-6))*pow(leftSensorAvg,3) + 0.00157807*pow(leftSensorAvg,2) - 0.756313 *leftSensorAvg + 158.344;
  rightSensorAvg= -1.09725*pow(10,-6)*pow(rightSensorAvg,3)+0.0012996*pow(rightSensorAvg,2)-0.545108*rightSensorAvg+92.9372;
  NewRightSensorAvg=-5.84716*pow(10,-7)*pow(NewRightSensorAvg,3)+0.00088273*pow(NewRightSensorAvg,2)-0.458497*NewRightSensorAvg+91.5766;
  
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
  frontRightSensorAvg = -2.90778*pow(10,-7)*pow(frontRightSensorAvg,3)+0.000476141*pow(frontRightSensorAvg,2)-0.276684*frontRightSensorAvg+65.1692;
  frontLeftSensorAvg = -3.97168 * pow(10, -7) * pow(frontLeftSensorAvg, 3) + 0.000595119 * frontLeftSensorAvg * frontLeftSensorAvg - 0.314918 * frontLeftSensorAvg + 68.1434;
  frontCentreSensorAvg=-9.85343 * pow(10, -7) * pow(frontCentreSensorAvg, 3) + 0.00121121 * pow(frontCentreSensorAvg, 2) - 0.525592 * frontCentreSensorAvg + 92.371;
 
}


//havent calibrate to straight line
void repositionRobotFront() {
  int reposCount = 0;
  FindFrontSensorAvg();
  //Serial.println(abs(frontLeftSensorAvg - frontRightSensorAvg));

  md.setBrakes(400, 400);
  while ((abs(frontLeftSensorAvg - frontRightSensorAvg) > 0.9)) {

    if (frontLeftSensorAvg > frontRightSensorAvg) {
     //Serial.println("RIGHT");
      TurnAngle(-3);
    } else if (frontLeftSensorAvg < frontRightSensorAvg) {
     // Serial.println("LEFT");
      TurnAngle(3);
    }

    for (long startTime = millis(); (millis() - startTime) < 100;) {
      FindFrontSensorAvg();
    }
    reposCount++;
  }
  md.setBrakes(400, 400);
  delay(350);
}

int realignRideSide(){
  FindLeftRightSensorsAvg();
  //Serial.print("RIGHT");
  //Serial.println(rightSensorAvg);
  if(rightSensorAvg>=18.8 && rightSensorAvg<=25  ||rightSensorAvg<14.0 &&rightSensorAvg>=0)//&&rightSensorAvg<=24 ||rightSensorAvg<14  )
  {
    //Serial.println("REPO");
    return 1;
  }
  else return 0;
}

void realignRobotCentre() { 
  FindFrontSensorAvg();
  while ((frontCentreSensorAvg - calibratedFrontCentreDist) > 0.1) {
    moveForward(70, 60);
    for (long startTime = millis(); (millis() - startTime) < 50;) {
      FindFrontSensorAvg();
    }
  }

  md.setBrakes(350,350);
  delay(300);
  
  while ((frontCentreSensorAvg - calibratedFrontCentreDist) < 0) {
    moveForward(70, 60);
    left=-1;
    right=-1;
    for (long startTime = millis(); (millis() - startTime) < 100;) {
      FindFrontSensorAvg();
    }
  }
  left=1;
  right=1;
  md.setBrakes(350, 350);
  delay(300);
}

void objScan(){
 /* for (long startTime = millis(); (millis() - startTime) < 120;) 
  {
      FindFrontSensorAvg();
      FindLeftRightSensorsAvg();
  }*/
  for(long startTime=millis();(millis()-startTime)<50;)
  {
    computeMedian();
  }
  
  //---------------Scan Left----------------------------------------     
  if(leftSensorMedian<=18 && leftSensorMedian>0){
        objPos[0] = 1;
  }
     
     
  else if(leftSensorMedian<=28 && leftSensorMedian>18)
    objPos[0] = 2;
  
   /*else if(leftSensorAvg<=41 && leftSensorAvg>31)
     objPos[0] = 3;
  
    else if(leftSensorAvg<=51 && leftSensorAvg>41)
     objPos[0] = 4;*/
  else 
    objPos[0] = -2;
  
    //---------------Scan Front----------------------------------------    
    //Scan Front Left
    if(frontLeftSensorMedian<=18 && frontLeftSensorMedian>0)
      objPos[1] = 1;
    else if(frontLeftSensorMedian<=28 && frontLeftSensorMedian>18)
      objPos[1] = 2;
   
     else 
      objPos[1] = -2;
  //Serial.println(frontCentreSensorAvg);
    if(frontCentreSensorMedian<=19 && frontCentreSensorMedian>0)
      objPos[2] = 1;
    else if(frontCentreSensorMedian<=26 && frontCentreSensorMedian>19)
      objPos[2] = 2;
     
    else 
      objPos[2] = -2;
      
    //Scan Front Right
    if(frontRightSensorMedian<=13 && frontRightSensorMedian>0)
      objPos[3] = 1;
    else if(frontRightSensorMedian<=23 && frontRightSensorMedian>13)
      objPos[3] = 2;
    else
      objPos[3] = -2;
  
  
     if(rightSensorMedian<=19 && rightSensorMedian>0)
      objPos[4] = 1;
      else if(rightSensorMedian<=28 && rightSensorMedian>15)
      objPos[4] = 2;
    else
      objPos[4] = -2;
      if(NewRightSensorAvg<=14 &&NewRightSensorAvg>0)
            objPos[5] = 1;
            else if(NewRightSensorAvg>14 &&NewRightSensorAvg<23)
            objPos[5] = 2;
            else
            
                  objPos[5] = -2;


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
    objPos[0]='\0';
    objPos[1]='\0';
    objPos[2]='\0';
    objPos[3]='\0';
    objPos[4]='\0';
    objPos[5]='\0';
    
     
  }

  //-------------Sensors-------------------------------
double frontRightSensorReading(){
    double dist = analogRead(frontRightSensorPin);
  
  return -2.90778*pow(10,-7)*pow(dist,3)+0.000476141*pow(dist,2)-0.276684*dist+65.1692;
  //return -3.83732 * pow(10, -7) * pow(dist, 3) + 0.000610225 * pow(dist, 2) - 0.338653 * dist + 74.688;
}

double frontLeftSensorReading(){
  
  double dist = analogRead(frontLeftSensorPin);
  return -3.97168 * pow(10, -7) * pow(dist, 3) + 0.000595119 * dist * dist - 0.314918 * dist + 68.1434;  
}

double frontCentreSensorReading(){
  
  double dist = analogRead(frontCentreSensorPin);
  return -9.85343 * pow(10, -7) * pow(dist, 3) + 0.00121121 * pow(dist, 2) - 0.525592 * dist + 92.371;  
}

double rightSensorReading(){
  
  double dist = analogRead(RightSensorPin);
  return -1.09725*pow(10,-6)*pow(dist,3)+0.0012996*pow(dist,2)-0.545108*dist+92.9372;
}


double leftSensorReading(){
   double dist = analogRead(leftSensorPin);
  return -1.2293*(pow(10,-6))*pow(dist,3) + 0.00157807*pow(dist,2) - 0.756313 *dist + 158.344;
}

double backRightSensorReading(){
   double dist = analogRead(NewRightSensorPin);
  return -5.84716*pow(10,-7)*pow(dist,3)+0.00088273*pow(dist,2)-0.458497*dist+91.5766;
}

void computeMedian(){
  static int index=0;

  // get reading
  leftSensorArray[index] = leftSensorReading();
  rightSensorArray[index] = rightSensorReading();
  frontRightSensorArray[index] = frontRightSensorReading();
  frontLeftSensorArray[index] = frontLeftSensorReading();
  frontCentreSensorArray[index] = frontCentreSensorReading();
  NewRightSensorArray[index]=backRightSensorReading();
  // sort data     
  insertionSort();
  
  leftSensorMedian = leftSensorArray[arraySize/2];
  rightSensorMedian = rightSensorArray[arraySize/2];
  frontRightSensorMedian = frontRightSensorArray[arraySize/2];
  frontLeftSensorMedian = frontLeftSensorArray[arraySize/2];
  frontCentreSensorMedian = frontCentreSensorArray[arraySize/2];
  NewRightSensorMedian=NewRightSensorArray[arraySize/2];
  index = (index+1)%arraySize;
 }

void insertionSort(){
  for(int i=1; i<arraySize; i++){
    for(int j=i; j>0;j--){
      if(leftSensorArray[j]<leftSensorArray[j-1]){
        double temp = leftSensorArray[j];
        leftSensorArray[j] = leftSensorArray[j-1];
        leftSensorArray[j-1] = temp;
      }
      if(rightSensorArray[j]<rightSensorArray[j-1]){
        double temp = rightSensorArray[j];
        rightSensorArray[j] = rightSensorArray[j-1];
        rightSensorArray[j-1] = temp;
      }
    
      if(frontLeftSensorArray[j]<frontLeftSensorArray[j-1]){
        double temp = frontLeftSensorArray[j];
        frontLeftSensorArray[j] = frontLeftSensorArray[j-1];
        frontLeftSensorArray[j-1] = temp;
      }
      if(frontCentreSensorArray[j]<frontCentreSensorArray[j-1]){
        double temp = frontCentreSensorArray[j];
        frontCentreSensorArray[j] = frontCentreSensorArray[j-1];
        frontCentreSensorArray[j-1] = temp;
      }

        if(frontRightSensorArray[j]<frontRightSensorArray[j-1]){
        double temp = frontRightSensorArray[j];
        frontRightSensorArray[j] = frontRightSensorArray[j-1];
        frontRightSensorArray[j-1] = temp;
      }

       if(NewRightSensorArray[j]<NewRightSensorArray[j-1]){
        double temp = NewRightSensorArray[j];
        NewRightSensorArray[j] = NewRightSensorArray[j-1];
        NewRightSensorArray[j-1] = temp;
      }
    }
  } 
}



















