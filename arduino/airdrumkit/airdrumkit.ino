#include <SoftwareSerial.h>
int threshold=800,r[6],n[6];
int A[6] = {A0,A1,A2,A3,A4,A5};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i = 0; i < 6; i++)
  {
    r[i] = 0;
  }
  
  for(int j = 0; j < 6; j++)
  {
    n[j] = 0;
  }

}

void loop() {
  
  for(int i=0; i<6; i++){
    n[i]=analogRead(A[i]);
    if(n[i]>threshold && r[i]<threshold){
      char c = i + 48;
      Serial.write(c);
    }
    r[i]=n[i];
  }
  
}
