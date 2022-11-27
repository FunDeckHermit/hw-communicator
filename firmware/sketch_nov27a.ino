#include "RP2040_PWM.h"
#include "RPi_Pico_TimerInterrupt.h"

#define DEBOUNCETIME_MS 160
#define HOLDTIME_MS 1500
#define BLINKTIME_MS 142

#define big_button 26

#define led_status 1
#define led_wifi 12
#define led_lora 20
#define led1_heart 15
#define led2_ja 14
#define led3_nee 11
#define led4_kook 10
#define led5_later 9
#define led6_huis 8
#define led7_vergeten 7
#define led8_denk 3
#define led9_succes 2
#define NUM_OF_LEDS 9

uint led_array[] = {led1_heart, led2_ja, led3_nee, led4_kook, led5_later, led6_huis, led7_vergeten, led8_denk, led9_succes };

RP2040_PWM* PWM_Instance[NUM_OF_LEDS];
RPI_PICO_Timer ITimer0(0);
RPI_PICO_Timer ITimer1(1);

volatile int activeLED = -1;

bool Exclusive_On(int Index)
{
  for (uint i = 0; i < NUM_OF_LEDS; i++) {
    PWM_Instance[i]->setPWM(led_array[i], 20000, 0.5f);
  }
  if(Index < NUM_OF_LEDS && Index >= 0)
  {
    PWM_Instance[Index]->setPWM(led_array[Index], 20000, 10);
    return true;
  }
  return false;
}

void selectNextLed()
{
  activeLED = (activeLED + 1) % (NUM_OF_LEDS + 1);
  if(Exclusive_On(activeLED))
  {
    ITimer0.restartTimer();
  }
}

void onInterruptFalling() {
  static uint lasttime = 0;

  if ((millis() - lasttime) > DEBOUNCETIME_MS) {
    lasttime = millis();
    selectNextLed();
  }
}

bool TimerHandler0(struct repeating_timer *t)
{
  (void) t;
  ITimer0.stopTimer();
  Serial.println("Sending Signal to Wifi");
  ITimer1.restartTimer();
  return true;
}

bool TimerHandler1(struct repeating_timer *t)
{
  (void) t;
  volatile static uint timercount = 0;
  timercount++;

  if(timercount > 30)
  {
    ITimer1.stopTimer();
    timercount = 0;
    activeLED = -1;
    Exclusive_On(activeLED);
    Serial.println("Stop blinking!");
  }

  if(activeLED != 10 && activeLED != -1)
  {
    if(timercount % 2 == 1)
    {
      PWM_Instance[activeLED]->setPWM(led_array[activeLED], 20000, 0);
    }
    else
    {
      PWM_Instance[activeLED]->setPWM(led_array[activeLED], 20000, 10);
    }
  }
  return true;
}

void setup() {
  //Setup the pushbutton
  pinMode(big_button, INPUT_PULLUP);
  attachInterrupt(big_button, onInterruptFalling, FALLING);

  //Setup leds
  for (uint i = 0; i < NUM_OF_LEDS; i++) {
    PWM_Instance[i] = new RP2040_PWM(led_array[i], 20000, 0.5f);
    PWM_Instance[i]->setPWM();
  }

  //Setup timers
  ITimer0.attachInterruptInterval(HOLDTIME_MS * 1000, TimerHandler0);
  ITimer0.stopTimer();
  ITimer1.attachInterruptInterval(BLINKTIME_MS * 1000, TimerHandler1);
  ITimer1.stopTimer();  
}

void loop() {
  // put your main code here, to run repeatedly:
}
