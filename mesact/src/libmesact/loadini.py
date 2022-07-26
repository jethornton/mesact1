import os, configparser
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton)

from libmesact import loadss

config = configparser.ConfigParser(strict=False)
config.optionxform = str

def openini(parent, configName = ''):
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
			msg = f'Create and Save the Default File\n{iniFile}'
			parent.errorMsgOk(msg, 'Not Found')
			return
	if iniFile:
		with open(iniFile) as f:
			contents = f.read()
			if 'PNCconf' in contents:
				parent.errorMsgOk('Can not open a PNCconf ini file!', 'Incompatable File')
				return
		parent.machinePTE.appendPlainText(f'Loading {iniFile[0]}')
	else:
		parent.machinePTE.appendPlainText('Open File Cancled')
		iniFile = ''
	if config.read(iniFile):
		if config.has_option('MESA', 'VERSION'):
			iniVersion = config['MESA']['VERSION']
			if iniVersion == parent.version:
				loadini(parent, iniFile, config)
			else:
				msg = (f'The ini file version is {iniVersion}\n'
					f'The Configuration Tool version is {parent.version}\n'
					'Try and open the ini?')
				if parent.errorMsg(msg, 'Version Difference'):
					loadini(parent, iniFile, config)
		else:
			msg = ('This ini was not created with the\n'
				'Mesa Configuration Tool!')
			parent.errorMsgOk(msg, 'Incompatable File')

