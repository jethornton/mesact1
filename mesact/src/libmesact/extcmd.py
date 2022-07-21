import os
from subprocess import Popen, PIPE
from PyQt5.QtCore import QProcess

"""
Usage extcmd.job(self, cmd="something", args="",
dest=self.QPlainTextEdit, clean="file to delete when done")

To pipe the output of cmd1 to cmd2 use the following
Usage extcmd.pipe_job(self, cmd1="something", arg1="", cmd2="pipe to",
arg2, "", dest=self.QPlainTextEdit)
"""

class extcmd:
	def __init__(self):
		super().__init__()

		self.p1 = None  # Default empty value.
		self.p2 = None  # Default empty value.

		self.destination = None
		self.cleanup = None

	def message(self, text):
		if self.destination:
			self.destination.appendPlainText(text)

	def pipe_job(self, **kwargs):
		cmd1 = kwargs.get('cmd1')
		arg1 = kwargs.get('arg1')
		cmd2 = kwargs.get('cmd2')
		arg2 = kwargs.get('arg2')
		self.destination = kwargs.get('dest')
		self.destination.clear()
		self.p1 = QProcess()
		self.p2 = QProcess()
		self.p1.setStandardOutputProcess(self.p2)
		self.p1.errorOccurred.connect(self.p1_handle_error)
		self.p1.stateChanged.connect(self.p1_handle_state)
		self.p2.readyReadStandardOutput.connect(self.p2_handle_stdout)
		self.p2.readyReadStandardError.connect(self.p2_handle_stderr)
		self.p2.stateChanged.connect(self.p2_handle_state)
		self.p2.errorOccurred.connect(self.p2_handle_error)
		# Clean up once complete.
		self.p2.finished.connect(self.p2_process_finished)
		if arg1:
			self.p1.start(cmd1, [arg1])
		else:
			self.p1.start(cmd1)
		if arg2:
			self.p2.start(cmd2, [arg2])
		else:
			self.p2.start(cmd2)

	def job(self, **kwargs):
		cmd = kwargs.get('cmd')
		args = kwargs.get('args')
		self.destination = kwargs.get('dest')
		#self.destination.clear()
		self.cleanup = kwargs.get('clean')
		self.p1 = QProcess()
		if self.destination:
			self.destination.clear()
		self.p1.readyReadStandardOutput.connect(self.p1_handle_stdout)
		self.p1.readyReadStandardError.connect(self.p1_handle_stderr)
		self.p1.errorOccurred.connect(self.p1_handle_error)
		self.p1.stateChanged.connect(self.p1_handle_state)
		# Clean up once complete.
		self.p1.finished.connect(self.p1_process_finished)
		if args:
			self.p1.start(cmd, args)
		else:
			self.p1.start(cmd)
		if self.destination:
			self.message(f"Executing process {self.p1.program()}")

	def p1_handle_stderr(self):
		data = self.p1.readAllStandardError()
		stderr = bytes(data).decode("utf8")
		if type(self.destination) != str:
			self.message(stderr)
		else:
			self.message = stderr

	def p1_handle_stdout(self):
		data = self.p1.readAllStandardOutput()
		stdout = bytes(data).decode("utf8")
		if type(self.destination) != str:
			self.message(stdout)
		else:
			self.message = stdout

	def p1_handle_state(self, state):
		states = {   
			QProcess.NotRunning: 'Not running',
			QProcess.Starting: 'Starting',
			QProcess.Running: 'Running',
		}
		state_name = states[state]
		if not self.p1.errorOccurred:
			self.message(f"State changed: {state_name}")

	def p1_process_finished(self):
		self.message("Process finished.")
		self.p1 = None
		if self.cleanup:
			os.remove(self.cleanup)

	def p1_handle_error(self):
		errors = {
			0:'Failed to Start',
			1:'Crashed',
			2:'Timedout',
			3:'ReadError',
			4:'WriteError',
			5:'UnknownError',
			}
		if type(self.destination) != str:
			self.message(f"{self.p1.program()} had the following error:\nerrors.get(self.p.error())")

	def p2_handle_stderr(self):
		data = self.p2.readAllStandardError()
		stderr = bytes(data).decode("utf8")
		self.message(stderr)

	def p2_handle_stdout(self):
		data = self.p2.readAllStandardOutput()
		stdout = bytes(data).decode("utf8")
		self.message(stdout)

	def p2_handle_state(self, state):
		states = {   
			QProcess.NotRunning: 'Not running',
			QProcess.Starting: 'Starting',
			QProcess.Running: 'Running',
		}
		state_name = states[state]
		if not self.p2.errorOccurred:
			self.message(f"State changed: {state_name}")

	def p2_process_finished(self):
		self.message("Process finished.")
		self.p2 = None        

	def p2_handle_error(self):
		errors = {
			0:'Failed to Start',
			1:'Crashed',
			2:'Timedout',
			3:'ReadError',
			4:'WriteError',
			5:'UnknownError',
			}
		self.message(f"{self.p2.program()} had the following error:\nerrors.get(self.p.error())")
