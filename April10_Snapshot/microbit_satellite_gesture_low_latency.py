# Low-latency gesture satellite controller for string ensemble mode.
#
# Kids: if you want to change the control numbers, only edit the
# "STUDENT MAPPINGS" section below.
#
# This layout is intentionally simple so it has a better chance of
# round-tripping between MakeCode Python and Blocks.

# STUDENT MAPPINGS -----------------------------------------------------------

# Action codes
buttonACode = 1
buttonBCode = 2
buttonABCode = 3
logoCode = 4

# Gesture codes
logoUpCode = 1
logoDownCode = 2
tiltLeftCode = 3
tiltRightCode = 4
screenUpCode = 5
screenDownCode = 6
freeFallCode = 7
shakeCode = 8
threeGCode = 9
sixGCode = 10
eightGCode = 11

# Settings
RADIO_GROUP = 1
BUTTON_COOLDOWN_MS = 100
GESTURE_COOLDOWN_MS = 100
REPEAT_GAP_MS = 24
FLASH_HOLD_MS = 20

# ---------------------------------------------------------------------------

last_button_time = 0
last_gesture_time = 0


def clear_screen():
    basic.clear_screen()


def button_ready():
    return input.running_time() - last_button_time >= BUTTON_COOLDOWN_MS


def gesture_ready():
    return input.running_time() - last_gesture_time >= GESTURE_COOLDOWN_MS


def send_value_once(name: str, value: number):
    radio.send_value(name, value)


def send_value_twice(name: str, value: number):
    radio.send_value(name, value)
    basic.pause(REPEAT_GAP_MS)
    radio.send_value(name, value)


def flash_button_a():
    basic.show_leds("""
        . . . . .
        . . . . .
        # # . . .
        . . . . .
        . . . . .
        """)
    basic.pause(FLASH_HOLD_MS)
    clear_screen()


def flash_button_b():
    basic.show_leds("""
        . . . . .
        . . . . .
        . . . # #
        . . . . .
        . . . . .
        """)
    basic.pause(FLASH_HOLD_MS)
    clear_screen()


def flash_button_ab():
    basic.show_leds("""
        # . . . #
        . . . . .
        . . # . .
        . . . . .
        # . . . #
        """)
    basic.pause(FLASH_HOLD_MS)
    clear_screen()


def flash_logo():
    basic.show_leds("""
        . # . # .
        . . # . .
        . # . # .
        . . # . .
        . # . # .
        """)
    basic.pause(FLASH_HOLD_MS)
    clear_screen()


def flash_gesture(code: number):
    if code == logoUpCode:
        basic.show_leds("""
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            """)
    elif code == logoDownCode:
        basic.show_leds("""
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            """)
    elif code == tiltLeftCode:
        basic.show_leds("""
            . . . . #
            . . . # .
            # # # . .
            . . . . .
            . . . . .
            """)
    elif code == tiltRightCode:
        basic.show_leds("""
            # . . . .
            . # . . .
            . . # # #
            . . . . .
            . . . . .
            """)
    elif code == screenUpCode:
        basic.show_leds("""
            # # # # #
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            """)
    elif code == screenDownCode:
        basic.show_leds("""
            . . . . .
            . . . . .
            . . . . .
            . . . . .
            # # # # #
            """)
    elif code == freeFallCode:
        basic.show_leds("""
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            . . # . .
            """)
    elif code == shakeCode:
        basic.show_leds("""
            # . . . #
            . . . . .
            . . # . .
            . . . . .
            # . . . #
            """)
    elif code == threeGCode:
        basic.show_leds("""
            . . # . .
            . # . # .
            . . # . .
            . . # . .
            . . # . .
            """)
    elif code == sixGCode:
        basic.show_leds("""
            # . . . #
            . . . . .
            . . # . .
            . . . . .
            # . . . #
            """)
    elif code == eightGCode:
        basic.show_leds("""
            . . # . .
            . # . # .
            # . . . #
            . # . # .
            . . # . .
            """)
    else:
        basic.show_leds("""
            . . . . .
            . . . . .
            . . # . .
            . . . . .
            . . . . .
            """)
    basic.pause(FLASH_HOLD_MS)
    clear_screen()


def send_button(code: number):
    send_value_once("a", code)
    if code == buttonACode:
        flash_button_a()
    elif code == buttonBCode:
        flash_button_b()
    elif code == buttonABCode:
        flash_button_ab()
    else:
        flash_logo()


def send_gesture(code: number):
    send_value_once("g", code)
    flash_gesture(code)


def on_button_pressed_a():
    global last_button_time
    if button_ready():
        last_button_time = input.running_time()
        send_button(buttonACode)
input.on_button_pressed(Button.A, on_button_pressed_a)


def on_button_pressed_b():
    global last_button_time
    if button_ready():
        last_button_time = input.running_time()
        send_button(buttonBCode)
input.on_button_pressed(Button.B, on_button_pressed_b)


def on_button_pressed_ab():
    global last_button_time
    if button_ready():
        last_button_time = input.running_time()
        send_button(buttonABCode)
input.on_button_pressed(Button.AB, on_button_pressed_ab)


def on_logo_pressed():
    global last_button_time
    if button_ready():
        last_button_time = input.running_time()
        send_button(logoCode)
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_pressed)


def on_gesture_logo_up():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(logoUpCode)
input.on_gesture(Gesture.LOGO_UP, on_gesture_logo_up)


def on_gesture_logo_down():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(logoDownCode)
input.on_gesture(Gesture.LOGO_DOWN, on_gesture_logo_down)


def on_gesture_tilt_left():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(tiltLeftCode)
input.on_gesture(Gesture.TILT_LEFT, on_gesture_tilt_left)


def on_gesture_tilt_right():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(tiltRightCode)
input.on_gesture(Gesture.TILT_RIGHT, on_gesture_tilt_right)


def on_gesture_screen_up():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(screenUpCode)
input.on_gesture(Gesture.SCREEN_UP, on_gesture_screen_up)


def on_gesture_screen_down():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(screenDownCode)
input.on_gesture(Gesture.SCREEN_DOWN, on_gesture_screen_down)


def on_gesture_free_fall():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(freeFallCode)
input.on_gesture(Gesture.FREE_FALL, on_gesture_free_fall)


def on_gesture_shake():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(shakeCode)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)


def on_gesture_three_g():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(threeGCode)
input.on_gesture(Gesture.THREE_G, on_gesture_three_g)


def on_gesture_six_g():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(sixGCode)
input.on_gesture(Gesture.SIX_G, on_gesture_six_g)


def on_gesture_eight_g():
    global last_gesture_time
    if gesture_ready():
        last_gesture_time = input.running_time()
        send_gesture(eightGCode)
input.on_gesture(Gesture.EIGHT_G, on_gesture_eight_g)


radio.set_group(RADIO_GROUP)
radio.set_transmit_serial_number(True)
basic.show_icon(IconNames.HEART)


def on_forever():
    basic.pause(10)
basic.forever(on_forever)