def loadini(parent, iniFile, config):
	# Section, Item, Object Name
	iniList = []
	iniList.append(['MESA', 'BOARD', 'boardCB'])
	iniList.append(['MESA', 'FIRMWARE', 'firmwareCB'])
	iniList.append(['MESA', 'CARD_0', 'daughterCB_0'])
	iniList.append(['MESA', 'CARD_1', 'daughterCB_1'])

	iniList.append(['EMC', 'MACHINE', 'configName'])

	iniList.append(['EMC', 'DEBUG', 'debugCB'])

	iniList.append(['HM2', 'IPADDRESS', 'ipAddressCB'])
	iniList.append(['HM2', 'STEPGENS', 'stepgensCB'])
	iniList.append(['HM2', 'PWMGENS', 'pwmgensCB'])
	iniList.append(['HM2', 'ENCODERS', 'encodersCB'])

	iniList.append(['DISPLAY', 'DISPLAY', 'guiCB'])
	iniList.append(['DISPLAY', 'EDITOR', 'editorCB'])
	iniList.append(['DISPLAY', 'POSITION_OFFSET', 'positionOffsetCB'])
	iniList.append(['DISPLAY', 'POSITION_FEEDBACK', 'positionFeedbackCB'])
	iniList.append(['DISPLAY', 'MAX_FEED_OVERRIDE', 'maxFeedOverrideSB'])
	iniList.append(['DISPLAY', 'MIN_VELOCITY', 'minLinJogVelDSB'])
	iniList.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', 'defLinJogVelDSB'])
	iniList.append(['DISPLAY', 'MAX_LINEAR_VELOCITY', 'maxLinJogVelDSB'])
	iniList.append(['DISPLAY', 'MIN_ANGULAR_VELOCITY', 'minAngJogVelDSB'])
	iniList.append(['DISPLAY', 'DEFAULT_ANGULAR_VELOCITY', 'defAngJogVelDSB'])
	iniList.append(['DISPLAY', 'MAX_ANGULAR_VELOCITY', 'maxAngJogVelDSB'])

	iniList.append(['EMCMOT', 'SERVO_PERIOD', 'servoPeriodSB'])

	iniList.append(['TRAJ', 'LINEAR_UNITS', 'linearUnitsCB'])
	iniList.append(['TRAJ', 'COORDINATES', 'coordinatesLB'])
	iniList.append(['TRAJ', 'MAX_LINEAR_VELOCITY', 'trajMaxLinVelDSB'])

	card = 'c0'
	for i in range(6):
			iniList.append([f'JOINT_{i}', 'AXIS', f'{card}_axisCB_{i}'])
			iniList.append([f'JOINT_{i}', 'DRIVE', f'{card}_driveCB_{i}'])
			iniList.append([f'JOINT_{i}', 'STEP_INVERT', f'{card}_StepInvert_{i}'])
			iniList.append([f'JOINT_{i}', 'DIR_INVERT', f'{card}_DirInvert_{i}'])
			iniList.append([f'JOINT_{i}', 'STEPLEN', f'{card}_StepTime_{i}'])
			iniList.append([f'JOINT_{i}', 'STEPSPACE', f'{card}_StepSpace_{i}'])
			iniList.append([f'JOINT_{i}', 'DIRSETUP', f'{card}_DirSetup_{i}'])
			iniList.append([f'JOINT_{i}', 'DIRHOLD', f'{card}_DirHold_{i}'])
			iniList.append([f'JOINT_{i}', 'MIN_LIMIT', f'{card}_minLimit_{i}'])
			iniList.append([f'JOINT_{i}', 'MAX_LIMIT', f'{card}_maxLimit_{i}'])
			iniList.append([f'JOINT_{i}', 'MAX_VELOCITY', f'{card}_maxVelocity_{i}'])
			iniList.append([f'JOINT_{i}', 'MAX_ACCELERATION', f'{card}_maxAccel_{i}'])
			iniList.append([f'JOINT_{i}', 'SCALE', f'{card}_scale_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME', f'{card}_home_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_OFFSET', f'{card}_homeOffset_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_SEARCH_VEL', f'{card}_homeSearchVel_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_LATCH_VEL', f'{card}_homeLatchVel_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_FINAL_VEL', f'{card}_homeFinalVelocity_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_USE_INDEX', f'{card}_homeUseIndex_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_IGNORE_LIMITS', f'{card}_homeIgnoreLimits_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_IS_SHARED', f'{card}_homeSwitchShared_{i}'])
			iniList.append([f'JOINT_{i}', 'HOME_SEQUENCE', f'{card}_homeSequence_{i}'])
			iniList.append([f'JOINT_{i}', 'P', f'{card}_p_{i}'])
			iniList.append([f'JOINT_{i}', 'I', f'{card}_i_{i}'])
			iniList.append([f'JOINT_{i}', 'D', f'{card}_d_{i}'])
			iniList.append([f'JOINT_{i}', 'FF0', f'{card}_ff0_{i}'])
			iniList.append([f'JOINT_{i}', 'FF1', f'{card}_ff1_{i}'])
			iniList.append([f'JOINT_{i}', 'FF2', f'{card}_ff2_{i}'])
			iniList.append([f'JOINT_{i}', 'DEADBAND', f'{card}_deadband_{i}'])
			iniList.append([f'JOINT_{i}', 'BIAS', f'{card}_bias_{i}'])
			iniList.append([f'JOINT_{i}', 'MAX_OUTPUT', f'{card}_maxOutput_{i}'])
			iniList.append([f'JOINT_{i}', 'MAX_ERROR', f'{card}_maxError_{i}'])
			iniList.append([f'JOINT_{i}', 'FERROR', f'{card}_ferror_{i}'])
			iniList.append([f'JOINT_{i}', 'MIN_FERROR', f'{card}_min_ferror_{i}'])

			iniList.append([f'JOINT_{i}', 'ENCODER_SCALE', f'{card}_encoderScale_{i}'])
			iniList.append([f'JOINT_{i}', 'ANALOG_SCALE_MAX', f'{card}_analogScaleMax_{i}'])
			iniList.append([f'JOINT_{i}', 'ANALOG_MIN_LIMIT', f'{card}_analogMinLimit_{i}'])
			iniList.append([f'JOINT_{i}', 'ANALOG_MAX_LIMIT', f'{card}_analogMaxLimit_{i}'])

	iniList.append(['SPINDLE', 'SPINDLE_TYPE', 'spindleTypeCB'])
	iniList.append(['SPINDLE', 'ENCODER_SCALE', 'spindleEncoderScale'])
	iniList.append(['SPINDLE', 'SCALE', 'spindleStepScale'])
	iniList.append(['SPINDLE', 'SPINDLE_PWM_TYPE', 'spindlePwmTypeCB'])
	iniList.append(['SPINDLE', 'PWM_FREQUENCY', 'pwmFrequencySB'])
	iniList.append(['SPINDLE', 'MAX_RPM', 'spindleMaxRpm'])
	iniList.append(['SPINDLE', 'MIN_RPM', 'spindleMinRpm'])
	iniList.append(['SPINDLE', 'DEADBAND', 'deadband_s'])
	iniList.append(['SPINDLE', 'FEEDBACK', 'spindleFeedbackCB'])
	iniList.append(['SPINDLE', 'P', 'p_s'])
	iniList.append(['SPINDLE', 'I', 'i_s'])
	iniList.append(['SPINDLE', 'D', 'd_s'])
	iniList.append(['SPINDLE', 'FF0', 'ff0_s'])
	iniList.append(['SPINDLE', 'FF1', 'ff1_s'])
	iniList.append(['SPINDLE', 'FF2', 'ff2_s'])
	iniList.append(['SPINDLE', 'BIAS', 'bias_s'])
	iniList.append(['SPINDLE', 'MAX_ERROR', 'maxError_s'])
	iniList.append(['SPINDLE', 'MAX_OUTPUT', 'maxOutput_s'])
	iniList.append(['SPINDLE', 'DRIVE', 'spindleDriveCB'])
	iniList.append(['SPINDLE', 'STEPLEN', 'spindleStepTime'])
	iniList.append(['SPINDLE', 'STEPSPACE', 'spindleStepSpace'])
	iniList.append(['SPINDLE', 'DIRSETUP', 'spindleDirSetup'])
	iniList.append(['SPINDLE', 'DIRHOLD', 'spindleDirHold'])
	iniList.append(['SPINDLE', 'STEP_INVERT', 'spindleStepInvert'])
	iniList.append(['SPINDLE', 'DIR_INVERT', 'spindleDirInvert'])
	iniList.append(['SPINDLE', 'MAX_ACCEL_RPM', 'spindleMaxAccel'])

	for i in range(32):
		iniList.append(['INPUTS', f'INPUT_{i}', f'inputPB_{i}'])
		iniList.append(['INPUTS', f'INPUT_INVERT_{i}', f'inputInvertCB_{i}'])
		iniList.append(['INPUTS', f'INPUT_SLOW_{i}', f'inputDebounceCB_{i}'])

	for i in range(16):
		iniList.append(['OUTPUTS', f'OUTPUT_{i}', f'outputPB_{i}'])

	iniList.append(['OPTIONS', 'LOAD_CONFIG', 'loadConfigCB'])
	iniList.append(['OPTIONS', 'INTRO_GRAPHIC', 'introGraphicLE'])
	iniList.append(['OPTIONS', 'INTRO_GRAPHIC_TIME', 'splashScreenSB'])
	iniList.append(['OPTIONS', 'MANUAL_TOOL_CHANGE', 'manualToolChangeCB'])
	iniList.append(['OPTIONS', 'CUSTOM_HAL', 'customhalCB'])
	iniList.append(['OPTIONS', 'POST_GUI_HAL', 'postguiCB'])
	iniList.append(['OPTIONS', 'SHUTDOWN_HAL', 'shutdownCB'])
	iniList.append(['OPTIONS', 'HALUI', 'haluiCB'])
	iniList.append(['OPTIONS', 'PYVCP', 'pyvcpCB'])
	iniList.append(['OPTIONS', 'GLADEVCP', 'gladevcpCB'])
	iniList.append(['OPTIONS', 'LADDER', 'ladderGB'])
	iniList.append(['OPTIONS', 'LADDER_RUNGS', 'ladderRungsSB'])
	iniList.append(['OPTIONS', 'BACKUP', 'backupCB'])

