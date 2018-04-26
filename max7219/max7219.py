from wiringpi import wiringPiSPISetup as spiSetup
from wiringpi import wiringPiSPIDataRW as spiRW
import copy

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

# Rotation
ROTATION_0 = 0
ROTATION_90 = 1
ROTATION_270 = 2
ROTATION_180 = 3


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

    def __init__(self, channel=0, auto_update=True, number_screens=1, brightness=15, **kwargs):
        """
        Args:
            channel (int): Channel for SPI communication
            auto_update (bool): Update screen on functions that change the frame
            number_screens (int): Number of screens being controlled by MAX7219 (TODO)

        Keyword Args:
            flip_x (bool): Flip X of the frame when drawing it to the screen.
            flip_y (bool): Flip Y of the frame when drawing it to the screen.
            rotation (int): Rotation of the frame when drawing it to the screen, to rotate 180° just flip x and flip y

        """
        self._brightness = brightness
        self._channel = channel
        self.auto_update = auto_update
        self.number_screens = number_screens

        # Keyword Args
        self.rotation = kwargs.get('rotation')
        if not self.rotation:
            self.rotation = ROTATION_0

        self.flip_x = kwargs.get('flip_x')
        self.flip_y = kwargs.get('flip_y')

        # Initialization
        spiSetup(self._channel, MAX7219_HZ)  # SPI Channel
        self.__setup_screen()  # MAX1729 Registers

        self._frame = self.get_empty_frame(8, 8)
        self.clear_screen()

    def __setup_screen(self, screen=0):
        spiRW(self._channel, bytes([MAX7219_REG_DECODEMODE, 0x0]))  # Don't decode the bytes in any digit
        spiRW(self._channel, bytes([MAX7219_REG_SCANLIMIT, 0x7]))  # Scan limit to all (8x8) - Don't use it to clear the screen!!!s
        spiRW(self._channel, bytes([MAX7219_REG_INTENSITY, self._brightness]))  # Brightness (0-15)
        spiRW(self._channel, bytes([MAX7219_REG_SHUTDOWN, 0x1]))  # Normal Operation

    def clear_screen(self, screen=0):
        self.set_frame([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])

    def fill_screen(self, screen=0):
        self.set_frame([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]
        ])

    def set_point(self, x, y, value=True, screen=0):
        value = int(bool(value))
        self._frame[y][x] = value
        if self.auto_update:
            self.update_screen()

    def update_screen(self, screen=0):
        frame = copy.copy(self._frame)

        # Flippity flips
        if self.flip_y:
            frame = frame[::-1]
        if self.flip_x:
            flipped_frame = []
            for f in frame:
                flipped_frame.append(f[::-1])
            frame = flipped_frame

        # Rotation stuff
        if self.rotation != ROTATION_0:
            rotated_frame = self.get_empty_frame(8, 8)
            if self.rotation == ROTATION_90:
                count_x = 7
                count_y = 0
                for line_y in frame:
                    for point in line_y:
                        rotated_frame[count_y][count_x] = point
                        count_y += 1
                    count_y = 0
                    count_x -= 1

            if self.rotation == ROTATION_270:
                count_x = 0
                count_y = 7
                for line_y in frame:
                    for point in line_y:
                        rotated_frame[count_y][count_x] = point
                        count_y -= 1
                    count_y = 7
                    count_x += 1

            if self.rotation == ROTATION_180:
                count_x = 7
                count_y = 7
                for line_y in frame:
                    for point in line_y:
                        rotated_frame[count_y][count_x] = point
                        count_x -= 1
                    count_x = 7
                    count_y -= 1

            frame = rotated_frame

        # Create bytes
        screen_bytes = []
        for f in frame:
            # Convert to byte and append
            f_str = [str(x) for x in f]
            f_bytes = int(''.join(f_str), 2)
            screen_bytes.append(f_bytes)

        # Write to registers
        for i, reg in enumerate(Matrix8X8.display_registers):
            spiRW(self._channel, bytes([reg, screen_bytes[i]]))

    def get_channel(self):
        return self._channel

    def set_channel(self, channel):
        self._channel = channel
        spiSetup(self._channel, MAX7219_HZ)
        self.__setup_screen()

    def get_frame(self):
        return self._frame

    def set_frame(self, frame, shift=0):
        if shift == 0:
            self._frame = self.get_valid_frame(frame)
        else:
            self._frame = self.get_shift_frame(frame, shift)

        if self.auto_update:
            self.update_screen()

    @classmethod
    def get_valid_frame(cls, frame):
        valid_frame = Matrix8X8.get_empty_frame(8, 8)
        for y in range(8):
            for x in range(8):
                valid_frame[y][x] = frame[y][x]
        return valid_frame

    @classmethod
    def get_empty_frame(cls, width, height):
        new_frame = []
        for y in range(height):
            line_y = []
            for x in range(width):
                line_y.append(0)
            new_frame.append(line_y)
        return new_frame

    @classmethod
    def get_shift_frame(cls, frame, shift):
        if shift == 0:
            return frame

        shifted_frame = Matrix8X8.get_empty_frame(8, 8)

        frame_cpy = copy.copy(frame)

        count_x = shift

        for x in range(8):
            for y in range(8):
                try:
                    shifted_frame[y][x] = frame_cpy[y][count_x]
                except IndexError:
                    shifted_frame[y][x] = 0

            count_x += 1

        return shifted_frame

    @classmethod
    def get_scrollable_string_chars(cls, chars):
        string = Matrix8X8.get_empty_frame(8*(len(chars)+1), 8)
        count_x = 8
        for char in chars:
            for x in range(8):
                for y in range(8):
                    string[y][count_x] = char[y][x]
                count_x += 1

        return string


def example_scroll_text():
    from time import sleep
    from charset8x8 import charset8x8

    matrix = Matrix8X8(brightness=1, rotation=ROTATION_90)

    print('running')

    # Scrolling Text

    string = matrix.get_scrollable_string_chars(
        [x for x in charset8x8.values()]
    )

    count = 0
    while True:
        matrix.set_frame(string, count)
        count += 1
        if count >= len(string[0]):
            break
        sleep(0.07)


def example_ball():
    from time import sleep

    matrix = Matrix8X8(brightness=1, rotation=ROTATION_90)

    print('running')

    ball_x, ball_y = 4,0
    dir_x , dir_y = 1,-1

    for i in range(round(100)):
        ball_x += dir_x
        ball_y += dir_y

        if ball_y <= 0 or ball_y >= 7:
            dir_y *= -1
        if ball_x <= 0 or ball_x >= 7:
            dir_x *= -1

        if ball_y < 0:
            ball_y = 0
        if ball_y > 7:
            ball_y = 7
        if ball_x < 0:
            ball_x = 0
        if ball_x > 7:
            ball_x = 7

        matrix.clear_screen()
        matrix.set_point(ball_x, ball_y)
        sleep(0.033)


def example_anim():
    from time import sleep

    matrix = Matrix8X8(brightness=1, rotation=ROTATION_90)

    print('running')

    for i in range(4):
        for y in range(8):
            for x in range(8):
                matrix.set_point(x,y)
                sleep(0.016)

        for y in range(7, -1, -1):
            for x in range(7, -1, -1):
                matrix.set_point(x, y, False)
                sleep(0.016)


if __name__ == '__main__':
    try:
        example_scroll_text()
        example_ball()
        example_anim()
    except KeyboardInterrupt:
        matrix = Matrix8X8(brightness=1, rotation=ROTATION_90)
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
