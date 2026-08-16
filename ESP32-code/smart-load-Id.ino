#include "BluetoothSerial.h"

BluetoothSerial SerialBT;

#define VOLT_PIN 34
#define CURR_PIN 35
#define SAMPLES 400

const float CALIBRATION_FACTOR = 1.0;
const float SCALE_FACTOR = 70;
const float OFFSET = 0.0;

int v_raw[SAMPLES];
int i_raw[SAMPLES];

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_LOAD");
}

double convertVoltage(int adc) {
  return (adc / 4095.0) * 3.3;
}

void loop() {

  // ================= Sampling =================
  for (int i = 0; i < SAMPLES; i++) {
    v_raw[i] = analogRead(VOLT_PIN);
    i_raw[i] = analogRead(CURR_PIN);
    delayMicroseconds(400);
  }

  // ================= Send calibrated data =================
 for (int i = 0; i < SAMPLES; i++) {

    
    double v_raw_volts = (v_raw[i] / 4095.0) * 3.3;
    double v_final = v_raw_volts * 70; 

    double i_raw_volts = (i_raw[i] / 4095.0) * 3.3;
    double i_final = i_raw_volts / 0.185; // 
    SerialBT.print(v_final, 4);
    SerialBT.print(",");
    SerialBT.println(i_final, 4);
  }

  SerialBT.println("END");

  delay(2000);
}