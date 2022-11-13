from machine import Pin

class Pins:
    def __init__(self):
        self.big_button = Pin(26, Pin.IN, Pin.PULL_UP)

        self.led0_inbuilt = Pin(25, Pin.OUT)
        self.led_status = Pin(1, Pin.OUT)
        self.led_wifi = Pin(12, Pin.OUT)
        self.led_lora = Pin(20, Pin.OUT)

        self.led1_heart = Pin(15, Pin.OUT)
        self.led2_ja = Pin(14, Pin.OUT)
        self.led3_nee = Pin(11, Pin.OUT)
        self.led4_kook = Pin(10, Pin.OUT)
        self.led5_later = Pin(9, Pin.OUT)
        self.led6_huis = Pin(8, Pin.OUT)
        self.led7_vergeten = Pin(7, Pin.OUT)
        self.led8_denk = Pin(3, Pin.OUT)
        self.led9_succes = Pin(2, Pin.OUT)
        
        self.selectable_leds = [self.led0_inbuilt, self.led1_heart, self.led2_ja, self.led3_nee, self.led4_kook, self.led5_later, self.led6_huis, self.led7_vergeten, self.led8_denk, self.led9_succes]

    def get_output_led_list(self):
        return self.selectable_leds
    
    def all_leds_off(self):
        for led in self.selectable_leds:
            led.value(0)
            
    def exclusive_on(self, onled_index):
        self.all_leds_off()
        self.selectable_leds[onled_index].value(1)

