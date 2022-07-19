import os
from datetime import datetime

def build(parent):
	# if Axis is the GUI add the shutup file
	if parent.guiCB.currentData() == 'axis':
		shutupFilepath = os.path.expanduser('~/.axisrc')
		shutupContents = ['root_window.tk.call("wm","protocol",".","WM_DELETE_WINDOW","destroy .")']
		try: # if this file exists don't write over it
			with open(shutupFilepath, 'x') as shutupFile:
				shutupFile.writelines(shutupContents)
			parent.machinePTE.appendPlainText(f'Building {shutupFilepath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if parent.customhalCB.isChecked():
		customFilePath = os.path.join(parent.configPath, 'custom.hal')
		customContents = []
		customContents = ['# Place any HAL commands in this file that you want to run before the GUI.\n']
		customContents.append('# This file will not be written over by the configuration tool.\n')
		try: # if this file exists don't write over it
			with open(customFilePath, 'x') as customFile:
				customFile.writelines(customContents)
			parent.machinePTE.appendPlainText(f'Building {customFilePath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if parent.postguiCB.isChecked():
		# create the postgui.hal file if not there
		postguiFilePath = os.path.join(parent.configPath, 'postgui.hal')
		postguiContents = []
		postguiContents = ['# Place any HAL commands in this file that you want to run AFTER the GUI finishes loading.\n']
		postguiContents.append('# GUI HAL pins are not visible until after the GUI loads.\n')
		postguiContents.append('# This file will not be written over by the configuration tool.\n')
		try: # if this file exists don't write over it
			with open(postguiFilePath, 'x') as postguiFile:
				postguiFile.writelines(postguiContents)
			parent.machinePTE.appendPlainText(f'Building {postguiFilePath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	if parent.shutdownCB.isChecked():
		# create the shutdown.hal file if not there
		shutdownFilePath = os.path.join(parent.configPath, 'shutdown.hal')
		shutdownContents = []
		shutdownContents = ['# Place any HAL commands in this file that you want to run AFTER the GUI shuts down.\n']
		shutdownContents.append('# this may make it possible to set outputs when LinuxCNC is exited normally.\n')
		shutdownContents.append('# This file will not be written over by the configuration tool.\n')
		try: # if this file exists don't write over it
			with open(shutdownFilePath, 'x') as shutdownFile:
				shutdownFile.writelines(shutdownContents)
			parent.machinePTE.appendPlainText(f'Building {shutdownFilePath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	# create the readme file if text in readmePTE
	if parent.readmePTE.toPlainText():
		readmeFilePath = os.path.join(parent.configPath, 'README')
		with open(readmeFilePath, 'w') as readmeFile:
			readmeFile.writelines(parent.readmePTE.toPlainText())

	# create the tool file if not there
	toolFilePath = os.path.join(parent.configPath, 'tool.tbl')
	toolContents = []
	toolContents = [';\n']
	toolContents.append('T1 P1\n')
	try: # if this file exists don't write over it
		with open(toolFilePath, 'x') as toolFile:
			toolFile.writelines(toolContents)
		parent.machinePTE.appendPlainText(f'Building {toolFilePath}')
	except FileExistsError:
		pass
	except OSError:
		parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	# create the var file if not there
	varFilePath = os.path.join(parent.configPath, parent.configNameUnderscored + '.var')
	try: #
		open(varFilePath, 'x')
	except FileExistsError:
		pass
	except OSError:
		parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	# create the pyvcp panel if checked and not there
	if parent.pyvcpCB.isChecked():
		pyvcpFilePath = os.path.join(parent.configPath, parent.configNameUnderscored + '.xml')
		pyvcpContents = ["<?xml version='1.0' encoding='UTF-8'?>\n"]
		pyvcpContents.append('<pyvcp>\n')
		pyvcpContents.append('<!--\n')
		pyvcpContents.append('Build your PyVCP panel between the <pyvcp></pyvcp> tags.\n')
		pyvcpContents.append('Make sure your outside the comment tags.\n')
		pyvcpContents.append('The contents of this file will not be overwritten\n')
		pyvcpContents.append('when you run this wizard again.\n')
		pyvcpContents.append('-->\n')
		pyvcpContents.append('	<label>\n')
		pyvcpContents.append('		<text>"This is a Sample Label:"</text>\n')
		pyvcpContents.append('		<font>("Helvetica",10)</font>\n')
		pyvcpContents.append('	</label>\n')
		pyvcpContents.append('</pyvcp>\n')
		try: # if this file exists don't write over it
			with open(pyvcpFilePath, 'x') as pyvcpFile:
				pyvcpFile.writelines(pyvcpContents)
			parent.machinePTE.appendPlainText(f'Building {pyvcpFilePath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')

	# create the clp file if selected
	if parent.ladderGB.isChecked():
		ladderFilePath = os.path.join(parent.configPath, parent.configNameUnderscored + '.clp')
		ladderContents = """_FILES_CLASSICLADDER
_FILE-symbols.csv
#VER=1.0
_/FILE-symbols.csv
_FILE-modbusioconf.csv
#VER=1.0
_/FILE-modbusioconf.csv
_FILE-com_params.txt
MODBUS_MASTER_SERIAL_PORT=
MODBUS_MASTER_SERIAL_SPEED=9600
MODBUS_ELEMENT_OFFSET=0
MODBUS_MASTER_SERIAL_USE_RTS_TO_SEND=0
MODBUS_MASTER_TIME_INTER_FRAME=100
MODBUS_MASTER_TIME_OUT_RECEIPT=500
MODBUS_MASTER_TIME_AFTER_TRANSMIT=0
MODBUS_DEBUG_LEVEL=0
MODBUS_MAP_COIL_READ=0
MODBUS_MAP_COIL_WRITE=0
MODBUS_MAP_INPUT=0
MODBUS_MAP_HOLDING=0
MODBUS_MAP_REGISTER_READ=0
MODBUS_MAP_REGISTER_WRITE=0
_/FILE-com_params.txt
_FILE-timers_iec.csv
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
1,0,0
_/FILE-timers_iec.csv
_FILE-timers.csv
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
_/FILE-timers.csv
_FILE-counters.csv
0
0
0
0
0
0
0
0
0
0
_/FILE-counters.csv
_FILE-sections.csv
#VER=1.0
#NAME000=Prog1
000,0,-1,0,0,0
_/FILE-sections.csv
_FILE-arithmetic_expressions.csv
#VER=2.0
_/FILE-arithmetic_expressions.csv
_FILE-rung_0.csv
#VER=2.0
#LABEL=
#COMMENT=
#PREVRUNG=0
#NEXTRUNG=0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0 , 0-0-0/0
_/FILE-rung_0.csv
_FILE-ioconf.csv
#VER=1.0
_/FILE-ioconf.csv
_FILE-monostables.csv
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
1,0
_/FILE-monostables.csv
_FILE-sequential.csv
#VER=1.0
_/FILE-sequential.csv
_FILE-general.txt
PERIODIC_REFRESH=50
SIZE_NBR_RUNGS=100
SIZE_NBR_BITS=500
SIZE_NBR_WORDS=100
SIZE_NBR_TIMERS=10
SIZE_NBR_MONOSTABLES=10
SIZE_NBR_COUNTERS=10
SIZE_NBR_TIMERS_IEC=10
SIZE_NBR_PHYS_INPUTS=15
SIZE_NBR_PHYS_OUTPUTS=15
SIZE_NBR_ARITHM_EXPR=100
SIZE_NBR_SECTIONS=10
SIZE_NBR_SYMBOLS=100
_/FILE-general.txt
_/FILES_CLASSICLADDER
"""

		try: # if this file exists don't write over it
			with open(ladderFilePath, 'x') as ladderFile:
				ladderFile.writelines(ladderContents)
				parent.machinePTE.appendPlainText(f'Building {ladderFilePath}')
		except FileExistsError:
			pass
		except OSError:
			parent.machinePTE.appendPlainText(f'OS error\n {traceback.print_exc()}')
