from __future__ import division
from flask import Flask, request
import Adafruit_PCA9685
import time


DELAY = 0.2  # delay between steps of shrink(), stand()

SERVO_LEG_RO_MIN = 150
SERVO_LEG_RO_MAX = 450
SERVO_LEG_MAX  = 500  # shrink(lay down) limit
SERVO_LEG_MID  = 304
SERVO_LEG_MIN  = 148
SERVO_LEG_STEP = 80  # SERVO_LEG_MID +- SERVO_LEG_STEP
SERVO_FOOT_MAX = 473  # shrink(lay down) limmit
SERVO_FOOT_MID = 307  # stand still
SERVO_FOOT_MIN = 160  # limit of raising foot
SERVO_FOOT_LIFT= 230

# pulse values of moving forward and backward
SERVO_LEG_FWARD_PAIR1  = [SERVO_LEG_MID+SERVO_LEG_STEP, SERVO_LEG_MID+SERVO_LEG_STEP, SERVO_LEG_MID-SERVO_LEG_STEP]
SERVO_LEG_FWARD_PAIR2  = [SERVO_LEG_MID+SERVO_LEG_STEP, SERVO_LEG_MID-SERVO_LEG_STEP, SERVO_LEG_MID-SERVO_LEG_STEP]
SERVO_LEG_BACK_PAIR1  = [SERVO_LEG_MID-SERVO_LEG_STEP, SERVO_LEG_MID-SERVO_LEG_STEP, SERVO_LEG_MID+SERVO_LEG_STEP]
SERVO_LEG_BACK_PAIR2  = [SERVO_LEG_MID-SERVO_LEG_STEP, SERVO_LEG_MID+SERVO_LEG_STEP, SERVO_LEG_MID+SERVO_LEG_STEP]

SERVO_CHs_LEG  = [0, 1, 2, 3, 4,  5]
SERVO_CHs_FOOT = [6, 7, 8, 9, 10, 11]
SERVO_CHs_LEG_PAIR1  = [0, 2, 4]
SERVO_CHs_LEG_PAIR2  = [1, 3, 5]
SERVO_CHs_FOOT_PAIR1 = [6, 8, 10]
SERVO_CHs_FOOT_PAIR2 = [7, 9, 11]

# __name__: current module
app = Flask(__name__)


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

# dir: =1 for rotate clock-wise, =0 for rotate counter-clock-wise
def rotate(dir=True):
  # lift pair 1 foot, rotate pair 1 leg and drop pair 1 foot to middle
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)
  time.sleep(DELAY)
  for ch in SERVO_CHs_LEG_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_LEG_RO_MIN  if dir else SERVO_LEG_RO_MAX)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)
  
  # lift pair 2 foot and rotate pair 1 leg to middle
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR2:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)  
  time.sleep(DELAY)
  for ch in SERVO_CHs_LEG_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_LEG_MID)
  
  # rotate pair 2 leg and drop pair 2 foot to middle
  time.sleep(DELAY)
  for ch in SERVO_CHs_LEG_PAIR2:
    pwm.set_pwm(ch, 0, SERVO_LEG_RO_MIN  if dir else SERVO_LEG_RO_MAX)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR2:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)
  time.sleep(DELAY)
  
  # lift pair 1 foot so pair 2 leg can rotate to middle
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)
  time.sleep(DELAY)
  
  # put everything back to middle
  for ch in SERVO_CHs_LEG:
    pwm.set_pwm(ch, 0, SERVO_LEG_MID)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)

# dir: =1 for walk forward, =0 for walk backward
def walk(dir=True):
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)
    
  time.sleep(DELAY)
  for i in range(len(SERVO_CHs_LEG_PAIR1)):
    pwm.set_pwm(SERVO_CHs_LEG_PAIR1[i], 0, SERVO_LEG_FWARD_PAIR1[i] if dir else SERVO_LEG_BACK_PAIR1[i])
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)
  
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR2:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)
  time.sleep(DELAY)
  for i in range(len(SERVO_CHs_LEG_PAIR1)):
    pwm.set_pwm(SERVO_CHs_LEG_PAIR1[i], 0, SERVO_LEG_MID)
    pwm.set_pwm(SERVO_CHs_LEG_PAIR2[i], 0, SERVO_LEG_FWARD_PAIR2[i] if dir else SERVO_LEG_BACK_PAIR2[i])
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR2:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT_PAIR1:
    pwm.set_pwm(ch, 0, SERVO_FOOT_LIFT)
    
  # put everything back to middle
  time.sleep(DELAY)
  for ch in SERVO_CHs_LEG:
    pwm.set_pwm(ch, 0, SERVO_LEG_MID)
  time.sleep(DELAY)
  for ch in SERVO_CHs_FOOT:
    pwm.set_pwm(ch, 0, SERVO_FOOT_MID)

def test(chs, pulse):
  for ch in chs:
    pwm.set_pwm(ch, 0, pulse)


# @ : the decorator of the function
# when connect to the root of the server, run controller()
@app.route("/", methods=["POST"])
def controller():
    # get the payload sent from the post request
    json_dict = request.get_json(force=True)
    print(json_dict)  # for debugging
    act = json_dict['direction']
    if   act == 'up'      : walk(True)
    elif act == 'down'    : walk(False)
    elif act == 'left'    : rotate(True)
    elif act == 'right'   : rotate(False)
    elif act == 'stretch' : stand()
    elif act == 'shrink'  : shrink()
    else :                  rest()
    return "oh you posted something\n"  # for debugging
    
@app.route("/",methods=["GET"])
def test():
    return "Hello World\n"


# ============= main entry =============
pwm = Adafruit_PCA9685.PCA9685(address=0x40)  # I2C address for 
pwm.set_pwm_freq(50)  # set to 50 Hz
# pwm.set_pwm(ch, bus, pulse) # pulse=0~4095
app.run(host='0.0.0.0',port=5000)  # run the server


