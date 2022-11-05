import os
from configparser import ConfigParser
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QSpinBox,
	QDoubleSpinBox, QCheckBox, QGroupBox, QComboBox, QPushButton)

# Do all config settings here.

def update_value(parent):
	configPath = os.path.expanduser('~/.config/measct/mesact.conf')
	sender = parent.sender().objectName()
	section = parent.sender().property('Section')
	option = parent.sender().property('Option')
	value = None
	# check to see what type of object it is to get correct value
	if isinstance(parent.sender(), QCheckBox):
		if sender == 'loadConfigCB' and parent.sender().isChecked():
			value = parent.configNameLE.text()
		else:
			value = f'{parent.sender().isChecked()}'

	if value is not None: # Update config
		config = ConfigParser()
		config.optionxform = str
		if os.path.isfile(configPath): # Read the file
			config.read(configPath)
			if not config.has_section(section):
				config.add_section(section)
			if not config.has_option(section, option):
				config[section][option] = value
			config.set(section, option, value)
		else: # config file does not exist
			config.add_section('NAGS')
			config['NAGS']['MESAFLASH'] = f'{parent.checkMesaflashCB.isChecked()}'
			config['NAGS']['NEWUSER'] = f'{parent.newUserCB.isChecked()}'
			config.add_section('STARTUP')
			if parent.loadConfigCB.isChecked():
				config['STARTUP']['CONFIG'] = parent.configNameLE.text()
			else:
				config['STARTUP']['CONFIG'] = 'False'
		with open(configPath, 'w') as cf:
			config.write(cf)
