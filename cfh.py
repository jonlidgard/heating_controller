import wiringpi, logging, time
from common import bounce_check
import nextion

CFH_PINS = [7,21,22]

class CFH:
    def __init__(self,cfh_no, name, widget, notifier):
        self._name = name
        self._widget = widget
        self._notifier = notifier
        if cfh_no < 1 or cfh_no > len(CFH_PINS):
            raise IndexError('CFH out of range')
        self._cfh_no = cfh_no
        pin = CFH_PINS[cfh_no-1]
        wiringpi.pinMode(pin, 0)
        self._pin_state = {'pin': pin, 'changed': False, 'new': -1, 'stable': -1, 'samples': -1}
        self._pin_state['new'] = self.get_pin_state()
        self._on_period = 0
        self._off_period = 0
        self._on_time = 0
        self._off_time = 0
        if self._widget:
                self._widget.update(self._pin_state['new'])

        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())

    def get_channel(self):
        return self._cfh_no

    def get_name(self):
        return self._name
        
    def get_name(self):
        return self._name

    def get_state(self):
        return self._pin_state['stable'] == 1

    def get_pin_state(self):
        return 1-wiringpi.digitalRead(self._pin_state['pin'])
    
    def get_on_period(self):
        return self._on_period

    def get_off_period(self):
        return self._off_period

    def calc_timings(self):
        if self.get_state(): # Calling for heat
            self._on_time = time.time()
            if self._on_time > self._off_time and self._off_time > 0:
                self._off_period = (self._on_time - self._off_time) / 60
        else:
            self._off_time = time.time()
            if self._off_time > self._on_time and self._on_time > 0:
                self._on_period = (self._off_time - self._on_time) / 60

    def check_contact_state(self):        
        # get the new pin state
        self._pin_state['new'] = self.get_pin_state()
        self._pin_state = bounce_check(self._pin_state)

    def poll(self):
        self.check_contact_state()
#        print (self._pin_state)
        if self._pin_state['changed'] == True:
            self._pin_state['changed'] = False
            if self._widget:
                self._widget.update(self.get_state())
            
            self.calc_timings()

            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug('Pin state changed: %s',self.get_name())
                if self.get_state():
                    self._logger.debug('%s calling for heat after %dm',self.get_name(), self.get_off_period())
                else:
                    self._logger.debug('%s satisfied after %dm',self.get_name(), self.get_on_period())
            
            self._notifier(self, self.get_name(), self.get_state()) 

# Tests

def printState(cfh, name, state):
    print ('CFH:', cfh.get_channel(), name,  '-', state)
    print('%s calling for heat after %dm',cfh.get_name(), cfh.get_off_period())
    print('%s satisfied after %dm',cfh.get_name(), cfh.get_on_period())


if __name__ == "__main__":
    import time

    wiringpi.wiringPiSetup()
    cfh1 = CFH(1, 'Kitchen', None, printState)
    cfh2 = CFH(2, 'Lounge', None, printState)
    cfh3 = CFH(3, 'Landing', None, printState)
    cfhs = [cfh1,cfh2,cfh3]

    while True:
        for cfh in cfhs:
            cfh.poll()
        time.sleep(.2)
