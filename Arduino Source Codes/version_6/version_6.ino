#include "PinChangeInt.h"
//#include "QuickStats.h"

#include "DualVNH5019MotorShield.h"
DualVNH5019MotorShield md;
#define arraySize 10

//----------------------Sensors------------------------------------------------------------
int  RightSensorPin= A3;
int frontCentreSensorPin = A0;//A5
int frontLeftSensorPin = A2; //A1
int leftSensorPin = A5;
int frontRightSensorPin = A4;

double kd = 0;
int count = 0, left = 1, right = 1;
int MovementCountAvg;
double totaltick = 0;
double calibratedFrontCentreDist = 10.5 ;//9.6

double LeftSensorValue = 0, rightSensorValue = 0, frontRightSensorValue = 0, frontLeftSensorValue = 0, frontCentreSensorValue = 0;
char commands='m';

double leftSensorAvg = 0.0, rightSensorAvg = 0.0,  frontRightSensorAvg = 0.0, frontLeftSensorAvg = 0.0, frontCentreSensorAvg = 0.0;

//----------------Motor movement---------------------------------------------------------
//Measuring movement counts and ticks of m1 and m2
volatile int m1Ticks = 0, m2Ticks = 0;
volatile int m1MovementCount = 0, m2MovementCount = 0, avgCount = 0, m1 = 0, m2 = 0;

//PID Parameters
double curError = 0.0;
double prevError = 0.0;


double kP = -6.3;//-3.8;
double Adjust = 0;

unsigned long prev_ms = 0;
unsigned long interval = 0;

double m1Speed = 0, m2Speed = 0;

int objPos[7];
boolean sendMapping=false, explorationMode=false, startFlag=false;

void setup() {
  Serial.begin(115200);
  // attach a PinChange Interrupt to our pin on the rising edge
  // (RISING, FALLING and CHANGE all work with this library)

  PCintPort::attachInterrupt(3, &compute_m1_ticks, RISING); //Attached to Pin 3
  PCintPort::attachInterrupt(5, &compute_m2_ticks, RISING); //Attached to Pin 5
  md.init();

}


