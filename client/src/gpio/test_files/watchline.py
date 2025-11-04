import gpiod

from datetime import timedelta
from gpiod.line import Bias, Edge

prev_val = ""

def edge_type_str(event):
    if event.event_type is event.Type.RISING_EDGE:
        return "Rising"
    if event.event_type is event.Type.FALLING_EDGE:
        return "Falling"
    return "Unknown"

def watch_line_value(chip, line_offset, prev_val):
    
    with gpiod.request_lines(
        f"/dev/gpiochip{chip}",
        consumer="watch-line-value",
        config={
            line_offset: gpiod.LineSettings(edge_detection=Edge.BOTH)
        },
    ) as request:
        while True:
            for event in request.read_edge_events():
                direction = edge_type_str(event)
                if direction != prev_val:
                    print(
                        "line: {}  type: {:<7}  event #{}".format(
                            event.line_offset, edge_type_str(event), event.line_seqno
                        )
                    )
                    prev_val = direction
                else:
                    print("BOUNCE DETECTED")  
        return prev_val    

if __name__ == "__main__":
    try:
        prev_val = watch_line_value(0, 12, prev_val)
    except OSError as ex:
        print(ex, "\nCustomise the example configuration to suit your situation")