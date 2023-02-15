import os, subprocess
from configparser import ConfigParser
from functools import partial

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QAction, QWidget

from libmesact import utilities
from libmesact import updates

def setup(parent):

	libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact/boards')
	if not os.path.exists(libpath):
		os.makedirs(libpath)

	try:
		parent.resize(parent.settings.value('window size'))
		parent.move(parent.settings.value('window position'))
	except:
		pass
	parent.configNameLE.setFocus()

	# setup tabs and group boxes
	parent.mainTabs.setTabEnabled(3, False)
	parent.mainTabs.setTabEnabled(4, False)
	parent.cardTabs.setTabEnabled(1, False)
	parent.spindleGB.setEnabled(False)
	parent.spindlepwmGB.setEnabled(False)
	parent.spindlepidGB.setEnabled(False)
	parent.minAngJogVelDSB.setEnabled(False)
	parent.defAngJogVelDSB.setEnabled(False)
	parent.maxAngJogVelDSB.setEnabled(False)
	parent.spindleStepgenGB.setEnabled(False)

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

	exitAction = QAction(QIcon.fromTheme('application-exit'), 'Exit', parent)
	#exitAction.setShortcut('Ctrl+Q')
	exitAction.setStatusTip('Exit application')
	exitAction.triggered.connect(parent.close)
	parent.menuFile.addAction(exitAction)

	docsAction = QAction(QIcon.fromTheme('document-open'), 'Mesa Manuals', parent)
	docsAction.setStatusTip('Download Mesa Documents')
	#preferencesAction.triggered.connect(partial(menu.edit_preferences, parent))
	docsAction.triggered.connect(partial(updates.downloadDocs, parent))
	parent.menuDownloads.addAction(docsAction)
	loadBoards(parent)

def loadBoards(parent):
	# load card images
	if os.path.isdir(parent.image_path):
		print(os.path.join(parent.image_path, '7i76.png'))
		pixmap = QPixmap(os.path.join(parent.image_path, '7i76.png'))
		parent.card7i76LB.setPixmap(pixmap)
		pixmap = QPixmap(os.path.join(parent.image_path, '7i77.png'))
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
	else:
		parent.boardLB.setText('No Board Images Found\nDownloads > Board Images')


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


