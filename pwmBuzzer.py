from time import sleep
import wiringpi as wpi

wpi.wiringPiSetupGpio()

buzzer = 18

wpi.softToneCreate(buzzer)

while True:
    wpi.softToneWrite(buzzer, 10)
    sleep(1)
    wpi.softToneWrite(buzzer, 20)
    sleep(1)
    wpi.softToneWrite(buzzer, 30)
    sleep(1)
    wpi.softToneWrite(buzzer, 50)
    sleep(1)
    wpi.softToneWrite(buzzer, 100)
    sleep(1)
    wpi.softToneWrite(buzzer, 120)
    sleep(1)
    wpi.softToneWrite(buzzer, 3000)
    sleep(1)
    wpi.softToneWrite(buzzer, 4000)
    sleep(1)
    wpi.softToneWrite(buzzer, 5000)
    sleep(1)
    wpi.softToneWrite(buzzer, 0)
    sleep(1)
