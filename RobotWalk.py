import RPi.GPIO as GPIO
import time
import random

cnt = 0
timer = 0

# Distance Calculator
# Output Unit is mm
def Distance(Trigger, Echo):
    global cnt
    global tic

    #Send Trigger Pulse
    GPIO.output(Trigger, 1)     
    time.sleep(0.00001)
    GPIO.output(Trigger, 0)
    
    while True:

        #Monitor Ultrasonic Echo
        if (GPIO.input(Echo) == 1):
            if (cnt == 0):
                tic = time.time()       #Log initial Echo
                cnt += 1
        else:
            if (cnt != 0):
                dist = (time.time() - tic) * 171500;    #Log final Echo and Calculate Distance
                
                cnt = 0
                break
            
    return dist

def Walk():

    #setup GPIO using Board numbering
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #Optical Encoder on Drive Wheel
    Opt_enc = 6
    GPIO.setup(Opt_enc,GPIO.IN)

    #Ultrasonic Front
    Echo_F = 22
    Trigger_F = 17
    GPIO.setup(Echo_F, GPIO.IN)
    GPIO.setup(Trigger_F, GPIO.OUT)

    #Ultrasonic Left Front
    Echo_LF = 21
    Trigger_LF = 25
    GPIO.setup(Echo_LF, GPIO.IN)
    GPIO.setup(Trigger_LF, GPIO.OUT)

    #Ultrasonic Right Front
    Echo_RF = 27
    Trigger_RF = 24
    GPIO.setup(Echo_RF, GPIO.IN)
    GPIO.setup(Trigger_RF, GPIO.OUT)

    #Ultrasonic Rear
    Echo_R = 23
    Trigger_R = 26
    GPIO.setup(Echo_R, GPIO.IN)
    GPIO.setup(Trigger_R, GPIO.OUT)

    #Motor Pins
    Motor_Bwd = 20
    Motor_Fwd = 19
    Steer = 16
    GPIO.setup(Motor_Fwd, GPIO.OUT)
    GPIO.setup(Motor_Bwd, GPIO.OUT)
    GPIO.setup(Steer, GPIO.OUT)

    #Motor Control Parameters
    motor_fwd = GPIO.PWM(Motor_Fwd, 500)
    motor_bwd = GPIO.PWM(Motor_Bwd, 500)
    Fast = 100
    Casual = 75
    Slow = 50
    Stop = 0
    motor_fwd.start(Stop)
    motor_bwd.start(Stop)

    #4 is full right
    #14 is full left
    #7.5 is straight
    steer = GPIO.PWM(Steer, 50)
    right = 4
    left = 14
    straight = 7.5
    steer.start(straight)

    #E Stop Button
    E_stop = 13
    GPIO.setup(E_stop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    #Extra Parameters
    global cnt
    global tic
    decision_cnt_F = 0
    decision_cnt_B = 0

    while not GPIO.input(E_stop):

        #Forwards
        #Measure Front Distance
        distance_F = Distance(Trigger_F,Echo_F)
        distance_LF = Distance(Trigger_LF,Echo_LF)
        distance_RF = Distance(Trigger_RF,Echo_RF)
        
        while distance_F >= 300 and distance_LF >= 250 and distance_RF >= 250 and not GPIO.input(E_stop):
            while distance_F >= 800 and distance_LF >= 600 and distance_RF >= 600 and not GPIO.input(E_stop):

                steer.ChangeDutyCycle(straight)

                #Move Forward
                motor_fwd.ChangeDutyCycle(Casual)
                motor_bwd.ChangeDutyCycle(Stop)
                time.sleep(0.025)

                distance_F = Distance(Trigger_F,Echo_F)
                distance_LF = Distance(Trigger_LF,Echo_LF)
                distance_RF = Distance(Trigger_RF,Echo_RF)

                decision_cnt_F = 0;


            #Getting closer to something
            motor_fwd.ChangeDutyCycle(Casual)
            motor_bwd.ChangeDutyCycle(Stop)
            
            #Decide on Steering
            if (decision_cnt_F == 0):
                if (abs(distance_LF - distance_RF) <= 20):
                    motor_fwd.ChangeDutyCycle(Slow)
                    motor_bwd.ChangeDutyCycle(Stop)
                else:
                    if (distance_LF < distance_RF):
                        steer.ChangeDutyCycle(right)
                    else:
                        steer.ChangeDutyCycle(left)
            

            distance_F = Distance(Trigger_F,Echo_F)
            distance_LF = Distance(Trigger_LF,Echo_LF)
            distance_RF = Distance(Trigger_RF,Echo_RF)

            decision_cnt_F = 1 


        #Backwards

        decision_cnt_B = 0
        
        distance_R = Distance(Trigger_R,Echo_R)

        while distance_R >= 300 and not GPIO.input(E_stop):

            #Decide on Steering
            if (decision_cnt_B == 0):
                if (abs(distance_LF - distance_RF) <= 20):
                    motor_fwd.ChangeDutyCycle(Stop)
                    motor_bwd.ChangeDutyCycle(Slow)
                else:
                    if (distance_LF < distance_RF):
                        steer.ChangeDutyCycle(left)
                    else:
                        steer.ChangeDutyCycle(right)
            
            #Move Backward
            motor_fwd.ChangeDutyCycle(Stop)
            motor_bwd.ChangeDutyCycle(Casual)

            distance_R = Distance(Trigger_R,Echo_R)

            decision_cnt_B = 1    


    GPIO.cleanup()
    exit()

try:
    Walk()

except:
    GPIO.cleanup()
