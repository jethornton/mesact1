from PyQt5.QtWidgets import QMenu, QAction

inputs = [{'Not Used':'Select'},
	{'Homing':['Joint 0 Home', 'Joint 1 Home', 'Joint 2 Home',
		'Joint 3 Home', 'Joint 4 Home', 'Joint 5 Home',
		'Joint 6 Home', 'Joint 7 Home', 'Joint 8 Home', 'Home All']},
	{'Limits':[
		{'Joint 0':['Joint 0 Plus', 'Joint 0 Minus', 'Joint 0 Both']},
		{'Joint 1':['Joint 1 Plus', 'Joint 1 Minus', 'Joint 1 Both']},
		{'Joint 2':['Joint 2 Plus', 'Joint 2 Minus', 'Joint 2 Both']},
		{'Joint 3':['Joint 3 Plus', 'Joint 3 Minus', 'Joint 3 Both']},
		{'Joint 4':['Joint 4 Plus', 'Joint 4 Minus', 'Joint 4 Both']},
		{'Joint 5':['Joint 5 Plus', 'Joint 5 Minus', 'Joint 5 Both']},
		{'Joint 6':['Joint 6 Plus', 'Joint 6 Minus', 'Joint 6 Both']},
		{'Joint 7':['Joint 7 Plus', 'Joint 7 Minus', 'Joint 7 Both']},
		{'Joint 8':['Joint 8 Plus', 'Joint 8 Minus', 'Joint 8 Both']}]},
	{'Jog':[{'X Axis':['Jog X Plus', 'Jog X Minus']},
		{'Y Axis':['Jog Y Plus', 'Jog Y Minus']},
		{'Z Axis':['Jog Z Plus', 'Jog Z Minus']},
		{'A Axis':['Jog A Plus', 'Jog A Minus']},
		{'B Axis':['Jog B Plus', 'Jog B Minus']},
		{'C Axis':['Jog C Plus', 'Jog C Minus']},
		{'U Axis':['Jog U Plus', 'Jog U Minus']},
		{'V Axis':['Jog V Plus', 'Jog V Minus']},
		{'W Axis':['Jog W Plus', 'Jog W Minus']}
	]},
	{'Motion':['Probe Input', 'Digital 0', 'Digital 1', 'Digital 2', 'Digital 3']},
	{'Spindle':['Spindle Amp Fault', 'Spindle Inhibit', 'Spindle Oriented', 'Spindle Orient Fault']},
	{'I/O Control':[
		{'External E Stop':['E Stop 0', 'E Stop 1', 'E Stop 2', 'E Stop 3',
		'E Stop 4', 'E Stop 5', 'E Stop 6', 'E Stop 7', 'E Stop 8']},
		'Lube Level', 'Tool Changed', 'Tool Prepared', 'Tool Changer Fault']}
]

# {'':['', ]},
# '', 
outputs = [{'Not Used':'Select'},
	{'Spindle':['Spindle On', 'Spindle CW', 'Spindle CCW', 'Spindle Brake']},
	{'I/O Control':['Coolant Flood', 'Coolant Mist', 'Lube Pump',
		'Tool Change', 'Tool Prepare', 'E-Stop Out']},
	{'Digital Out':['Digital Out 0', 'Digital Out 1', 'Digital Out 2', 'Digital Out 3', ]}
]

ain = [{'Not Used':'Select'},
	{'Analog':['Analog In 0', 'Analog In 1', 'Analog In 2','Analog In 3']}
]

def build(parent):
	for i in range(32):
		button = getattr(parent, "inputPB_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(16):
		button = getattr(parent, "outputPB_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)


	for i in range(24):
		button = getattr(parent, "ss7i64in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i69in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i70in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(32):
		button = getattr(parent, "ss7i84in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)


	for i in range(24):
		button = getattr(parent, "ss7i64out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(24):
		button = getattr(parent, "ss7i69out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i71out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(48):
		button = getattr(parent, "ss7i72out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(15):
		button = getattr(parent, "ss7i73in_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)

	for i in range(2):
		button = getattr(parent, "ss7i73out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	for i in range(16):
		button = getattr(parent, "ss7i84out_{}".format(i))
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	# 7i73 I/O
	for i in range(8):
		getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Output {i+10}')
		button = getattr(parent, f'ss7i73key_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)
	for i in range(8,16):
		getattr(parent, 'ss7i73keylbl_' + str(i)).setText(f'Input {i+8}')
		button = getattr(parent, f'ss7i73key_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)
	for i in range(8):
		getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+2}')
		button = getattr(parent, f'ss7i73lcd_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)
	for i in range(8,12):
		getattr(parent, 'ss7i73lcdlbl_' + str(i)).setText(f'Output {i+10}')
		button = getattr(parent, f'ss7i73lcd_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)
	for i in range(16):
		button = getattr(parent, f'ss7i73in_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(inputs, menu)
		button.setMenu(menu)
	for i in range(2):
		button = getattr(parent, f'ss7i73out_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(outputs, menu)
		button.setMenu(menu)

	# 7i87 inputs
	for i in range(8):
		button = getattr(parent, f'ss7i87in_{i}')
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		add_menu(ain, menu)
		button.setMenu(menu)

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