#iniList.append(['', '', ''])
	# iniList section, item, value
	for item in iniList:
		if config.has_option(item[0], item[1]):
			if isinstance(getattr(parent, item[2]), QLabel):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			elif isinstance(getattr(parent, item[2]), QLineEdit):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])
			elif isinstance(getattr(parent, item[2]), QSpinBox):
				getattr(parent, item[2]).setValue(abs(int(config[item[0]][item[1]])))
			elif isinstance(getattr(parent, item[2]), QDoubleSpinBox):
				if config[item[0]][item[1]]:
					getattr(parent, item[2]).setValue(float(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QCheckBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QGroupBox):
				getattr(parent, item[2]).setChecked(eval(config[item[0]][item[1]]))
			elif isinstance(getattr(parent, item[2]), QComboBox):
				index = getattr(parent, item[2]).findData(config[item[0]][item[1]])
				if item[1] == 'DRIVE':
					index = getattr(parent, item[2]).findText(config[item[0]][item[1]])
					if index >= 0:
						getattr(parent, item[2]).setCurrentIndex(index)
					if index == -1:
						getattr(parent, item[2]).setItemText(0, config[item[0]][item[1]])
				if item[1] == 'FIRMWARE':
					index = getattr(parent, item[2]).findText(config[item[0]][item[1]])
				if item[1] == 'DISPLAY': # Allow custom GUIs we don't have an option to pick (Ex: probe_basic)
					if index == -1:
						getattr(parent, item[2]).addItem(config[item[0]][item[1]], config[item[0]][item[1]])
						index = getattr(parent, item[2]).count()-1
				if index >= 0:
					getattr(parent, item[2]).setCurrentIndex(index)
			elif isinstance(getattr(parent, item[2]), QPushButton):
				getattr(parent, item[2]).setText(config[item[0]][item[1]])

	parent.machinePTE.appendPlainText(f'{iniFile} Loaded')

	if config.has_section('SSERIAL'):
		card = config.get('SSERIAL', 'SS_CARD')
		index = parent.ssCardCB.findText(card)
		if index > 0:
			parent.ssCardCB.setCurrentIndex(index)
		loadss.load(parent, config)
	parent.machinePTE.appendPlainText('Smart Serial file Loaded')

def loadReadMe(parent, configName):
	configsDir = os.path.expanduser('~/linuxcnc/configs')
	readmeFile = os.path.join(configsDir, configName, 'README')
	if os.path.isfile(readmeFile):
		with open(readmeFile) as f:
			contents = f.read()
		parent.readmePTE.appendPlainText(contents)

