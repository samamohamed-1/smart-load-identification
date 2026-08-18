#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int currentPin = A1;
const float sensitivity = 0.185; 

void setup() {
  lcd.begin(16, 2);
  lcd.print("RMS Current Mode");
  delay(1000);
  lcd.clear();
}

void loop() {
  float vMax = 0;
  uint32_t startTime = millis();


  while((millis() - startTime) < 20) {
    int rawValue = analogRead(currentPin);
    float voltage = rawValue * (5.0 / 1023.0);
    float vFromCenter = abs(voltage - 2.5); 
    if (vFromCenter > vMax) {
      vMax = vFromCenter; 
    }
  }


  float peakCurrent = vMax / sensitivity;

  float rmsCurrent = (vMax / 0.185) * 0.707;
  


  rmsCurrent = rmsCurrent * 0.88; 

  if (rmsCurrent < 0.05) rmsCurrent = 0;


  lcd.setCursor(0, 0);
  lcd.print("I (RMS):");
  lcd.setCursor(0, 1);
  lcd.print(rmsCurrent, 3); 
  lcd.print(" A   ");

  delay(200);
}