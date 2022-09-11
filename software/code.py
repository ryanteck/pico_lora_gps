# Pico GPS Car LoRa Tracker Code
# Based from Adafruit's Circuitpython code & @aalan's LoRa Demo Code

import time
import busio
import digitalio
import board
import microcontroller
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
import board

# Board LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.GP8)
irq = digitalio.DigitalInOut(board.GP7)
rst = digitalio.DigitalInOut(board.GP9)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0x26, 0x0B, 0xD4, 0xCA])

# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray( [0xDC, 0x6E, 0x64, 0x42, 0xBE, 0x5D, 0xD5, 0xFF, 0x7F, 0x3D, 0x76, 0x16, 0x0B, 0xC5, 0xBC, 0xEF] )

# TTN Application Key, 16 Bytess, MSB
app = bytearray( [0x09, 0x05, 0x64, 0x0E, 0x02, 0xA2, 0x0A, 0xC3, 0x44, 0xFE, 0x11, 0xEE, 0xF8, 0xBE, 0xAE, 0x6D] )

# To Decide ABP or OTA for this. I'm leaning towards ABP.
ttn_config = TTN(devaddr, nwkey, app, country="EU")

lora = TinyLoRa(spi, cs, irq, rst, ttn_config)

# Data Packet to send to TTN
data = bytearray(2)

# We want to change the transmission time based on the speed we're travelling at.
# Set delay in seconds for different speeds.

sleepTimes = {
    '0' : 600,
    '10': 300,
    '20': 300,
    '30': 300,
    '40': 300,
    '50': 300,
    '60': 300,
    '70': 300,
    '80': 300
}



while True:
    speed = '0'

    data[0] = 0x00

    # Send data packet
    print("Sending packet...")
    lora.send_data(data, len(data), lora.frame_counter)
    print("Packet Sent!")
    led.value = True
    lora.frame_counter += 1
    time.sleep(sleepTimes[speed])
    led.value = False
