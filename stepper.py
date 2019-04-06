
import sys
import time
import argparse
from adafruit_motorkit import MotorKit
kit = MotorKit()

parser = argparse.ArgumentParser(description='Test multiple stepper motors')
parser.add_argument('--motor', type=int, default=1,
                    help='Motor to turn')
parser.add_argument('--distance', type=int, default=10, 
                    help='Distance to turn')
parser.add_argument('--direction', default='forward', 
                    help='Direction to turn (forward or backward)')
args = parser.parse_args()
#kit.stepper2.onestep()

if (args.motor == 1):
    s = kit.stepper1
else:
    s = kit.stepper2


from adafruit_motor import stepper
if (args.direction == 'backward'):
    dir = stepper.BACKWARD
else:
    dir = stepper.FORWARD

for i in range(args.distance):
    val = s.onestep(direction=dir, style=stepper.INTERLEAVE)
    print(val)
    time.sleep(0.05)
    
s.release()
