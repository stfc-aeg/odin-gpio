import time

import gpiod
from gpiod.line import Direction, Value

with gpiod.Chip("/dev/gpiochip0") as chip:
    info = chip.get_info()
    print(f"{info.name} [{info.label}] ({info.num_lines} lines)")

prev_req = ""
LINE = 13
with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="pushbutton",
    config={
        LINE: gpiod.LineSettings(
            direction=Direction.INPUT
        )
    },
) as request:
    while True:
        result = request.get_value(LINE)
        if prev_req != result:
            print(result)
            prev_req = result
        time.sleep(1)