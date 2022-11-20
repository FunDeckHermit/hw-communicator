from machine import Pin, PWM


class Pins:
    def __init__(self):
        self.maxpwm = 2**16
        
        self.big_button = Pin(26, Pin.IN, Pin.PULL_UP)

        self.led0_inbuilt = Pin('LED', Pin.OUT)
        self.led_status = Pin(1, Pin.OUT)
        self.led_wifi = Pin(12, Pin.OUT)
        self.led_lora = Pin(20, Pin.OUT)

        self.led1_heart = PWM(Pin(15, Pin.OUT))
        self.led2_ja = PWM(Pin(14, Pin.OUT))
        self.led3_nee = PWM(Pin(11, Pin.OUT))
        self.led4_kook = PWM(Pin(10, Pin.OUT))
        self.led5_later = PWM(Pin(9, Pin.OUT))
        self.led6_huis = PWM(Pin(8, Pin.OUT))
        self.led7_vergeten = PWM(Pin(7, Pin.OUT))
        self.led8_denk = PWM(Pin(3, Pin.OUT))
        self.led9_succes = PWM(Pin(2, Pin.OUT))
            
        self.selectable_leds = [self.led0_inbuilt, self.led1_heart, self.led2_ja, self.led3_nee, self.led4_kook, self.led5_later, self.led6_huis, self.led7_vergeten, self.led8_denk, self.led9_succes]

    def set_max_pwm_u16(self, maxvalue):
        self.maxpwm = maxvalue
    
    def get_output_led_list(self):
        return self.selectable_leds
    
    def all_leds_off(self):
        for led in self.selectable_leds:
            self.led_off(led)
            
    def exclusive_on(self, onled_index):
        self.all_leds_off()
        self.led_on(self.selectable_leds[onled_index])
        
    def led_off(self, led):
        if type(led).__name__ is 'PWM':
            led.duty_u16(0)
        else:
            led.value(0)
    
    def led_on(self, led):
        if type(led).__name__  is 'PWM':
            led.duty_u16(self.maxpwm)
        else:
            led.value(0)

