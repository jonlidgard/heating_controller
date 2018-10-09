import zonevalve
import wiringpi
import time

def printState(valve):
    state = (valve.get_state())
    print ('Valve:', valve.get_channel(), '-', state)
    if (state == "open" or state == "closed"):
        valve.toggle()

wiringpi.wiringPiSetup()
zv1 = zonevalve.ZoneValve(1, printState)
zv2 = zonevalve.ZoneValve(2, printState)
zv3 = zonevalve.ZoneValve(3, printState)
valves = [zv1,zv2,zv3]

for v in valves:
    v.close()
time.sleep(2)
for v in valves:
    v.open()
time.sleep(2)

while True:
    for v in valves:
        v.poll()
    time.sleep(.5)