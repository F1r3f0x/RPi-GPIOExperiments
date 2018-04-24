import time
import wiringpi as wpi

CHANNEL = 0

# SPI Speed
MAX7219_HZ = 1000000

# MAX7219 Registers
MAX7219_REG_NOOP = 0x0
MAX7219_REG_DIGIT0 = 0x1
MAX7219_REG_DIGIT1 = 0x2
MAX7219_REG_DIGIT2 = 0x3
MAX7219_REG_DIGIT3 = 0x4
MAX7219_REG_DIGIT4 = 0x5
MAX7219_REG_DIGIT5 = 0x6
MAX7219_REG_DIGIT6 = 0x7
MAX7219_REG_DIGIT7 = 0x8
MAX7219_REG_DECODEMODE = 0x9
MAX7219_REG_INTENSITY = 0xA
MAX7219_REG_SCANLIMIT = 0xB
MAX7219_REG_SHUTDOWN = 0xC
MAX7219_REG_DISPLAYTEST = 0xF

# Setup SPI in channel 0
wpi.wiringPiSPISetup(CHANNEL, MAX7219_HZ)

push = wpi.wiringPiSPIDataRW

# # Test your display
# push(CHANNEL, bytes([MAX7219_REG_DISPLAYTEST, 0x1]))
# push(CHANNEL, bytes([MAX7219_REG_DISPLAYTEST, 0x0]))

# Setup
push(CHANNEL, bytes([MAX7219_REG_DECODEMODE, 0x0]))  # Don't decode the bytes in any digit
push(CHANNEL, bytes([MAX7219_REG_SCANLIMIT, 0x7]))  # Scan limit to all (8x8)
push(CHANNEL, bytes([MAX7219_REG_INTENSITY, 0x5]))  # Intensity to half
push(CHANNEL, bytes([MAX7219_REG_SHUTDOWN, 0x1]))  # Normal Operation

# Ways to push your byte
# push(CHANNEL, bytes([MAX7219_REG_DIGIT0, 0x0]))
# push(CHANNEL, bytes([MAX7219_REG_DIGIT0, int('10000001', 2)]))

dots = [
    int('10000000', 2),
    int('00100000', 2),
    int('00010000', 2),
    int('00001000', 2),
    int('00000100', 2),
    int('00000010', 2),
    int('00000001', 2)
]

while True:
    for d in dots:
        push(CHANNEL, bytes([MAX7219_REG_DIGIT0, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT1, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT2, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT3, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT4, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT5, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT6, d]))
        push(CHANNEL, bytes([MAX7219_REG_DIGIT7, d]))
        time.sleep(0.05)
