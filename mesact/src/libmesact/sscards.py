INPUTS = [
	['Select', False],
	['Signal Only', ''],
	['Probe', 'motion.probe-input'],
	['Digital In 0', 'motion.digital-in-00'],
	['Digital In 1', 'motion.digital-in-01'],
	['Digital In 2', 'motion.digital-in-02'],
	['Digital In 3', 'motion.digital-in-03'],
]

OUTPUTS = [
	['Select', False],
	['Signal Only', ''],
	['Coolant Flood', 'iocontrol.0.coolant-flood'],
	['Coolant Mist', 'iocontrol.0.coolant-mist'],
	['Spindle On', 'spindle.0.on'],
	['Spindle CW', 'spindle.0.forward'],
	['Spindle CCW', 'spindle.0.reverse'],
	['Spindle Brake', 'spindle.0.brake'],
	['E-Stop Out', 'iocontrol.0.user-enable-out'],
	['Digital Out 0', 'motion.digital-out-00'],
	['Digital Out 1', 'motion.digital-out-01'],
	['Digital Out 2', 'motion.digital-out-02'],
	['Digital Out 3', 'motion.digital-out-03'],
]

AIN = [
	['Select', False],
	['Analog In 0', 'motion.analog-in-00'],
	['Analog In 1', 'motion.analog-in-01'],
	['Analog In 2', 'motion.analog-in-02'],
	['Analog In 3', 'motion.analog-in-03'],
]

def build(parent):
	sscards = {
	'Select':'No Card Selected',
	'7i64':'24 Outputs, 24 Inputs',
	'7i69':'48 Digital I/O Bits',
	'7i70':'48 Inputs',
	'7i71':'48 Sourcing Outputs',
	'7i72':'48 Sinking Outputs',
	'7i73':'Pendant Card',
	'7i84':'32 Inputs 16 Outputs',
	'7i87':'8 Analog Inputs'
	}

	sspage = {
	'Select':0,
	'7i64':1,
	'7i69':2,
	'7i70':3,
	'7i71':4,
	'7i72':5,
	'7i73':6,
	'7i84':7,
	'7i87':8
	}
	parent.smartSerialInfoLbl.setText(sscards[parent.ssCardCB.currentText()])
	parent.smartSerialSW.setCurrentIndex(sspage[parent.ssCardCB.currentText()])

	pins7i64 = {}
	pins7i69 = {}
	pins7i70 = {}
	pins7i71 = {}
	pins7i72 = {}
	pins7i73 = {}
	pins7i84 = {}
	pins7i87 = {}

def buildCB(parent):

	# 7i73 Combo Boxes
	parent.ss7i73_keypadCB.addItem('None', ['w5d', 'w6d'])
	parent.ss7i73_keypadCB.addItem('4x8', ['w5d', 'w6u'])
	parent.ss7i73_keypadCB.addItem('8x8', ['w5u', 'w6d'])

	parent.ss7i92lcdCB.addItem('None', 'w7d')
	parent.ss7i92lcdCB.addItem('Enabled', 'w7u')

	for i in range(16):
		for item in INPUTS:
			getattr(parent, 'ss7i73in_' + str(i)).addItem(item[0], item[1])
	for i in range(2):
		for item in OUTPUTS:
			getattr(parent, 'ss7i73out_' + str(i)).addItem(item[0], item[1])

	# 7i87 Combo Boxes
	for i in range(8):
		for item in AIN:
			getattr(parent, 'ss7i87in_' + str(i)).addItem(item[0], item[1])

def ss7i73setup(parent):
	if parent.ss7i92lcdCB.currentData() == 'w7d': # no LCD
		parent.ss7i92w7Lbl.setText('W7 Down')
		lcd = False
	elif parent.ss7i92lcdCB.currentData() == 'w7u': # LCD
		parent.ss7i92w7Lbl.setText('W7 Up')
		lcd = True
	if parent.ss7i73_keypadCB.currentData()[0] == 'w5d':
		if parent.ss7i73_keypadCB.currentData()[1] == 'w6d': # no keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = False
		elif parent.ss7i73_keypadCB.currentData()[1] == 'w6u': # 4x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Down')
			parent.ss7i73w6Lbl.setText('W6 Up')
			keypad = True
			keys = '4x8'
	elif parent.ss7i73_keypadCB.currentData()[0] == 'w5u': # 8x8 keypad
			parent.ss7i73w5Lbl.setText('W5 Up')
			parent.ss7i73w6Lbl.setText('W6 Down')
			keypad = True
			keys = '8x8'

	# No LCD No Keypad
	if not lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+10}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(8,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'In {i+8}')
			for item in INPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+10}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+6}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(8,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'In {i+8}')
			for item in INPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).clear()

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+6}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).clear()
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).clear()

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).clear()
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).clear()

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Out {i+10}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73key_' + str(i)).addItem(item[0], item[1])
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).clear()
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+6}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).clear()
		for i in range(12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Out {i+2}')
			for item in OUTPUTS:
				getattr(parent, 'ss7i73lcd_' + str(i)).addItem(item[0], item[1])

