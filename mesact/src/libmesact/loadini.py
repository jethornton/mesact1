import os
from configparser import ConfigParser

from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton, QRadioButton)

from libmesact import utilities

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
					msg = (f'The ini file is created with PNCconf!\n'
						'Save a Backup and try and open the ini?')
					if parent.errorMsg(msg, 'PNCconf File'):
						path, filename = os.path.split(iniFile)
						utilities.backupFiles(parent, path)
						utilities.cleanDir(parent, path)
					else:
						return
				elif 'Mesa' not in contents:
					msg = (f'The ini file was is not created\n'
						'with the Mesa Configuration Tool!\n'
						'Save a Backup and try and open the ini?')
					if parent.errorMsg(msg, 'Unknown File'):
						path, filename = os.path.split(iniFile)
						utilities.backupFiles(parent, path)
						utilities.cleanDir(parent, path)
					else:
						return

			parent.machinePTE.appendPlainText(f'Loading {iniFile}')
			self.loadini(parent, iniFile)
			self.loadReadMe(parent, configName)
		else:
			parent.machinePTE.appendPlainText('Open File Cancled')
			iniFile = ''

	def loadini(self, parent, iniFile):
		parent.loading = True
		iniDict = {}
		with open(iniFile,'r') as file:
			self.content = file.readlines() # create a list of the ini file
		self.get_sections()
		if '[MESA]' in self.sections:
			start = self.sections['[MESA]'][0]
			end = self.sections['[MESA]'][1]
			for line in self.content[start:end]:
				if line.startswith('VERSION'):
					key, value = line.split('=')
					iniVersion = value.strip()
					if parent.version != iniVersion:
						msg = (f'The ini file version is {iniVersion}\n'
							f'The Configuration Tool version is {parent.version}\n'
							'Save a Backup and try and open the ini?')
						if parent.errorMsg(msg, 'Version Difference'):
							path, filename = os.path.split(iniFile)
							utilities.backupFiles(parent, path)
						else:
							return

		mesa = [
		['[MESA]', 'NAME', 'boardCB'],
		['[MESA]', 'FIRMWARE', 'firmwareCB'],
		['[MESA]', 'CARD_0', 'daughterCB_0'],
		['[MESA]', 'CARD_1', 'daughterCB_1']
		]
		for item in mesa:
			self.update(parent, item[0], item[1], item[2])

		emc = [
		['[EMC]', 'MACHINE', 'configNameLE'],
		['[EMC]', 'DEBUG', 'debugCB']
		]
		for item in emc:
			self.update(parent, item[0], item[1], item[2])

		hm2 = [
		['[HM2]', 'IPADDRESS', 'ipAddressCB'],
		['[HM2]', 'STEPGENS', 'stepgensCB'],
		['[HM2]', 'PWMGENS', 'pwmgensCB'],
		['[HM2]', 'ENCODERS', 'encodersCB']
		]
		for item in hm2:
			self.update(parent, item[0], item[1], item[2])

		display = [
		['[DISPLAY]', 'DISPLAY', 'guiCB'],
		['[DISPLAY]', 'EDITOR', 'editorCB'],
		['[DISPLAY]', 'POSITION_OFFSET', 'positionOffsetCB'],
		['[DISPLAY]', 'POSITION_FEEDBACK', 'positionFeedbackCB'],
		['[DISPLAY]', 'MAX_FEED_OVERRIDE', 'maxFeedOverrideSB'],
		['[DISPLAY]', 'MIN_VELOCITY', 'minLinJogVelDSB'],
		['[DISPLAY]', 'DEFAULT_LINEAR_VELOCITY', 'defLinJogVelDSB'],
		['[DISPLAY]', 'MAX_LINEAR_VELOCITY', 'maxLinJogVelDSB'],
		['[DISPLAY]', 'MIN_ANGULAR_VELOCITY', 'minAngJogVelDSB'],
		['[DISPLAY]', 'DEFAULT_ANGULAR_VELOCITY', 'defAngJogVelDSB'],
		['[DISPLAY]', 'MAX_ANGULAR_VELOCITY', 'maxAngJogVelDSB'],
		['[DISPLAY]', 'LATHE', 'frontToolLatheRB'],
		['[DISPLAY]', 'BACK_TOOL_LATHE', 'backToolLatheRB'],
		['[DISPLAY]', 'FOAM', 'foamRB'],
		]

		for item in display:
			self.update(parent, item[0], item[1], item[2])

		if '[FILTER]' in self.sections:
			start = self.sections['[FILTER]'][0]
			end = self.sections['[FILTER]'][1]
			for item in self.content[start:end]:
				if 'G code Files' in item:
					extList = []
					for word in item.split():
						if word.startswith('.'):
							extList.append(word.rstrip(','))
					for i, item in enumerate(extList):
						getattr(parent, f'filterExtLE_{i}').setText(item)
					break

		traj = [
		['[TRAJ]', 'LINEAR_UNITS', 'linearUnitsCB'],
		['[TRAJ]', 'MAX_LINEAR_VELOCITY', 'trajMaxLinVelDSB'],
		]

		for item in traj:
			self.update(parent, item[0], item[1], item[2])

		if '[HALUI]' in self.sections:
			start = self.sections['[HALUI]'][0]
			end = self.sections['[HALUI]'][1]
			mdicmd = []
			for item in self.content[start:end]:
				if item != '\n':
					item = item.split('=')
					item = item[1].strip()
					mdicmd.append(item)
			for i, item in enumerate(mdicmd):
					getattr(parent, f'mdiCmdLE_{i}').setText(item)

		for i in range(6):
			joint = [
			[f'[JOINT_{i}]', 'AXIS', f'c0_axisCB_{i}'],
			[f'[JOINT_{i}]', 'DRIVE', f'c0_driveCB_{i}'],
			[f'[JOINT_{i}]', 'STEP_INVERT', f'c0_StepInvert_{i}'],
			[f'[JOINT_{i}]', 'DIR_INVERT', f'c0_DirInvert_{i}'],
			[f'[JOINT_{i}]', 'STEPLEN', f'c0_StepTime_{i}'],
			[f'[JOINT_{i}]', 'STEPSPACE', f'c0_StepSpace_{i}'],
			[f'[JOINT_{i}]', 'DIRSETUP', f'c0_DirSetup_{i}'],
			[f'[JOINT_{i}]', 'DIRHOLD',  f'c0_DirHold_{i}'],
			[f'[JOINT_{i}]', 'MIN_LIMIT', f'c0_minLimit_{i}'],
			[f'[JOINT_{i}]', 'MAX_LIMIT',  f'c0_maxLimit_{i}'],
			[f'[JOINT_{i}]', 'MAX_VELOCITY', f'c0_maxVelocity_{i}'],
			[f'[JOINT_{i}]', 'MAX_ACCELERATION', f'c0_maxAccel_{i}'],
			[f'[JOINT_{i}]', 'SCALE', f'c0_scale_{i}'],
			[f'[JOINT_{i}]', 'HOME', f'c0_home_{i}'],
			[f'[JOINT_{i}]', 'HOME_OFFSET', f'c0_homeOffset_{i}'],
			[f'[JOINT_{i}]', 'HOME_SEARCH_VEL', f'c0_homeSearchVel_{i}'],
			[f'[JOINT_{i}]', 'HOME_LATCH_VEL', f'c0_homeLatchVel_{i}'],
			[f'[JOINT_{i}]', 'HOME_FINAL_VEL', f'c0_homeFinalVelocity_{i}'],
			[f'[JOINT_{i}]', 'HOME_USE_INDEX', f'c0_homeUseIndex_{i}'],
			[f'[JOINT_{i}]', 'HOME_IGNORE_LIMITS', f'c0_homeIgnoreLimits_{i}'],
			[f'[JOINT_{i}]', 'HOME_IS_SHARED', f'c0_homeSwitchShared_{i}'],
			[f'[JOINT_{i}]', 'HOME_SEQUENCE', f'c0_homeSequence_{i}'],
			[f'[JOINT_{i}]', 'P', f'c0_p_{i}'],
			[f'[JOINT_{i}]', 'I', f'c0_i_{i}'],
			[f'[JOINT_{i}]', 'D', f'c0_d_{i}'],
			[f'[JOINT_{i}]', 'FF0', f'c0_ff0_{i}'],
			[f'[JOINT_{i}]', 'FF1', f'c0_ff1_{i}'],
			[f'[JOINT_{i}]', 'FF2', f'c0_ff2_{i}'],
			[f'[JOINT_{i}]', 'DEADBAND', f'c0_deadband_{i}'],
			[f'[JOINT_{i}]', 'BIAS', f'c0_bias_{i}'],
			[f'[JOINT_{i}]', 'MAX_OUTPUT', f'c0_maxOutput_{i}'],
			[f'[JOINT_{i}]', 'MAX_ERROR', f'c0_maxError_{i}'],
			[f'[JOINT_{i}]', 'FERROR', f'c0_ferror_{i}'],
			[f'[JOINT_{i}]', 'MIN_FERROR', f'c0_min_ferror_{i}'],
			[f'[JOINT_{i}]', 'ENCODER_SCALE', f'c0_encoderScale_{i}'],
			[f'[JOINT_{i}]', 'ANALOG_SCALE_MAX', f'c0_analogScaleMax_{i}'],
			[f'[JOINT_{i}]', 'ANALOG_MIN_LIMIT', f'c0_analogMinLimit_{i}'],
			[f'[JOINT_{i}]', 'ANALOG_MAX_LIMIT', f'c0_analogMaxLimit_{i}'],
			]

			for item in joint:
				self.update(parent, item[0], item[1], item[2])

		spindle = [
		['[SPINDLE_0]', 'SPINDLE_TYPE', 'spindleTypeCB'],
		['[SPINDLE_0]', 'ENCODER_SCALE', 'spindleEncoderScale'],
		['[SPINDLE_0]', 'SCALE', 'spindleStepScale'],
		['[SPINDLE_0]', 'SPINDLE_PWM_TYPE', 'spindlePwmTypeCB'],
		['[SPINDLE_0]', 'PWM_FREQUENCY', 'pwmFrequencySB'],
		['[SPINDLE_0]', 'MAX_RPM', 'spindleMaxRpm'],
		['[SPINDLE_0]', 'MIN_RPM', 'spindleMinRpm'],
		['[SPINDLE_0]', 'DEADBAND', 'deadband_s'],
		['[SPINDLE_0]', 'FEEDBACK', 'spindleFeedbackCB'],
		['[SPINDLE_0]', 'P', 'p_s'],
		['[SPINDLE_0]', 'I', 'i_s'],
		['[SPINDLE_0]', 'D', 'd_s'],
		['[SPINDLE_0]', 'FF0', 'ff0_s'],
		['[SPINDLE_0]', 'FF1', 'ff1_s'],
		['[SPINDLE_0]', 'FF2', 'ff2_s'],
		['[SPINDLE_0]', 'BIAS', 'bias_s'],
		['[SPINDLE_0]', 'MAX_ERROR', 'maxError_s'],
		['[SPINDLE_0]', 'MAX_OUTPUT', 'maxOutput_s'],
		['[SPINDLE_0]', 'DRIVE', 'spindleDriveCB'],
		['[SPINDLE_0]', 'STEPLEN', 'spindleStepTime'],
		['[SPINDLE_0]', 'STEPSPACE', 'spindleStepSpace'],
		['[SPINDLE_0]', 'DIRSETUP', 'spindleDirSetup'],
		['[SPINDLE_0]', 'DIRHOLD', 'spindleDirHold'],
		['[SPINDLE_0]', 'STEP_INVERT', 'spindleStepInvert'],
		['[SPINDLE_0]', 'DIR_INVERT', 'spindleDirInvert'],
		['[SPINDLE_0]', 'MAX_ACCEL_RPM', 'spindleMaxAccel'],
		]

		for item in spindle:
			self.update(parent, item[0], item[1], item[2])

		for i in range(32):
			inputs = [
			['[INPUTS]', 'INPUT_{i}', f'inputPB_{i}'],
			['[INPUTS]', 'INPUT_INVERT_{i}', f'inputInvertCB_{i}'],
			['[INPUTS]', 'INPUT_SLOW_{i}', f'inputDebounceCB_{i}'],
			]

			for item in inputs:
				self.update(parent, item[0], item[1], item[2])

		for i in range(16):
			outputs = [
			['[OUTPUTS]', 'OUTPUT_{i}', f'outputPB_{i}'],
			['[INPUTS]', 'OUTPUT_INVERT_{i}', f'outputInvertCB_{i}'],
			]

			for item in outputs:
				self.update(parent, item[0], item[1], item[2])

		options = [
		['[OPTIONS]', 'LOAD_CONFIG', 'loadConfigCB'],
		['[OPTIONS]', 'INTRO_GRAPHIC', 'introGraphicLE'],
		['[OPTIONS]', 'INTRO_GRAPHIC_TIME', 'splashScreenSB'],
		['[OPTIONS]', 'MANUAL_TOOL_CHANGE', 'manualToolChangeCB'],
		['[OPTIONS]', 'CUSTOM_HAL', 'customhalCB'],
		['[OPTIONS]', 'POST_GUI_HAL', 'postguiCB'],
		['[OPTIONS]', 'SHUTDOWN_HAL', 'shutdownCB'],
		['[OPTIONS]', 'HALUI', 'haluiCB'],
		['[OPTIONS]', 'PYVCP', 'pyvcpCB'],
		['[OPTIONS]', 'GLADEVCP', 'gladevcpCB'],
		['[OPTIONS]', 'LADDER', 'ladderGB'],
		['[OPTIONS]', 'BACKUP', 'backupCB'],
		]

		for item in options:
			self.update(parent, item[0], item[1], item[2])

		plc = [
		['[PLC]','LADDER_RUNGS', 'ladderRungsSB'],
		['[PLC]','LADDER_BITS', 'ladderBitsSB'],
		['[PLC]','LADDER_WORDS', 'ladderWordsSB'],
		['[PLC]','LADDER_TIMERS', 'ladderTimersSB'],
		['[PLC]','LADDER_IEC_TIMERS', 'iecTimerSB'],
		['[PLC]','LADDER_MONOSTABLES', 'ladderMonostablesSB'],
		['[PLC]','LADDER_COUNTERS', 'ladderCountersSB'],
		['[PLC]','LADDER_HAL_INPUTS', 'ladderInputsSB'],
		['[PLC]','LADDER_HAL_OUTPUTS', 'ladderOutputsSB'],
		['[PLC]','LADDER_EXPRESSIONS', 'ladderExpresionsSB'],
		['[PLC]','LADDER_SECTIONS', 'ladderSectionsSB'],
		['[PLC]','LADDER_SYMBOLS', 'ladderSymbolsSB'],
		['[PLC]','LADDER_S32_INPUTS', 'ladderS32InputsSB'],
		['[PLC]','LADDER_S32_OUTPUTS', 'ladderS32OuputsSB'],
		['[PLC]','LADDER_FLOAT_INPUTS', 'ladderFloatInputsSB'],
		['[PLC]','LADDER_FLOAT_OUTPUTS', 'ladderFloatOutputsSB'],
		]

		for item in plc:
			self.update(parent, item[0], item[1], item[2])

		if '[SSERIAL]' in self.sections:
			start = self.sections['[SSERIAL]'][0]
			end = self.sections['[SSERIAL]'][1]
			for i, j in enumerate(range(start, end)):
				line = self.content[j].strip()
				if len(line.strip()) > 0 and '=' in line:
					line = self.content[j].split('=')
					key = line[0].strip()
					value = line[1].strip()
					if key == 'SS_CARD':
						self.update(parent, '[SSERIAL]', 'SS_CARD', 'ssCardCB')
					elif key.startswith('ss'):
						if value != 'Select':
							self.update(parent, '[SSERIAL]', key, key)


		return



		noUpdate = ['None', 'False', 'Select']
		section = ''
		for line in self.content:
			if line.startswith('['):
				section = line.strip()
			elif section in iniDict:
				if len(line.strip()) > 0  and not line.strip().startswith('#'):
					i, v = line.split('=')
					item = i.strip()
					value = v.strip()
					if item in iniDict[section]:
						obj = iniDict[section][item]
					else:
						obj = False
					if obj and value not in noUpdate:
						if isinstance(getattr(parent, obj), QComboBox):
							#print(f'item {item} value {value} obj {obj}')
							index = 0
							if getattr(parent, obj).findData(value) >= 0:
								index = getattr(parent, obj).findData(value)
							elif getattr(parent, obj).findText(value) >= 0:
								index = getattr(parent, obj).findText(value)
							#print(f'{obj} {index}')
							if index >= 0:
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
						elif isinstance(getattr(parent, obj), QPushButton):
							getattr(parent, obj).setText(value)

		# update the mesact.conf file
		configPath = os.path.expanduser('~/.config/measct/mesact.conf')
		config = ConfigParser()
		config.optionxform = str
		config.read(configPath)
		if config.has_option('NAGS', 'NEWUSER'):
			if parent.newUserCB.isChecked():
				config['NAGS']['NEWUSER'] = 'True'
		if config.has_option('STARTUP', 'CONFIG'):
			if parent.loadConfigCB.isChecked():
				config['STARTUP']['CONFIG'] = parent.configNameLE.text().lower()
		if config.has_option('TOOLS', 'FIRMWARE'):
			if parent.enableMesaflashCB.isChecked():
				config['TOOLS']['FIRMWARE'] = 'True'
		with open(configPath, 'w') as cf:
			config.write(cf)

		parent.loading = False

	def update(self, parent, section, key, obj):
		booleanDict = {'true': True, 'yes': True, '1': True,
			'false': False, 'no': False, '0': False,}
		if section in self.sections:
			start = self.sections[section][0]
			end = self.sections[section][1]
			for item in self.content[start:end]:
				if item.strip().startswith(key):
					value = item.split('=')[1].strip()
					if isinstance(getattr(parent, obj), QComboBox):
						index = 0
						if getattr(parent, obj).findData(value) >= 0:
							index = getattr(parent, obj).findData(value)
						elif getattr(parent, obj).findText(value) >= 0:
							index = getattr(parent, obj).findText(value)
						if index >= 0:
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
					elif isinstance(getattr(parent, obj), QPushButton):
						getattr(parent, obj).setText(value)




	def get_sections(self):
		self.sections = {}
		end = len(self.content)
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index + 1, end]

		# set start and stop index for each section
		previous = ''
		for key, value in self.sections.items():
			if previous:
				self.sections[previous][1] = value[0] - 2
			previous = key

	def loadReadMe(self, parent, configName):
		configsDir = os.path.expanduser('~/linuxcnc/configs')
		readmeFile = os.path.join(configsDir, configName, 'README')
		if os.path.isfile(readmeFile):
			with open(readmeFile) as f:
				contents = f.read()
			parent.readmePTE.appendPlainText(contents)

