from time import sleep
from gpiozero import LED

selected_pin = input('led pin: ')  # See: https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering

led = LED(selected_pin)

print('blink!')
led.on()
sleep(4)
led.off()