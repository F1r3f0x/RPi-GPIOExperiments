import wiringpi as wpi


class GraphLED:
    """Graph of GPIO LEDs."""
    def __init__(self, leds, max_value=100, value=0):
        """
        Args:
            leds (list): Pins of LEDs (first to last)
            max_value (int): Max value of the graph
            value (int): Current value of the graph
        """
        self.leds = leds
        self.max_value = max_value
        self.value = value

        self.setup_leds()

    @property
    def leds(self):
        """list: GPIO Pins of the LEDs in the graph from first to last."""
        return self._leds

    @leds.setter
    def leds(self, leds):
        self._leds = leds
        self.setup_leds()

    @property
    def value(self):
        """int: Current value of the graph"""
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.update()

    def setup_leds(self):
        """Setups the pins for the LEDs."""
        for l in self.leds:
            wpi.pinMode(l, wpi.OUTPUT)
            wpi.digitalWrite(l, wpi.LOW)

    def update(self):
        """Turns on the LEDs to represent the current value."""
        for l in self.leds:
            wpi.digitalWrite(l, wpi.LOW)

        steps = round(self.max_value / len(self.leds))

        graph_step = self.value // steps
        if self.value % steps > 0:
            graph_step += 1

        if self.value <= 0:
            return
        if self.value >= self.max_value:
            for l in self.leds:
                wpi.digitalWrite(l, wpi.HIGH)
            return

        for i, l in enumerate(self.leds):
            if i < graph_step:
                wpi.digitalWrite(l, wpi.HIGH)
            else:
                wpi.digitalWrite(l, wpi.LOW)


if __name__ == '__main__':
    import time

    wpi.wiringPiSetupGpio()

    graph = GraphLED([7, 8, 25, 18, 15, 14])

    print(graph.leds)

    quit()

    print('running...')
    while True:
        if graph.value > 100:
            graph.value = 0

        time.sleep(0.01)

        graph.value += 1
