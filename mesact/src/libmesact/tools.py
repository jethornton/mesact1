import subprocess
from libmesact import functions

def runLatencyHisogram(parent):
	# check to see if emc is running
	if functions.check_emc():
		parent.errorMsgOk(f'LinuxCNC must NOT be running\n to run the Latency Histogram', 'Error')
		return

	cmd = ['latency-histogram']
	if parent.latencyTestNoBaseCB.isChecked():
		cmd.append('--nobase')
	if parent.latencyTestShowCB.isChecked():
		cmd.append('--show')

	subprocess.run(cmd)
	#subprocess.run(["latency-histogram", "--nobase", "--show"])

"""
   latency-histogram [Options]

Options:
  --base      nS   (base  thread interval, default:   25000, min:  5000)
  --servo     nS   (servo thread interval, default: 1000000, min: 25000)
  --bbinsize  nS   (base  bin size,  default: 100
  --sbinsize  nS   (servo bin size, default: 100
  --bbins     n    (base  bins, default: 200
  --sbins     n    (servo bins, default: 200
  --logscale  0|1  (y axis log scale, default: 1)
  --text      note (additional note, default: "" )
  --show           (show count of undisplayed bins)
  --nobase         (servo thread only)
  --verbose        (progress and debug)

Notes:
  Linuxcnc and Hal should not be running, stop with halrun -U.
  Large number of bins and/or small binsizes will slow updates.
  For single thread, specify --nobase (and options for servo thread).
  Measured latencies outside of the +/- bin range are reported
  with special end bars.  Use --show to show count for
  the off-chart [pos|neg] bin
"""
