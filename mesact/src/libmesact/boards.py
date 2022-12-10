import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMenu, QAction

from libmesact import utilities

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

def loadFirmware(parent):
		# firmware combobox
		parent.firmwareCB.clear()
		parent.firmwareDescPTE.clear()
		path = os.path.join(parent.firmware_path, parent.boardCB.currentData())
		files = sorted([entry.path for entry in os.scandir(path) if entry.is_file()])
		bitFiles = False
		extensions = ['.bit', '.bin']

		for file in files:
			if os.path.splitext(file)[1] in extensions:
				# might want to do ('Default', False) for 7i76e, 7i95, 7i96, 7i97
				parent.firmwareCB.addItem('Select', False)
				bitFiles = True
				break

		if bitFiles:
			for file in files:
				if os.path.splitext(file)[1] in extensions:
					parent.firmwareCB.addItem(os.path.basename(file), file)
			parent.machinePTE.appendPlainText(f'Firmware for {parent.boardCB.currentText()} Loaded')
			parent.machinePTE.appendPlainText('Select Firmware for Daughter Cards')
			parent.machinePTE.appendPlainText('Not all Firmware has a dictionary entry for Daughter Cards\n')
		else:
			parent.machinePTE.appendPlainText(f'No Firmware found {parent.boardCB.currentText()}!')
			parent.machinePTE.appendPlainText(f'No Daughter Cards are available for {parent.boardCB.currentText()}\n')

