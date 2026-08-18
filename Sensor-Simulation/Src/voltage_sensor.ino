#include <LiquidCrystal.h>

// --- إعدادات الشاشة العادية (RS, En, D4, D5, D6, D7) ---
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// --- إعدادات الحساس ---
const int sensorPin = A0;             
const float CALIBRATION_FACTOR = 3.98; 
const float VOLTAGE_REF = 5.0;   

void setup() {

  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("AC Voltmeter");
  lcd.setCursor(0, 1);
  lcd.print("Loading...");
  delay(1500);
  lcd.clear();
}

void loop() {
  unsigned long startTime = millis();
  int maxValue = 0;
  int minValue = 1024;


  while (millis() - startTime < 100) {
    int sensorValue = analogRead(sensorPin);
    
    if (sensorValue > maxValue) maxValue = sensorValue;
    if (sensorValue < minValue) minValue = sensorValue;
  }

  // --- مرحلة الحسابات (Calculations) ---
  

  int peakToPeak = maxValue - minValue;


  double voltageRMS = ((peakToPeak * VOLTAGE_REF) / 1024.0) * 0.707;


  double finalVoltage = voltageRMS * CALIBRATION_FACTOR;
  double finaltest = (27.8 *finalVoltage ) + 0.3;

  // --- عرض النتائج على الشاشة ---
  lcd.setCursor(0, 0);
  lcd.print("Voltage Reading");
  
  lcd.setCursor(0, 1);
  if (peakToPeak > 10) { 
    lcd.print("V: ");
    lcd.print(finaltest, 1);
    lcd.print(" VAC      ");   
  } else {
    lcd.print("V: 0.0 VAC     ");
  }

  delay(300); 
}