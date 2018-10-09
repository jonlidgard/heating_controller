# Raspberry Pi Based Heating Controller

The circuit for this is stored under the kicad directory

This code should be run as a daemon

The heating controller connects to a worcester-bosch combi boiler via the TR2 interface (3 4 F) & acts to control demand for heating.
It has it's own TR2 interface for connecting to the existing thermostat but also has 3 'Call For Heat' connections to allow Nest & other devices to control the boiler in a zoned setup.

Control Flow:
* Set the Boiler output to be off using the X9C digital programmable pots.
* Read the TR2 resistances between 3&4 & F&4 to get thermostat mode and sensed temperature.
* Drive the zone valve & when the zone valve is open:
* Set the Boiler output to mimic those resistances using the X9C digital programmable pots.
* If any CFH contacts made, 

Set the X9C to