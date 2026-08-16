\# Smart Load Identification System



\## Overview



The \*\*Smart Load Identification System\*\* is an electrical load monitoring and classification system designed to analyze the electrical signatures of different loads and classify the connected load based on its voltage and current characteristics.



The system acquires real-time voltage and current measurements using an \*\*ESP32\*\*, processes the acquired signals using \*\*Python\*\*, extracts electrical features, and applies a \*\*Random Forest classifier\*\* for load classification.



The system was tested on three different loads: \*\*Resistor, Motor, and Charger\*\*, using both real hardware measurements and MATLAB-based simulation results for analysis and comparison.



\---



\## Technologies



\- ESP32

\- Python

\- MATLAB

\- Signal Processing

\- Feature Extraction

\- Machine Learning

\- Bluetooth Communication

\- IoT



\---



\## System Architecture



\*\*Electrical Load → Voltage \& Current Sensors → ESP32 → Bluetooth → Python → Signal Processing → Feature Extraction → Random Forest → Load Classification\*\*



The ESP32 collects voltage and current samples at a predefined sampling rate and transmits the acquired data to Python via Bluetooth.



Python processes the incoming data, visualizes the electrical signals in real time, calculates the required electrical features, and applies the trained machine learning classifier to determine the connected load.



\---



\## MATLAB Simulation



MATLAB was used to model and analyze the electrical behavior of the different load configurations.



Three load circuits were simulated:



1\. \*\*Resistive Load\*\*

2\. \*\*Inductive Load\*\*

3\. \*\*Nonlinear Load\*\*



The nonlinear load was modeled using a \*\*KBL606 bridge rectifier and capacitor\*\* to represent a charger-type load.



MATLAB-generated data and results were used for comparison with measurements obtained from the real hardware implementation.



\---



\## Hardware Components



\- ESP32

\- AC Voltage Sensor

\- Current Sensor

\- Resistors

\- Thermal Resistors

\- Transformer

\- Inductor

\- KBL606 Bridge Rectifier

\- Capacitor



\### Tested Loads



| Load | Electrical Representation |

|---|---|

| Resistor | Resistive Load |

| Motor | Inductive Load |

| Charger | Nonlinear Load |



The resistive load can represent appliances such as a \*\*heater or lamp\*\*, while the inductive load represents a \*\*motor\*\*. The charger is represented using a \*\*bridge rectifier and capacitor\*\*.



\---



\## Signal Processing \& Feature Extraction



Python processes the acquired voltage and current signals and extracts electrical features used to characterize each load.



The extracted features include:



\- RMS Voltage

\- RMS Current

\- Power Factor

\- Total Harmonic Distortion (THD)

\- Crest Factor



The Python application also provides real-time visualization of the acquired signals, including \*\*voltage and current waveforms\*\* and \*\*V-I characteristics\*\*.



\---



\## Load Classification



A \*\*Random Forest classifier\*\* was used to classify the connected load based on the extracted electrical features.



The classifier was trained using real measurement data collected from the hardware system.



The system classifies the connected load into one of three categories:



\- \*\*Resistor\*\*

\- \*\*Motor\*\*

\- \*\*Charger\*\*



\---



\## IoT Integration



The system also includes an IoT component for remote monitoring and communication using:



\- \*\*Blynk\*\*

\- \*\*Telegram Bot\*\*



\---



\## Real-Time Operation



During operation, the desired load is connected to the system and the Python application is executed.



The system acquires and processes the electrical measurements, calculates the required features, visualizes the signals in real time, and classifies the connected load using the trained Random Forest classifier.



\---



\## My Role



As a \*\*Software Team Member\*\*, my responsibilities included:



\- Developed the \*\*ESP32 firmware\*\* for real-time voltage and current data acquisition at a predefined sampling rate.

\- Developed Python scripts for real-time data visualization and signal analysis.

\- Implemented electrical feature extraction from the acquired voltage and current signals.

\- Applied the trained \*\*Random Forest classifier\*\* to the extracted electrical features for load classification.



\---



\## Team



This was a \*\*team project\*\* developed collaboratively by a team of eight members.



\### Contributors



\- Fatma Nagah AbdelAzim

\- Hoda Mahmoud Shalaby

\- Fatma Emad El-Deba

\- Nesreen Ashraf El-Emairy

\- Aisha Belal Ibrahim

\- Sama Mohamed Rashad

\- Zamzam Ali Sarhan

\- Fatma Mohsen El-Saber