void loop(){
 if (Serial.available() > 0){
    commands = (char)Serial.read(); 
    
  }
  switch(commands){
   case 'm': objScan();
   delay(350);
   break;
  
    case 'f':moveOneGrid(1);
    delay(100);
    commands='m';
    break;

    case 'l': TurnAngle(90);
    delay(300);
        commands='m';
    break;

    case 'r': TurnAngle(-90);
    delay(300);
      commands='m';
    break;

    case 'p':  repositionRobotFront();    
    commands='m';
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
  grid=grid*(280+inc);
    //Serial.print(MovementCountAvg);
  while (MovementCountAvg < grid) {
 
moveForward(170,160);//200//190

    MovementCountAvg = (m1MovementCount + m2MovementCount) / 2;

  }
    
  md.setBrakes(400, 400);
  //delay(100);

}

void TurnAngle(int degree)
{

  int tick = 0;
  unsigned long current_ms = millis();

  if (degree > 0) {
    left = 1;
    right = -1;
kd = 3.25;
  }
  else if (degree < 0) {
    left = -1;
    right = 1;
     kd = 3.21;
  }
  tick = kd * abs(degree);
  //Serial.println(tick);
  while(tick>0)
  {
    moveForward(180, 170); 
        delay(2);
        tick--;
      
  }
   
  left = 1;
  right = 1;
  md.setBrakes(400, 400);
delay(380);  
}




//Sensors Reading


void FindLeftRightSensorsAvg() {
  int sum = 0;
  rightSensorAvg = 0;
  leftSensorAvg = 0;


  for (sum = 0; sum < 20; sum++) {
    rightSensorValue = analogRead(RightSensorPin);


    LeftSensorValue = analogRead(leftSensorPin);

    leftSensorAvg = leftSensorAvg + LeftSensorValue,
    rightSensorAvg = rightSensorValue + rightSensorAvg;
   

  }


//right sensor=centre
  leftSensorAvg = leftSensorAvg / 20;

  rightSensorAvg = rightSensorAvg / 20;
 leftSensorAvg = -1.2293*(pow(10,-6))*pow(leftSensorAvg,3) + 0.00157807*pow(leftSensorAvg,2) - 0.756313 *leftSensorAvg + 158.344;
  rightSensorAvg= -4.06798*pow(10,-7)*pow(rightSensorAvg,3)+0.000634694*pow(rightSensorAvg,2)-0.349889*rightSensorAvg+76.0713; 
//rightSensorAvg=-3.73778 * pow(10, -7) * pow(leftSensorAvg, 3) + 0.000590571 * pow(leftSensorAvg, 2) - 0.327893 * leftSensorAvg + 72.1572;



}

void FindFrontSensorAvg() {
  int sum = 0;

  frontRightSensorAvg = 0;
  frontLeftSensorAvg = 0;
  frontCentreSensorAvg = 0;

  for (sum = 0; sum < 20; sum++) {
    frontRightSensorValue = analogRead(frontRightSensorPin);
    frontRightSensorAvg = frontRightSensorValue + frontRightSensorAvg;

    frontLeftSensorValue = analogRead(frontLeftSensorPin);
    frontLeftSensorAvg = frontLeftSensorValue + frontLeftSensorAvg;

    frontCentreSensorValue = analogRead(frontCentreSensorPin);
    frontCentreSensorAvg = frontCentreSensorAvg + frontCentreSensorValue;
  }
  frontRightSensorAvg = frontRightSensorAvg / 20;
  frontLeftSensorAvg = frontLeftSensorAvg / 20;
  frontCentreSensorAvg = frontCentreSensorAvg / 20;
  frontRightSensorAvg = -3.83732 * pow(10, -7) * pow(frontRightSensorAvg, 3) + 0.000610225 * pow(frontRightSensorAvg, 2) - 0.338653 * frontRightSensorAvg + 74.6882;
  frontLeftSensorAvg = -3.97168 * pow(10, -7) * pow(frontLeftSensorAvg, 3) + 0.000595119 * frontLeftSensorAvg * frontLeftSensorAvg - 0.314918 * frontLeftSensorAvg + 68.1434;
frontCentreSensorAvg=-3.73778 * pow(10, -7) * pow(frontCentreSensorAvg, 3) + 0.000590571 * pow(frontCentreSensorAvg, 2) - 0.327893 * frontCentreSensorAvg + 72.1572;

}


//havent calibrate to straight line
void repositionRobotFront() {
  int reposCount = 0;
  FindFrontSensorAvg();
  Serial.println(abs(frontLeftSensorAvg - frontRightSensorAvg));

  md.setBrakes(400, 400);
  while ((abs(frontLeftSensorAvg - frontRightSensorAvg) > 0.7)) {

    if (frontLeftSensorAvg > frontRightSensorAvg) {
      Serial.println("RIGHT");
      TurnAngle(-3);
      
      
    } else if (frontLeftSensorAvg < frontRightSensorAvg) {
      Serial.println("LEFT");
      TurnAngle(3);
      
    }

    for (long startTime = millis(); (millis() - startTime) < 50;) {

      FindFrontSensorAvg();

    }
    reposCount++;
  }

  md.setBrakes(400, 400);
delay(300);
//Serial.println(m1Speed);
//Serial.println(m2Speed);

}

void realignRobotCentre() { // might need to use IR instead of UR if too close to the wall unless we calibrate to never move more then 1 grid
  int reposCount = 0;
        FindFrontSensorAvg();
        Serial.print("frontCentreSensorAvg");
        Serial.println(frontCentreSensorAvg);
  while (abs(frontCentreSensorAvg - calibratedFrontCentreDist) > 0.7) {
    Serial.println(abs(frontCentreSensorAvg - calibratedFrontCentreDist));
    if (abs(frontCentreSensorAvg - calibratedFrontCentreDist) > 0.7 ) {
      if (abs(frontCentreSensorAvg - calibratedFrontCentreDist) > 0) {
        // Setting wheels to move robot forward
        moveForward(70, 60);

      }
     for (long startTime = millis(); (millis() - startTime) < 50;) {
      FindFrontSensorAvg();
       }
    }
  }
//  while ((frontCentreSensorMedian - calibratedFrontCentreDist) < 0) {
//
//    moveForward(-110, -100);
//  }
  md.setBrakes(400, 400);

}

void objScan(){
  for (long startTime = millis(); (millis() - startTime) < 50;) 
  {
      FindFrontSensorAvg();
    FindLeftRightSensorsAvg();
  }
  
  //---------------Scan Left----------------------------------------     
  //Scan Left
  if(leftSensorAvg<=14.5 && leftSensorAvg>0)
    objPos[0] = 1;
  else 
    objPos[0] = 0;

  //---------------Scan Front----------------------------------------    
  //Scan Front Left
  if(frontLeftSensorAvg<=13 && frontLeftSensorAvg>0)
    objPos[1] = 1;
  else 
    objPos[1] = 0;

  if(frontCentreSensorAvg<=15.5 && frontCentreSensorAvg>0)
    objPos[2] = 1;
  else 
    objPos[2] = 0;
    
  //Scan Front Right
  if(frontRightSensorAvg<=13 && frontRightSensorAvg>0)
    objPos[3] = 1;
  else
    objPos[3] = 0;


   if(rightSensorAvg<=11 && rightSensorAvg>0)
    objPos[4] = 1;
  else
    objPos[4] = 0;
  //if((sendMapping&&explorationMode)/*||(!explorationMode&&(commandBuffer.length()==0))*/){
    Serial.print('s');

    Serial.print(objPos[0]);
    Serial.print(objPos[1]);
    Serial.print(objPos[2]);
    Serial.print(objPos[3]);
    Serial.print(objPos[4]);
    Serial.print('e');
    Serial.print("\n");
        
   //}
}














