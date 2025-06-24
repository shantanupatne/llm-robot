import RPi.GPIO as GPIO
import time

# Pin Definitions
# Right Front Motor
MF_PWMA = 13
MF_AI1 = 6
MF_AI2 = 5

# Left Front Motor
MF_PWMB = 26
MF_BI1 = 33
MF_BI2 = 25

# Right Rear Motor
MR_PWMA = 12
MR_AI1 = 1
MR_AI2 = 8

# Left Rear Motor
MR_PWMB = 18
MR_BI1 = 24
MR_BI2 = 23

# PWM Setup
PWM_FREQ = 1000  # Frequency in Hz

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Setup pins as output
motor_pins = [MF_PWMA, MF_AI1, MF_AI2, MF_PWMB, MF_BI1, MF_BI2, MR_PWMA, MR_AI1, MR_AI2, MR_PWMB, MR_BI1, MR_BI2]
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

# Initialize PWM
pwm_channels = {
    "RF": GPIO.PWM(MF_PWMA, PWM_FREQ),
    "LF": GPIO.PWM(MF_PWMB, PWM_FREQ),
    "RR": GPIO.PWM(MR_PWMA, PWM_FREQ),
    "LR": GPIO.PWM(MR_PWMB, PWM_FREQ),
}

# Start PWM with 0 duty cycle
for pwm in pwm_channels.values():
    pwm.start(0)  # Start PWM with 0 duty cycle

# Motor Control functions
def move_motors(speedRF, speedLF, speedRR, speedLR, dircontrol):
    # Right Front Motor
    GPIO.output(MF_AI1, (dircontrol & 0b10000000) > 0)
    GPIO.output(MF_AI2, (dircontrol & 0b01000000) > 0)
    pwm_channels["RF"].ChangeDutyCycle(abs(speedRF))

    # Left Front Motor
    GPIO.output(MF_BI1, (dircontrol & 0b00100000) > 0)
    GPIO.output(MF_BI2, (dircontrol & 0b00010000) > 0)
    pwm_channels["LF"].ChangeDutyCycle(abs(speedLF))

    # Right Rear Motor
    GPIO.output(MR_AI1, (dircontrol & 0b00001000) > 0)
    GPIO.output(MR_AI2, (dircontrol & 0b00000100) > 0)
    pwm_channels["RR"].ChangeDutyCycle(abs(speedRR))

    # Left Rear Motor
    GPIO.output(MR_BI1, (dircontrol & 0b00000010) > 0)
    GPIO.output(MR_BI2, (dircontrol & 0b00000001) > 0)
    pwm_channels["LR"].ChangeDutyCycle(abs(speedLR))

def stop_motors():
    for pwm in pwm_channels.values():
        pwm.ChangeDutyCycle(0)
    for pin in motor_pins:
        GPIO.output(pin, 0)

# Define movement directions in binary
MEC_STRAIGHT_FORWARD = 0b10101010
MEC_STRAIGHT_BACKWARD = 0b01010101
MEC_SIDEWAYS_RIGHT = 0b01101001
MEC_SIDEWAYS_LEFT = 0b10010110

# Code to test Movement
try:
    while True:
        print("Straight Forward")
        move_motors(50, 50, 50, 50, MEC_STRAIGHT_FORWARD)
        time.sleep(1)
        stop_motors()
        time.sleep(5)

        # print("Straight Backward")
        # move_motors(50, 50, 50, 50, MEC_STRAIGHT_BACKWARD)
        # time.sleep(1)
        # stop_motors()
        # time.sleep(0.5)

        # print("Sideways Right")
        # move_motors(50, 50, 50, 50, MEC_SIDEWAYS_RIGHT)
        # time.sleep(1)
        # stop_motors()
        # time.sleep(0.5)

        # print("Sideways Left")
        # move_motors(50, 50, 50, 50, MEC_SIDEWAYS_LEFT)
        # time.sleep(1)
        # stop_motors()
        # time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    stop_motors()
    GPIO.cleanup()
