from time import sleep
from gpiozero import PWMLED

pwm_led = PWMLED('GPIO13')


# Blink the easy way
print('I\'m blinking!')
pwm_led.blink(0.5, 0.25, n=25, background=False)


# Change the brightnes with PWM
while True:
    print('I\'m glowing!')
    for v in range(0, 11):
        pwm_led.value = v/10
        sleep(0.25)
    for v in range(10, -1, -1):
        pwm_led.value = v/10
        sleep(0.25)
