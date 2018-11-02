# Raspberry Pi Based Heating Controller

The circuit for this is stored under the kicad directory

# Adafruit Python MCP3008

Python code to use the MCP3008 analog to digital converter with a Raspberry Pi or BeagleBone black.

## Installation

To install the library from source (recommended) run the following commands on a Raspberry Pi or other Debian-based OS system:

    sudo apt-get install git build-essential python-dev
    cd ~
    git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
    cd Adafruit_Python_MCP3008
    sudo python setup.py install

Alternatively you can install from pip with:

    sudo pip install adafruit-mcp3008

Note that the pip install method **won't** install the example code.


#WiringPi

See jonsblog.lidgard.uk/cross-compile
and info held in cpp/build-libDigiPot


# Heating Controller Code

## This code should be run as a daemon

The heating controller connects to a worcester-bosch combi boiler via the TR2 interface (3 4 F) & acts to control demand for heating.
It has it's own TR2 interface for connecting to the existing thermostat but also has 3 'Call For Heat' connections to allow Nest & other devices to control the boiler in a zoned setup.

Control Flow:
* Set the Boiler output to be off using the X9C digital programmable pots.
* Read the TR2 resistances between 3&4 & F&4 to get thermostat mode and sensed temperature.
* Drive the zone valve & when the zone valve is open:
* Set the Boiler output to mimic those resistances using the X9C digital programmable pots.
* If any CFH contacts made, 

Set the X9C to