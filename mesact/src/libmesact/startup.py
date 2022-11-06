import os, subprocess
from configparser import ConfigParser
from PyQt5.QtGui import QPixmap

from libmesact import utilities

def setup(parent):
	# if the config file does not exist create it
	if not os.path.isdir(os.path.expanduser('~/.config/measct')):
		os.makedirs(os.path.expanduser('~/.config/measct'))
		config = ConfigParser()
		config.optionxform = str
		config.add_section('MESACT')
		config['MESACT']['VERSION'] = f'{parent.version}'
		config.add_section('NAGS')
		config['NAGS']['NEWUSER'] = 'True'
		config.add_section('STARTUP')
		config['STARTUP']['CONFIG'] = 'False'
		config.add_section('TOOLS')
		config['TOOLS']['FIRMWARE'] = 'False'
		configPath = os.path.expanduser('~/.config/measct/mesact.conf')
		with open(configPath, 'w') as cf:
			config.write(cf)
		parent.newUserCB.setChecked(True)
		newuser(parent)
	else: # .config/measct/mesact.conf exists then read it
		readconfig(parent)

	# get emc version if installed
	parent.emcVersionLB.clear()
	emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
	if emc:
		# get second line
		line = emc.split('\n')[1]
		version = line.split()[1]
		if ':' in version:
			version = version.split(':')[1]
		if '+' in version:
			version = version.split('+')[0]
		if 'none' in version:
			parent.emcVersionLB.setText('Not Installed')
		else:
			parent.emcVersionLB.setText(version)

	# load card images
	parent.configNameLE.setFocus()
	pixmap = QPixmap(os.path.join(parent.lib_path, '7i76.png'))
	parent.card7i76LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.lib_path, '7i77.png'))
	parent.card7i77LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i33-card.png'))
	parent.card7i33LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i37-card.png'))
	parent.card7i37LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i47-card.png'))
	parent.card7i47LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i48-card.png'))
	parent.card7i48LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i76-card.png'))
	parent.card7i76LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i77-card.png'))
	parent.card7i77LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i78-card.png'))
	parent.card7i78LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i85-card.png'))
	parent.card7i85LB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i85s-card.png'))
	parent.card7i85sLB.setPixmap(pixmap)
	pixmap = QPixmap(os.path.join(parent.image_path, '7i88-card.png'))
	parent.card7i88LB.setPixmap(pixmap)

def readconfig(parent):
	config = ConfigParser()
	config.optionxform = str
	configPath = os.path.expanduser('~/.config/measct/mesact.conf')
	if os.path.isfile(os.path.expanduser('~/.config/measct/mesact.conf')):
		rebuild = False
		config.read(os.path.expanduser('~/.config/measct/mesact.conf'))
		if config.has_option('NAGS', 'NEWUSER'):
			if config['NAGS']['NEWUSER'] == 'True':
				parent.newUserCB.setChecked(True)
				newuser(parent)
		if config.has_option('STARTUP', 'CONFIG'):
			if config['STARTUP']['CONFIG'] != 'False':
				parent.loadini.getini(parent, config['STARTUP']['CONFIG'].lower())
				parent.loadConfigCB.setChecked(True)
		if config.has_option('TOOLS', 'FIRMWARE'):
			if config['TOOLS']['FIRMWARE'] != 'False':
				parent.enableMesaflashCB.setChecked(True)
				utilities.checkmesaflash(parent)

def newuser(parent):
	msg = ('If this is your first time using the '
		'Mesa Configuration Tool press the Documents '
		'Button and read the Basic Usage for general '
		'instructions on getting started.\n'
		'You can turn this notification off on the '
		'Options Tab in the Startup Box'
	)
	parent.infoMsgOk(msg, 'Greetings')

def getpref(parent):
	pass


