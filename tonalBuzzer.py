from time import sleep
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

buzzerPin = 'GPIO13'

buzzer = TonalBuzzer(buzzerPin, octaves=3)

crappy_jingle = [Tone('C#6'), 'P', 'P', 'P', Tone('C#5'), Tone('F#5'), Tone('C#5'), Tone('G#5')]

for note in crappy_jingle:
    print(note)
    if note != 'P':
        buzzer.play(note)
    sleep(0.25)
