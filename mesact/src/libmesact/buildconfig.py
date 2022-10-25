import os, traceback, configparser

from libmesact import settings

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

	settings.update(parent)

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

	if os.path.exists(iniFile):
		parent.updateini.update(parent, iniFile)
	else:
		buildini.build(parent)

	# build halfiles.hal
	halfiles = []
	halfiles.append(f'source {os.path.join(parent.configNameUnderscored + ".hal")}')
	halfiles.append('source io.hal')
	if parent.customhalCB.isChecked():
		halfiles.append('source custom.hal')
	if parent.ssCardCB.currentData():
		halfiles.append('source sserial.hal')

	with open(os.path.join(parent.configPath, 'filelist' + '.hal'), 'w') as f:
		f.write('\n'.join(halfiles))

	#buildini.build(parent)
	buildhal.build(parent)
	buildio.build(parent)
	buildmisc.build(parent)
	buildss.build(parent)


