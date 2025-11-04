import gpiod
import threading

from gpiod.line import Edge

class inputManager():

    def __init__(self, chip_path, line_offset, lineSignal, on_rising_edge):
        self.active = True
        self.times_risen = 0
        self.lineSignal = lineSignal
        self.on_rising_edge = on_rising_edge
        self.request = gpiod.request_lines(
            f"/dev/gpiochip{chip_path}",
            consumer="watch-line-value",
            config={
                line_offset: gpiod.LineSettings(edge_detection=Edge.BOTH)
            }
        )
        self.thread = threading.Thread(target=self.watch_line_value)
        self.thread.start()

    def watch_line_value(self):
        while self.active:
            if self.request.wait_edge_events(0.01):
                for event in self.request.read_edge_events():
                    if event.event_type is event.Type.RISING_EDGE:
                       self.times_risen += 1
                       self.on_rising_edge(self.times_risen)
