import os

def configNameChanged(parent, text):
	if text:
		parent.configNameUnderscored = text.replace(' ','_').lower()
		parent.configPath = os.path.expanduser('~/linuxcnc/configs') + '/' + parent.configNameUnderscored
		parent.pathLabel.setText(parent.configPath)
	else:
		parent.pathLabel.setText('')

def daughterCardChanged(parent):
	# if boardCB.currentData() in MAIN_BOARDS:
		# enable cardTabs(0)
	# elif boardCB.currentData() in ALL_IN_ONE_BOARDS:
		# enable cardTabs(0)
		# enable cardTabs(1)

	if parent.sender().currentData():
		#print(parent.sender().currentData())

		#motherBoards = ['5i25', '7i80db', '7i80hd', '7i92', '7i93', '7i98']
		axes = {'7i33': 4, '7i47': 6, '7i76': 5, '7i77': 6, '7i78': 4, '7i85': 6, '7i85s': 6, '5ABOB': 5}
		inputs = {'7i76': '32', '7i77': '32', '7i78': '0', '7i85': 0, '7i85s': 0, '5ABOB': '5'}
		outputs = {'7i76': '16', '7i77': '16', '7i78': '0', '7i85': 0, '7i85s': 0, '5ABOB': '1'}
		stepper = ['7i76', '7i78']
		servo = ['7i77']
		cardType = {'7i33': 'servo', '7i47': 'step', '7i76': 'step', '7i77': 'servo',
		'7i78': 'step', '7i85': 'servo', '7i85s': 'servo', '5ABOB': 'step'}

		if parent.sender().currentData() == '7i76':
			spinnotes = ('SPINDLE INTERFACE\n'
			'The 7I76 provides one analog output for spindle control. The analog output is a\n'
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
			'The 7I76 provides 2 isolated outputs for use for spindle direction control, and\n'
			'spindle enable. These outputs are OPTO coupler Darlington transistors. They are all\n'
			'isolated from one another so can be used for pull up or pull-down individually. They will\n'
			'switch a maximum of 50 mA at 0 to 100 VDC. The SPINENA output is special as it uses\n'
			'the same signal that enables the analog output. When the analog output is enabled, the\n'
			'SPINENA OPTO output is on.\n')
			parent.spindlePTE.setPlainText(spinnotes)

		if parent.sender().currentData() == '7i77':
			spinnotes = ('SPINDLE INTERFACE\n'
			'A 7I77, analog channel 5 is designed for spindle use, no other channel is\n'
			'suitable since only analog channel 5 can be enabled/disabled independently.\n'
			)

			parent.spindlePTE.setPlainText(spinnotes)


		if parent.sender().objectName() == 'daughterCB_0':
			parent.daughterCB_1.setEnabled(False)
		elif parent.sender().objectName() == 'daughterCB_1':
			parent.daughterCB_0.setEnabled(False)
		parent.mainTabs.setTabEnabled(3, True)
		parent.mainTabs.setTabEnabled(4, True)
		parent.axes = axes[parent.sender().currentData()]

		parent.cardTabs.setTabText(0, parent.sender().currentData())
		parent.cardType_0 = cardType[parent.sender().currentData()]

		if axes[parent.sender().currentData()] == 6:
			parent.jointTabs_0.setTabEnabled(4, True)
			parent.jointTabs_0.setTabEnabled(5, True)
		elif axes[parent.sender().currentData()] == 5:
			parent.jointTabs_0.setTabEnabled(4, True)
			parent.jointTabs_0.setTabEnabled(5, False)
		elif axes[parent.sender().currentData()] == 4:
			parent.jointTabs_0.setTabEnabled(4, False)
			parent.jointTabs_0.setTabEnabled(5, False)

		if parent.daughterCB_0.currentData():
			if cardType[parent.daughterCB_0.currentData()] == 'step':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
					getattr(parent, f'c0_analogGB_{i}').setVisible(False)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(False)
			elif cardType[parent.daughterCB_0.currentData()] == 'servo':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
					getattr(parent, f'c0_analogGB_{i}').setVisible(True)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(True)

		if parent.daughterCB_1.currentData():
			if cardType[parent.daughterCB_1.currentData()] == 'step':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(True)
					getattr(parent, f'c0_analogGB_{i}').setVisible(False)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(False)
			elif cardType[parent.daughterCB_1.currentData()] == 'servo':
				for i in range(5):
					getattr(parent, f'c0_stepgenGB_{i}').setVisible(False)
					getattr(parent, f'c0_analogGB_{i}').setVisible(True)
					getattr(parent, f'c0_encoderGB_{i}').setVisible(True)

		# Setup I/O
		for i in range(int(inputs[parent.sender().currentData()])):
			getattr(parent, f'inputPB_{i}').setEnabled(True)
			getattr(parent, f'inputInvertCB_{i}').setEnabled(True)
		for i in range(int(inputs[parent.sender().currentData()]),32):
			getattr(parent, f'inputPB_{i}').setEnabled(False)
			getattr(parent, f'inputInvertCB_{i}').setEnabled(False)
		for i in range(32):
			getattr(parent, f'inputDebounceCB_{i}').setEnabled(False)
		for i in range(int(outputs[parent.sender().currentData()])):
			getattr(parent, f'outputPB_{i}').setEnabled(True)
		for i in range(int(outputs[parent.sender().currentData()]),16):
			getattr(parent, f'outputPB_{i}').setEnabled(False)

	else:
		if parent.boardCB.currentData() in MAIN_BOARDS:
			if not parent.sender().currentData():
				parent.daughterCB_0.setEnabled(True)
				parent.daughterCB_1.setEnabled(True)
				parent.mainTabs.setTabEnabled(3, False)
				parent.mainTabs.setTabEnabled(4, False)
				return