def boardChanged(parent):
	if parent.boardCB.currentData():
		#print(f'Board {parent.boardCB.currentData()}')
		parent.machinePTE.clear()
		parent.daughterCB_0.clear()
		parent.daughterCB_1.clear()
		if parent.boardCB.currentData() == '7i76e':
			parent.device = '7i76e-16'
		else:
			parent.device = parent.boardCB.currentData()

		if parent.boardCB.currentData() == '5i24': # DOUBLE CHECK THE SETTINGS
			parent.board = '5i24'
			parent.boardType = 'pci'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			parent.boardTW.setTabText(0, '5i24')
			parent.ipAddressCB.setEnabled(False)
			parent.daughterCB_0.setEnabled(True)
			parent.daughterCB_1.setEnabled(True)
			parent.ipAddressCB.setCurrentIndex(0)
			pixmap = QPixmap(os.path.join(parent.image_path, '5i24-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			info = ('')
			parent.boardInfoLB.setText(info)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		if parent.boardCB.currentData() == '5i25':
			parent.board = '5i25'
			parent.boardType = 'pci'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			parent.boardTW.setTabText(0, '5i25')
			parent.ipAddressCB.setEnabled(False)
			parent.daughterCB_0.setEnabled(True)
			parent.daughterCB_1.setEnabled(True)
			parent.ipAddressCB.setCurrentIndex(0)
			pixmap = QPixmap(os.path.join(parent.image_path, '5i25-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			info = ('')
			parent.boardInfoLB.setText(info)
			parent.daughterLB_0.setText('P2')
			parent.daughterLB_1.setText('P3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		# 5 axes of step & dir 32 sinking inputs and 16 sourcing outputs
		elif parent.boardCB.currentData() == '7i76e':
			parent.board = '7i76e'
			parent.machinePTE.appendPlainText('Field Power is required for the I/O')
			parent.machinePTE.appendPlainText(f'Firmware is optional for {parent.board} all in one boards')
			parent.machinePTE.appendPlainText('Default Firmware is 7i76e_7i76x1D.bit\n')
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.axes = 5
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(32):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(16):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
				# to do
				getattr(parent, f'outputInvertCB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i76e')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i76e')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i76e-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			pixmap = QPixmap(os.path.join(parent.image_path, '7i76e-schematic-0.png'))
			parent.schematicLB_0.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(6):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

			parent.spindleTypeCB.clear()
			parent.spindleTypeCB.addItem('None', False)
			parent.spindleTypeCB.addItem('Analog', 'analog')
			parent.spindleTypeCB.addItem('Digital', 'digital')
			for i in range(parent.axes):
				parent.spindleTypeCB.addItem(f'Stepgen {i}', f'stepgen_{i}')
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('TB3')
			parent.ssWiring_1.setText('15')
			parent.ssWiring_2.setText('16')
			parent.ssWiring_3.setText('17')
			parent.ssWiring_4.setText('18')
			parent.ssWiring_5.setText('19')
			parent.ssWiring_6.setText('20')
			parent.ssNotesGB.setTitle(f'{parent.boardCB.currentText()} Notes')
			text = ('Note: The 6 pin terminal block requires the +5V\n'
			'(brown and brown/white) and ground (blue and blue/white)\n'
			'pairs to be terminated in single screw terminal positions.')
			parent.ssWiringPTE.setPlainText(text)
			# Spindle Notes
			spinnotes = ('SPINDLE INTERFACE\n'
			'The 7I76E provides one analog output for spindle control. The analog output is a\n'
			'isolated potentiometer replacement type device. It functions like a potentiometer with\n'
			'SPINDLE + being one end of the potentiometer, SPINDLEOUT being the wiper and\n'
			'SPINDLE- being the other end. The voltage on SPINDLEOUT can be set to any voltage\n'
			'between SPINDLE- and SPINDLE+. Polarity and voltage range must always be observed\n'
			'for proper operation. The voltage supplied between SPINDLE+ and SPINDLE- must be\n'
			'between 5VDC an 15VDC with SPINDLE + always being more positive than SPINDLE-.\n'
			'Because the analog output is isolated, bipolar output is possible, for example with\n'
			'SPINDLE+ connected to 5V and SPINDLE- connected to -5V, a +-5V analog output range\n'
			'is created. In this case the spindle output must be offset so that 50% of full scale is output\n'
			'when a 0V output is required. Note that if bipolar output is used, the output will be forced\n'
			'to SPINDLE- at startup or when SPINENA is false.\n\n'
			'SPINDLE ISOLATED OUTPUTS\n'
			'The 7I76E provides 2 isolated outputs for use for spindle direction control, and\n'
			'spindle enable. These outputs are OPTO coupler Darlington transistors. They are all\n'
			'isolated from one another so can be used for pull up or pull-down individually. They will\n'
			'switch a maximum of 50 mA at 0 to 100 VDC. The SPINENA output is special as it uses\n'
			'the same signal that enables the analog output. When the analog output is enabled, the\n'
			'SPINENA OPTO output is on.\n')
			parent.spindlePTE.setPlainText(spinnotes)

		elif parent.boardCB.currentData() == '7i80db-16':
			parent.board = '7i80db-16'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80DB')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80db-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()


		elif parent.boardCB.currentData() == '7i80db-25':
			parent.board = '7i80db-25'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80DB')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80db-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('J2')
			parent.daughterLB_1.setText('J3')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		elif parent.boardCB.currentData() == '7i80hd-16':
			parent.board = '7i80hd-16'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80HD')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80hd-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			instructions = (
			'Firmware Notes\n'
			'SV = Servo\n'
			'ST = Step\n'
			'SS = SmartSerial\n'
			'RM = Resolver\n'
			'FA = Fanuc Absolute\n'
			'BI = BISS\n'
			'UA = UART\n')
			parent.machinePTE.appendPlainText(instructions)
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		elif parent.boardCB.currentData() == '7i80hd-25':
			parent.board = '7i80hd-25'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i80HD')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i80hd-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			instructions = (
			'Firmware Notes\n'
			'SV = Servo\n'
			'ST = Step\n'
			'SS = SmartSerial\n'
			'RM = Resolver\n'
			'FA = Fanuc Absolute\n'
			'BI = BISS\n'
			'UA = UART\n')
			parent.machinePTE.appendPlainText(instructions)
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		elif parent.boardCB.currentData() == '7i92':
			parent.board = '7i92'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i92')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i92-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		elif parent.boardCB.currentData() == '7i92t':
			parent.board = '7i92'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i92T')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i92t-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked() or parent.loading:
				if utilities.checkmesaflash(parent, '3.4.4', '7i92T'):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		elif parent.boardCB.currentData() == '7i93':
			parent.board = '7i93'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i93')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i93-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('')
			parent.ssWiring_1.setText('')
			parent.ssWiring_2.setText('')
			parent.ssWiring_3.setText('')
			parent.ssWiring_4.setText('')
			parent.ssWiring_5.setText('')
			parent.ssWiring_6.setText('')
			parent.ssNotesGB.setTitle('')
			parent.ssWiringGB.setEnabled(False)
			parent.ssNotesGB.setEnabled(False)
			parent.ssWiringPTE.clear()

		# 6 axes of step & dir 24 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i95':
			parent.board = '7i95'
			parent.machinePTE.appendPlainText(f'Firmware is optional for {parent.board} all in one boards')
			parent.machinePTE.appendPlainText('Default Firmware is 7i95_d.bit\n')
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.axes = 6
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(24):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(24,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
				# To Do
				getattr(parent, f'outputInvertCB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i95')
			parent.jointTabs_0.setTabEnabled(5, True)
			parent.mainTabs.setTabEnabled(4, True)
			parent.boardTW.setTabText(0, '7i95')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i95-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(6):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

			parent.spindleTypeCB.clear()
			parent.spindleTypeCB.addItem('None', False)
			parent.spindleTypeCB.addItem('Analog', 'analog')
			parent.spindleTypeCB.addItem('Digital', 'digital')
			for i in range(parent.axes):
				parent.spindleTypeCB.addItem(f'Stepgen {i}', f'stepgen_{i}')
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('TB4')
			parent.ssWiring_1.setText('13, 19')
			parent.ssWiring_2.setText('14, 20')
			parent.ssWiring_3.setText('15, 21')
			parent.ssWiring_4.setText('16, 22')
			parent.ssWiring_5.setText('17, 23')
			parent.ssWiring_6.setText('18, 24')
			parent.ssNotesGB.setTitle(f'{parent.boardCB.currentText()} Notes')
			text = ('Note: The 6 pin terminal block requires the +5V\n'
			'(brown and brown/white) and ground (blue and blue/white)\n'
			'pairs to be terminated in single screw terminal positions.')
			parent.ssWiringPTE.setPlainText(text)


		# 5 axes of step & dir 11 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i96':
			parent.board = '7i96'
			parent.machinePTE.appendPlainText('Field Power is required for the I/O')
			parent.machinePTE.appendPlainText(f'Firmware is optional for {parent.board} all in one boards')
			parent.machinePTE.appendPlainText('Default Firmware is 7i96_7i76d.bit\n')
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.axes = 5
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(11):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
				# Change to True when done
				getattr(parent, f'outputInvertCB_{i}').setEnabled(False)
			for i in range(32):
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(11,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
				getattr(parent, f'outputInvertCB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i96')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i96')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i96-card.png'))
			parent.boardLB.setPixmap(pixmap)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i96-schematic-0.png'))
			parent.schematicLB_0.setPixmap(pixmap)
			#parent.schematicLB_0.clear()
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(6):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)

			parent.spindleTypeCB.clear()
			parent.spindleTypeCB.addItem('None', False)
			parent.spindleTypeCB.addItem('Analog', 'analog')
			parent.spindleTypeCB.addItem('Digital', 'digital')
			for i in range(parent.axes):
				parent.spindleTypeCB.addItem(f'Stepgen {i}', f'stepgen_{i}')
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('TB2')
			parent.ssWiring_1.setText('15')
			parent.ssWiring_2.setText('16')
			parent.ssWiring_3.setText('17')
			parent.ssWiring_4.setText('18')
			parent.ssWiring_5.setText('19')
			parent.ssWiring_6.setText('20')
			parent.ssNotesGB.setTitle(f'{parent.boardCB.currentText()} Notes')
			text = ('Note: The 6 pin terminal block requires the +5V\n'
			'(brown and brown/white) and ground (blue and blue/white)\n'
			'pairs to be terminated in single screw terminal positions.')
			parent.ssWiringPTE.setPlainText(text)

		# 5 axes of step & dir 11 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i96s':
			parent.board = '7i96s'
			# load .bin files for this one
			parent.boardType = 'eth'
			parent.cardType_0 = 'step'
			parent.axes = 5
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(11):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
				getattr(parent, f'outputInvertCB_{i}').setEnabled(True)
			for i in range(11,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
				getattr(parent, f'outputInvertCB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i96S')
			parent.jointTabs_0.setTabEnabled(5, False)
			parent.boardTW.setTabText(0, '7i96S')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i96s-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			pixmap = QPixmap(os.path.join(parent.image_path, '7i96s-schematic-0.png'))
			parent.schematicLB_0.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('5', False)
			for i in range(4, -1, -1):
				parent.stepgensCB.addItem(f'{i}', f'{i}')
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			for i in range(6):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
				getattr(parent, f'c0_analogGB_{i}').setVisible(False)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(False)
			parent.machinePTE.clear()
			parent.machinePTE.appendPlainText('The 7i96S requires LinuxCNC Uspace 2.8.4 or 2.9 Febuary 24, 2022 or newer!')
			parent.machinePTE.appendPlainText(f'Firmware is optional for {parent.board} all in one boards')
			parent.machinePTE.appendPlainText(f'Default firmware for {parent.board} is 7i96s_d.bin\n')
			parent.spindleTypeCB.clear()
			parent.spindleTypeCB.addItem('None', False)
			parent.spindleTypeCB.addItem('Analog', 'analog')
			parent.spindleTypeCB.addItem('Digital', 'digital')
			for i in range(parent.axes):
				parent.spindleTypeCB.addItem(f'Stepgen {i}', f'stepgen_{i}')
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent, '3.4.3', '7i96S'):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('TB2')
			parent.ssWiring_1.setText('15')
			parent.ssWiring_2.setText('16')
			parent.ssWiring_3.setText('17')
			parent.ssWiring_4.setText('18')
			parent.ssWiring_5.setText('19')
			parent.ssWiring_6.setText('20')
			parent.ssNotesGB.setTitle(f'{parent.boardCB.currentText()} Notes')
			text = ('Note: The 6 pin terminal block requires the +5V\n'
			'(brown and brown/white) and ground (blue and blue/white)\n'
			'pairs to be terminated in single screw terminal positions.')
			parent.ssWiringPTE.setPlainText(text)

			# Spindle Notes
			spinnotes = ('ANALOG SPINDLE INTERFACE\n'
			'The 7I96S provides one analog output for spindle control. The analog output is a\n'
			'isolated potentiometer replacement type device. It functions like a potentiometer with\n'
			'SPINDLE+ being one end of the potentiometer, SPINDLE OUT being the wiper and\n'
			'SPINDLE- being the other end. The voltage on SPINDLE OUT can be set to any voltage\n'
			'between SPINDLE- and SPINDLE+. Polarity and voltage range must always be observed\n'
			'for proper operation. The voltage supplied between SPINDLE+ and SPINDLE- must be\n'
			'between 5VDC an 18VDC with SPINDLE + always being more positive than SPINDLE-.\n'
			'Because the analog output is isolated, bipolar output is possible, for example with\n'
			'SPINDLE+ connected to 5V and SPINDLE- connected to -5V, a +-5V analog output range\n'
			'is created. In this case the spindle PWM must be offset so that 50% of full scale is output\n'
			'when a 0V output is required. Note that if bipolar output is used, the output will be forced\n'
			'to SPINDLE- at startup.\n'
			'The analog output is driven by a FPGA PWM output (normally PWM 0). Optimum\n'
			'PWM frequency is 10-20 KHz but frequencies from 5 KHz to 50 KHz are acceptable, lower\n'
			'frequencies will have higher output ripple and higher frequencies will have worse linearity.\n')
			parent.spindlePTE.setPlainText(spinnotes)

			# Custom HAL
			halInputs = ['Select']
			for i in range(10):
				halInputs.append(f'hm2_7i96s.0.inm.00.input-{i:02}')
			for i in range(6):
				button = getattr(parent, f'inputPinPB_{i}')
				menu = QMenu()
				menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
				add_menu(halInputs, menu)
				button.setMenu(menu)

			halOutputs = ['Select']
			for i in range(4):
				halOutputs.append(f'hm2_7i96s.0.ssr.00.out-{i:02}')
			for i in range(4,6):
				halOutputs.append(f'hm2_7i96s.0.outm.00.out-{i:02}')
			for i in range(6):
				button = getattr(parent, f'outputPinPB_{i}')
				menu = QMenu()
				menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
				add_menu(halOutputs, menu)
				button.setMenu(menu)

		# 6 axes of analog servo 16 isolated inputs 6 isolated outputs
		elif parent.boardCB.currentData() == '7i97':
			parent.board = '7i97'
			parent.boardType = 'eth'
			parent.cardType_0 = 'servo'
			parent.axes = 6
			parent.mainTabs.setTabEnabled(3, True)
			parent.mainTabs.setTabEnabled(4, True)
			for i in range(16):
				getattr(parent, f'inputPB_{i}').setEnabled(True)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(True)
			for i in range(6):
				getattr(parent, f'outputPB_{i}').setEnabled(True)
			for i in range(16,32):
				getattr(parent, f'inputPB_{i}').setEnabled(False)
				getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
				getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
			for i in range(6,16):
				getattr(parent, f'outputPB_{i}').setEnabled(False)
			parent.cardTabs.setTabText(0, '7i97')
			parent.jointTabs_0.setTabEnabled(5, True)
			parent.boardTW.setTabText(0, '7i97')
			parent.ipAddressCB.setEnabled(True)
			parent.boardLB.clear()
			pixmap = QPixmap(os.path.join(parent.image_path, '7i97-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.schematicLB_0.clear()
			pixmap = QPixmap(os.path.join(parent.image_path, '7i97-schematic-0.png'))
			parent.schematicLB_0.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('N/A')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.pwmgensCB.addItem(f'{i}', f'{i}')
			parent.encodersCB.clear()
			parent.encodersCB.addItem('6', False)
			for i in range(5, -1, -1):
				parent.encodersCB.addItem(f'{i}', f'{i}')
			for i in range(6):
				getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
				getattr(parent, f'c0_analogGB_{i}').setVisible(True)
				getattr(parent, f'c0_encoderGB_{i}').setVisible(True)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)
			# Smart Serial
			parent.ssWiring_0.setText('TB2')
			parent.ssWiring_1.setText('13, 14')
			parent.ssWiring_2.setText('15')
			parent.ssWiring_3.setText('16')
			parent.ssWiring_4.setText('17')
			parent.ssWiring_5.setText('18')
			parent.ssWiring_6.setText('19, 20')
			parent.ssNotesGB.setTitle(f'{parent.boardCB.currentText()} Notes')
			text = ('Note: The 6 pin terminal block requires the +5V\n'
			'BROWN to 20 and BROWN/WHITE to 19 and ground BLUE to 13\n'
			'and BLUE/WHITE to 14.')
			parent.ssWiringPTE.setPlainText(text)

		elif parent.boardCB.currentData() == '7i98':
			parent.board = '7i98'
			parent.boardType = 'eth'
			parent.cardType_0 = ''
			parent.mainTabs.setTabEnabled(3, False)
			parent.mainTabs.setTabEnabled(4, False)
			parent.boardTW.setTabText(0, '7i98')
			parent.ipAddressCB.setEnabled(True)
			pixmap = QPixmap(os.path.join(parent.image_path, '7i98-card.png'))
			parent.boardLB.setPixmap(pixmap)
			parent.daughterLB_0.setText('P1')
			parent.daughterLB_1.setText('P2')
			parent.stepgensCB.clear()
			parent.stepgensCB.addItem('N/A', False)
			parent.pwmgensCB.clear()
			parent.pwmgensCB.addItem('N/A', False)
			parent.encodersCB.clear()
			parent.encodersCB.addItem('N/A', False)
			if parent.enableMesaflashCB.isChecked():
				if utilities.checkmesaflash(parent):
					loadFirmware(parent)


	else: # No Board Selected
		parent.board = ''
		parent.boardType = ''
		parent.ipAddressCB.setEnabled(False)
		parent.daughterCB_0.setEnabled(False)
		parent.daughterCB_1.setEnabled(False)
		parent.board = ''
		parent.boardLB.clear()
		parent.firmwareCB.clear()
		parent.schematicLB_0.clear()
		parent.daughterLB_0.setText('N/A')
		parent.daughterLB_1.setText('N/A')
		parent.mainTabs.setTabText(2, 'N/A')
		parent.mainTabs.setTabText(3, 'N/A')
		parent.mainTabs.setTabEnabled(2, False)
		parent.mainTabs.setTabEnabled(3, False)
		parent.stepgensCB.clear()
		parent.pwmgensCB.clear()
		parent.encodersCB.clear()
		# Smart Serial
		parent.ssWiring_0.setText('')
		parent.ssWiring_1.setText('')
		parent.ssWiring_2.setText('')
		parent.ssWiring_3.setText('')
		parent.ssWiring_4.setText('')
		parent.ssWiring_5.setText('')
		parent.ssWiring_6.setText('')
		parent.ssNotesGB.setTitle('')
		parent.ssWiringGB.setEnabled(False)
		parent.ssNotesGB.setEnabled(False)
		parent.ssWiringPTE.clear()

