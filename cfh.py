import wiringpi

BOUNCE_COUNT = 5


Class CFH:
    def __init__(self,cfh_no, notifier):
         self._notifier = notifier
        self._pins = [7,21,22]
        if (cfh_no < 1 or cfh_no > len(self._pins)):
            raise IndexError('CFH out of range')
        self._cfh_no = cfh_no
        self._pin = self._pins[self._cfh_no-1]
        wiringpi.pinMode(self._pin, 0)
        self._current_state = -1
        self.check_state()
        self._state_changed = False
        self._old_pin_state = -1 # unknown
        self._bounce_count = -1

    def get_channel(self):
        return self._cfh_no

    def get_state(self):
        return self._current_state

    def get_contact_state(self):
        
        # get the new pin state
        new_state = 1-wiringpi.digitalRead(self._pin)

        stable_state, self._old_pin_state, 

        return pin_state

    def check_state(self):
        state = (self.get_contact_state() == 1)
        if (self._current_state != state):
            self._current_state = state
            self._state_changed = True
    #        print ('Current State:', self._current_state)
    #        print ('State Changed:', self._state_changed)

    def poll(self):
        self.check_state()
        if (self._state_changed == True):
#            print ('Notify')
            self._notifier(self)
            self._state_changed = False
 
