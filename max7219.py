from wiringpi import wiringPiSPISetup as spiSetup
from wiringpi import wiringPiSPIDataRW as spiRW

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

class Matrix8X8:
    """
    Matrix(s) of 8x8 LEDs controlled by a MAX7219

    Attributes:
        display_registers (list): List of the registers for the MAX7219 (CLASS)
        frame: Frame to draw to the "screen" (matrix)
    """
    display_registers = [
        MAX7219_REG_DIGIT0,
        MAX7219_REG_DIGIT1,
        MAX7219_REG_DIGIT2,
        MAX7219_REG_DIGIT3,
        MAX7219_REG_DIGIT4,
        MAX7219_REG_DIGIT5,
        MAX7219_REG_DIGIT6,
        MAX7219_REG_DIGIT7
    ]

    def __init__(self, channel=0, auto_update=True, number_screens=1, **kwargs):
        """
        Args:
            channel (int): Channel for SPI communication
            auto_update (bool): Update screen on functions that change the frame
            number_screens (int): Number of screens being controlled by MAX7219 (TODO)

        Keyword Args:
            flip_x (bool): Flip X of the frame when drawing it to the screen.
            flip_y (bool): Flip Y of the frame when drawing it to the screen.

        """
        self.channel = channel
        self.auto_update = True
        self.number_screens = number_screens
        self.frame = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]

        # Keyword Args
        self.flip_x = kwargs.get('flip_x')
        self.flip_y = kwargs.get('flip_y')

    def __setup_screen(self, screen=0):
        spiRW(self.channel, bytes([MAX7219_REG_DECODEMODE, 0x0]))  # Don't decode the bytes in any digit
        spiRW(self.channel, bytes([MAX7219_REG_SCANLIMIT, 0x7]))  # Scan limit to all (8x8)
        spiRW(self.channel, bytes([MAX7219_REG_INTENSITY, 0x5]))  # Intensity to half
        spiRW(self.channel, bytes([MAX7219_REG_SHUTDOWN, 0x1]))  # Normal Operation

    def clear_screen(self, screen=0):
        self.frame = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.update_screen()

    def fill_screen(self, screen=0):
        self.frame = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ]
        self.update_screen()

    def set_point(self, x, y, value=True, screen=0):
        value = int(bool(value))
        self.frame[y][x] = value
        if self.auto_update:
            self.update_screen()

    def update_screen(self, screen=0):
        # Create bytes
        screen_bytes = []
        for f in self.frame:
            # Convert to byte and append
            if self.flip_y:
                f_str = [str(x) for x in f[::-1]]
            else:
                f_str = [str(x) for x in f]
            f_bytes = int(''.join(f_str), 2)
            screen_bytes.append(f_bytes)

        # Write to registers
        if self.flip_x:
            for i, reg in enumerate(Matrix8X8.display_registers[::-1]):
                spiRW(self.channel, bytes([reg, screen_bytes[i]]))
        else:
            for i, reg in enumerate(Matrix8X8.display_registers):
                spiRW(self.channel, bytes([reg, screen_bytes[i]]))

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
        spiSetup(self.channel, MAX7219_HZ)
        self.__setup_screen()


if __name__ == '__main__':
    from time import sleep

    matrix = Matrix8X8(flip_y=True)

    print('running')
    matrix.set_point(0, 0)
    matrix.set_point(0, 1)
    matrix.set_point(0, 2)
    matrix.set_point(0, 3)
    matrix.set_point(0, 4)

    matrix.set_point(7, 3)
    matrix.set_point(7, 7)

    sleep(3)

    matrix.clear_screen()

# CHANNEL = 0
#
# # SPI Speed
# MAX7219_HZ = 1000000
#
# # MAX7219 Registers
# MAX7219_REG_NOOP = 0x0
# MAX7219_REG_DIGIT0 = 0x1
# MAX7219_REG_DIGIT1 = 0x2
# MAX7219_REG_DIGIT2 = 0x3
# MAX7219_REG_DIGIT3 = 0x4
# MAX7219_REG_DIGIT4 = 0x5
# MAX7219_REG_DIGIT5 = 0x6
# MAX7219_REG_DIGIT6 = 0x7
# MAX7219_REG_DIGIT7 = 0x8
# MAX7219_REG_DECODEMODE = 0x9
# MAX7219_REG_INTENSITY = 0xA
# MAX7219_REG_SCANLIMIT = 0xB
# MAX7219_REG_SHUTDOWN = 0xC
# MAX7219_REG_DISPLAYTEST = 0xF
#
# # Setup SPI in channel 0
# wpi.wiringPiSPISetup(CHANNEL, MAX7219_HZ)
#
# push = wpi.wiringPiSPIDataRW
#
# # # Test your display
# # push(CHANNEL, bytes([MAX7219_REG_DISPLAYTEST, 0x1]))
# # push(CHANNEL, bytes([MAX7219_REG_DISPLAYTEST, 0x0]))
#
# # Setup
# push(CHANNEL, bytes([MAX7219_REG_DECODEMODE, 0x0]))  # Don't decode the bytes in any digit
# push(CHANNEL, bytes([MAX7219_REG_SCANLIMIT, 0x7]))  # Scan limit to all (8x8)
# push(CHANNEL, bytes([MAX7219_REG_INTENSITY, 0x5]))  # Intensity to half
# push(CHANNEL, bytes([MAX7219_REG_SHUTDOWN, 0x1]))  # Normal Operation
#
# # Ways to push your byte
# # push(CHANNEL, bytes([MAX7219_REG_DIGIT0, 0x0]))
# # push(CHANNEL, bytes([MAX7219_REG_DIGIT0, int('10000001', 2)]))
#
# dots = [
#     int('10000000', 2),
#     int('00100000', 2),
#     int('00010000', 2),
#     int('00001000', 2),
#     int('00000100', 2),
#     int('00000010', 2),
#     int('00000001', 2)
# ]
#
# while True:
#     for d in dots:
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT0, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT1, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT2, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT3, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT4, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT5, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT6, d]))
#         push(CHANNEL, bytes([MAX7219_REG_DIGIT7, d]))
#         time.sleep(0.05)
