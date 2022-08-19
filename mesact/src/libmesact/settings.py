import os
from configparser import ConfigParser
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton)


# Do all config settings here.

def update(parent):
	configPath = os.path.expanduser('~/.config/measct/mesact.conf')
	sender = parent.sender().objectName()
	section = parent.sender().property('Section')
	item = parent.sender().property('Item')
	value = None
	# check to see what type of object it is to get correct value
	if isinstance(parent.sender(), QCheckBox):
		value = f'{parent.sender().isChecked()}'
	elif isinstance(parent.sender(), QLabel):
		print('yes')
	else:
		print('no')

	if value is not None: # Update config
		config = ConfigParser()
		config.optionxform = str
		if os.path.isfile(configPath): # Read the file
			config.read(configPath)
			config.set(section, item, value)
		else: # config file does not exist
			config.add_section('NAGS')
			config['NAGS']['MESAFLASH'] = f'{parent.checkMesaflashCB.isChecked()}'
			config['NAGS']['NEWUSER'] = f'{parent.newUserCB.isChecked()}'
			os.makedirs(os.path.expanduser('~/.config/measct')) # this is moved to startup
		with open(configPath, 'w') as cf:
			config.write(cf)


	'''

	else: # no mesact.conf file found set defaults
		#print(f'{os.path.expanduser("~/.config/measct/mesact.conf")} not found')
		config.add_section('NAGS')
		config['NAGS']['MESAFLASH'] = 'True'
		parent.checkMesaflashCB.setChecked(True)
		checkmf(parent)
		config['NAGS']['NEWUSER'] = 'True'
		parent.newUserCB.setChecked(True)
		if not os.path.isdir(os.path.expanduser('~/.config/measct')):
			os.makedirs(os.path.expanduser('~/.config/measct'))
		with open(os.path.expanduser('~/.config/measct/mesact.conf'), 'w') as configfile:
			config.write(configfile)





	#print(f'Check MF {parent.checkMesaflashCB.isChecked()}')
	#print(f'Check NU {parent.newUserCB.isChecked()}')


	#checkmf(parent)
	#if config.has_option('NAGS', 'NEWUSER'):
	#if config['NAGS']['NEWUSER'] == 'True':
	#parent.newUserCB.setChecked(True)

def update_system_status_values(file, section, system, value):
    config.read(file)
    cfgfile = open(file, 'w')
    config.set(section, system, value)
    config.write(cfgfile)
    cfgfile.close()

1) Read it

2) Open it

3) Update it

4) Write it

5) Close it
'''

