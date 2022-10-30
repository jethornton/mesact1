import os, subprocess, requests
from packaging import version
from functools import partial
from datetime import datetime

from PyQt5.QtWidgets import QMessageBox, QApplication, QInputDialog, QLineEdit

from libmesact import firmware

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def unitsChanged(parent):
	if not parent.linearUnitsCB.currentData():
		unitsSecond = ''
		unitsMinute = ''
		for i in range(6):
			getattr(parent, f'c0_unitsLB_{i}').setText('Select Units\nMachine Tab')
		return
	if parent.linearUnitsCB.currentData() == 'mm':
		unitsSecond = 'mm/sec'
		unitsMinute = 'mm/min'
	elif parent.linearUnitsCB.currentData() == 'inch':
		unitsSecond = 'in/sec'
		unitsMinute = 'in/min'
	for i in range(6):
		getattr(parent, f'c0_unitsLB_{i}').setText(f'Vel & Acc\n{unitsSecond}')
	parent.trajMaxLinVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.defLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.maxLinJogVelDSB.setSuffix(f' {unitsSecond}')
	parent.minLinearVelLB.setText(f'{parent.minLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.jogSpeedLB.setText(f'{parent.defLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	parent.maxLinearVelLB.setText(f'{parent.maxLinJogVelDSB.value() * 60:.1f} {unitsMinute}')
	if set('ABC')&set(parent.coordinatesLB.text()): # angular axis
		parent.defAngularVelLB.setText(f'{parent.defAngJogVelDSB.value() * 60:.1f} deg/min')

	maxVelChanged(parent)

def maxVelChanged(parent):
	if parent.trajMaxLinVelDSB.value() > 0:
		val = parent.trajMaxLinVelDSB.value()
		if parent.linearUnitsCB.currentData() == 'mm':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} mm/min')
		if parent.linearUnitsCB.currentData() == 'inch':
			parent.mlvPerMinLB.setText(F'{val * 60:.1f} in/min')
	else:
		parent.mlvPerMinLB.setText('')

#def createError(parent):
#	os.makedirs(os.path.expanduser('~/.config/measct'))

def isNumber(s):
	try:
		s[-1].isdigit()
		float(s)
		return True
	except ValueError:
		return False

def checkmesaflash(parent, required = None):
	flashOk = True
	try:
		subprocess.check_output('mesaflash', encoding='UTF-8')
		if required != None:
			t = (f'Mesaflash version installed is less than {required}\n'
				f'The Mesa 7i96S requires Mesaflash {required} or later.\n'
				'Go to https://github.com/LinuxCNC/mesaflash\n'
				'for installation/update instructions.')
			try:
				version = subprocess.check_output(['mesaflash', '--version'], encoding='UTF-8')[-6:]
				if int(version.replace('.', '')) >= int(required.replace('.', '')):
					parent.machinePTE.appendPlainText(f'Mesaflash Version: {version}')
				else:
					parent.errorMsgOk(t, 'Mesaflash Version')
					parent.machinePTE.appendPlainText(t)
					flashOk = False
			except:
				parent.errorMsgOk(t, 'Mesaflash Version')
				parent.machinePTE.appendPlainText(t)
				flashOk = False
	except FileNotFoundError:
		#parent.errorMsgOk(('Mesaflash not found go to\n'
		#	'https://github.com/LinuxCNC/mesaflash\n'
		#	'for installation instructions.'), 'Notice! Can Not Flash Firmware')
		t = ('Mesaflash not found go to\n'
			'https://github.com/LinuxCNC/mesaflash\n'
			'for installation instructions.')
		parent.machinePTE.appendPlainText(t)
		parent.statusbar.showMessage('Mesaflash not found!')

	if not flashOk:
		parent.firmwareCB.setEnabled(False)
		parent.readhmidPB.setEnabled(False)
		parent.readpdPB.setEnabled(False)
		parent.flashPB.setEnabled(False)
		parent.reloadPB.setEnabled(False)
		parent.verifyPB.setEnabled(False)

def firmwareChanged(parent):
	if parent.firmwareCB.currentData():
		board = parent.board
		if parent.boardCB.currentData() in parent.mainBoards:
			daughters = getattr(firmware, f'd{parent.board}')(parent)
			if parent.firmwareCB.currentText() in daughters:
				cards = daughters[parent.firmwareCB.currentText()]
				parent.daughterCB_0.clear()
				if cards[0]:
					parent.daughterCB_0.addItem('Select', False)
					parent.daughterCB_0.addItem(cards[0], cards[0])
				parent.daughterCB_1.clear()
				if cards[1]:
					parent.daughterCB_1.addItem('Select', False)
					parent.daughterCB_1.addItem(cards[1], cards[1])
			else:
				parent.daughterCB_0.clear()
				parent.daughterCB_1.clear()


		# might combine these
		elif  parent.boardCB.currentData() in parent.allInOneBoards:
			daughters = getattr(firmware, f'd{parent.board}')(parent)
			if daughters:
				if parent.firmwareCB.currentText() in daughters:
					cards = daughters[parent.firmwareCB.currentText()]
					parent.daughterCB_0.clear()
					if cards[0]:
						parent.daughterCB_0.addItem('Select', False)
						parent.daughterCB_0.addItem(cards[0], cards[0])
					parent.daughterCB_1.clear()
					if cards[1]:
						parent.daughterCB_1.addItem('Select', False)
						parent.daughterCB_1.addItem(cards[1], cards[1])

		path = os.path.splitext(parent.firmwareCB.currentData())[0]
		pinfile = os.path.join(path + '.pin')
		if os.path.exists(pinfile):
			with open(pinfile, 'r') as file:
				data = file.read()
			parent.machinePTE.clear()
			parent.machinePTE.setPlainText(data)
		else:
			parent.machinePTE.clear()
			parent.machinePTE.setPlainText(f'No pin file found for {parent.firmwareCB.currentText()}')
		if '-' in board:
			board = board.replace("-", "_")

		options = getattr(firmware, f'o{board}')(parent)
		# options stepgens, pwmgens, qcount
		if options:
			if parent.firmwareCB.currentText() in options:
				parent.stepgensCB.clear()
				if options[parent.firmwareCB.currentText()][0]:
					for i in range(options[parent.firmwareCB.currentText()][0], -1, -1):
						parent.stepgensCB.addItem(f'{i}', f'{i}')
				parent.pwmgensCB.clear()
				if options[parent.firmwareCB.currentText()][1]:
					for i in range(options[parent.firmwareCB.currentText()][1], -1, -1):
						parent.pwmgensCB.addItem(f'{i}', f'{i}')
				parent.encodersCB.clear()
				if options[parent.firmwareCB.currentText()][2]:
					for i in range(options[parent.firmwareCB.currentText()][2], -1, -1):
						parent.encodersCB.addItem(f'{i}', f'{i}')
	else:
		parent.machinePTE.clear()

def connectorChanged(parent):
	if parent.connectorCB.currentText() == 'P1':
		parent.ioPort = '3'
		parent.analogPort = '4'
	if parent.connectorCB.currentText() == 'P2':
		parent.ioPort = '0'
		parent.analogPort = '1'

def axisDisplayChanged(parent, radioButton):
	#print(parent.sender().objectName())
	for button in parent.axisButtonGroup.buttons():
		if button is not radioButton:
			button.setChecked(False)

def updateAxisInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	card = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, f'{card}_scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, f'{card}_maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, f'{card}_maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if parent.linearUnitsCB.currentData():
		accelTime = maxVelocity / maxAccel
		getattr(parent, f'{card}_timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
		accelDistance = accelTime * 0.5 * maxVelocity
		getattr(parent, f'{card}_distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
		stepRate = scale * maxVelocity
		getattr(parent, f'{card}_stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')


def axisChanged(parent):
	connector = parent.sender().objectName()[:3]
	joint = parent.sender().objectName()[-1]
	axis = parent.sender().currentText()
	if axis in ['X', 'Y', 'Z', 'U', 'V', 'W']:
		getattr(parent, f'{connector}axisType_{joint}').setText('LINEAR')
		parent.minAngJogVelDSB.setEnabled(False)
		parent.defAngJogVelDSB.setEnabled(False)
		parent.maxAngJogVelDSB.setEnabled(False)
	elif axis in ['A', 'B', 'C']:
		getattr(parent, f'{connector}axisType_{joint}').setText('ANGULAR')
		parent.minAngJogVelDSB.setEnabled(True)
		parent.defAngJogVelDSB.setEnabled(True)
		parent.maxAngJogVelDSB.setEnabled(True)
	else:
		getattr(parent, f'{connector}axisType_{joint}').setText('')
		parent.minAngJogVelDSB.setEnabled(False)
		parent.defAngJogVelDSB.setEnabled(False)
		parent.maxAngJogVelDSB.setEnabled(False)
	coordList = []

	for i in range(6): # Card 0
		axisLetter = getattr(parent, f'c0_axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		#parent.axes = len(parent.coordinatesLB.text())

	'''
	for i in range(6): # Card 1
		axisLetter = getattr(parent, f'c1_axisCB_{i}').currentText()
		if axisLetter != 'Select':
			coordList.append(axisLetter)
		parent.coordinatesLB.setText(''.join(coordList))
		parent.axes = len(parent.coordinatesLB.text())
	'''

def inputChanged(parent): # test to see if not checked then enable both
	debounce = ['7i96s', '7i97']
	state = getattr(parent, parent.sender().objectName()).checkState()
	item, n = parent.sender().objectName().split('_')
	if state == 0: # only 7i96s and 7i97 have debounce
		if parent.board in debounce:
			getattr(parent, f'inputDebounceCB_{n}').setEnabled(True)
		getattr(parent, f'inputInvertCB_{n}').setEnabled(True)
	if item == 'inputInvertCB' and state == 2:
		getattr(parent, f'inputDebounceCB_{n}').setEnabled(False)
	elif item == 'inputDebounceCB' and state == 2:
		getattr(parent, f'inputInvertCB_{n}').setEnabled(False)


def ferrorSetDefault(parent):
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if parent.linearUnitsCB.currentData() == 'inch':
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.0002')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0001')
	else:
		getattr(parent, f'{connector}_ferror_{joint}').setText(' 0.005')
		getattr(parent, f'{connector}_min_ferror_{joint}').setText(' 0.0025')

def pidSetDefault(parent):
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	if not parent.linearUnitsCB.currentData():
		QMessageBox.warning(parent,'Warning', 'Machine Tab\nLinear Units\nmust be selected', QMessageBox.Ok)
		return
	if joint == 's':
		getattr(parent, 'p_s').setValue(0)
		getattr(parent, 'i_s').setValue(0)
		getattr(parent, 'd_s').setValue(0)
		getattr(parent, 'ff0_s').setValue(1)
		getattr(parent, 'ff1_s').setValue(0)
		getattr(parent, 'ff2_s').setValue(0)
		getattr(parent, 'bias_s').setValue(0)
		getattr(parent, 'maxOutput_s').setValue(parent.spindleMaxRpm.value())
		getattr(parent, 'maxError_s').setValue(0)
		getattr(parent, 'deadband_s').setValue(0)
		return

	p = int(1000/(int(parent.servoPeriodSB.cleanText())/1000000))
	getattr(parent,  f'{connector}_p_{joint}').setText(f'{p}')
	getattr(parent, f'{connector}_i_{joint}').setText('0')
	getattr(parent, f'{connector}_d_{joint}').setText('0')
	getattr(parent, f'{connector}_ff0_{joint}').setText('0')
	getattr(parent, f'{connector}_ff1_{joint}').setText('1')
	getattr(parent, f'{connector}_ff2_{joint}').setText('0')
	getattr(parent, f'{connector}_bias_{joint}').setText('0')
	getattr(parent, f'{connector}_maxOutput_{joint}').setText('0')
	if parent.linearUnitsCB.itemData(parent.linearUnitsCB.currentIndex()) == 'inch':
		maxError = '0.0005'
	else:
		maxError = '0.0127'
	getattr(parent, f'{connector}_maxError_{joint}').setText(maxError)
	getattr(parent, f'{connector}_deadband_{joint}').setText('0')

def analogSetDefault(parent): # think this is broken...
	#tab = parent.sender().objectName()[-1]
	connector = parent.sender().objectName()[:2]
	joint = parent.sender().objectName()[-1]
	getattr(parent, f'{connector}_analogMinLimit_{joint}').setText('-10')
	getattr(parent, f'{connector}_analogMaxLimit_{joint}').setText('10')
	getattr(parent, f'{connector}_analogScaleMax_{joint}').setText('10')

def driveChanged(parent):
	timing = parent.sender().currentData()
	connector = parent.sender().objectName()[:3]
	joint = f'_{parent.sender().objectName()[-1]}'
	if parent.sender().objectName() == 'spindleDriveCB':
		connector = 'spindle'
		joint = ''
	if timing:
		parent.sender().setEditable(False)
		getattr(parent, f'{connector}StepTime{joint}').setText(timing[0])
		getattr(parent, f'{connector}StepSpace{joint}').setText(timing[1])
		getattr(parent, f'{connector}DirSetup{joint}').setText(timing[2])
		getattr(parent, f'{connector}DirHold{joint}').setText(timing[3])
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(False)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(False)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(False)
	else:
		parent.sender().setEditable(True)
		getattr(parent, f'{connector}StepTime{joint}').setEnabled(True)
		getattr(parent, f'{connector}StepSpace{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirSetup{joint}').setEnabled(True)
		getattr(parent, f'{connector}DirHold{joint}').setEnabled(True)

def plcOptions():
	return ['ladderRungsSB', 'ladderBitsSB', 'ladderWordsSB',
	'ladderTimersSB', 'iecTimerSB', 'ladderMonostablesSB', 'ladderCountersSB',
	'ladderInputsSB', 'ladderOutputsSB', 'ladderExpresionsSB',
	'ladderSectionsSB', 'ladderSymbolsSB', 'ladderS32InputsSB',
	'ladderS32OuputsSB', 'ladderFloatInputsSB', 'ladderFloatOutputsSB']

def updateJointInfo(parent):
	if parent.sender().objectName() == 'actionOpen':
		return
	joint = parent.sender().objectName()[-1]
	scale = getattr(parent, 'scale_' + joint).text()
	if scale and isNumber(scale):
		scale = float(scale)
	else:
		return

	maxVelocity = getattr(parent, 'maxVelocity_' + joint).text()
	if maxVelocity and isNumber(maxVelocity):
		maxVelocity = float(maxVelocity)
	else:
		return

	maxAccel = getattr(parent, 'maxAccel_' + joint).text()
	if maxAccel and isNumber(maxAccel):
		maxAccel = float(maxAccel)
	else:
		return

	if not parent.linearUnitsCB.currentData():
		parent.errorDialog('Machine Tab:\nLinear Units must be selected')
		return
	accelTime = maxVelocity / maxAccel
	getattr(parent, 'timeJoint_' + joint).setText(f'{accelTime:.2f} seconds')
	accelDistance = accelTime * 0.5 * maxVelocity
	getattr(parent, 'distanceJoint_' + joint).setText(f'{accelDistance:.2f} {parent.linearUnitsCB.currentData()}')
	if parent.cardCB.currentData() == '7i76':
		stepRate = scale * maxVelocity
		getattr(parent, 'stepRateJoint_' + joint).setText(f'{abs(stepRate):.0f} pulses')
	else:
		getattr(parent, 'stepRateJoint_' + joint).setText('N/A')

def spindleChanged(parent):
	#print(parent.axes)
	if not parent.spindleTypeCB.currentData():
		parent.spindleGB.setEnabled(False)
		parent.spindlepwmGB.setEnabled(False)
		parent.spindlepidGB.setEnabled(False)
		parent.spindleStepgenGB.setEnabled(False)
	else:
		if parent.spindleTypeCB.currentData() == 'analog':
			parent.spindleGB.setEnabled(True)
			parent.spindlepwmGB.setEnabled(True)
			parent.spindlepidGB.setEnabled(True)
			parent.spindleStepgenGB.setEnabled(False)
			for i in range(parent.axes):
				parent.jointTabs_0.setTabEnabled(i, True)

		if parent.spindleTypeCB.currentData() == 'digital':
			parent.spindleGB.setEnabled(False)
			parent.spindlepwmGB.setEnabled(False)
			parent.spindlepidGB.setEnabled(False)
			parent.spindleStepgenGB.setEnabled(False)
			for i in range(parent.axes):
				parent.jointTabs_0.setTabEnabled(i, True)

		if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
			parent.spindlepwmGB.setEnabled(False)
			parent.spindlepidGB.setEnabled(False)
			for i in range(parent.axes):
				if i == int(parent.spindleTypeCB.currentData()[-1]):
					parent.jointTabs_0.setTabEnabled(i, False)
				else:
					parent.jointTabs_0.setTabEnabled(i, True)
			parent.spindleGB.setEnabled(True)
			parent.spindleMinRpm.setEnabled(False)
			parent.spindleStepgenGB.setEnabled(True)

def spindleSettingsChanged(parent):
	if parent.spindleMinRpm.value() > 0:
		parent.spindleMinRps.setText(f'{parent.spindleMinRpm.value() / 60:.2f}')
	else:
		parent.spindleMinRps.setText('')
	if parent.spindleMaxRpm.value() > 0:
		parent.spindleMaxRps.setText(f'{parent.spindleMaxRpm.value() / 60:.2f}')
	else:
		parent.spindleMaxRps.setText('')
	if parent.spindleMaxAccel.value() > 0:
		parent.spindleMaxRpss.setText(f'{parent.spindleMaxAccel.value() / 60:.2f}')
	else:
		parent.spindleMaxRpss.setText('')


def spindleFeedbackChanged(parent):
	if parent.spindleFeedbackCB.currentData() == 'encoder':
		parent.spindlepidGB.setEnabled(True)
	else:
		parent.spindlepidGB.setEnabled(False)

	'''
		parent.encoderGB.setEnabled(True)
		parent.encoderGB.setEnabled(False)
	'''
''' left over from 7i96 tool
def spindleTypeChanged(parent): 
	if parent.spindleTypeCB.currentData():
		parent.spindleGB.setEnabled(True)
		parent.spindleInfoGB.setEnabled(True)
		parent.encoderGB.setEnabled(True)
		parent.spindlepidGB.setEnabled(True)
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '1':
			parent.spindleInfo1Lbl.setText("PWM on Step 4")
			parent.tb2p3LB.setText("PWM +")
			parent.tb2p2LB.setText("PWM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '2':
			parent.spindleInfo1Lbl.setText("UP on Step 4")
			parent.tb2p3LB.setText("UP +")
			parent.tb2p2LB.setText("UP -")
			parent.spindleInfo2Lbl.setText("Down on Dir 4")
			parent.tb2p5LB.setText("DOWN +")
			parent.tb2p4LB.setText("DOWN -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '3':
			parent.spindleInfo1Lbl.setText("PDM on Step 4")
			parent.tb2p3LB.setText("PDM +")
			parent.tb2p2LB.setText("PDM -")
			parent.spindleInfo2Lbl.setText("Direction on Dir 4")
			parent.tb2p5LB.setText("Direction +")
			parent.tb2p4LB.setText("Direction -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
		if parent.spindleTypeCB.itemData(parent.spindleTypeCB.currentIndex()) == '4':
			parent.spindleInfo1Lbl.setText("Direction on Step 4")
			parent.tb2p3LB.setText("Direction +")
			parent.tb2p2LB.setText("Direction -")
			parent.spindleInfo2Lbl.setText("PWM on Dir 4")
			parent.tb2p5LB.setText("PWM +")
			parent.tb2p4LB.setText("PWM -")
			parent.spindleInfo3Lbl.setText("Select Enable on the Outputs tab")
'''

def ssCardChanged(parent):
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


def ss7i73Changed(parent):
	if parent.ss7i73lcdCB.currentData() == 'w7d': # no LCD
		parent.ss7i73w7Lbl.setText('W7 Down')
		lcd = False
	elif parent.ss7i73lcdCB.currentData() == 'w7u': # LCD
		parent.ss7i73w7Lbl.setText('W7 Up')
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
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(8):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# LCD No Keypad
	if lcd and not keypad:
		for i in range(8):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,16):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(inputs, menu)
			button.setMenu(menu)
		for i in range(4):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 4x8 Keypad
	if lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# LCD 8x8 Keypad
	if lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(5):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(4,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'LCD {i}')
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(False)

	# No LCD 4x8 Keypad
	if not lcd and keypad and keys == '4x8':
		for i in range(4):
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
			button = getattr(parent, f'ss7i73key_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

		for i in range(4,16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(8):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)
		for i in range(8,12):
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+6}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

	# No LCD 8x8 Keypad
	if not lcd and keypad and keys == '8x8':
		for i in range(16):
			getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Key {i}')
			getattr(parent, 'ss7i73key_' + str(i)).setEnabled(False)
		for i in range(12):
			getattr(parent, 'ss7i73lcd_' + str(i)).setEnabled(True)
			getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
			button = getattr(parent, f'ss7i73lcd_{i}')
			menu = QMenu()
			menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
			add_menu(outputs, menu)
			button.setMenu(menu)

def backupFiles(parent, configPath=None):
	if not configPath:
		configPath = parent.configPath
	if not os.path.exists(configPath):
		parent.machinePTE.setPlainText('Nothing to Back Up')
		return
	backupDir = os.path.join(configPath, 'backups')
	if not os.path.exists(backupDir):
		os.mkdir(backupDir)
	p1 = subprocess.Popen(['find',configPath,'-maxdepth','1','-type','f','-print'], stdout=subprocess.PIPE)
	backupFile = os.path.join(backupDir, f'{datetime.now():%m-%d-%y-%H:%M:%S}')
	p2 = subprocess.Popen(['zip','-j',backupFile,'-@'], stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	parent.machinePTE.appendPlainText('Backing up Confguration')
	output = p2.communicate()[0]
	parent.machinePTE.appendPlainText(output.decode())

def fileNew(parent):
	parent.errorMsgOk('Close the Tool,\n Then open', 'Info!')

def fileSaveAs(parent):
	parent.errorMsgOk('Change the Name,\n Then Save', 'Info!')

def copyOutput(parent):
	qclip = QApplication.clipboard()
	qclip.setText(parent.machinePTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def copyhelp(ui, parent):
	qclip = QApplication.clipboard()
	qclip.setText(ui.helpPTE.toPlainText())
	parent.statusbar.showMessage('Output copied to clipboard')

def add_menu(data, menu_obj):
	if isinstance(data, dict):
		for k, v in data.items():
			sub_menu = QMenu(k, menu_obj)
			menu_obj.addMenu(sub_menu)
			add_menu(v, sub_menu)
	elif isinstance(data, list):
		for element in data:
			add_menu(element, menu_obj)
	else:
		action = menu_obj.addAction(data)
		action.setIconVisibleInMenu(False)


