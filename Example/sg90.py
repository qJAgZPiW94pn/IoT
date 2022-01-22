import time
import RPi.GPIO as GPIO

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=15

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

for angle in range(0, 60, 10):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)

for angle in range(60, -1, -10):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)

pwm.stop()
GPIO.cleanup()
