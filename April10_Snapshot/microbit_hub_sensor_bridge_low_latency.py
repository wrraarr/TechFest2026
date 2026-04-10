"""

Micro:bit sensor hub bridge

Purpose:

- receive short radio name/value updates from up to 12 satellite micro:bits

- read the sender radio serial number

- forward browser-friendly serial lines over USB

Important:

Each satellite micro:bit must call:

radio.setTransmitSerialNumber(true)

or the hub cannot distinguish which device sent the packet.

Incoming satellite names:

x, y, z = accelerometer axes

l = light level

c = compass heading

s = sound level

a = event code

1 -> button A

2 -> button B

3 -> shake

Outgoing USB serial lines:

1151096431|x=123

1151096431|y=-456

1151096431|l=98

1151096431|a=1

"""

def on_received_value(name, value):
    global serialNumber
    serialNumber = radio.received_packet(RadioPacketProperty.SERIAL_NUMBER)
    serial.write_line("" + str(abs(serialNumber)) + "|" + name + "=" + str(value))
    led.plot(2, 2)
    basic.pause(20)
    led.unplot(2, 2)
radio.on_received_value(on_received_value)

serialNumber = 0
RADIO_GROUP = 1
radio.set_group(RADIO_GROUP)
basic.show_string("H")