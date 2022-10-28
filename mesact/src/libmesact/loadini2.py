import os
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton, QRadioButton)

class openini:
	def __init__(self):
		super().__init__()
		self.sections = {}
		self.iniFile = ''

	def getini(self, parent, configName = ''):
		parent.mainTabs.setCurrentIndex(0)
		parent.machinePTE.clear()
		if not configName: # open file dialog
			if os.path.isdir(os.path.expanduser('~/linuxcnc/configs')):
				configsDir = os.path.expanduser('~/linuxcnc/configs')
			else:
				configsDir = os.path.expanduser('~/')
			fileName = QFileDialog.getOpenFileName(parent,
			caption="Select Configuration INI File", directory=configsDir,
			filter='*.ini', options=QFileDialog.DontUseNativeDialog,)
			iniFile = fileName[0]
			base = os.path.basename(iniFile)
			configName = os.path.splitext(base)[0]
		else: # we passed a file name
			configName = configName.replace(' ','_').lower()
			configsDir = os.path.expanduser('~/linuxcnc/configs')
			iniFile = os.path.join(configsDir, configName, configName + '.ini')
			if not os.path.isfile(iniFile):
				msg = f'File {iniFile} not found'
				parent.errorMsgOk(msg, 'Not Found')
				return
		if iniFile:
			with open(iniFile) as f:
				contents = f.read()
				if 'PNCconf' in contents:
					parent.errorMsgOk('Can not open a PNCconf ini file!', 'Incompatable File')
					return
			parent.machinePTE.appendPlainText(f'Loading {iniFile}')
		else:
			parent.machinePTE.appendPlainText('Open File Cancled')
			iniFile = ''
		'''
		if config.read(iniFile):
			if config.has_option('MESA', 'VERSION'):
				iniVersion = config['MESA']['VERSION']
				if iniVersion == parent.version:
					loadini(parent, iniFile, config)
					loadReadMe(parent, configsDir, configName)
				else:
					msg = (f'The ini file version is {iniVersion}\n'
						f'The Configuration Tool version is {parent.version}\n'
						'Try and open the ini?')
					if parent.errorMsg(msg, 'Version Difference'):
						loadini(parent, iniFile, config)
						loadReadMe(parent, configsDir, configName)
			else:
				msg = ('This ini was not created with the\n'
					'Mesa Configuration Tool!')
				parent.errorMsgOk(msg, 'Incompatable File')
		'''
		self.loadini(parent, iniFile)

	def loadini(self, parent, iniFile):
		booleanDict = {'true': True, 'yes': True, '1': True,
			'false': False, 'no': False, '0': False,}
		self.iniFile = iniFile
		iniDict = {}
		with open(self.iniFile,'r') as file:
			self.content = file.readlines() # create a list of the ini file
		self.get_sections()
		start = self.sections['[MESA]'][0]
		end = self.sections['[MESA]'][1]

		iniDict['[MESA]'] = {}
		iniDict['[MESA]']['VERSION'] = None
		iniDict['[MESA]']['BOARD'] = 'boardCB'
		iniDict['[MESA]']['FIRMWARE'] = 'firmwareCB'
		iniDict['[MESA]']['CARD_0'] = 'daughterCB_0'
		iniDict['[MESA]']['CARD_1'] = 'daughterCB_1'

		iniDict['[EMC]'] = {}
		iniDict['[EMC]']['MACHINE'] = 'configName'
		iniDict['[EMC]']['DEBUG'] = 'debugCB'

		iniDict['[HM2]'] = {}
		iniDict['[HM2]']['IPADDRESS'] = 'ipAddressCB'
		iniDict['[HM2]']['STEPGENS'] = 'stepgensCB'
		iniDict['[HM2]']['PWMGENS'] = 'pwmgensCB'
		iniDict['[HM2]']['ENCODERS'] = 'encodersCB'

		iniDict['[DISPLAY]'] = {}
		iniDict['[DISPLAY]']['DISPLAY'] = 'guiCB'
		iniDict['[DISPLAY]']['EDITOR'] = 'editorCB'
		iniDict['[DISPLAY]']['POSITION_OFFSET'] = 'positionOffsetCB'
		iniDict['[DISPLAY]']['POSITION_FEEDBACK'] = 'positionFeedbackCB'
		iniDict['[DISPLAY]']['MAX_FEED_OVERRIDE'] = 'maxFeedOverrideSB'
		iniDict['[DISPLAY]']['MIN_VELOCITY'] = 'minLinJogVelDSB'
		iniDict['[DISPLAY]']['DEFAULT_LINEAR_VELOCITY'] = 'defLinJogVelDSB'
		iniDict['[DISPLAY]']['MAX_LINEAR_VELOCITY'] = 'maxLinJogVelDSB'
		iniDict['[DISPLAY]']['MIN_ANGULAR_VELOCITY'] = 'minAngJogVelDSB'
		iniDict['[DISPLAY]']['DEFAULT_ANGULAR_VELOCITY'] = 'defAngJogVelDSB'
		iniDict['[DISPLAY]']['MAX_ANGULAR_VELOCITY'] = 'maxAngJogVelDSB'
		iniDict['[DISPLAY]']['LATHE'] = 'frontToolLatheRB'
		iniDict['[DISPLAY]']['BACK_TOOL_LATHE'] = 'backToolLatheRB'
		iniDict['[DISPLAY]']['FOAM'] = 'foamRB'

		'''
		iniDict['[FILTER]'] = {}
		iniDict['[FILTER]']['PROGRAM_EXTENSION'] = 'programFilterLE_0'
		iniDict['[FILTER]']['PROGRAM_EXTENSION'] = 'programFilterLE_1'
		'''



		noUpdate = ['None', 'False', 'Select']

		#for key, value in iniDict.items():
		#	print(key, value)
		section = ''
		for line in self.content:
			if line.startswith('['):
				section = line.strip()
			elif section in iniDict and line != '\n':
				i, v = line.split('=')
				item = i.strip()
				value = v.strip()
				#print(section,item,value)
				if item in iniDict[section]:
					obj = iniDict[section][item]
				else:
					obj = False
				#print(section, item, obj, value)
				if obj and value not in noUpdate:
					if isinstance(getattr(parent, obj), QComboBox):
						#index = getattr(parent, item[2]).findData(config[item[0]][item[1]])
						if getattr(parent, obj).findData(value) >= 0:
							index = getattr(parent, obj).findData(value)
						elif getattr(parent, obj).findText(value) >= 0:
							index = getattr(parent, obj).findText(value)
						if index >= 0:
							#print(obj, value)
							getattr(parent, obj).setCurrentIndex(index)
					elif isinstance(getattr(parent, obj), QLabel):
						getattr(parent, obj).setText(value)
					elif isinstance(getattr(parent, obj), QLineEdit):
						getattr(parent, obj).setText(value)
					elif isinstance(getattr(parent, obj), QSpinBox):
						getattr(parent, obj).setValue(abs(int(value)))
					elif isinstance(getattr(parent, obj), QDoubleSpinBox):
						getattr(parent, obj).setValue(float(value))
					elif isinstance(getattr(parent, obj), QCheckBox):
						getattr(parent, obj).setChecked(booleanDict[value.lower()])
					elif isinstance(getattr(parent, obj), QRadioButton):
						getattr(parent, obj).setChecked(booleanDict[value.lower()])
					elif isinstance(getattr(parent, obj), QGroupBox):
						getattr(parent, obj).setChecked(booleanDict[value.lower()])


		'''
		section = 'MESA'
		print(iniDict)
		for i in range(start +1 , end):
			key, value = self.content[i].split('=')
			#print(key.strip(), value.strip())
			item = iniDict[section][key.strip()]
			print(item, value.strip())
		'''

	def get_sections(self):
		self.sections = {}
		end = len(self.content)
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index, end]

		# set start and stop index for each section
		previous = ''
		for key, value in self.sections.items():
			#print(key)
			if previous:
				self.sections[previous][1] = value[0] - 1
			previous = key

