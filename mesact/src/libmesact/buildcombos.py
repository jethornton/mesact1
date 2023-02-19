import shutil, os

def build(parent):
	linearUnits = [
		['Select', False],
		['Inch', 'inch'],
		['Millimeter', 'mm']
		]

	for item in linearUnits:
		parent.linearUnitsCB.addItem(item[0], item[1])

	boards = [
	['Select', False],
	['5i24/6i24', '5i24'],
	['5i25/6i25', '5i25'],
	['7i76e', '7i76e'],
	['7i80DB-16', '7i80db16'],
	['7i80DB-25', '7i80db25'],
	['7i80HD-16', '7i80hd16'],
	['7i80HD-25', '7i80hd25'],
	['7i92', '7i92'],
	['7i92T', '7i92t'],
	['7i93', '7i93'],
	['7i95', '7i95'],
	['7i96', '7i96'],
	['7i96S', '7i96s'],
	['7i97', '7i97'],
	['7i98', '7i98'],
	]

	for item in boards:
		parent.boardCB.addItem(item[0], item[1])

	ipAddress = [
	['Select', False],
	['10.10.10.10', '10.10.10.10'],
	['192.168.1.121', '192.168.1.121']
	]

	for item in ipAddress:
		parent.ipAddressCB.addItem(item[0], item[1])
	parent.ipAddressCB.setEditable(True)

	axes = [
		['Select', False],
		['X', 'X'],
		['Y', 'Y'],
		['Z', 'Z'],
		['A', 'A'],
		['B', 'B'],
		['C', 'C'],
		['U', 'U'],
		['V', 'V'],
		['W', 'W']
		]

	for i in range(6):
		for item in axes:
			getattr(parent, f'c0_axisCB_{i}').addItem(item[0], item[1])
			getattr(parent, f'c1_axisCB_{i}').addItem(item[0], item[1])

	gui = [
		['Select', False],
		['AXIS', 'axis'],
		['GMOCCAPY', 'gmoccapy'],
		['TkLinuxCNC', 'tklinuxcnc'],
		['Touchy', 'touchy']
		]

	# Display Tab
	for item in gui:
		parent.guiCB.addItem(item[0], item[1])

	positionOffset = [
		['Select', False],
		['Relative', 'RELATIVE'],
		['Machine', 'MACHINE']
		]

	for item in positionOffset:
		parent.positionOffsetCB.addItem(item[0], item[1])

	positionFeedback = [
		['Select', False],
		['Commanded', 'COMMANDED'],
		['Actual', 'ACTUAL']
		]

	for item in positionFeedback:
		parent.positionFeedbackCB.addItem(item[0], item[1])

	editors = {'Gedit':'gedit', 'Geany':'geany', 'Pyroom':'pyroom',
		'Pluma':'pluma', 'Scite':'scite', 'Kwrite':'kwrite',
		'Kate':'kate', 'Mousepad':'mousepad', 'Jedit':'jedit',
		'XED':'xed'}
	installed = False
	for key, value in editors.items():
		if shutil.which(value) is not None:
			if not installed:
				parent.editorCB.addItem('Select', False)
				installed = True
			parent.editorCB.addItem(key, value)
	if not installed:
		parent.editorCB.addItem('None', False)
		parent.machinePTE.appendPlainText('No Editors were found!')

	drives = [
		['Custom', False],
		['Gecko 201', ['500', '4000', '20000', '1000']],
		['Gecko 202', ['500', '4500', '20000', '1000']],
		['Gecko 203v', ['1000', '2000', '200', '200']],
		['Gecko 210', ['500', '4000', '20000', '1000']],
		['Gecko 212', ['500', '4000', '20000', '1000']],
		['Gecko 320', ['3500', '500', '200', '200']],
		['Gecko 540', ['1000', '2000', '200', '200']],
		['TB6600', ['5000', '5000', '20000', '20000']],
		['L297', ['500', '4000', '4000', '1000']],
		['PMDX 150', ['1000', '2000', '1000', '1000']],
		['Sherline', ['22000', '22000', '100000', '100000']],
		['Xylotex BS-3', ['2000', '1000', '200', '200']],
		['Parker 750', ['1000', '1000', '1000', '200000']],
		['JVL SMD41/42', ['500', '500', '2500', '2500']],
		['Hobbycnc', ['2000', '2000', '2000', '2000']],
		['Keling 4030', ['5000', '5000', '20000', '20000']]
		]

	for i in range(6):
		for item in drives:
			getattr(parent, f'c0_driveCB_{i}').addItem(item[0], item[1])
			getattr(parent, f'c1_driveCB_{i}').addItem(item[0], item[1])
		getattr(parent, f'c0_driveCB_{i}').setEditable(True)

	for item in drives:
		getattr(parent, 'spindleDriveCB').addItem(item[0], item[1])
	getattr(parent, 'spindleDriveCB').setEditable(True)

	spindle = [
	['None', False],
	['Analog', 'analog'],
	['Digital', 'digital'],
	]

	for item in spindle:
		parent.spindleTypeCB.addItem(item[0], item[1])

	spindleFeedback = [
	['None', False],
	['Encoder', 'encoder']
	]

	# 1(PWM & Dir), 2(Up & Down), 3 (PWM & DIr), and 4 (Dir & PWM)
	# 1 (PWM on Out0 and Direction on Out1)
	# 2 (Up on Out0 and Down on Out1)
	# 3 (PDM mode, PDM on Out0 and Dir on Out1)
	# 4 (Direction on Out0 and PWM on Out1, for locked antiphase). 

	for item in spindleFeedback:
		parent.spindleFeedbackCB.addItem(item[0], item[1])

	spindlePwmType = [
	['Select', False],
	['PWM & Dir', '1'],
	['Up & Down', '2'],
	['PDM & Dir', '3'],
	['Dir & PWM', '4'],
	]

	for item in spindlePwmType:
		parent.spindlePwmTypeCB.addItem(item[0], item[1])

	ssCards = [
		['Select', False],
		['7i64', '7i64'],
		['7i69', '7i69'],
		['7i70', '7i70'],
		['7i71', '7i71'],
		['7i72', '7i72'],
		['7i73', '7i73'],
		['7i84', '7i84'],
		['7i87', '7i87']
		]

	for item in ssCards:
		parent.ssCardCB.addItem(item[0], item[1])

	# 7i73 Combo Boxes
	parent.ss7i73_keypadCB.addItem('None', ['w5d', 'w6d'])
	parent.ss7i73_keypadCB.addItem('4x8', ['w5d', 'w6u'])
	parent.ss7i73_keypadCB.addItem('8x8', ['w5u', 'w6d'])

	parent.ss7i73lcdCB.addItem('None', 'w7d')
	parent.ss7i73lcdCB.addItem('Enabled', 'w7u')

	debug = [
		['Debug Off', '0x00000000'],
		['Debug Configuration', '0x00000002'],
		['Debug Task Issues', '0x00000008'],
		['Debug NML', '0x00000010'],
		['Debug Motion Time', '0x00000040'],
		['Debug Interpreter', '0x00000080'],
		['Debug RCS', '0x00000100'],
		['Debug Interperter List', '0x00000800'],
		['Debug IO Control', '0x00001000'],
		['Debug O Word', '0x00002000'],
		['Debug Remap', '0x00004000'],
		['Debug Python', '0x00008000'],
		['Debug Named Parameters', '0x00010000'],
		['Debug Gdbon Signal', '0x00020000'],
		['Debug Python Task', '0x00040000'],
		['Debug User 1', '0x10000000'],
		['Debug User 2', '0x20000000'],
		['Debug Unconditional', '0x40000000'],
		['Debug All', '0x7FFFFFFF']
		]

	for item in debug:
		parent.debugCB.addItem(item[0], item[1])

	cpuSpeed = [
		['GHz', 1000],
		['MHz', 1]
		]

	for item in cpuSpeed:
		parent.cpuSpeedCB.addItem(item[0], item[1])

