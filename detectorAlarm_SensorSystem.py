#The alarm system consists of the three LEDs(Yellow, Blue, and Red) that light up in alternation dpeending on motion senser input and button element input and a piezzo buzzer produces a buzzing sound of certain frequency(500) when motion sensor is triggered 
#The electrical circuit system consists of different electrical components; 3 LEDs, 6 220ohms resistors, motion sensor(GND, VCC, Sensor Input/data Pin), button element(GND, PIN) and a piezzo buzzer(+ and - terminals)
#Slow alternating flashing indicates alarm is active but not triggered, steady flashing for continuous time indicates interference button pressed to halt alarm system function, otherwise quick alternating flashes between LEDs, buzzer sound initiated, and message output on the Shell indicates that alarm has been triggered by motion detected by the PIR sensor


import machine #Library for interfacing from the IDE to the raspberry pi pico
import utime 

pir_sensor = machine.Pin(28, machine.Pin.IN) #PIR Sensor Input
builtin_led = machine.Pin(25, machine.Pin.OUT) #internal chip LED output
red_led = machine.Pin(13, machine.Pin.OUT) #red LED output
yellow_led = machine.Pin(12, machine.Pin.OUT) #Yellow LED output
blue_led = machine.Pin(11, machine.Pin.OUT) #Blue LED output
button = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)#Control Button element configured as input and current regulated with internal pull-up resistors

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

pre_button_state = 1 #Setting previous state of button as a default 1

#Main Loop
while True:
    if pir_sensor.value() and not motion_already_detected and button.value()!=0: #If sensor has been triggered and it has'nt been triggered previously(motion was just detected), and button is not pressed
        print("ALARM TRIGGERED: Motion detected")
        builtin_led.value(1) #Internal LED shows up once, indicating motion has been detected
        utime.sleep(0.5)
        builtin_led.value(0) 
        motion_already_detected = True #Motion has already been detected
        
    if pir_sensor.value() and button.value()!=0: #If motion sensor has been triggered, without the interference of button, alternate the lights and beep the buzzer in intervals of 0.1 seconds
        light_configure(1)
        buzzer.duty_u16(200) #Configuring the buzzer volume for the buzz
        utime.sleep(0.1)
        light_configure(0)
        buzzer.duty_u16(0)
        utime.sleep(0.1)
        
    #If button changes state from 0 to 1(Button Released) -> Rising Edge     
    if pre_button_state == 0 and button.value() == 1:
        print("Button has been released - Alarm System Functional")
    
    #If button changes state from 1 to 0(Button Pressed) -> Falling Edge Triggered
    if pre_button_state == 1 and button.value() == 0:
        print("Button has been pressed - Alarm System disabled")
    
    #Reconfiguring the previous Button State
    pre_button_state = button.value()
        
    if not pir_sensor.value(): #if the motion sensor has not detected anything; normal LED alternation to indicate alarm is working 
        while button.value() == 0:#Special case where button is pressed and held onto; this initiates a different lighting sequence that continuously turns on all the LEDs
            light_configure(1)
            builtin_led.value(1)
        builtin_led.value(0)#Button released
        light_configure(0)
        motion_already_detected = False #Motion has not been detected previosuly, reset variable for next detection
        light_configure(1)
        utime.sleep(1)
        light_configure(0)
        utime.sleep(3)

