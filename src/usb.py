import asyncio
import evdev
from os import getenv
from evdev import InputDevice, categorize, ecodes  

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'z', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'y', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Z', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Y', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT',  57: u' ', 100: u'RALT'
}

def get_device(DEVICE_NAME):
    # Find and return an evdev.InputDevice for the input device
    for dev_path in evdev.list_devices():
        device = evdev.InputDevice(dev_path)

        if device.name == DEVICE_NAME:
            return device

async def listen_to_usb_device(dev: InputDevice) -> str:
	# setup vars
	x = ''
	caps = False

	# grab provides exclusive access to the device
	dev.grab()

	# loop
	async for event in dev.async_read_loop():
		if event.type == ecodes.EV_KEY:
			data = categorize(event)  # Save the event temporarily to introspect it
			if data.scancode == 42:
				if data.keystate == 1:
					caps = True
				if data.keystate == 0:
					caps = False
			if data.keystate == 1:  # Down events only
				if caps:
					key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  # Lookup or return UNKNOWN:XX
				else:
					key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)  # Lookup or return UNKNOWN:XX
				if (data.scancode != 42) and (data.scancode != 28):
					x += key_lookup  
				if(data.scancode == 28):
					break
	dev.close()
	return x

def listen_to_rfid() -> str:
	dev = get_device(getenv('RFID_DEVICE_NAME'))
	loop = asyncio.get_event_loop()
	id = loop.run_until_complete(listen_to_usb_device(dev))
	return id

def listen_to_scanner() -> str:
	dev = get_device(getenv('SCANNER_DEVICE_NAME'))
	loop = asyncio.get_event_loop()
	id = loop.run_until_complete(listen_to_usb_device(dev))
	return id