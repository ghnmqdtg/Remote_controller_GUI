from __future__ import division
import Adafruit_PCA9685
import time

DELAY = 0.5  # delay between steps of shrink(), stand()

SERVO_LEG_MAX  = 500
SERVO_LEG_MID  = 304
SERVO_LEG_MIN  = 148
SERVO_FOOT_MAX = 473  # shrink(lay down) limmit
SERVO_FOOT_MID = 307  # stand still
SERVO_FOOT_MIN = 160  # limit of raising foot

SERVO_CHs_TEST = [7,9,11]
SERVO_CHs_LEG  = [0, 1, 2, 3, 4,  5]
SERVO_CHs_FOOT = [6, 7, 8, 9, 10, 11]
SERVO_CHs_LEG_PAIR1  = [0, 2, 4]
SERVO_CHs_LEG_PAIR2  = [1, 3, 5]
SERVO_CHs_FOOT_PAIR1 = [6, 8, 10]
SERVO_CHs_FOOT_PAIR2 = [7, 9, 11]


pwm = Adafruit_PCA9685.PCA9685(address=0x40)  # I2C address for 
pwm.set_pwm_freq(50)  # set to 50 Hz

# turn off dead-lock of servos
def rest():
  for ch in SERVO_CHs_LEG:
    pwm.set_pwm(ch, 0, 0)
  
  for ch in SERVO_CHs_FOOT:
    pwm.set_pwm(ch, 0, 0)


def shrink():
  for ch in SERVO_CHs_FOOT:  # lay down
    pwm.set_pwm(ch, 0, SERVO_FOOT_MAX)
  time.sleep(DELAY)
  for ch in SERVO_CHs_LEG:
    pwm.set_pwm(ch, 0, SERVO_LEG_MAX)  # shrink
  time.sleep(DELAY)

def stand():
  for ch in SERVO_CHs_LEG:  # set leg to middle
    pwm.set_pwm(ch, 0, SERVO_LEG_MID)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT:  # stand up
    pwm.set_pwm(ch, 0, SERVO_LEG_MID)

def test(chs, pulse):
  for ch in chs:
    pwm.set_pwm(ch, 0, pulse)

rest()
time.sleep(DELAY)
print("Hit ctrl+c to exit.")
test(SERVO_CHs_FOOT_PAIR1, SERVO_FOOT_MID)
try:
  while True:
    str = input('enter pulse(0~4095):')
    s = int(str)
    test(SERVO_CHs_TEST, s)

except KeyboardInterrupt:
  rest()
  print("Exiting.")
