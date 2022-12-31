import os, requests, subprocess, tarfile
import urllib.request

from packaging import version

from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox

'''

'''

def downloadFirmware(parent):
	board = parent.boardCB.currentData()
	if board:
		libpath = os.path.join(os.path.expanduser('~'), '.local/lib/libmesact')
		if not os.path.exists(libpath):
			os.makedirs(libpath)
		firmware_url = f'https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/{board}.tar.xz'
		destination = os.path.join(os.path.expanduser('~'), f'.local/lib/libmesact/{board}.tar.xz')
		#print(f'{libpath}\n{firmware_url}\n{destination}')
		#print('Downloading')
		download(parent, firmware_url, destination)
		#print('Download Done')
		with tarfile.open(destination) as f:
			f.extractall(libpath)
		if os.path.isfile(destination):
			os.remove(destination)
		# update firmware tab
		#print(f'Download {firmware_url}\n{destination}')
		# https://github.com/jethornton/mesact_firmware/releases/download/1.0.0/5i24.tar.xz
	else:
		parent.infoMsgOk('Select a Board', 'Board')

def checkUpdates(parent):
	response = requests.get(f"https://api.github.com/repos/jethornton/mesact/releases/latest")
	repoVersion = response.json()["name"]
	if version.parse(repoVersion) > version.parse(parent.version):
		parent.machinePTE.appendPlainText(f'A newer version {repoVersion} is available for download')
	elif version.parse(repoVersion) == version.parse(parent.version):
		parent.machinePTE.appendPlainText(f'The Repo version {repoVersion} is the same as this version')

def downloadAmd64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} amd64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_amd64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_amd64.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArmhDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} armhf Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_armhf.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_armhf.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArm64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} arm64 Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_arm64.deb')
		deburl = f'https://github.com/jethornton/mesact/releases/download/{repoVersion}/mesact_{repoVersion}_arm64.deb'
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
		parent.infoMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')


def download(parent, down_url, save_loc):
	def Handle_Progress(blocknum, blocksize, totalsize):
		## calculate the progress
		readed_data = blocknum * blocksize
		if totalsize > 0:
			download_percentage = readed_data * 100 / totalsize
			parent.progressBar.setValue(int(download_percentage))
			QApplication.processEvents()
	urllib.request.urlretrieve(down_url, save_loc, Handle_Progress)
	parent.progressBar.setValue(100)
	parent.timer.start(1000)
	#return True

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.timer.stop()

def showDocs(parent, pdfDoc):
	docPath = False
	if isinstance(pdfDoc, str):
		docPath = os.path.join(parent.docs_path, pdfDoc)
	elif isinstance(pdfDoc, QComboBox):
		if pdfDoc.currentData():
			docPath = os.path.join(parent.docs_path, pdfDoc.currentData())
		else:
			parent.errorMsgOk('Select a Manual First!', 'Error')
	if docPath:
		subprocess.call(('xdg-open', docPath))

