import os, sys, subprocess
from subprocess import Popen, PIPE
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialogButtonBox
from libmesact import functions

def getPassword(parent):
	dialog = 'You need root privileges\nfor this operation.\nEnter your Password:'
	password, okPressed = QInputDialog.getText(parent, 'Password Required', dialog, QLineEdit.Password, "")
	if okPressed and password != '':
		return password

def check_ip(parent):
	if not parent.ipAddressCB.currentData():
		parent.errorMsgOk('An IP address must be selected', 'Error!')
		return False
	return True

'''
def check_emc():
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		return True
	else:
		return False
'''

def check_mesaflash():
	if subprocess.call(['which', 'mesaflash']) == 0:
		return True
	else:
		return False

def getResults(parent, prompt, result):
	if result == 0:
		output = prompt[0]
	else:
		output = prompt[1]
	parent.machinePTE.clear()
	parent.machinePTE.setPlainText(f'Return Code: {result}')
	parent.machinePTE.appendPlainText(output)

def checkCard(parent):
	prompt = None
	board = parent.device
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if not check_mesaflash():
		parent.errorMsgOk(f'Mesaflash is not Installed', 'Error')
		return

	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', board, '--addr', ipAddress], stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', board],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode)

def readpd(parent):
	prompt = None
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', parent.device, '--addr', ipAddress, '--print-pd'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.device, '--print-pd'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')
	if prompt:
		getResults(parent, prompt, p.returncode)

def readhmid(parent):
	prompt = None
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', parent.device, '--addr', ipAddress, '--readhmid'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.device, '--readhmid'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode)

def flashCard(parent):
	prompt = None
	arguments = []
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to flash the {parent.board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if check_ip(parent):
				ipAddress = parent.ipAddressCB.currentText()
				p = Popen(['mesaflash', '--device', parent.device, '--addr', ipAddress, '--write', firmware],
					stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.device, '--write', firmware],
					stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode)

	else:
		parent.errorMsgOk('A firmware must be selected', 'Error!')
		return

def reloadCard(parent):
	prompt = None
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to reload the {board}', 'Error')
		return
	if parent.boardType == 'eth':
		if check_ip(parent):
			ipAddress = parent.ipAddressCB.currentText()
			p = Popen(['mesaflash', '--device', parent.device, '--addr', ipAddress, '--reload'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
		else:
			return

	elif parent.boardType == 'pci':
		if not parent.password:
			password = getPassword(parent)
			parent.password = password
		if parent.password != None:
			p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.device, '--reload'],
				stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate(parent.password + '\n')

	if prompt:
		getResults(parent, prompt, p.returncode)

def verifyCard(parent):
	prompt = None
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to verify the {board}', 'Error')
		return
	if parent.firmwareCB.currentData():
		firmware = os.path.join(parent.lib_path, parent.firmwareCB.currentData())
		if parent.boardType == 'eth':
			if check_ip(parent):
				ipAddress = parent.ipAddressCB.currentText()
				p = Popen(['mesaflash', '--device', parent.device, '--addr', ipAddress, '--verify', firmware],
					stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate()
			else:
				return

		elif parent.boardType == 'pci':
			if not parent.password:
				password = getPassword(parent)
				parent.password = password
			if parent.password != None:
				p = Popen(['sudo', '-S', 'mesaflash', '--device', parent.device, '--verify', firmware],
					stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
				prompt = p.communicate(parent.password + '\n')

		if prompt:
			getResults(parent, prompt, p.returncode)
	else:
		parent.errorMsgOk('A firmware must be selected', 'Error!')
		return

def getCardPins(parent):
	if parent.boardType == '':
		parent.errorMsgOk(f'No Board Selected\non the Machine Tab', 'Error')
		return

	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to read the {parent.board}', 'Error')
		return

	prompt = None
	if parent.boardType == 'eth':
		if check_ip(parent):
			with open('temp.hal', 'w') as f:
				f.write('loadrt hostmot2\n')
				f.write(f'loadrt hm2_eth board_ip={parent.ipAddressCB.currentText()}\n')
				f.write('quit')
			p = Popen(['halrun', '-f', 'temp.hal'], stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
			prompt = p.communicate()
			os.remove('temp.hal')
		else:
			return

	elif parent.boardType == 'pci':
		with open('temp.hal', 'w') as f:
			f.write('loadrt hostmot2\n')
			f.write(f'loadrt hm2_eth board_ip={parent.ipAddressCB.currentText()}\n')
			f.write('quit')

	print(f'returncode {p.returncode}')
	getResults(parent, prompt, p.returncode)


def savePins(parent):
	if parent.configNameLE.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configNameLE.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show pin')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-pins.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Pins saved to {fp}')

def saveSignals(parent):
	if parent.configNameLE.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configNameLE.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show sig')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-sigs.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Signals saved to {fp}')

def saveParameters(parent):
	if parent.configNameLE.text() == '':
		parent.errorMsgOk('A Configuration\nmust be loaded', 'Error')
		return
	if not "0x48414c32" in subprocess.getoutput('ipcs'):
		parent.errorMsgOk(f'LinuxCNC must be running\nthe {parent.configNameLE.text()} configuration', 'Error')
		return
	parent.results = subprocess.getoutput('halcmd show parameter')
	fp = os.path.join(parent.configPath, parent.configNameUnderscored + '-parameters.txt')
	with open(fp, 'w') as f:
		f.writelines(parent.results)
	parent.statusbar.showMessage(f'Parameters saved to {fp}')

def firmwarePins(parent):
	if parent.firmwareCB.currentData():
		bitFile = os.path.join(parent.firmware_path, parent.firmwareCB.currentData())
		pinFile = os.path.splitext(bitFile)[0]+'.pin'
		if os.path.exists(pinFile):
			parent.machinePTE.clear()
			with open(pinFile, 'r') as file:
				data = file.read()
			parent.machinePTE.appendPlainText(data)
		else:
			parent.machinePTE.clear()
			parent.machinePTE.appendPlainText(f'No pin file found for {os.path.basename(bitFile)}')
	else:
		parent.machinePTE.clear()
		parent.machinePTE.appendPlainText('Select a Firmware to view pins')
