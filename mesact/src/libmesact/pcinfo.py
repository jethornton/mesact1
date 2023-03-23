import subprocess
from subprocess import Popen, PIPE
from libmesact import card
from libmesact import functions
from libmesact import utilities

"""
Usage extcmd.job(self, cmd="something", args="",
dest=self.QPlainTextEdit, clean="file to delete when done")

To pipe the output of cmd1 to cmd2 use the following
Usage extcmd.pipe_job(self, cmd1="something", arg1="", cmd2="pipe to",
arg2, "", dest=self.QPlainTextEdit)
"""

def ipInfo(parent):
	ip = subprocess.check_output(['ip', '-br', 'addr', 'show'], encoding='UTF-8')
	parent.ipInfoPTE.setPlainText(ip)

def mbInfo(parent):
	if not parent.password:
		password = utilities.getPassword(parent)
		parent.password = password
	if parent.password != None:
		p = Popen(['sudo', '-S', 'dmidecode', '-t 2'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate(parent.password + '\n')

		if prompt:
			parent.infoPTE.clear()
			if p.returncode == 0:
				output = prompt[0]
			else:
				output = prompt[1]
			parent.infoPTE.setPlainText(f'Return Code: {p.returncode}')
			parent.infoPTE.appendPlainText(output)

def cpuInfo(parent):
	parent.extcmd.job(cmd="lscpu", args=None, dest=parent.infoPTE)

def nicInfo(parent):
	parent.extcmd.job(cmd="lspci", args=None, dest=parent.infoPTE)

def nicCalc(parent):
	cpuSpeedText = int(parent.cpuSpeedLE.text())
	readtmaxText = int(parent.readtmaxLE.text())
	writetmaxText = int(parent.writetmaxLE.text())
	if cpuSpeedText != '' and readtmaxText != '' and writetmaxText != '':
		readtmax = int(readtmaxText / 1000)
		writetmax = int(writetmaxText / 1000)
		tMax = readtmax + writetmax
		cpuSpeed = int(cpuSpeedText)
		print(f'parent.cpuSpeedCB.currentData() {parent.cpuSpeedCB.currentData()}')
		print(f'tMax {tMax}')
		print(f'cpuSpeed {cpuSpeed}')
		packetTime = tMax / cpuSpeed
		parent.packetTimeLB.setText(f'{packetTime:.1%}')
	else:
		errorText = []
		if parent.cpuSpeedLE.text() == '':
			errorText.append('CPU Speed can not be empty')
		if parent.readtmaxLE.text() == '':
			errorText.append('read.tmax can not be empty')
		if parent.writetmaxLE.text() == '':
			errorText.append('write.tmax can not be empty')
		parent.errorMsgOk('\n'.join(errorText))

def readServoTmax(parent):
	if "0x48414c32" in subprocess.getoutput('ipcs'):
		p = Popen(['halcmd', 'show', 'param', 'servo-thread.tmax'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate()
		if prompt:
			parent.tmaxPTE.appendPlainText(prompt[0])
			ret = prompt[0].splitlines()
			parent.servoThreadTmaxLB.setText(ret[2].split()[3])
	else:
		parent.errorMsgOk('LinuxCNC must be running this configuration!','Error')

def calcServoPercent(parent):
	cpu_speed_Hz = int(parent.cpuSpeedLE.text()) * parent.cpuSpeedCB.currentData()
	#cpu_speed_Hz = int(2333) * parent.cpuSpeedCB.currentData()
	print(f'cpu_speed_Hz: {cpu_speed_Hz}')
	cpu_clock_time = 0.000000001 * parent.servoPeriodSB.value()
	print(f'cpu_clock_time: {cpu_clock_time}')
	clocks_per_period = int(cpu_speed_Hz * cpu_clock_time)
	print(f'clocks_per_period: {clocks_per_period}')
	servoTmax = 1747291
	#servoTmax = int(parent.servoThreadTmaxLB.text())
	cpu_clocks_used = servoTmax / clocks_per_period
	print(f'cpu_clocks_used: {cpu_clocks_used}')
	result = cpu_clocks_used * 100
	parent.servoResultLB.setText(f'{result:.0f}%')

def readTmax(parent):
	if not functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must be running\nto get read.tmax', 'Error')
		return

	p = Popen(['halcmd', 'show', 'param', 'hm2*read.tmax'],
		stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
	prompt = p.communicate()
	if prompt:
		parent.tmaxPTE.appendPlainText(prompt[0])
		if 'hm2' in prompt[0]:
			ret = prompt[0].splitlines()
			parent.readtmaxLE.setText(ret[2].split()[3])
		else:
			parent.errorMsgOk(f'LinuxCNC must be running\na Mesa Ethernet configuration\nto get read.tmax', 'Error')

def writeTmax(parent):
	if not functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must be running\nto get write.tmax', 'Error')
		return
	p = Popen(['halcmd', 'show', 'param', 'hm2*write.tmax'],
		stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
	prompt = p.communicate()
	if prompt:
		parent.tmaxPTE.appendPlainText(prompt[0])
		if 'hm2' in prompt[0]:
			ret = prompt[0].splitlines()
			parent.writetmaxLE.setText(ret[2].split()[3])
	else:
		parent.errorMsgOk(f'LinuxCNC must be running\na Mesa Ethernet configuration\nto get write.tmax', 'Error')


def cpuSpeed(parent):
	if not parent.password:
		password = card.getPassword(parent)
		parent.password = password
	if parent.password != None:
		p = Popen(['sudo', '-S', 'dmidecode'],
			stdin=PIPE, stderr=PIPE, stdout=PIPE, text=True)
		prompt = p.communicate(parent.password + '\n')
	if prompt:
		ret = prompt[0].splitlines()

		for line in ret: 
			if 'MHz' in line:
				parent.tmaxPTE.appendPlainText(line.strip())

