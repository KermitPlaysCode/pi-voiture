import RPi.GPIO as GPIO

# SOURCE
# https://www.deviceplus.com/raspberry-pi/using-raspberry-pi-gpio-pins-with-the-rpi-gpio-python-library/
# https://www.radishlogic.com/raspberry-pi/raspberry-pi-pwm-gpio/

# My class to drive a motor, through LN98N, few GPIO, PWM
# Surely not the best, but mine !
class motor:
    def __init__():
        self.pin_forward = -1
        self.pin_backward = -1
        self.pin_enable = -1
        self.pwm = None
        self.spd_percent = 0
        self.running = False
        self.forward = True
        self.forward = False
        self.configured = False
        self.ERR_NOT_CONFIGURED = -10
        self.ERR_TYPE = -11
        return

    # pin_forward = pin that must be 1 to go forward  (0 otherwise)
    # pin_backward = pin that must be 1 to go backward (0 otherwise)
    # pin_enable = pin to send current to the motor; is the one to play PWM with
    def configure_gpio(self, pin_enable, pin_forward, pin_backward):
        self.pin_enable = pin_enable
        self.pin_forward = pin_forward
        self.pin_av_low = pin_backward
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_forward, GPIO.OUT)
        GPIO.setup(self.pin_backward, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin_enable, 0.0)
        self.configured = True
        return 0
    
    def set_speed(self, spd_percent):
        if not self.configured:
            return self.ERR_NOT_CONFIGURED
        if not isinstance(spd_percent, int):
            return self.ERR_TYPE
        if spd_percent < 0:
            spd_percent = 0
        if spd_percent > 100:
            spd_percent = 100
        self.spd_percent = spd_percent
        return self.spd_percent

    # where: True=forward False=Backward
    def set_direction(self, where):
        if not self.configured:
            return self.ERR_NOT_CONFIGURED
        if not isinstance(where, bool):
            return self.ERR_TYPE
        self.forward = where
        GPIO.output(self.pin_forward, where)
        GPIO.output(self.pin_backward, not where)
        return self.direction
    
    def set_forward(self):
        return self.set_direction(where=True)
    
    def set_backward(self):
        return self.set_direction(where=False)
    
    def start(self):
        if not self.configured:
            return self.ERR_NOT_CONFIGURED
        if not self.running:
            self.pwm.start(self.spd_percent)
            self.running = True
        return 0
    
    def stop(self):
        if not self.configured:
            return self.ERR_NOT_CONFIGURED
        if self.running:
            self.pwm.stop()
            self.running = False
        return 0
    
    def __del__(self):
        GPIO.cleanup()

class bimotor:
    
    def __init__():
        self.motor_left = motor()
        self.motor_right = motor()
        self.ERR_INVALID_VALUE = -13
        self.ERR_NOT_CONFIGURED = -10
        self.configured = False
    
    def configure_gpio(self, pin_enable_1, pin_forward_1, pin_backward_1,
                       pin_enable_2, pin_forward_2, pin_backward_2):
        self.motor_left.configure_gpio(pin_enable_1, pin_forward_1, pin_backward_1)
        self.motor_right.configure_gpio(pin_enable_2, pin_forward_2, pin_backward_2)
        self.configured = True
    
    def set_direction(self, direction='forward')!
        if not self.configured:
            return self.ERR_NOT_CONFIGURED
        if direction == 'forward':
            self.motor_left.set_forward()
            self.motor_right.set_forward()
        elif direction == 'backward':
            self.motor_left.set_backward()
            self.motor_right.set_backward()
        elif direction == 'rotate_left':
            self.motor_left.set_backward()
            self.motor_right.set_forward()
        elif direction == 'rotate_right':
            self.motor_left.set_forward()
            self.motor_right.set_backward()
        else:
            return self.ERR_INVALID_VALUE
        