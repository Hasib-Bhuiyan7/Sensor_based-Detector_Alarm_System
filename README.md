# Sensor_based-Detector_Alarm_System
#This program replicates an intruder alarm/detector system
#Using the raspberry Pi Pico as the microcontroller implemented onto the breadboard to interface with the other electrical devices such as the PIR motion sensor which gives inputs which are read and processed, subsequently triggering the alarm system
#The alarm system consists of the three LEDs(Yellow, Blue, and Red) that light up in alternation dpeending on motion senser input and a piezzo buzzer produces a buzzing sound of certain frequency(500) when motion sensor is triggered 
#The electrical circuit system consists of different electrical components; 3 LEDs, 6 220ohms resistors, motion sensor(GND, VCC, Sensor Input/data Pin) and a piezzo buzzer(+ and - terminals)
#Slow alternating flashing indicates alarm is active but not triggered, otherwise quick alternating flashes between LEDs, buzzer sound initiated, and message output on the Shell indicates that alarm has been triggered by motion detected by the PIR sensor
