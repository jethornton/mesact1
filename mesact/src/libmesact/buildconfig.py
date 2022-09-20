import os, traceback, configparser

from libmesact import settings

from libmesact import checkconfig
#from libmesact import buildsetup
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

	#buildsetup.build(parent)
	buildini.build(parent)
	buildhal.build(parent)
	buildio.build(parent)
	buildmisc.build(parent)
	buildss.build(parent)


