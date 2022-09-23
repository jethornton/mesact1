import os, requests, subprocess
import urllib.request

from packaging import version

from PyQt5.QtWidgets import QApplication, QFileDialog, QComboBox

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
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_amd64.deb')
		deburl = os.path.join('https://github.com/jethornton/mesact/raw/master/mesact_' + repoVersion + '_amd64.deb')
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArmhDeb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_armhf.deb')
		deburl = os.path.join('https://github.com/jethornton/mesact/raw/master/mesact_' + repoVersion + '_armhf.deb')
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
	else:
		parent.statusbar.showMessage('Download Cancled')

def downloadArm64Deb(parent):
	directory = str(QFileDialog.getExistingDirectory(parent, "Select Directory"))
	if directory != '':
		parent.statusbar.showMessage('Checking Repo')
		response = requests.get("https://api.github.com/repos/jethornton/mesact/releases/latest")
		repoVersion = response.json()["name"]
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Starting')
		destination = os.path.join(directory, 'mesact_' + repoVersion + '_arm64.deb')
		deburl = os.path.join('https://github.com/jethornton/mesact/raw/master/mesact_' + repoVersion + '_arm64.deb')
		download(parent, deburl, destination)
		parent.statusbar.showMessage(f'Mesa Configuration Tool Version {repoVersion} Download Complete')
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

def clearProgressBar(parent):
	parent.progressBar.setValue(0)
	parent.statusbar.clearMessage()
	parent.errorMsgOk('Close the Configuration tool and reinstall', 'Download Complete')
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

