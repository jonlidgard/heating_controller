from relays import Relay
import wiringpi
import time

wiringpi.wiringPiSetup()
r1 = Relay(1)
r2 = Relay(2)
r3 = Relay(3)
r4 = Relay(4)
relays = [r1,r2,r3,r4]

for i in range(4):
    r = relays[i]
    r.off()

while True:
    for i in range(4):
        r = relays[i]
        r.toggle()
        time.sleep(.5)

