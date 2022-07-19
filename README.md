# mesact

Due to my perception that no one used this tool I removed it only to find that
a user uses my tool and requested that I restore it so I'm restoring it.

If I can help just one person then all the thousands of hours of beating my head
against the desk, searching the internet for coding examples and all the coding
done on this tool it is worth the effort.

The Mesa Configuration Tool is designed to create LinuxCNC configuration for the
following boards 5i25, 6i25, 7i76E, 7i80DB, 7i80HD, 7i92, 7i93, 7i95, 7i96,
7i96S, 7i97 and 7i98.

The Mesa Configuration Tool will create a complete configuration from scratch.
This way you can modify values in the ini file and when you run the Mesa
Configuration Tool again those changes are not lost.

The Mesa Configuration Tool reads in the ini configuration file for changes.

You can create a configuration then run it with the Axis GUI and use
Machine > Calibration to tune each axis. Save the values to the ini file and
next time you run the Mesa Configuration Tool it will read the values from the
ini file.

The Mesa Configuration Tool requires Python 3.6 or newer to work.

See the [documentation](https://gnipsel.com/mesa/mesact/index.html) for installation and
usage instructions.

Note: The Mesa 7i96 requires LinuxCNC 2.8 Uspace or newer to work.
[LinuxCNC 2.8](https://gnipsel.com/linuxcnc/uspace/debian10-emc.html)

Note: The Mesa 7i96S requires LinuxCNC 2.9 (Master) or newer to work and it
requires Mesaflash 3.4.3 or newer to flash or read the board.

