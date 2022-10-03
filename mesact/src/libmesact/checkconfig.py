
def checkit(parent):
	parent.mainTabs.setCurrentIndex(0)
	configErrors = []
	tabError = False
	nextHeader = 0
	validNumber = 'is not a valid number in the form 0.0 or 0'

	# check the Machine Tab for errors
	# check to see if a daughter card is selected for that type
	if not parent.configName.text():
		tabError = True
		configErrors.append('\tA configuration name must be entered')
	if parent.linearUnitsCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tLinear Units must be selected')
	if parent.trajMaxLinVelDSB.value() == 0:
		tabError = True
		configErrors.append('\tMaximum Linear Velocity must be more than 0')
	required = ['5i25', '7i92', '7i93', '7i80db_16',  '7i80db_25', '7i80hd_16', '7i80hd_25','7i98']
	if parent.boardCB.currentData() in required:
		if not parent.firmwareCB.currentData():
			tabError = True
			configErrors.append(f'\tFirmware must be selected for {parent.board}')
	if not parent.boardCB.currentData():
		tabError = True
		configErrors.append('\tA Board must be selected')
	if parent.boardType == 'eth' and parent.ipAddressCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tAn IP address must be selected, 10.10.10.10 is recommended')
	if parent.daughterCB_0.currentData() and parent.daughterCB_1.currentData():
		tabError = True
		configErrors.append('\tAt this time only one daughter card can be selected')

	if tabError:
		configErrors.insert(nextHeader, 'Machine Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Machine Tab

	# check the Display Tab for errors
	if parent.guiCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA GUI must be selected')
	if parent.positionOffsetCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA Position Offset must be selected')
	if parent.positionFeedbackCB.currentText() == 'Select':
		tabError = True
		configErrors.append('\tA Position Feedback must be selected')
	if parent.maxFeedOverrideSB.value() == 0.0:
		tabError = True
		configErrors.append('\tThe Max Feed Override must be greater than zero, 1.2 is suggested')
	if parent.frontToolLatheCB.isChecked() and parent.backToolLatheCB.isChecked():
		configErrors.append('\tOnly one lathe display option can be checked')
		tabError = True
	if set('XYZUVW')&set(parent.coordinatesLB.text()):
		if parent.defLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tDefault Linear Jog Velocity must be greater than zero')
		if parent.maxLinJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tMaximum Linear Jog Velocity must be greater than zero')
	if set('ABC')&set(parent.coordinatesLB.text()):
		if parent.defAngJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tDefault Angular Jog Velocity must be greater than zero')
		if parent.maxAngJogVelDSB.value() == 0.0:
			tabError = True
			configErrors.append('\tMaximum Angular Jog Velocity must be greater than zero')
	if tabError:
		configErrors.insert(nextHeader, 'Display Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Display Tab

	# check the Axis Tab for errors
	# bitch and bail if the Axis Tab is not enabled
	# To Do check for mis matched limits on tandem joints
	if parent.mainTabs.isTabEnabled(3):
		if len(parent.coordinatesLB.text()) == 0:
			tabError = True
			configErrors.append('\tAt least one Joint must be configured starting with Joint 0')
		else: #check the joints
			# make this a loop getattr(parent, f'_{i}')
			coordinates = parent.coordinatesLB.text()

			# check for multiple joints per axis
			joints = {}
			for i in range(len(parent.coordinatesLB.text())):
				joints[f'joint{i}'] = {}
				joints[f'joint{i}']['axis'] = getattr(parent, f'c0_axisCB_{i}').currentData()
				joints[f'joint{i}']['minLimit'] = getattr(parent, f'c0_minLimit_{i}').text()
				joints[f'joint{i}']['maxLimit'] = getattr(parent, f'c0_maxLimit_{i}').text()
				joints[f'joint{i}']['homeSeq'] = getattr(parent, f'c0_homeSequence_{i}').text()

			axes = set(parent.coordinatesLB.text())
			gantry = []
			for item in axes:
				if parent.coordinatesLB.text().count(item) > 1:
					gantry.append(item)

			gantryJoints = []
			for item in joints:
				if joints[item]['axis'] in gantry:
					gantryJoints.append(item)

			if gantryJoints:
				check = True
				compare = []
				for i, item in enumerate(gantryJoints):
					compare.append(joints[item]['minLimit'])
				if len(set(compare)) > 1:
					tabError = True
					configErrors.append(f'\tMultiple Joint Axis {"".join(gantry)} {" & ".join(gantryJoints)} Min Limit must match.')
				compare = []
				for i, item in enumerate(gantryJoints):
					compare.append(joints[item]['maxLimit'])
				if len(set(compare)) > 1:
					tabError = True
					configErrors.append(f'\tMultiple Joint Axis {"".join(gantry)} {" & ".join(gantryJoints)} Max Limit must match.')

				for i, item in enumerate(gantryJoints):
					if not joints[item]['homeSeq']:
						tabError = True
						configErrors.append(f'\tMultiple Joint Axis {item} Home Sequence must be specified.')
						check = False

				if check:
					compare = []
					for i, item in enumerate(gantryJoints):
						compare.append(joints[item]['homeSeq'].strip('-'))
					if len(set(compare)) > 1:
						tabError = True
						configErrors.append(f'\tMultiple Joint Axis {"".join(gantry)} {" & ".join(gantryJoints)} Home Sequence must match.')

				homeOk = False
				for i, item in enumerate(gantryJoints):
					if joints[item]['homeSeq'].startswith('-'):
						homeOk = True
				if not homeOk:
					tabError = True
					configErrors.append(f'\tMultiple Joint Axis {"".join(gantry)} {" & ".join(gantryJoints)} must be negative for at least one Joint.')


			card = 'c0'
			for i in range(6):
				if getattr(parent, f'{card}_axisCB_{i}').currentText() != 'Select':
					pass

			''' This is not the same as the daughter tab enables...
			if parent.daughterCB_0.currentData():
				card = 'c0'
			elif parent.daughterCB_1.currentData():
				card = 'c1'
				print('here')
			else:
				card = 'c0'
			'''
			card = 'c0'
			for i in range(6): # Axes
				#print(getattr(parent, f'{card}_axisCB_{i}').currentData())
				if getattr(parent, f'{card}_axisCB_{i}').currentData():
					#print(getattr(parent, f'{card}_axisCB_{i}').currentData())
					if not getattr(parent, f'{card}_scale_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Scale must be specified for Joint {i}')
					# make sure it's a valid number
					if not isNumber(getattr(parent, f'{card}_scale_{i}').text()):
						tabError = True
						configErrors.append(f'\tThe Scale for Joint {i} {validNumber}')
					if isNumber(getattr(parent, f'{card}_scale_{i}').text()):
						if float(getattr(parent, f'{card}_scale_{i}').text()) < 0:
							if getattr(parent, f'{card}_reverse_{i}').isChecked():
								tabError = True
								configErrors.append(f'\tThe Scale for Joint {i} can not be negative if Reverse Dir is checked')
					if not getattr(parent, f'{card}_minLimit_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Mininum Limit for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_minLimit_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Mininum Limit for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_maxLimit_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Maximum Limit for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_maxLimit_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Maximum Limit for Joint {i} {validNumber}')

					if not getattr(parent, f'{card}_maxVelocity_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Maximum Velocity for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_maxVelocity_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Maximum Velocity for Joint {i} {validNumber}')

					if not getattr(parent, f'{card}_maxAccel_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Maximum Acceleration for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_maxAccel_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Maximum Acceleration for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_p_{i}').text():
						tabError = True
						configErrors.append(f'\tThe P for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_p_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe P for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_i_{i}').text():
						tabError = True
						configErrors.append(f'\tThe I for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_i_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe I for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_d_{i}').text():
						tabError = True
						configErrors.append(f'\tThe D for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_d_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe D for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_ff0_{i}').text():
						tabError = True
						configErrors.append(f'\tThe FF0 for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_ff0_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe FF0 for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_ff1_{i}').text():
						tabError = True
						configErrors.append(f'\tThe FF1 for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_ff1_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe FF1 for Joint {i} {validNumber}')
					if not getattr(parent, f'{card}_ff2_{i}').text():
						tabError = True
						configErrors.append(f'\tThe FF2 for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_ff2_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe FF2 for Joint {i} {validNumber}')
					if getattr(parent, f'{card}_min_ferror_{i}').text(): # not a required entry
						if not isNumber(getattr(parent, f'{card}_ferror_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Min Following Error for Joint {i} {validNumber}')

					if not getattr(parent, f'{card}_ferror_{i}').text():
						tabError = True
						configErrors.append(f'\tThe Max Following Error for Joint {i} must be specified')
					else: # make sure it's a valid number
						if not isNumber(getattr(parent, f'{card}_ferror_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Max Following Error for Joint {i} {validNumber}')

					# stepper only checks
					if parent.cardType_0 == 'step':
						if not getattr(parent, f'{card}_StepTime_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Step Time for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_StepTime_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Step Time for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_StepSpace_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Step Space for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_StepSpace_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Step Space for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_DirSetup_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Direction Setup for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_DirSetup_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Direction Setup for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_DirHold_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Direction Hold for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_DirHold_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Direction Hold for Joint {i} {validNumber}')

					# servo only checks
					if parent.cardType_0 == 'servo':
						if not getattr(parent, f'{card}_analogMinLimit_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Analog Min Limit for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_analogMinLimit_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Analog Min Limit for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_analogMaxLimit_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Analog Max Limit for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_analogMaxLimit_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Analog Max Limit for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_analogScaleMax_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Analog Scale Max for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_analogScaleMax_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Analog Scale Max for Joint {i} {validNumber}')

						if not getattr(parent, f'{card}_encoderScale_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Encoder Scale for Joint {i} must be specified')
						else: # make sure it's a valid number
							if not isNumber(getattr(parent, f'{card}_encoderScale_{i}').text()):
								tabError = True
								configErrors.append(f'\tThe Encoder Scale for Joint {i} {validNumber}')

					# add sanity check for home entries
					if getattr(parent, f'{card}_home_{i}').text():
						if not isNumber(getattr(parent, f'{card}_home_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Home Location for Joint {i} {validNumber}')
					if getattr(parent, f'{card}_homeOffset_{i}').text():
						if not isNumber(getattr(parent, f'{card}_homeOffset_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Home Offset for Joint {i} {validNumber}')
					if getattr(parent, f'{card}_homeSearchVel_{i}').text():
						if not isNumber(getattr(parent, f'{card}_homeSearchVel_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Home Search Velocity for Joint {i} {validNumber}')
					if getattr(parent, f'{card}_homeLatchVel_{i}').text():
						if not isNumber(getattr(parent, f'{card}_homeLatchVel_{i}').text()):
							tabError = True
							configErrors.append(f'\tThe Home Latch Velocity for Joint {i} {validNumber}')
					if getattr(parent, f'{card}_homeSequence_{i}').text():
						if not isNumber(getattr(parent, f'{card}_homeSequence_{i}').text()):
							tabError = True
							hs = getattr(parent, f'{card}_homeSequence_{i}').text()
							configErrors.append(f'\tThe Home Sequence for Joint {i} must be a number')

					if not f'joint{i}' in gantryJoints:
						if '-' in getattr(parent, f'{card}_homeSequence_{i}').text():
							tabError = True
							configErrors.append(f'\tThe Home Sequence for Joint {i} must be a positive number')

	else: # Axes Tab not enabled
		if parent.boardCB.currentData():
			board = parent.boardCB.currentData()
			tabError = True
			configErrors.append(f'\tA firmware and Daughter card needs to be selected for the {board}.')

	if tabError:
		configErrors.insert(nextHeader, 'Axes Tab:')
		nextHeader = len(configErrors)
		tabError = False
	# end of Axis Tab

	# check the I/O Tab for errors
	for i in range(32): # check for Home All
		# check for home all
		if getattr(parent, f'inputPB_{i}').text() == 'Home All':
			seq = []
			seqStart = ['-1', '-0', '0', '1']
			for i in range(6):
				if getattr(parent, f'{card}_axisCB_{i}').currentText() != 'Select':
					if getattr(parent, f'{card}_homeSequence_{i}').text() == '':
						tabError = True
						configErrors.append(f'\tThe Home All Input requires a Home Sequence for Joint {i}')
						break
					if not isNumber(getattr(parent, f'{card}_homeSequence_{i}').text()):
						tabError = True
						e = getattr(parent, f'{card}_homeSequence_{i}').text()
						configErrors.append(f'\tThe Home All Input requires the Home Sequence for Joint {i} be a number not {e}')
					else:
						seq.append(getattr(parent, f'{card}_homeSequence_{i}').text())
			if seq:
				seqRemoveDups = list(dict.fromkeys(seq))
				seqSorted = sorted(seqRemoveDups)
				if seqSorted[0] not in seqStart:
					tabError = True
					configErrors.append(f'\tThe Home All Input requires the Home Sequence to start with 0 or 1')
				numList = [int(i) for i in seqSorted]
				checkList = list(range(min(numList), max(numList)+1))
				if not numList == checkList:
					tabError = True
					configErrors.append(f'\tThe Home All Input requires the Home Sequence to not skip a number {numList}')

	for i in range(32): # check for invert and debounce
		invert = getattr(parent, f'inputInvertCB_{i}').isChecked()
		debounce = getattr(parent, f'inputDebounceCB_{i}').isChecked()
		if invert and debounce:
			tabError = True
			configErrors.append(f'\tInvert and Debouce for Joint {i} can not be used together')

	for i in range(16): # check for spindle on
		if getattr(parent, f'outputPB_{i}').text() == 'Spindle On':
			if parent.spindleTypeCB.currentText() != 'Digital':
				tabError = True
				configErrors.append(f'\tSpindle Output must be set to Digital to use Spindle On')

	if tabError:
		configErrors.insert(nextHeader, 'I/O Tab:')
		nextHeader = len(configErrors)
		tabError = False

	# end of I/O Tab

	# check the Spindle Tab for errors

	if parent.spindleTypeCB.currentData():
		if parent.spindleTypeCB.currentData() == 'analog':
			if not parent.spindlePwmTypeCB.currentData():
				tabError = True
				configErrors.append(f'\tAnalog spindle PWM Type must be selected')

		if parent.spindleFeedbackCB.currentData() == 'encoder':
			if parent.spindleMaxRpm.value() != parent.maxOutput_s.value():
				tabError = True
				configErrors.append(f'\tPID Max Output {parent.maxOutput_s.value()} needs to match Max RPM {parent.spindleMaxRpm.value()}')
			if parent.spindleEncoderScale.value() == 0:
				tabError = True
				configErrors.append(f'\tEncoder Scale {parent.spindleEncoderScale.value()} needs to greater than 0')

		if parent.spindleTypeCB.currentData()[:7] == 'stepgen':
			if not parent.spindleStepTime.text():
				tabError = True
				configErrors.append(f'\tThe Step Time for Spindle must be specified')
			else: # make sure it's a valid number
				if not isNumber(parent.spindleStepTime.text()):
					tabError = True
					configErrors.append(f'\tThe Step Time for Spindle {validNumber}')

			if not parent.spindleStepSpace.text():
				tabError = True
				configErrors.append(f'\tThe Step Space for Spindle must be specified')
			else: # make sure it's a valid number
				if not isNumber(parent.spindleStepSpace.text()):
					tabError = True
					configErrors.append(f'\tThe Step Space for Spindle {validNumber}')

			if not parent.spindleDirSetup.text():
				tabError = True
				configErrors.append(f'\tThe Direction Setup for Spindle must be specified')
			else: # make sure it's a valid number
				if not isNumber(parent.spindleDirSetup.text()):
					tabError = True
					configErrors.append(f'\tThe Direction Setup for Spindle {validNumber}')

			if not parent.spindleDirHold.text():
				tabError = True
				configErrors.append(f'\tThe Direction Hold for Spindle must be specified')
			else: # make sure it's a valid number
				if not isNumber(parent.spindleDirHold.text()):
					tabError = True
					configErrors.append(f'\tThe Direction Hold for Spindle {validNumber}')



	if tabError:
		configErrors.insert(nextHeader, 'Spindle Tab:')
		nextHeader = len(configErrors)
		tabError = False

	# end of Spindle Tab

	parent.machinePTE.clear()
	if configErrors:
		checkit.result = '\n'.join(configErrors)
		parent.machinePTE.setPlainText(checkit.result)
		return False
	else:
		parent.machinePTE.setPlainText('Configuration checked OK')
		return True
	
def isNumber(x):
	try:
		float(x)
		return True
	except ValueError:
		return False
