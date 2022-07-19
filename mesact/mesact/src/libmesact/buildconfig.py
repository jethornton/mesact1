import os, traceback, configparser
 
from libmesact import checkconfig
from libmesact import buildini
from libmesact import buildhal
from libmesact import buildio
from libmesact import buildmisc
from libmesact import buildss
from libmesact import utilities

def build(parent):

	if not checkconfig.checkit(parent):
		parent.machinePTE.appendPlainText('Build Failed')
		return
	if parent.backupCB.isChecked():
		utilities.backupFiles(parent)

	config = configparser.ConfigParser()
	config.add_section('NAGS')
	if parent.checkMesaflashCB.isChecked():
		config['NAGS']['MESAFLASH'] = 'True'
	else:
		config['NAGS']['MESAFLASH'] = 'False'
	if parent.newUserCB.isChecked():
		config['NAGS']['NEWUSER'] = 'True'
	else:
		config['NAGS']['NEWUSER'] = 'False'


	config.add_section('STARTUP')
	if parent.loadConfigCB.isChecked():
		config['STARTUP']['CONFIG'] = parent.configName.text()
	else:
		config['STARTUP']['CONFIG'] = 'False'
	with open(os.path.expanduser('~/.config/measct/mesact.conf'), 'w') as configfile:
		config.write(configfile)

		if config.has_option('NAGS', 'MESAFLASH'):
			if config['NAGS']['MESAFLASH'] == 'True':
				parent.checkMesaflashCB.setChecked(True)
		if config.has_option('NAGS', 'MESAFLASH'):
			if config['NAGS']['NEWUSER'] == 'True':
				parent.newUserCB.setChecked(True)

	# check for linuxcnc paths
	if not os.path.exists(os.path.expanduser('~/linuxcnc')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc'))
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if not os.path.exists(os.path.expanduser('~/linuxcnc/configs')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc/configs'))
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if not os.path.exists(os.path.expanduser('~/linuxcnc/nc_files')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc/nc_files'))
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if not os.path.exists(os.path.expanduser('~/linuxcnc/subroutines')):
		try:
			os.mkdir(os.path.expanduser('~/linuxcnc/subroutines'))
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	buildini.build(parent)
	buildhal.build(parent)
	buildio.build(parent)
	buildmisc.build(parent)
	buildss.build(parent)


