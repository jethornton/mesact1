import os, subprocess
from configparser import ConfigParser
from PyQt5.QtGui import QPixmap

from libmesact import loadini
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
		config['NAGS']['MESAFLASH'] = 'True'
		config['NAGS']['NEWUSER'] = 'True'
		config.add_section('STARTUP')
		config['STARTUP']['CONFIG'] = 'False'
		configPath = os.path.expanduser('~/.config/measct/mesact.conf')
		with open(configPath, 'w') as cf:
			config.write(cf)
	# update config file
	if os.path.isfile(os.path.expanduser('~/.config/measct/mesact.conf')):
		pass

	parent.emcVersionLB.clear()
	emc = subprocess.check_output(['apt-cache', 'policy', 'linuxcnc-uspace'], encoding='UTF-8')
	for line in emc.split('\n'):
		if 'installed' in line.casefold():
			if '+' in line:
				line = line.split('+')[0]
			#print(line[line.index('2'):])
			parent.emcVersionLB.setText(line[line.index('2'):])
			break
		else:
			parent.emcVersionLB.setText('Not Installed')

	try:
		mf = subprocess.check_output('mesaflash', encoding='UTF-8')
		if len(mf) > 0:
			parent.mesaflashVersionLB.setText(mf.split()[2])
	except FileNotFoundError as error:
		parent.mesaflashVersionLB.setText('Not Installed')
	parent.mainTabs.setTabEnabled(3, False)
	parent.mainTabs.setTabEnabled(4, False)
	parent.cardTabs.setTabEnabled(1, False)
	parent.spindleGB.setEnabled(False)
	parent.spindlepidGB.setEnabled(False)
	parent.minAngJogVelDSB.setEnabled(False)
	parent.defAngJogVelDSB.setEnabled(False)
	parent.maxAngJogVelDSB.setEnabled(False)
	parent.spindleStepgenGB.setEnabled(False)

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

def checkconfig(parent):
	config = ConfigParser()
	config.optionxform = str
	configPath = os.path.expanduser('~/.config/measct/mesact.conf')
	if os.path.isfile(os.path.expanduser('~/.config/measct/mesact.conf')):
		rebuild = False
		config.read(os.path.expanduser('~/.config/measct/mesact.conf'))
		if config.has_option('NAGS', 'mesaflash'):
			config.remove_option('NAGS', 'mesaflash')
			rebuild = True
		if config.has_option('NAGS', 'newuser'):
			config.remove_option('NAGS', 'newuser')
			rebuild = True
		if rebuild:
			config['NAGS']['MESAFLASH'] = 'True'
			config['NAGS']['NEWUSER'] = 'True'
			with open(configPath, 'w') as cf:
				config.write(cf)

		if config.has_option('NAGS', 'MESAFLASH'):
			if config['NAGS']['MESAFLASH'] == 'True':
				parent.checkMesaflashCB.setChecked(True)
				checkmf(parent)
		if config.has_option('NAGS', 'NEWUSER'):
			if config['NAGS']['NEWUSER'] == 'True':
				parent.newUserCB.setChecked(True)
				newuser(parent)
		if config.has_option('STARTUP', 'CONFIG'):
			if config['STARTUP']['CONFIG'] != 'False':
				loadini.openini(parent, config['STARTUP']['CONFIG'].lower())
	else:
		config = ConfigParser()
		config.optionxform = str
		config.add_section('NAGS')
		config['NAGS']['MESAFLASH'] = 'True'
		config['NAGS']['NEWUSER'] = 'True'
		with open(os.path.expanduser('~/.config/measct/mesact.conf'), 'w') as configfile:
			config.write(configfile)
		parent.checkMesaflashCB.setChecked(True)
		checkmf(parent)
		parent.newUserCB.setChecked(True)
		newuser(parent)

def checkmf(parent):
	# only check to see if it's installed here mesaflashVersionLB
	try:
		subprocess.check_output('mesaflash', encoding='UTF-8')
	except FileNotFoundError:
		#parent.errorMsgOk(('Mesaflash not found go to\n'
		#	'https://github.com/LinuxCNC/mesaflash\n'
		#	'for installation instructions.'), 'Notice! Can Not Flash Firmware')
		t = ('Mesaflash not found go to\n'
			'https://github.com/LinuxCNC/mesaflash\n'
			'for installation instructions.\n'
			'This check can be turned off\n'
			'in the Options tab')
		parent.errorMsgOk(t,'Mesaflash')
		#parent.machinePTE.appendPlainText(t)
		parent.firmwareCB.setEnabled(False)
		parent.readpdPB.setEnabled(False)
		parent.readhmidPB.setEnabled(False)
		parent.flashPB.setEnabled(False)
		parent.reloadPB.setEnabled(False)
		parent.verifyPB.setEnabled(False)
		parent.statusbar.showMessage('Mesaflash not found!')

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


