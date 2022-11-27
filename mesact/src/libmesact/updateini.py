import os
from datetime import datetime

class updateini:
	def __init__(self):
		super().__init__()
		self.sections = {}
		self.iniFile = ''

	def update(self, parent, iniFile):
		self.iniFile = iniFile
		with open(self.iniFile,'r') as file:
			self.content = file.readlines() # create a list of the ini file
		self.get_sections()
		if self.content[0].startswith('# This file'):
			self.content[0] = ('# This file was updated with the Mesa Configuration'
				f' Tool on {datetime.now().strftime("%b %d %Y %H:%M:%S")}\n')

		mesa = [
		['MESA', 'VERSION', f'{parent.version}'],
		['MESA', 'BOARD', f'{parent.boardCB.currentData()}'],
		['MESA', 'FIRMWARE', f'{parent.firmwareCB.currentText()}'],
		['MESA', 'CARD_0', f'{parent.daughterCB_0.currentData()}'],
		['MESA', 'CARD_1', f'{parent.daughterCB_1.currentData()}']
		]
		for item in mesa:
			self.update_key(item[0], item[1], item[2])

		emc = [
		['EMC', 'VERSION', f'{parent.emcVersion}'],
		['EMC', 'MACHINE', f'{parent.configNameLE.text()}'],
		['EMC', 'DEBUG', f'{parent.debugCB.currentData()}']
		]
		for item in emc:
			self.update_key(item[0], item[1], item[2])

		if parent.boardType == 'eth':
			hm2 = [
			['HM2', 'DRIVER', 'hm2_eth'],
			['HM2', 'IPADDRESS', f'{parent.ipAddressCB.currentText()}']
			]
		else:
			self.delete_key('HM2', 'IPADDRESS')
		if parent.boardType == 'pci':
			hm2 = [['HM2', 'DRIVER', 'hm2_pci']]
		hm2.append(['HM2', 'STEPGENS', f'{parent.stepgensCB.currentData()}'])
		hm2.append(['HM2', 'PWMGENS', f'{parent.pwmgensCB.currentData()}'])
		hm2.append(['HM2', 'ENCODERS', f'{parent.encodersCB.currentData()}'])
		for item in hm2:
			self.update_key(item[0], item[1], item[2])

		display = [
		['DISPLAY', 'DISPLAY', f'{parent.guiCB.itemData(parent.guiCB.currentIndex())}'],
		['DISPLAY', 'PROGRAM_PREFIX', f'{os.path.expanduser("~/linuxcnc/nc_files")}'],
		['DISPLAY', 'POSITION_OFFSET', f'{parent.positionOffsetCB.currentData()}'],
		['DISPLAY', 'POSITION_FEEDBACK', f'{parent.positionFeedbackCB.currentData()}'],
		['DISPLAY', 'MAX_FEED_OVERRIDE', f'{parent.maxFeedOverrideSB.value()}'],
		['DISPLAY', 'CYCLE_TIME', '0.1'],
		['DISPLAY', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['DISPLAY', 'INTRO_TIME', f'{parent.splashScreenSB.value()}'],
		['DISPLAY', 'OPEN_FILE', f'""']
		]
		if parent.editorCB.currentData():
			display.append(['DISPLAY', 'EDITOR', f'{parent.editorCB.currentData()}'])
		else:
			self.delete_key('DISPLAY', 'EDITOR')
		if set('XYZUVW')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_LINEAR_VELOCITY', f'{parent.minLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_LINEAR_VELOCITY', f'{parent.defLinJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_LINEAR_VELOCITY', f'{parent.maxLinJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_LINEAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_LINEAR_VELOCITY')
		if set('ABC')&set(parent.coordinatesLB.text()):
			display.append(['DISPLAY', 'MIN_ANGULAR_VELOCITY', f'{parent.minAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'DEFAULT_ANGULAR_VELOCITY', f'{parent.defAngJogVelDSB.value()}'])
			display.append(['DISPLAY', 'MAX_ANGULAR_VELOCITY', f'{parent.maxAngJogVelDSB.value()}'])
		else:
			self.delete_key('DISPLAY', 'MIN_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'DEFAULT_ANGULAR_VELOCITY')
			self.delete_key('DISPLAY', 'MAX_ANGULAR_VELOCITY')
		if parent.pyvcpCB.isChecked():
			display.append(['DISPLAY', 'PYVCP', f'{parent.configNameUnderscored}.xml'])
		else:
			self.delete_key('DISPLAY', 'PYVCP')
		if parent.frontToolLatheRB.isChecked():
			display.append(['DISPLAY', 'LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'LATHE')
		if parent.frontToolLatheRB.isChecked():
			display.append(['DISPLAY', 'BACK_TOOL_LATHE', '1'])
		else:
			self.delete_key('DISPLAY', 'BACK_TOOL_LATHE')
		if parent.foamRB.isChecked():
			display.append(['DISPLAY', 'FOAM', '1'])
			display.append(['DISPLAY', 'Geometry', f'{parent.coordinatesLB.text()[0:2]};{parent.coordinatesLB.text()[2:4]}'])
		else:
			self.delete_key('DISPLAY', 'FOAM')
			self.delete_key('DISPLAY', 'Geometry')
		for item in display:
			self.update_key(item[0], item[1], item[2])

		# [FILTER]
		if '[FILTER]' in self.sections:
			index = self.sections['[FILTER]']
			for i in range(index[0], index[1]):
				if 'G code Files' in self.content[i]:
					ext_list = []
					for j in range(3):
						ext = getattr(parent, f'filterExtLE_{j}').text()
						if ext:
							if not ext.startswith('.'):
								ext_list.append(f'.{ext}')
							else:
								ext_list.append(ext)
					if ext_list:
						self.content[i] = f'PROGRAM_EXTENSION = {", ".join(ext_list)} # G code Files\n'

		# [KINS]
		if len(set(parent.coordinatesLB.text())) == len(parent.coordinatesLB.text()): # 1 joint for each axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()}']]
		else: # more than one joint per axis
			kins = [['KINS', 'KINEMATICS', f'trivkins coordinates={parent.coordinatesLB.text()} kinstype=BOTH']]
		kins.append(['KINS', 'JOINTS', f'{len(parent.coordinatesLB.text())}'])
		for item in kins:
			self.update_key(item[0], item[1], item[2])

		emcio = [
		['EMCIO', 'EMCIO', 'iov2'],
		['EMCIO', 'CYCLE_TIME', '0.100'],
		['EMCIO', 'TOOL_TABLE', 'tool.tbl']
		]
		for item in emcio:
			self.update_key(item[0], item[1], item[2])

		rs274ngc = [
		['RS274NGC', 'PARAMETER_FILE', f'{parent.configNameUnderscored}.var'],
		['RS274NGC', 'SUBROUTINE_PATH', f'{os.path.expanduser("~/linuxcnc/subroutines")}']
		]

		for item in rs274ngc:
			self.update_key(item[0], item[1], item[2])

		emcmot = [
		['EMCMOT', 'EMCMOT', 'motmod'],
		['EMCMOT', 'COMM_TIMEOUT', '1.0'],
		['EMCMOT', 'SERVO_PERIOD', f'{parent.servoPeriodSB.value()}']
		]

		for item in emcmot:
			self.update_key(item[0], item[1], item[2])

		task = [
		['TASK', 'TASK', 'milltask'],
		['TASK', 'CYCLE_TIME', '0.010']
		]

		for item in task:
			self.update_key(item[0], item[1], item[2])

		traj = [
		['TRAJ', 'COORDINATES', f'{parent.coordinatesLB.text()}'],
		['TRAJ', 'LINEAR_UNITS', f'{parent.linearUnitsCB.currentData()}'],
		['TRAJ', 'ANGULAR_UNITS', 'degree'],
		['TRAJ', 'MAX_LINEAR_VELOCITY', f'{parent.trajMaxLinVelDSB.value()}'],
		]
		if parent.noforcehomingCB.isChecked():
			traj.append(['TRAJ','NO_FORCE_HOMING', '0'])
		else:
			traj.append(['TRAJ','NO_FORCE_HOMING', '1'])

		for item in traj:
			self.update_key(item[0], item[1], item[2])

		# [HAL]
		if parent.haluiCB.isChecked():
			self.update_key('HAL', 'HALUI', 'halui')

		# [HALUI]
		if parent.haluiCB.isChecked() and '[HALUI]' not in self.sections:
			section = '[HALUI]'
			index = self.sections['[HAL]'][1]
			self.insert_section(index, section)

		if '[HALUI]' in self.sections:
			index = self.sections['[HALUI]']
			#print(index)
			if len(index) == 2:
				ini_mdi = []
				for i in range(index[0], index[1]):
					if self.content[i].startswith('MDI_COMMAND'):
						ini_mdi.append(self.content[i].split('=')[1].strip())
				tool_mdi = []
				for i in range(6):
					mdi_text = f'{getattr(parent, f"mdiCmdLE_{i}").text()}'
					if mdi_text:
						tool_mdi.append(f'{getattr(parent, f"mdiCmdLE_{i}").text()}')
				#print(len(tool_mdi))

				if len(ini_mdi) == len(tool_mdi):
					for i, j in enumerate(range(index[0] + 1, index[1])):
						if self.content[j].startswith('MDI_COMMAND'):
							self.content[j] = f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n'
				elif len(ini_mdi) > len(tool_mdi):
					remove = len(ini_mdi) - len(tool_mdi)
					for i in reversed(range(index[0] + 1, index[1])):
						if self.content[i].startswith('MDI_COMMAND') and remove > 0:
							del self.content[i]
							remove -= 1
					self.get_sections() # update section start/end
				elif len(ini_mdi) < len(tool_mdi):
					add = len(tool_mdi) - len(ini_mdi)
					for i, j in enumerate(range(index[0] + 1, index[1] + add)):
						if self.content[j].startswith('MDI_COMMAND'): # replace it
							self.content[j] = f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n'
						elif self.content[j].strip() == '': # insert it
							self.content.insert(j, f'MDI_COMMAND = {getattr(parent, f"mdiCmdLE_{i}").text()}\n')
					self.get_sections() # update section start/end

		# [AXIS_x] section
		if parent.cardTabs.isTabEnabled(0):
			card = 'c0'
		elif parent.cardTabs.isTabEnabled(1):
			card = 'c1'

		# build axis joint(s) dictionaries
		tool_ja = {}
		for i in range(6):
			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				tool_ja[f'[JOINT_{i}]'] = f'[AXIS_{getattr(parent, f"{card}_axisCB_{i}").currentData()}]'

		ini_ja = {}
		for key, value in self.sections.items():
			if key.startswith('[JOINT'):
				for i in range(value[0], value[1]):
					if self.content[i].startswith('AXIS'):
						axis = self.content[i].strip()
						axis = axis.split()
						axis = f'[AXIS_{axis[-1]}]'
						ini_ja[key] = axis

		if len(tool_ja) == len(ini_ja):
			if tool_ja != ini_ja:
				for key in tool_ja.keys():
					if tool_ja[key] != ini_ja[key]:
						index = self.content.index(f'{ini_ja[key]}\n')
						if index:
							self.content[index] = f'{tool_ja[key]}\n'
							self.get_sections() # update section start/end

		elif len(tool_ja) > len(ini_ja):
			for key in ini_ja.keys(): # check for axis letter changed
				if tool_ja[key] != ini_ja[key]:
					index = self.content.index(f'{ini_ja[key]}\n')
					if index:
						self.content[index] = f'{tool_ja[key]}\n'
						self.get_sections() # update section start/end

			ini_axes = []
			for key, value in ini_ja.items(): # get a list of axes
				if value not in ini_axes:
					ini_axes.append(value)

			last_axis = ''
			last_joint = ''
			for key, value in tool_ja.items(): # add missing axis
				if tool_ja[key] not in ini_axes:
					index = self.sections[last_joint][1]
					if index:
						self.insert_section(index, f'{tool_ja[key]}')
				last_joint = key

			for key, value in tool_ja.items(): # add missing joint after last axis
				if key not in ini_ja.keys():
					index = self.sections[value][1]
					self.insert_section(index, f'{key}')

		elif len(tool_ja) < len(ini_ja): # joint removed
			print('Joint Removed')
			for joint, axis in ini_ja.items():
				if joint not in tool_ja:
					self.delete_section(joint)
					self.delete_section(axis)

		# finally update the [AXIS_n] and [JOINT_n] sections
		axes = []
		for i in range(6):
			axis = getattr(parent, f'{card}_axisCB_{i}').currentData()
			if axis and axis not in axes:
				#print(axis)
				axes.append(axis)
				self.update_key(f'AXIS_{axis}', 'MIN_LIMIT', getattr(parent, f'{card}_minLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_LIMIT', getattr(parent, f'{card}_maxLimit_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_VELOCITY', getattr(parent, f'{card}_maxVelocity_{i}').text())
				self.update_key(f'AXIS_{axis}', 'MAX_ACCELERATION', getattr(parent, f'{card}_maxAccel_{i}').text())

			if getattr(parent, f'{card}_axisCB_{i}').currentData():
				self.update_key(f'JOINT_{i}', 'AXIS', getattr(parent, f'{card}_axisCB_{i}').currentData())
				self.update_key(f'JOINT_{i}', 'MIN_LIMIT', getattr(parent, f'{card}_minLimit_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_LIMIT', getattr(parent, f'{card}_maxLimit_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_VELOCITY', getattr(parent, f'{card}_maxVelocity_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_ACCELERATION', getattr(parent, f'{card}_maxAccel_{i}').text())
				self.update_key(f'JOINT_{i}', 'TYPE', getattr(parent, f'{card}_axisType_{i}').text())
				if getattr(parent, f'{card}_reverse_{i}').isChecked():
					self.update_key(f'JOINT_{i}', 'SCALE', f'-{getattr(parent, f"{card}_scale_{i}").text()}')
				else:
					self.update_key(f'JOINT_{i}', 'SCALE', f'{getattr(parent, f"{card}_scale_{i}").text()}')

				if parent.cardType_0 == 'step' or parent.cardType_1 == 'step': # add step and dir invert
					self.update_key(f'JOINT_{i}', 'DRIVE', getattr(parent, f'{card}_driveCB_{i}').currentText())
					self.update_key(f'JOINT_{i}', 'STEP_INVERT', getattr(parent, f'{card}_StepInvert_{i}').isChecked())
					self.update_key(f'JOINT_{i}', 'DIR_INVERT', getattr(parent, f'{card}_DirInvert_{i}').isChecked())
					self.update_key(f'JOINT_{i}', 'STEPGEN_MAX_VEL', f'{float(getattr(parent, f"{card}_maxVelocity_{i}").text()) * 1.2:.2f}')
					self.update_key(f'JOINT_{i}', 'STEPGEN_MAX_ACC', f'{float(getattr(parent, f"{card}_maxAccel_{i}").text()) * 1.2:.2f}')
					self.update_key(f'JOINT_{i}', 'DIRSETUP', getattr(parent, f'{card}_DirSetup_{i}').text())
					self.update_key(f'JOINT_{i}', 'DIRHOLD', getattr(parent, f'{card}_DirHold_{i}').text())
					self.update_key(f'JOINT_{i}', 'STEPLEN', getattr(parent, f'{card}_StepTime_{i}').text())
					self.update_key(f'JOINT_{i}', 'STEPSPACE', getattr(parent, f'{card}_StepSpace_{i}').text())

				if parent.cardType_0 == 'servo' or parent.cardType_1 == 'servo':
					self.update_key(f'JOINT_{i}', 'ENCODER_SCALE', getattr(parent, f'{card}_encoderScale_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_SCALE_MAX', getattr(parent, f'{card}_analogScaleMax_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_MIN_LIMIT', getattr(parent, f'{card}_analogMinLimit_{i}').text())
					self.update_key(f'JOINT_{i}', 'ANALOG_MAX_LIMIT', getattr(parent, f'{card}_analogMaxLimit_{i}').text())

				self.update_key(f'JOINT_{i}', 'FERROR', getattr(parent, f'{card}_ferror_{i}').text())
				self.update_key(f'JOINT_{i}', 'MIN_FERROR', getattr(parent, f'{card}_min_ferror_{i}').text())
				self.update_key(f'JOINT_{i}', 'DEADBAND', getattr(parent, f'{card}_deadband_{i}').text())
				self.update_key(f'JOINT_{i}', 'P', getattr(parent, f'{card}_p_{i}').text())
				self.update_key(f'JOINT_{i}', 'I', getattr(parent, f'{card}_i_{i}').text())
				self.update_key(f'JOINT_{i}', 'D', getattr(parent, f'{card}_d_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF0', getattr(parent, f'{card}_ff0_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF1', getattr(parent, f'{card}_ff1_{i}').text())
				self.update_key(f'JOINT_{i}', 'FF2', getattr(parent, f'{card}_ff2_{i}').text())
				self.update_key(f'JOINT_{i}', 'BIAS', getattr(parent, f'{card}_bias_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_OUTPUT', getattr(parent, f'{card}_maxOutput_{i}').text())
				self.update_key(f'JOINT_{i}', 'MAX_ERROR', getattr(parent, f'{card}_maxError_{i}').text())
				if getattr(parent, f"{card}_home_" + str(i)).text():
					self.update_key(f'JOINT_{i}', 'HOME', getattr(parent, f"{card}_home_{i}").text())
				if getattr(parent, f"{card}_homeOffset_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_OFFSET', getattr(parent, f"{card}_homeOffset_{i}").text())
				if getattr(parent, f"{card}_homeSearchVel_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_SEARCH_VEL', getattr(parent, f"{card}_homeSearchVel_{i}").text())
				if getattr(parent, f"{card}_homeLatchVel_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_LATCH_VEL', getattr(parent, f"{card}_homeLatchVel_{i}").text())
				if getattr(parent, f"{card}_homeFinalVelocity_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_FINAL_VEL', getattr(parent, f"{card}_homeFinalVelocity_{i}").text())
				if getattr(parent, f"{card}_homeSequence_{i}").text():
					self.update_key(f'JOINT_{i}', 'HOME_SEQUENCE', getattr(parent, f"{card}_homeSequence_{i}").text())
				if getattr(parent, f"{card}_homeIgnoreLimits_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_IGNORE_LIMITS', True)
				if getattr(parent, f"{card}_homeUseIndex_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_USE_INDEX', True)
				if getattr(parent, f"{card}_homeSwitchShared_{i}").isChecked():
					self.update_key(f'JOINT_{i}', 'HOME_IS_SHARED', True)

		# update the [SPINDLE_0] section
		if parent.spindleTypeCB.currentData():
			# If SPINDLE_0 section does not exist insert it after the last joint
			if '[SPINDLE_0]' not in self.sections:
				last_joint = None
				for key, value in self.sections.items():
					if key.startswith('[JOINT'):
						last_joint = key
				index = self.sections[last_joint][1]
				self.content.insert(index, '[SPINDLE_0]\n')
				self.content.insert(index, '\n')
				self.get_sections() # update section start/end

			self.update_key(f'SPINDLE_0', 'SPINDLE_TYPE', parent.spindleTypeCB.currentData())

			if parent.spindlePwmTypeCB.currentData():
				self.update_key(f'SPINDLE_0', 'SPINDLE_PWM_TYPE', parent.spindlePwmTypeCB.currentData())

			if parent.spindleTypeCB.currentData() == 'analog':
				self.update_key(f'SPINDLE_0', 'PWM_FREQUENCY', parent.pwmFrequencySB.value())
				self.update_key(f'SPINDLE_0', 'MAX_RPM', parent.spindleMaxRpm.value())
				self.update_key(f'SPINDLE_0', 'MIN_RPM', parent.spindleMinRpm.value())

			if parent.spindleFeedbackCB.currentData() == 'encoder':
				self.update_key(f'SPINDLE_0', 'FEEDBACK', parent.spindleFeedbackCB.currentData())
				self.update_key(f'SPINDLE_0', 'P', parent.p_s.value())
				self.update_key(f'SPINDLE_0', 'I', parent.i_s.value())
				self.update_key(f'SPINDLE_0', 'D', parent.d_s.value())
				self.update_key(f'SPINDLE_0', 'FF0', parent.ff0_s.value())
				self.update_key(f'SPINDLE_0', 'FF1', parent.ff1_s.value())
				self.update_key(f'SPINDLE_0', 'FF2', parent.ff2_s.value())
				self.update_key(f'SPINDLE_0', 'BIAS', parent.bias_s.value())
				self.update_key(f'SPINDLE_0', 'DEADBAND', parent.deadband_s.value())
				self.update_key(f'SPINDLE_0', 'MAX_ERROR', parent.maxError_s.value())
				self.update_key(f'SPINDLE_0', 'MAX_OUTPUT', parent.maxOutput_s.value())
				self.update_key(f'SPINDLE_0', 'OUTPUT_TYPE', parent.maxOutput_s.value())
				self.update_key(f'SPINDLE_0', 'ENCODER_SCALE', parent.spindleEncoderScale.value())

			if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
				self.update_key(f'SPINDLE_0', 'DRIVE', parent.spindleDriveCB.currentText())
				self.update_key(f'SPINDLE_0', 'SCALE', parent.spindleStepScale.text())
				self.update_key(f'SPINDLE_0', 'STEPLEN', parent.spindleStepTime.text())
				self.update_key(f'SPINDLE_0', 'STEPSPACE', parent.spindleStepSpace.text())
				self.update_key(f'SPINDLE_0', 'DIRSETUP', parent.spindleDirSetup.text())
				self.update_key(f'SPINDLE_0', 'DIRHOLD', parent.spindleDirHold.text())
				self.update_key(f'SPINDLE_0', 'STEP_INVERT', parent.spindleStepInvert.isChecked())
				self.update_key(f'SPINDLE_0', 'DIR_INVERT', parent.spindleDirInvert.isChecked())
				self.update_key(f'SPINDLE_0', 'MIN_RPM', parent.spindleMinRpm.value())
				self.update_key(f'SPINDLE_0', 'MAX_RPM', parent.spindleMaxRpm.value())
				self.update_key(f'SPINDLE_0', 'MIN_RPS', parent.spindleMinRps.text())
				self.update_key(f'SPINDLE_0', 'MAX_RPS', parent.spindleMaxRps.text())
				self.update_key(f'SPINDLE_0', 'MAX_ACCEL_RPM', parent.spindleMaxAccel.value())
				self.update_key(f'SPINDLE_0', 'MAX_ACCEL_RPS', parent.spindleMaxRpss.text())

		else: # if SPINDLE_0 is in ini delete it
			if '[SPINDLE_0]' in self.sections:
				self.delete_section('[SPINDLE_0]')

		# update the [INPUTS] section
		for i in range(32):
			self.update_key('INPUTS', f'INPUT_{i}', getattr(parent, "inputPB_" + str(i)).text())
			self.update_key('INPUTS', f'INPUT_INVERT_{i}', getattr(parent, "inputInvertCB_" + str(i)).isChecked())
			self.update_key('INPUTS', f'INPUT_SLOW_{i}', getattr(parent, "inputDebounceCB_" + str(i)).isChecked())

		# update the [OUTPUTS] section
		for i in range(16):
			self.update_key('OUTPUTS', f'OUTPUT_{i}', getattr(parent, "outputPB_" + str(i)).text())
			self.update_key('OUTPUTS', f'OUTPUT_INVERT_{i}', getattr(parent, "outputInvertCB_" + str(i)).isChecked())

		# update the [OPTIONS] section
		options = [
		['OPTIONS', 'LOAD_CONFIG', f'{parent.loadConfigCB.isChecked()}'],
		['OPTIONS', 'INTRO_GRAPHIC', f'{parent.introGraphicLE.text()}'],
		['OPTIONS', 'INTRO_GRAPHIC_TIME', f'{parent.splashScreenSB.value()}'],
		['OPTIONS', 'MANUAL_TOOL_CHANGE', f'{parent.manualToolChangeCB.isChecked()}'],
		['OPTIONS', 'CUSTOM_HAL', f'{parent.customhalCB.isChecked()}'],
		['OPTIONS', 'POST_GUI_HAL', f'{parent.postguiCB.isChecked()}'],
		['OPTIONS', 'SHUTDOWN_HAL', f'{parent.shutdownCB.isChecked()}'],
		['OPTIONS', 'HALUI', f'{parent.haluiCB.isChecked()}'],
		['OPTIONS', 'PYVCP', f'{parent.pyvcpCB.isChecked()}'],
		['OPTIONS', 'GLADEVCP', f'{parent.gladevcpCB.isChecked()}'],
		['OPTIONS', 'LADDER', f'{parent.ladderGB.isChecked()}'],
		['OPTIONS', 'BACKUP', f'{parent.backupCB.isChecked()}']
		]
		for item in options:
			self.update_key(item[0], item[1], item[2])

		# update [PLC] section
		if parent.ladderGB.isChecked(): # check for any options
			# If [PLC] section does not exist insert it after [OPTIONS] section
			if '[PLC]' not in self.sections:
				index = self.sections['[OPTIONS]'][1]
				self.insert_section(index, '[PLC]')

			for option in parent.ladderOptionsList:
				#print('PLC', f'{getattr(parent, option).property("item")}', f'{getattr(parent, option).value()}')
				self.update_key('PLC', f'{getattr(parent, option).property("item")}', f'{getattr(parent, option).value()}')
		else: # remove PLC section if it's in the ini file
			if '[PLC]' in self.sections:
				self.delete_section('[PLC]')

		# update the [SSERIAL] section
		if parent.ssCardCB.currentData():
			if '[SSERIAL]' not in self.sections:
				if '[PLC]'in self.sections:
					index = self.sections['[PLC]'][1]
				else:
					index = self.sections['[OPTIONS]'][1]
				self.insert_section(index, '[SSERIAL]')

			self.update_key(f'SSERIAL', 'SS_CARD', parent.ssCardCB.currentText())

			if parent.ssCardCB.currentText() == '7i64':
				for i in range(24):
					self.update_key(f'SSERIAL', f'ss7i64in_{i}', getattr(parent, f'ss7i64in_{i}').text())
					self.update_key(f'SSERIAL', f'ss7i64out_{i}', getattr(parent, f'ss7i64out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i69':
				for i in range(24):
					self.update_key(f'SSERIAL', f'ss7i69in_{i}', getattr(parent, f'ss7i69in_{i}').text())
					self.update_key(f'SSERIAL', f'ss7i69out_{i}', getattr(parent, f'ss7i69out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i70':
				for i in range(48):
					self.update_key(f'SSERIAL', f'ss7i70in_{i}', getattr(parent, f'ss7i70in_{i}').text())
			elif parent.ssCardCB.currentText() == '7i71':
				for i in range(48):
					self.update_key(f'SSERIAL', f'ss7i71out_{i}', getattr(parent, f'ss7i71out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i72':
				for i in range(48):
					self.update_key(f'SSERIAL', f'ss7i72out_{i}', getattr(parent, f'ss7i72out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i73':
				for i in range(16):
					self.update_key(f'SSERIAL', f'ss7i73key_{i}', getattr(parent, f'ss7i73key_{i}').text())
				for i in range(12):
					self.update_key(f'SSERIAL', f'ss7i73lcd_{i}', getattr(parent, f'ss7i73lcd_{i}').text())
				for i in range(16):
					self.update_key(f'SSERIAL', f'ss7i73in_{i}', getattr(parent, f'ss7i73in_{i}').text())
				for i in range(2):
					self.update_key(f'SSERIAL', f'ss7i73out_{i}', getattr(parent, f'ss7i73out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i84':
				for i in range(32):
					self.update_key(f'SSERIAL', f'ss7i84in_{i}', getattr(parent, f'ss7i84in_{i}').text())
				for i in range(16):
					self.update_key(f'SSERIAL', f'ss7i84out_{i}', getattr(parent, f'ss7i84out_{i}').text())
			elif parent.ssCardCB.currentText() == '7i87':
				for i in range(8):
					self.update_key(f'SSERIAL', f'ss7i87in_{i}', getattr(parent, f'ss7i87in_{i}').text())

		else: # remove the [SSERIAL] section
			if '[SSERIAL]' in self.sections:
				self.delete_section('[SSERIAL]')

		self.write_ini(parent)

	def write_ini(self, parent):
		with open(self.iniFile, 'w') as outfile:
			outfile.write(''.join(self.content))
		parent.machinePTE.appendPlainText(f'Updated {self.iniFile}')

	def get_sections(self):
		self.sections = {}
		end = len(self.content)
		for index, line in enumerate(self.content):
			if line.strip().startswith('['):
				self.sections[line.strip()] = [index, end]

		# set start and stop index for each section
		previous = ''
		for key, value in self.sections.items():
			if previous:
				self.sections[previous][1] = value[0] - 1
			previous = key

	def update_key(self, section, key, value):
		found = False
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		for item in self.content[start:end]:
			if item.split('=')[0].strip() == key:
				index = self.content.index(item)
				self.content[index] = f'{key} = {value}\n'
				found = True
				break
			else:
				found = False
		if not found:
			self.content.insert(end, f'{key} = {value}\n')
			self.get_sections() # update section start/end

	def delete_key(self, section, key):
		start = self.sections[f'[{section}]'][0]
		end = self.sections[f'[{section}]'][1]
		for item in self.content[start:end]:
			if item.startswith(key):
				index = self.content.index(item)
				del self.content[index]
				self.get_sections() # update section start/end

	def replace_section(self, section):
		print(section)

	def insert_section(self, index, section):
		self.content.insert(index, f'{section}\n')
		self.content.insert(index, '\n')
		self.get_sections() # update section start/end

	def delete_section(self, section):
		start = self.sections[section][0]
		end = self.sections[section][1]
		del self.content[start:end]
		self.get_sections() # update section start/end


