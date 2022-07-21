Basic Usage
===========

You can left click Check Config at any time to see if there are any errors.

Build Config will check for errors before build the configuration files.

Machine Tab
-----------

#. Enter a Configuration Name

#. Select Linear Units

#. Select Max Linear Velocity

#. Select the Mesa Board

#. Ethernet Boards you must select the IP Address 10.10.10.10 is recommened.

#. Boards like 5i25/6i25, 7i80, 7i92, 7i93, 7i98 to enable the Axes Tab
   and the I/O Tab you need to select a firmware then select a daughter card.


Display Tab
-----------

#. Select a GUI

#. Select Position Offset

#. Select Position Feedback

Axes Tab
--------

#. Select Axis

#. Enter Scale, Minimum Limit, Maximum Limit, Maximum Velocity, Maximum
   Acceleration

#. PID Settings select Default Values

#. Following Error select Default Values

#. For a Step and Direction select your drive or manually enter the Step
   Time, Step Space, Direction Setup, Direction Hold times

#. For a Servo System select Default Values in Analog Output and enter
   the Encoder Scale

#. Left Click Check Config to see if there are any errors

I/O Tab
-------

The selected board will configure the Inputs and Outputs avaliable and
if input debounce is avaliable.

#. Click Select for the I/O you want to use and select what you want it
to be used as.

Spindle Tab
-----------

Used to configure an Analog PWM or Stepgen Spindle. For Digital Run, CW
and CCW type spindles use outputs.

SS Cards Tab
------------

If you have a Smart Serial Card attached you can configure it here.

#. Select the Smart Serial Card and the page changes to that card where
you can make selections for that card


GPIO Tab
--------

Under Construction ATM, going to be where you could use the GPIO of a
pin directly. For example if you have an unused GPIO you could make it
either and input or output and use it.


Tool Changer Tab
----------------

Yet to come

Options Tab
-----------

Here you can select various options for your configuration and whether
to check for Mesaflash at startup or not.

PLC Tab
-------

If your going to be using the Classicladder PLC you can set number of
items created for each type of bit.

Pins Tab
--------

Displays the Terminal Block and pins for the selected card.

On most cards the Raw Output clicking Get Card Pinout will get a list of
pins.

PC Tab
------

You can get information about the PC CPU and NIC on the PC Info Tab.

If your using a Mesa Ethernet card you can test your NIC speed and get
the Packet Time and compare that to Threshold to see if your NIC and CPU
are fast enough at the current Servo Period.
