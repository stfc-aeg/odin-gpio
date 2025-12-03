import gpiod
from gpiod.line import Direction, Value, Edge

CHIP_PATH = "/dev/gpiochip0"
BUTTON_LINE = 12
LED_LINES = [13, 14]

def toggle_value(value):
    return Value.INACTIVE if value == Value.ACTIVE else Value.ACTIVE

def main():
    led_state = Value.INACTIVE

    config = {
        BUTTON_LINE: gpiod.LineSettings(
            direction=Direction.INPUT,
            edge_detection=Edge.FALLING
        )
    }

    for line in LED_LINES:
        config[line] = gpiod.LineSettings(
            direction=Direction.OUTPUT,
            output_value=led_state
        )

    with gpiod.request_lines(CHIP_PATH, consumer="button-toggle-multi-leds", config=config) as request:
        while True:
            for event in request.read_edge_events():
                if event.line_offset == BUTTON_LINE:
                    print("Button pressed!")
                    led_state = toggle_value(led_state)

                    for line in LED_LINES:
                        request.set_value(line, led_state)
                    state_str = "ON" if led_state == Value.ACTIVE else "OFF"
                    print(f"LEDs are now {state_str}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
    except OSError as ex:
        print(ex, "\nCustomise the example configuration to suit your situation")
