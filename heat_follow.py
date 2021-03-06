from Adafruit_AMG88xx import Adafruit_AMG88xx
from time import sleep

sensor = Adafruit_AMG88xx(busnum=1)


def get_pixels():
    raw_data = sensor.readPixels()
    data = []
    for i in range(8):
        data.append(raw_data[i*8:(i+1)*8])
    return data


from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
from adafruit_servokit import ServoKit

kit = MotorKit()
servokit = ServoKit(channels=16)

import atexit

@atexit.register
def goodbye():
    print("Exiting")
    kit.stepper1.release()
    kit.stepper2.release()
    servokit.continuous_servo[0].throttle = 0
    servokit.servo[0].angle = None

curangle = 45
angle_delta = 10
servokit.servo[0].angle = curangle 

temp =22
for t in range(100000):
    data=get_pixels()
    left = 0
    right = 0
    top = 0
    bottom = 0
    for i in range(8):
        if (data[0][i] > temp):
            left += 1
        if (data[1][i] > temp):
            left += 1
        if (data[2][i] > temp):
            left += 1
        if (data[5][i] > temp):
            right += 1
        if (data[6][i] > temp):
            right += 1
        if (data[7][i] > temp):
            right += 1

        if (data[i][5] > temp):
            top += 1
        if (data[i][6] > temp):
            top += 1
        if (data[i][7] > temp):
            top += 1
        if (data[i][0] > temp):
            bottom += 1
        if (data[i][1] > temp):
            bottom += 1
        if (data[i][2] > temp):
            bottom += 1
        
    print("L %i R %i" % (left, right))
    print("T %i B %i" % (top, bottom))
    
    if (left > 4 and right <= 2):
        dir = stepper.FORWARD
        #val = kit.stepper2.onestep(direction=dir, style=stepper.DOUBLE)
        curangle -= angle_delta
        servokit.servo[0].angle = curangle 
        print("L" + str(curangle))

    if (right > 4 and left <= 2):
        dir = stepper.BACKWARD
        curangle += angle_delta
        servokit.servo[0].angle = curangle 
        #val = kit.stepper2.onestep(direction=dir, style=stepper.DOUBLE)
        print("R" + str(curangle))

    if (top > 4 and bottom <= 2):
        dir = stepper.BACKWARD
        for z in range(50):
            val = kit.stepper1.onestep(direction=dir, style=stepper.DOUBLE)
        print("T" + str(val))

    if (bottom > 4 and top <= 2):
        dir = stepper.FORWARD
        for z in range(50):
            val = kit.stepper1.onestep(direction=dir, style=stepper.DOUBLE)
        print("B" + str(val))
        
    sleep(0.25)
    kit.stepper1.release()
    kit.stepper2.release()
