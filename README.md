# Smart Load Identification System

## Overview

The **Smart Load Identification System** is an electrical load monitoring and classification system that analyzes the electrical signatures of different loads and identifies the connected load based on their voltage and current characteristics.

The system uses an **ESP32** for real-time voltage and current acquisition, **Python** for signal processing and feature extraction, and a **Random Forest classifier** for load identification.

The system was tested on three load types: **Resistor, Motor, and Charger**, using real hardware measurements and simulation results.

---

## Technologies

- ESP32
- Arduino
- Python
- MATLAB
- Proteus
- Signal Processing
- Feature Extraction
- Random Forest
- IoT

---

## Project Structure

```text
Smart-Load-Identification/
│
├── Data/
│   ├── Loads_Dataset_Hardware.csv
│   └── Loads_Dataset_Software.csv
│
├── Sensor-Simulation/
│   ├── Proteus/
│   │   ├── Voltage_Sensor.pdsprj
│   │   └── Current_Sensor.pdsprj
│   │
│   └── src/
│       ├── Voltage_Sensor.ino
│       └── Current_Sensor.ino
│
├── ESP32-code/
│   └── smart-load-id.ino
│
├── Images/
│   ├── Matlab-Simulation/
│   ├── Hardware_setup/
│   ├── Real-Time-Results/
│   └── IoT/
│
├── python-code/
│   ├── smart_load_id.py
│   └── load_Classifier.pkl
│
└── README.md
```

---

## System Architecture

```text
Electrical Load
      ↓
Voltage & Current Sensors
      ↓
     ESP32
      ↓
    Python
      ↓
Signal Processing
      ↓
Feature Extraction
      ↓
Random Forest
      ↓
Load Classification
      ↓
 IoT Dashboard
```

The ESP32 acquires voltage and current samples at a predefined sampling rate. Python processes the acquired signals, extracts electrical features, visualizes the measurements, and classifies the connected load using the trained Random Forest model. The classification and monitoring results are then sent to the IoT dashboard.

---

## MATLAB Simulation

MATLAB was used to model and analyze the electrical behavior of the tested loads and study their electrical signatures.

Three load configurations were simulated:

- **Resistive Load:** Voltage and current are in phase, with a linear V-I relationship and a straight-line V-I trajectory.
- **Inductive Load:** Current lags voltage due to the inductance, producing an elliptical V-I trajectory.
- **Nonlinear Load:** A bridge rectifier and smoothing capacitor were used to represent a charger-type load. The resulting current contains sharp pulses and significant harmonic components.

The MATLAB simulation results were used to analyze and compare the electrical characteristics of the different load types.

---

## Sensor Circuit Simulation & Implementation

The voltage and current sensing circuits were designed and simulated using **Proteus** before being integrated into the complete system.

### Voltage Sensor

The voltage measurement circuit uses a **ZMPT101B** voltage sensor with signal isolation and voltage scaling.

The Arduino code acquires the analog signal, detects its peak values, calculates RMS voltage, applies calibration, and processes the measured signal.

### Current Sensor

The current measurement circuit uses an **ACS712 Hall-effect current sensor**.

The circuit provides isolation and a DC offset to shift the AC signal into the microcontroller's measurable range. The Arduino code removes the offset, detects the current peak, calculates RMS current, and applies calibration.

---

## Sensor Calibration

Sensor calibration was performed to compensate for practical hardware tolerances and signal-conditioning effects.

Multiple sensor readings were compared with a calibrated multimeter, and **linear regression** was used to derive a calibration equation. The resulting equation was integrated into the firmware to correct offset and scaling errors.

The voltage measurement error was reduced to **less than 2%** during validation.

---

## Hardware Components

- ESP32
- ZMPT101B AC Voltage Sensor
- ACS712 Current Sensor
- Thermal Resistors
- Transformer
- Inductor
- KBL606 Bridge Rectifier
- Capacitor

---

## Signal Processing & Feature Extraction

The acquired voltage and current signals are processed in Python using filtering, DC offset removal, smoothing, phase compensation, and calibration.

The extracted features are **RMS Voltage, RMS Current, Power Factor (PF), Total Harmonic Distortion (THD), and Crest Factor (CF)**.

---

## Frequency Domain Analysis

Frequency-domain analysis is used to study the harmonic content of the measured signals.

- **Resistive Load:** Dominant 50 Hz fundamental component with negligible harmonic distortion.
- **Inductive Load:** Mainly sinusoidal waveform with a phase shift between voltage and current.
- **Nonlinear Load:** Significant odd harmonics, including the 3rd, 5th, and 7th harmonics at 150 Hz, 250 Hz, and 350 Hz.

The harmonic content provides an additional electrical signature for distinguishing nonlinear loads from resistive and inductive loads.

---

## Load Classification

A **Random Forest classifier** was trained to identify the connected load based on the extracted electrical features.

The model was trained using data collected from the **real hardware measurements** and then used to classify the connected load.

The system classifies the load into three categories:

- **Resistor**
- **Motor**
- **Charger**

---

## Real-Time Signal Visualization & V-I Trajectory

The Python application provides real-time visualization of the voltage and current waveforms and their relationship.

The **V-I trajectory** provides a visual fingerprint for each load:

- **Resistive Load → Straight Line**
- **Inductive Load → Elliptical Shape**
- **Nonlinear Load → Asymmetric Loop**

These signatures provide an additional visual method for analyzing and verifying the electrical behavior of each load.

---

## IoT Integration

The system includes remote monitoring and notifications using **Blynk** and **Telegram Bot**.

The IoT interface provides access to selected electrical measurements, load classification, and power-quality information for remote monitoring.

---

## My Role

- Developed the ESP32 firmware for real-time voltage and current data acquisition.
- Developed Python scripts for signal processing, data visualization.
- Implemented electrical feature extraction, including RMS Voltage, RMS Current, Power Factor, THD, and Crest Factor.
- Trained the Random Forest classifier using hardware measurement data.

---

## Team & Contributors

This was a collaborative team project developed by a team of eight members:

- Fatma Nagah AbdelAzim
- Hoda Mahmoud Shalaby
- Fatma Emad El-Deba
- Nesreen Ashraf El-Emairy
- Aisha Belal Ibrahim
- Sama Mohamed Rashad
- Zamzam Ali Sarhan
- Fatma Mohsen El-Saber
