# WARINING: Hardware GPIO needs sudo or you RPi WILL CRASH.
from time import sleep
import wiringpi as wpi

wpi.wiringPiSetupGpio()

pin_led = 18

print('hola')

wpi.pinMode(pin_led, wpi.PWM_OUTPUT)
while True:
    print('loop')
    wpi.pwmWrite(pin_led, 200)
    sleep(1)
    wpi.pwmWrite(pin_led, 500)
    sleep(1)
    wpi.pwmWrite(pin_led, 700)
    sleep(1)
    wpi.pwmWrite(pin_led, 1024)
    sleep(1)
    wpi.pwmWrite(pin_led, 0)
    sleep(1)
