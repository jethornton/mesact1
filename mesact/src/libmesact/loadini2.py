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
		#start = self.sections['[MESA]'][0]
		#end = self.sections['[MESA]'][1]

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
		# build the [KINS] section
		# build the [EMCIO] section
		# build the [RS274NGC] section
		# build the [EMCMOT] section
		# build the [TASK] section
		'''

		# load the [TRAJ] section
		iniDict['[TRAJ]'] = {}
		iniDict['[TRAJ]']['LINEAR_UNITS'] = 'linearUnitsCB'
		iniDict['[TRAJ]']['MAX_LINEAR_VELOCITY'] = 'trajMaxLinVelDSB'


		# load the [HAL] section

		# load the [HALUI] section
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

		# load the [JOINT] sections
		for i in range(6):
			iniDict[f'[JOINT_{i}]'] = {}
			iniDict[f'[JOINT_{i}]']['AXIS'] = f'c0_axisCB_{i}'
			iniDict[f'[JOINT_{i}]']['DRIVE'] = f'c0_driveCB_{i}'
			iniDict[f'[JOINT_{i}]']['STEP_INVERT'] = f'c0_StepInvert_{i}'
			iniDict[f'[JOINT_{i}]']['DIR_INVERT'] = f'c0_DirInvert_{i}'
			iniDict[f'[JOINT_{i}]']['STEPLEN'] = f'c0_StepTime_{i}'
			iniDict[f'[JOINT_{i}]']['STEPSPACE'] = f'c0_StepSpace_{i}'
			iniDict[f'[JOINT_{i}]']['DIRSETUP'] = f'c0_DirSetup_{i}'
			iniDict[f'[JOINT_{i}]']['DIRHOLD'] = f'c0_DirHold_{i}'
			iniDict[f'[JOINT_{i}]']['MIN_LIMIT'] = f'c0_minLimit_{i}'
			iniDict[f'[JOINT_{i}]']['MAX_LIMIT'] = f'c0_maxLimit_{i}'
			iniDict[f'[JOINT_{i}]']['MAX_VELOCITY'] = f'c0_maxVelocity_{i}'
			iniDict[f'[JOINT_{i}]']['MAX_ACCELERATION'] = f'c0_maxAccel_{i}'
			iniDict[f'[JOINT_{i}]']['SCALE'] = f'c0_scale_{i}'
			iniDict[f'[JOINT_{i}]']['HOME'] = f'c0_home_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_OFFSET'] = f'c0_homeOffset_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_SEARCH_VEL'] = f'c0_homeSearchVel_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_LATCH_VEL'] = f'c0_homeLatchVel_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_FINAL_VEL'] = f'c0_homeFinalVelocity_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_USE_INDEX'] = f'c0_homeUseIndex_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_IGNORE_LIMITS'] = f'c0_homeIgnoreLimits_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_IS_SHARED'] = f'c0_homeSwitchShared_{i}'
			iniDict[f'[JOINT_{i}]']['HOME_SEQUENCE'] = f'c0_homeSequence_{i}'
			iniDict[f'[JOINT_{i}]']['P'] = f'c0_p_{i}'
			iniDict[f'[JOINT_{i}]']['I'] = f'c0_i_{i}'
			iniDict[f'[JOINT_{i}]']['D'] = f'c0_d_{i}'
			iniDict[f'[JOINT_{i}]']['FF0'] = f'c0_ff0_{i}'
			iniDict[f'[JOINT_{i}]']['FF1'] = f'c0_ff1_{i}'
			iniDict[f'[JOINT_{i}]']['FF2'] = f'c0_ff2_{i}'
			iniDict[f'[JOINT_{i}]']['DEADBAND'] = f'c0_deadband_{i}'
			iniDict[f'[JOINT_{i}]']['BIAS'] = f'c0_bias_{i}'
			iniDict[f'[JOINT_{i}]']['MAX_OUTPUT'] = f'c0_maxOutput_{i}'
			iniDict[f'[JOINT_{i}]']['MAX_ERROR'] = f'c0_maxError_{i}'
			iniDict[f'[JOINT_{i}]']['FERROR'] = f'c0_ferror_{i}'
			iniDict[f'[JOINT_{i}]']['MIN_FERROR'] = f'c0_min_ferror_{i}'
			iniDict[f'[JOINT_{i}]']['ENCODER_SCALE'] = f'c0_encoderScale_{i}'
			iniDict[f'[JOINT_{i}]']['ANALOG_SCALE_MAX'] = f'c0_analogScaleMax_{i}'
			iniDict[f'[JOINT_{i}]']['ANALOG_MIN_LIMIT'] = f'c0_analogMinLimit_{i}'
			iniDict[f'[JOINT_{i}]']['ANALOG_MAX_LIMIT'] = f'c0_analogMaxLimit_{i}'

		# load the [SPINDLE_0] section
		iniDict['[SPINDLE_0]'] = {}
		iniDict['[SPINDLE_0]']['SPINDLE_TYPE'] = 'spindleTypeCB'
		iniDict['[SPINDLE_0]']['ENCODER_SCALE'] = 'spindleEncoderScale'
		iniDict['[SPINDLE_0]']['SCALE'] = 'spindleStepScale'
		iniDict['[SPINDLE_0]']['SPINDLE_PWM_TYPE'] = 'spindlePwmTypeCB'
		iniDict['[SPINDLE_0]']['PWM_FREQUENCY'] = 'pwmFrequencySB'
		iniDict['[SPINDLE_0]']['MAX_RPM'] = 'spindleMaxRpm'
		iniDict['[SPINDLE_0]']['MIN_RPM'] = 'spindleMinRpm'
		iniDict['[SPINDLE_0]']['DEADBAND'] = 'deadband_s'
		iniDict['[SPINDLE_0]']['FEEDBACK'] = 'spindleFeedbackCB'
		iniDict['[SPINDLE_0]']['P'] = 'p_s'
		iniDict['[SPINDLE_0]']['I'] = 'i_s'
		iniDict['[SPINDLE_0]']['D'] = 'd_s'
		iniDict['[SPINDLE_0]']['FF0'] = 'ff0_s'
		iniDict['[SPINDLE_0]']['FF1'] = 'ff1_s'
		iniDict['[SPINDLE_0]']['FF2'] = 'ff2_s'
		iniDict['[SPINDLE_0]']['BIAS'] = 'bias_s'
		iniDict['[SPINDLE_0]']['MAX_ERROR'] = 'maxError_s'
		iniDict['[SPINDLE_0]']['MAX_OUTPUT'] = 'maxOutput_s'
		iniDict['[SPINDLE_0]']['DRIVE'] = 'spindleDriveCB'
		iniDict['[SPINDLE_0]']['STEPLEN'] = 'spindleStepTime'
		iniDict['[SPINDLE_0]']['STEPSPACE'] = 'spindleStepSpace'
		iniDict['[SPINDLE_0]']['DIRSETUP'] = 'spindleDirSetup'
		iniDict['[SPINDLE_0]']['DIRHOLD'] = 'spindleDirHold'
		iniDict['[SPINDLE_0]']['STEP_INVERT'] = 'spindleStepInvert'
		iniDict['[SPINDLE_0]']['DIR_INVERT'] = 'spindleDirInvert'
		iniDict['[SPINDLE_0]']['MAX_ACCEL_RPM'] = 'spindleMaxAccel'

		# load the [INPUTS] section
		iniDict['[INPUTS]'] = {}
		for i in range(32):
			iniDict['[INPUTS]'][f'INPUT_{i}'] = f'inputPB_{i}'
			iniDict['[INPUTS]'][f'INPUT_INVERT_{i}'] = f'inputInvertCB_{i}'
			iniDict['[INPUTS]'][f'INPUT_SLOW_{i}'] = f'inputDebounceCB_{i}'

		# load the [OUTPUTS] section
		iniDict['[OUTPUTS]'] = {}
		for i in range(16):
			iniDict['[OUTPUTS]'][f'OUTPUT_{i}'] = f'outputPB_{i}'
			iniDict['[OUTPUTS]'][f'OUTPUT_INVERT_{i}'] = f'outputInvertCB_{i}'

		# load the [OPTIONS] section
		iniDict['[OPTIONS]'] = {}
		iniDict['[OPTIONS]']['LOAD_CONFIG'] = 'loadConfigCB'
		iniDict['[OPTIONS]']['INTRO_GRAPHIC'] = 'introGraphicLE'
		iniDict['[OPTIONS]']['INTRO_GRAPHIC_TIME'] = 'splashScreenSB'
		iniDict['[OPTIONS]']['MANUAL_TOOL_CHANGE'] = 'manualToolChangeCB'
		iniDict['[OPTIONS]']['CUSTOM_HAL'] = 'customhalCB'
		iniDict['[OPTIONS]']['POST_GUI_HAL'] = 'postguiCB'
		iniDict['[OPTIONS]']['SHUTDOWN_HAL'] = 'shutdownCB'
		iniDict['[OPTIONS]']['HALUI'] = 'haluiCB'
		iniDict['[OPTIONS]']['PYVCP'] = 'pyvcpCB'
		iniDict['[OPTIONS]']['GLADEVCP'] = 'gladevcpCB'
		iniDict['[OPTIONS]']['LADDER'] = 'ladderGB'
		#iniDict['[OPTIONS]']['LADDER_RUNGS'] = 'ladderRungsSB'
		iniDict['[OPTIONS]']['BACKUP'] = 'backupCB'






		noUpdate = ['None', 'False', 'Select']

		section = ''
		for line in self.content:
			if line.startswith('['):
				section = line.strip()
			elif section in iniDict:
				if len(line.strip()) > 0  and not line.startswith('#'):
					i, v = line.split('=')
					item = i.strip()
					value = v.strip()
					if item in iniDict[section]:
						obj = iniDict[section][item]
					else:
						obj = False
					if obj and value not in noUpdate:
						if isinstance(getattr(parent, obj), QComboBox):
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
			#print(key)
			if previous:
				self.sections[previous][1] = value[0] - 2
			previous = key

