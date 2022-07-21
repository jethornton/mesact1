import os
from datetime import datetime

def build(parent):
	filePath = os.path.join(parent.configPath, 'sserial.hal')
	if os.path.exists(filePath):
		os.remove(filePath)
	if parent.ssCardCB.currentData():
		ssCard = parent.ssCardCB.currentText()
		board = parent.board
		parent.machinePTE.appendPlainText(f'Building {filePath}')
		contents = []
		contents = ['# This file was created with the Mesa Configuration Tool on ']
		contents.append(datetime.now().strftime('%b %d %Y %H:%M:%S') + '\n')
		contents.append('# If you make changes to this file DO NOT use the Configuration Tool\n\n')

		input_dict = {
			'Joint 0 Home':'net joint-0-home joint.0.home-sw-in <= ',
			'Joint 1 Home':'net joint-1-home joint.1.home-sw-in <= ',
			'Joint 2 Home':'net joint-2-home joint.2.home-sw-in <= ',
			'Joint 3 Home':'net joint-3-home joint.3.home-sw-in <= ',
			'Joint 4 Home':'net joint-4-home joint.4.home-sw-in <= ',
			'Joint 5 Home':'net joint-5-home joint.5.home-sw-in <= ',
			'Joint 6 Home':'net joint-6-home joint.6.home-sw-in <= ',
			'Joint 7 Home':'net joint-7-home joint.7.home-sw-in <= ',
			'Joint 8 Home':'net joint-8-home joint.8.home-sw-in <= ',
			'Home All':'fix me',

			'Joint 0 Plus':'net pos-limit-joint-0 joint.0.pos-lim-sw-in <= ',
			'Joint 0 Minus':'net neg-limit-joint-0 joint.0.neg-lim-sw-in <= ',
			'Joint 0 Both':'net both-limit-joint-0 joint.0.pos-lim-sw-in\n'
				'net both-limit-joint-0 joint.0.neg-lim-sw-in <= ',
			'Joint 1 Plus':'net pos-limit-joint-1 joint.1.pos-lim-sw-in <= ',
			'Joint 1 Minus':'net neg-limit-joint-1 joint.1.neg-lim-sw-in <= ',
			'Joint 1 Both':'net both-limit-joint-1 joint.1.pos-lim-sw-in\n'
				'net both-limit-joint-1 joint.1.neg-lim-sw-in <= ',
			'Joint 2 Plus':'net pos-limit-joint-2 joint.2.pos-lim-sw-in <= ',
			'Joint 2 Minus':'net neg-limit-joint-2 joint.2.neg-lim-sw-in <= ',
			'Joint 2 Both':'net both-limit-joint-2 joint.2.pos-lim-sw-in\n'
				'net both-limit-joint-2 joint.2.neg-lim-sw-in <= ',
			'Joint 3 Plus':'net pos-limit-joint-3 joint.3.pos-lim-sw-in <= ',
			'Joint 3 Minus':'net neg-limit-joint-3 joint.3.neg-lim-sw-in <= ',
			'Joint 3 Both':'net both-limit-joint-3 joint.3.pos-lim-sw-in\n'
				'net both-limit-joint-3 joint..neg-lim-sw-in <= ',
			'Joint 4 Plus':'net pos-limit-joint-4 joint.4.pos-lim-sw-in <= ',
			'Joint 4 Minus':'net neg-limit-joint-4 joint.4.neg-lim-sw-in <= ',
			'Joint 4 Both':'net both-limit-joint-4 joint.4.pos-lim-sw-in\n'
				'net both-limit-joint-4 joint.4.neg-lim-sw-in <= ',
			'Joint 5 Plus':'net pos-limit-joint-5 joint.5.pos-lim-sw-in <= ',
			'Joint 5 Minus':'net neg-limit-joint-5 joint.5.neg-lim-sw-in <= ',
			'Joint 5 Both':'net both-limit-joint-5 joint.5.pos-lim-sw-in\n'
				'net both-limit-joint-5 joint.5.neg-lim-sw-in <= ',
			'Joint 6 Plus':'net pos-limit-joint-6 joint.6.pos-lim-sw-in <= ',
			'Joint 6 Minus':'net neg-limit-joint-6 joint.6.neg-lim-sw-in <= ',
			'Joint 6 Both':'net both-limit-joint-6 joint.6.pos-lim-sw-in\n'
				'net both-limit-joint-6 joint.6.neg-lim-sw-in <= ',
			'Joint 7 Plus':'net pos-limit-joint-7 joint.7.pos-lim-sw-in <= ',
			'Joint 7 Minus':'net neg-limit-joint-7 joint.7.neg-lim-sw-in <= ',
			'Joint 7 Both':'net both-limit-joint-7 joint.7.pos-lim-sw-in\n'
				'net both-limit-joint-7 joint.7.neg-lim-sw-in <= ',
			'Joint 8 Plus':'net pos-limit-joint-8 joint.8.pos-lim-sw-in <= ',
			'Joint 8 Minus':'net neg-limit-joint-8 joint.8.neg-lim-sw-in <= ',
			'Joint 8 Both':'net both-limit-joint-8 joint.8.pos-lim-sw-in\n'
				'net both-limit-joint-8 joint.8.neg-lim-sw-in <= ',

			'Jog X Plus':'net jog-x-plus halui.axis.x.plus <= ',
			'Jog X Minus':'net jog-x-minus halui.axis.x.minus <= ',
			'Jog Y Plus':'net jog-y-plus halui.axis.y.plus <= ',
			'Jog Y Minus':'net jog-y-minus halui.axis.y.minus <= ',
			'Jog Z Plus':'net jog-z-plus halui.axis.z.plus <= ',
			'Jog Z Minus':'net jog-z-minus halui.axis.z.minus <= ',
			'Jog A Plus':'net jog-a-plus halui.axis.a.plus <= ',
			'Jog A Minus':'net jog-a-minus halui.axis.a.minus <= ',
			'Jog B Plus':'net jog-b-plus halui.axis.b.plus <= ',
			'Jog B Minus':'net jog-b-minus halui.axis.b.minus <= ',
			'Jog C Plus':'net jog-c-plus halui.axis.c.plus <= ',
			'Jog C Minus':'net jog-c-minus halui.axis.c.minus <= ',
			'Jog U Plus':'net jog-u-plus halui.axis.u.plus <= ',
			'Jog U Minus':'net jog-u-minus halui.axis.u.minus <= ',
			'Jog V Plus':'net jog-v-plus halui.axis.v.plus <= ',
			'Jog V Minus':'net jog-v-minus halui.axis.v.minus <= ',
			'Jog W Plus':'net jog-w-plus halui.axis.w.plus <= ',
			'Jog W Minus':'net jog-w-minus halui.axis.w.minus <= ',


			'Probe Input':'net probe-input motion.probe-input <= ',
			'Digital 0':'net digital-0-input motion.digital-in-00 <= ',
			'Digital 1':'net digital-1-input motion.digital-in-01 <= ',
			'Digital 2':'net digital-2-input motion.digital-in-02 <= ',
			'Digital 3':'net digital-3-input motion.digital-in-03 <= ',

			'Flood':'net coolant-flood iocontrol.0.coolant-flood <= ',
			'Mist':'net coolant-mist iocontrol.0.coolant-mist <= ',
			'Lube Level':'net lube-level iocontrol.0.lube_level <= ',
			'Tool Changed':'net tool-changed iocontrol.0.tool-changed <= ',
			'Tool Prepared':'net tool-prepared iocontrol.0.tool-prepared <= '
		}


		'''
		hm2_7i76e.0.7i76.0.0.input-00
		hm2_7i76e.0.7i76.0.0.input-00-not
		hm2_7i76e.0.7i76.0.0.output-00
		hm2_7i76e.0.7i76.0.0.spindir
		hm2_7i76e.0.7i76.0.0.spinena
		hm2_7i76e.0.7i76.0.0.spinout

		hm2_7i92.0.7i76.0.0.input-00
		hm2_7i92.0.7i76.0.0.input-00-not
		hm2_7i92.0.7i76.0.0.output-00
		hm2_7i92.0.7i76.0.0.spindir
		hm2_7i92.0.7i76.0.0.spinena
		hm2_7i92.0.7i76.0.0.spinout

		hm2_7i95.0.inmux.00.input-00
		hm2_7i95.0.inmux.00.input-00-not
		hm2_7i95.0.inmux.00.input-00-slow


		hm2_7i96.0.gpio.000.in
		hm2_7i96.0.gpio.000.in_not

		hm2_7i96s.0.inm.00.input-01
		hm2_7i96s.0.inm.00.input-01-not
		hm2_7i96s.0.inm.00.input-00-slow


		hm2_7i97.0.inmux.00.input-00
		hm2_7i97.0.inmux.00.input-00-not
		hm2_7i97.0.inmux.00.input-00-slow
		'''

		'''
		if parent.ssCardCB.currentIndex() > 0:
			contents.append(f'# Configuration file for the {parent.ssCardCB.currentText()} Smart Serial Card\n\n')

		# build inputs from qpushbutton menus
		for i in range(11):
			key = getattr(parent, 'inputPB_' + str(i)).text()
			invert = '_not' if getattr(parent, 'inputInvertCB_' + str(i)).isChecked() else ''
			if input_dict.get(key, False): # return False if key is not in dictionary
				contents.append(input_dict[key] + f'hm2_7i92.0.gpio.{i:03}.in{invert}\n')
			else: # handle special cases
				if key == 'Home All':
					contents.append('\n# Home All Joints\n')
					contents.append('net home-all ' + f'hm2_7i92.0.gpio.{i:03}.in{invert}\n')
					for i in range(5):
						if getattr(parent, 'axisCB_' + str(i)).currentData():
							contents.append('net home-all ' + f'joint.{i}.home-sw-in\n')
				elif key == 'External E Stop':
					contents.append('\n# External E-Stop\n')
					contents.append('loadrt estop_latch\n')
					contents.append('addf estop-latch.0 servo-thread\n')
					contents.append('net estop-loopout iocontrol.0.emc-enable-in <= estop-latch.0.ok-out\n')
					contents.append('net estop-loopin iocontrol.0.user-enable-out => estop-latch.0.ok-in\n')
					contents.append('net estop-reset iocontrol.0.user-request-enable => estop-latch.0.reset\n')
					contents.append(f'net remote-estop estop-latch.0.fault-in <= hm2_7i92.0.gpio.{i:03}.in{invert}\n\n')
		'''

		output_dict = {
		'Coolant Flood': 'net flood-output iocontrol.0.coolant-flood => ',
		'Coolant Mist': 'net mist-output iocontrol.0.coolant-mist => ',
		'Spindle On': 'net spindle-on spindle.0.on => ',
		'Spindle CW': 'net spindle-cw spindle.0.forward => ',
		'Spindle CCW': 'net spindle-ccw spindle.0.reverse => ',
		'Spindle Brake': 'net spindle-brake spindle.0.brake => ',
		'E-Stop Out': 'net estop-loopback => ',
		'Digital Out 0': 'net digital-out-0 motion.digital-out-00 => ',
		'Digital Out 1': 'net digital-out-1 motion.digital-out-01 => ',
		'Digital Out 2': 'net digital-out-2 motion.digital-out-02 => ',
		'Digital Out 3': 'net digital-out-3 motion.digital-out-03 => '
		}


		if ssCard == '7i64':
			inputs = 24
			outputs = 24
		elif ssCard == '7i69':
			inputs = 24
			outputs = 24
		elif ssCard == '7i70':
			inputs = 48
			outputs = 0
		elif ssCard == '7i71':
			inputs = 0
			outputs = 48
		elif ssCard == '7i72':
			inputs = 0
			outputs = 48
		elif ssCard == '7i73':
			inputs = 0
			outputs = 0
		elif ssCard == '7i84':
			inputs = 32
			outputs = 16
		elif ssCard == '7i87':
			inputs = 8
			outputs = 0
		else:
			inputs = 0
			outputs = 0

		motherBoards = ['5i25', '7i80db', '7i80hd', '7i92', '7i93', '7i98']
		daughterBoards =['7i76', '7i77', '7i78']

		combiBoards = ['7i76e', '7i95', '7i96', '7i96s', '7i97']
		if ssCard != '7i73' and board in combiBoards:
			for i in range(inputs):
				if getattr(parent, f'ss{ssCard}in_' + str(i)).text() != 'Select':
					key = getattr(parent, f'ss{ssCard}in_' + str(i)).text()
					contents.append(f'{input_dict[key]} hm2_{board}.0.{ssCard}.0.0.input-{i:02}\n')
			for i in range(outputs):
				if getattr(parent, f'ss{ssCard}out_' + str(i)).text() != 'Select':

					key = getattr(parent, f'ss{ssCard}out_' + str(i)).text()
					if output_dict.get(key, False): # return False if key is not in dictionary
						contents.append(f'{output_dict[key]} hm2_{board}.0.{ssCard}.0.0.output-{i:02}\n')

		elif ssCard == '7i73':
			for i in range(16):
				if getattr(parent, 'ss7i73key_' + str(i)).text() != 'Select':
					keyPin = getattr(parent, 'ss7i73key_' + str(i)).text()
					contents.append(f'net ss7i73key_{i} hm2_{board}.0.7i73.0.0.input-{i:02} <= {keyPin}\n')
			for i in range(12):
				if getattr(parent, 'ss7i73lcd_' + str(i)).text() != 'Select':
					lcdPin = getattr(parent, 'ss7i73lcd_' + str(i)).text()
					contents.append(f'net ss7i73lcd_{i} hm2_{board}.0.7i73.0.0.output-{i:02} => {lcdPin}\n')
			for i in range(16):
				if getattr(parent, 'ss7i73in_' + str(i)).text() != 'Select':
					inPin = getattr(parent, 'ss7i73in_' + str(i)).text()
					contents.append(f'net ss7i73in_{i} hm2_{board}.0.7i73.0.0.input-{i:02} <= {inPin}\n')
			for i in range(2):
				if getattr(parent, 'ss7i73out_' + str(i)).text() != 'Select':
					outPin = getattr(parent, 'ss7i73out_' + str(i)).text()
					contents.append(f'net ss7i73out_{i} hm2_{board}.0.7i84.0.0.output-{i:02} => {outPin}\n')

		try:
			with open(filePath, 'w') as f:
				f.writelines(contents)
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')
