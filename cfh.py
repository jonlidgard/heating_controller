import wiringpi
from common import bounce_check

CFH_PINS = [7,21,22]

class CFH:
    def __init__(self,cfh_no, notifier):
        self._notifier = notifier
        if cfh_no < 1 or cfh_no > len(CFH_PINS):
            raise IndexError('CFH out of range')
        self._cfh_no = cfh_no
        pin = CFH_PINS[cfh_no-1]
        wiringpi.pinMode(pin, 0)
        self._pin_state = {'pin': pin, 'old': -1, 'new': -1, 'stable': -1, 'samples': -1}

    def get_channel(self):
        return self._cfh_no

    def get_state(self):
        return self._pin_state['stable']

    def get_contact_state(self):        
        # get the new pin state
        self._pin_state['new'] = 1-wiringpi.digitalRead(self._pin_state['pin'])
        self._pin_state = bounce_check(self._pin_state)

        return self._pin_state['stable']

    def poll(self):
        self.get_contact_state()
        print (self._pin_state)
        if self._pin_state['old']  != self._pin_state['stable']:
            print ('Notify')
            self._notifier(self) 

# Tests

def printState(cfh):
    state = (cfh.get_state())
    print ('CFH:', cfh.get_channel(), '-', state)


if __name__ == "__main__":
    import time

    wiringpi.wiringPiSetup()
    cfh1 = CFH(1, printState)
    cfh2 = CFH(2, printState)
    cfh3 = CFH(3, printState)
    cfhs = [cfh1] #,cfh2,cfh3]

    while True:
        for cfh in cfhs:
            print ("Running")
            cfh.poll()
        time.sleep(.5)