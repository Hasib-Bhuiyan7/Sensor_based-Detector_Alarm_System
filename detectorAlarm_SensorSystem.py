#This program replicates an intruder alarm/detector system
#Using the raspberry Pi Pico as the microcontroller implemented onto the breadboard to interface with the other electrical devices such as the PIR motion sensor which gives inputs which are read and processed, subsequently triggering the alarm system
#The alarm system consists of the three LEDs(Yellow, Blue, and Red) that light up in alternation dpeending on motion senser input and a piezzo buzzer produces a buzzing sound of certain frequency(500) when motion sensor is triggered 
#The electrical circuit system consists of different electrical components; 3 LEDs, 6 220ohms resistors, motion sensor(GND, VCC, Sensor Input/data Pin) and a piezzo buzzer(+ and - terminals)
#Slow alternating flashing indicates alarm is active but not triggered, otherwise quick alternating flashes between LEDs, buzzer sound initiated, and message output on the Shell indicates that alarm has been triggered by motion detected by the PIR sensor


import machine #Library for interfacing from the IDE to the raspberry pi pico
import utime 

pir_sensor = machine.Pin(28, machine.Pin.IN) #PIR Sensor Input
builtin_led = machine.Pin(25, machine.Pin.OUT) #internal chip LED output
red_led = machine.Pin(13, machine.Pin.OUT) #red LED output
yellow_led = machine.Pin(12, machine.Pin.OUT) #Yellow LED output
blue_led = machine.Pin(11, machine.Pin.OUT) #Blue LED output

buzzer = machine.PWM(machine.Pin(14)) #Buzzer pin configuration
buzzer.freq(500) #Buzzer Frequency

motion_already_detected = False; #If motion has already been detected, to prevent repitition of output

def light_configure(On_or_Off): #Algorithm for alternating Light configuration based on whether its turning on(1) or off(0)
    if (On_or_Off == 1):
        red_led.value(1)
        utime.sleep(0.1)
        blue_led.value(1)
        utime.sleep(0.1)
        yellow_led.value(1)
        utime.sleep(0.1)
    if (On_or_Off == 0):
        red_led.value(0)
        utime.sleep(0.1)
        blue_led.value(0)
        utime.sleep(0.1)
        yellow_led.value(0)
        utime.sleep(0.1)
        
#Main Loop
while True:
    if pir_sensor.value() and not motion_already_detected: #If sensor has been triggered and it has'nt been triggered previously(motion was just detected)
        print("ALARM TRIGGERED: Motion detected")
        builtin_led.value(1) #Internal LED shows up once, indicating motion has been detected
        utime.sleep(0.5)
        builtin_led.value(0) 
        motion_already_detected = True #Motion has already been detected
        
    if pir_sensor.value(): #If motion sensor has been triggered, alternate the lights and beep the buzzer in intervals of 0.1 seconds
        light_configure(1)
        buzzer.duty_u16(1000) #Configuring the buzzer volume for the buzz
        utime.sleep(0.1)
        light_configure(0)
        buzzer.duty_u16(0)
        utime.sleep(0.1)
        
    else: #if the motion sensor has not detected anything; normal LED alternation to indicate alarm is working 
        motion_already_detected = False #Motion has not been detected previosuly, reset variable for next detection
        light_configure(1)
        utime.sleep(1)
        light_configure(0)
        utime.sleep(3)
        
