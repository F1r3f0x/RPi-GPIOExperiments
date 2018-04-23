from time import sleep
import wiringpi

OUTPUT = wiringpi.OUTPUT
INPUT = wiringpi.INPUT
HIGH = wiringpi.HIGH
LOW = wiringpi.LOW

# Setup with BCM Pin Numbers
wiringpi.wiringPiSetupGpio()

led = int(input('led pin: '))
wiringpi.pinMode(led, OUTPUT)

print('blink!')
wiringpi.digitalWrite(led, HIGH)
sleep(4)
wiringpi.digitalWrite(led, LOW)
