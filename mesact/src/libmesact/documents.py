from functools import partial

from PyQt5.QtWidgets import (QDialog, QLabel, QGridLayout, QPushButton,
	QCheckBox, QDialogButtonBox, QSpacerItem, QSizePolicy, QMenu, QFileDialog)
from PyQt5.Qt import Qt

from libmesact import utilities

class dialog(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		#parent.statusbar.showMessage('Preferences Opened')

		self.setGeometry(250, 250, 250, 250)
		self.manualsPB = QPushButton('Mesa Manuals')

		# center the label and increase the font size
		#manualsPB.setAlignment(Qt.AlignCenter)
		#parent.setFontSize(self.lblDialog, 15)
		gridLayout = QGridLayout()
		gridLayout.addWidget(self.manualsPB,0 ,0 )
		#gridLayout.addWidget(QLabel('Save'),1 ,0 )
		#gridLayout.addWidget(QCheckBox('Save Window Size & Position'),2 ,0 )
		verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding) 
		#gridLayout.addWidget(verticalSpacer, 2, 0)
		#pb = QPushButton('Exit')
		buttonBox = QDialogButtonBox()
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
		gridLayout.addWidget(buttonBox)
		cancelBtn = buttonBox.button(QDialogButtonBox.Cancel)
		cancelBtn.clicked.connect(self.reject)

		saveBtn = buttonBox.button(QDialogButtonBox.Save)
		saveBtn.clicked.connect(partial(self.apply, parent))

		#self.gridLayout.addWidget(pb)
		#pb.clicked.connect(self.close)

		self.setLayout(gridLayout)
		self.docs()

	def docs(self):
		docs = [
			{'Main Boards':['5i24', '5i25', '6i24', '6i25', '7i80DB', '7i80HD',
				'7i90HD', '7i92', '7i92T', '7i93', '7i98']},
			{'Combo Boards':['7i76E', '7i95', '7i96', '7i96S', '7i97', ]},
			{'Daughter Boards':['7i33', '7i37', '7i44', '7i47', '7i48', '7i76',
				'7i77', '7i78', '7i85', '7i85S', '7i88', '7i89', ]},
			{'Smart Serial Boards':['7i64', '7i69', '7i70', '7i71', '7i72', '7i73',
				'7i73 Pins', '7i74', '7i84', '7i87']},
			{'Misc. Boards':['7i77ISOL', 'THCAD', 'THCAD2']},
		]

		button = self.manualsPB
		menu = QMenu()
		menu.triggered.connect(lambda action, button=button: button.setText(action.text()))
		self.add_menu(docs, menu)
		button.setMenu(menu)


	def apply(self, parent):
		pdfs = {'':'',
		'5i24':'parallel/5i24man.pdf',
		'5i25':'parallel/5i25man.pdf',
		'6i24':'parallel/6i24man.pdf',
		'6i25':'parallel/6i25man.pdf',
		'7i80DB':'parallel/7i80dbman.pdf',
		'7i80HD':'parallel/7i80hdman.pdf',
		'7i90HD':'parallel/7i90hdman.pdf',
		'7i92':'parallel/7i92man.pdf',
		'7i92T':'parallel/7i92tman.pdf',
		'7i93':'parallel/7i93man.pdf',
		'7i98':'parallel/7i98man.pdf',
		'7i76E':'parallel/7i76eman.pdf',
		'7i95':'parallel/7i95man.pdf',
		'7i96':'parallel/7i96man.pdf',
		'7i96S':'parallel/7i96sman.pdf',
		'7i97':'parallel/7i97man.pdf',
		'7i33':'motion/7i33man.pdf',
		'7i37':'parallel/7i37man.pdf',
		'7i44':'parallel/7i44man.pdf',
		'7i47':'parallel/7i47man.pdf',
		'7i48':'motion/7i48man.pdf',
		'7i76':'parallel/7i76man.pdf',
		'7i77':'parallel/7i77man.pdf',
		'7i77ISOL':'parallel/7i77isolman.pdf',
		'7i78':'parallel/7i78man.pdf',
		'7i85':'parallel/7i85man.pdf',
		'7i85S':'parallel/7i85sman.pdf',
		'7i88':'parallel/7i88man.pdf',
		'7i89':'parallel/7i89man.pdf',
		'7i64':'parallel/7i64man.pdf',
		'7i69':'parallel/7i69man.pdf',
		'7i70':'parallel/7i70man.pdf',
		'7i71':'parallel/7i71man.pdf',
		'7i72':'parallel/7i72man.pdf',
		'7i73':'parallel/7i73man.pdf',

		'7i74':'parallel/7i74man.pdf',
		'7i84':'parallel/7i84man.pdf',
		'7i87':'parallel/7i87man.pdf',
		'THCAD':'parallel/thcadman.pdf',
		'THCAD2':'parallel/thcad2man.pdf',
		}

		#		'7i73 Pins':'man.pdf',

		# http://www.mesanet.com/pdf/motion/7i48man.pdf
		# http://www.mesanet.com/pdf/motion/7i33man.pdf

		destination = str(QFileDialog.getExistingDirectory(parent, "Select a Directory to Save to"))
		if destination != '':
			manual = pdfs[self.manualsPB.text()]
			pdf_url = f'http://www.mesanet.com/pdf/{manual}'
			pdf_location = f'{destination}/{self.manualsPB.text()}man.pdf'
			utilities.download(parent, pdf_url, pdf_location)
			parent.statusbar.showMessage(f'{self.manualsPB.text()} selected')
		self.close()

	def _okBtn(self):
		print('ok')

	def add_menu(self, data, menu_obj):
		if isinstance(data, dict):
			for k, v in data.items():
				sub_menu = QMenu(k, menu_obj)
				menu_obj.addMenu(sub_menu)
				self.add_menu(v, sub_menu)
		elif isinstance(data, list):
			for element in data:
				self.add_menu(element, menu_obj)
		else:
			action = menu_obj.addAction(data)
			action.setIconVisibleInMenu(False)
