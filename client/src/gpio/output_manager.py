import gpiod
import threading
import time

from gpiod.line import Direction, Value

class outputManager():

    def __init__(self, chip_path, line_offset):
        self.active = False
        self.LINE_OFFSET = line_offset
        self.start_time = 0
        self.request = gpiod.request_lines(
            f"/dev/gpiochip{chip_path}",
            consumer="toggle-line-value",
            config={
                self.LINE_OFFSET: gpiod.LineSettings(
                    direction=Direction.OUTPUT, output_value=Value.INACTIVE
                )
            }
        )

    def toggle_value(self, value):
        if value == True:
            return Value.ACTIVE
        return Value.INACTIVE

    def pulse(self, val):
        self.request.set_value(self.LINE_OFFSET, self.toggle_value(not self.active))
        thread = threading.Thread(target=self.line_pulse)
        thread.start()

    def line_pulse(self):
        time.sleep(0.1)
        self.request.set_value(self.LINE_OFFSET, self.toggle_value(self.active))
      
