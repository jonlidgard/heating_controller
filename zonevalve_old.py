from relays import Relay
from common import bounce_check
import wiringpi
import logging
import time
import pushover 

LIMIT_PINS = [3,4,5]
ON_TIMEOUT_SECS = 30
OFF_TIMEOUT_SECS = 30

class ZoneValve:
    def __init__(self, valve_no, name, notifier):
        self._name = name
        self._notifier = notifier


        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())


        self._pushover_client = pushover.Client("u1nntc8b4zqy9p565krjpnq2wqfp6t", api_token="ayexnq66ykz79gdr8q4wx2tto6qri7")
        
        self._motor_on_time = 0
        self._motor_off_time = 0
        if (valve_no < 1 or valve_no > len(LIMIT_PINS)):
            raise IndexError('ZoneValve out of range')
        self._valve_no = valve_no
        pin = LIMIT_PINS[valve_no-1] 
        wiringpi.pinMode(pin, 0)
        self._pin_state = {'pin': pin, 'changed': False, 'new': -1, 'stable': -1, 'samples': -1}

        self._relay = Relay(valve_no+1)
        self._valve_state = {'current': 'unknown', 'changed': False}
        self._logger.debug('ZoneValve module started')
        self.check_state()


    def check_state(self):
        motor_on = (self._relay.get() == 1) # Motor on
        switch_made = (self.get_limit_switch_state() == 1)
                
        if self._motor_on_time > 0: # Commanded open
            if time.time() > self._motor_on_time + ON_TIMEOUT_SECS:
                self.warn(ON_TIMEOUT_SECS)
        elif self._motor_off_time > 0: #Commanded off
            if time.time() > self._motor_off_time + OFF_TIMEOUT_SECS:
                self.warn(OFF_TIMEOUT_SECS)

        if motor_on:
            if switch_made:
                state = "open"
            else:
                state = "opening"
        else:
            if switch_made:
                state = "closing"
            else:
                state = "closed"
        
        if (self._valve_state['current'] != state):
            self._valve_state['current'] = state
            self._valve_state['changed'] = True
            if self._logger.isEnabledFor(logging.DEBUG):
                if self._valve_state == 'open': # Successfully opened
                    if self._motor_on_time > 0:
                        self._logger.debug('%s valve opened after %ds',self.get_name(), time.time() - self._motor_on_time)
                        self._motor_on_time = 0

                if self._valve_state == 'closed':
                    if self._motor_off_time > 0:
                        self._logger.debug('%s valve closed after %ds',self.get_name(), time.time() - self._motor_off_time)
                        self._motor_off_time = 0

    def get_channel(self):
        return self._valve_no


    def get_name(self):
        return self._name

    def get_state(self):
        return self._valve_state['current']

    def get_pin_state(self):
        return 1-wiringpi.digitalRead(self._pin_state['pin'])

    def get_limit_switch_state(self):
        # get the new pin state
        self._pin_state['new'] = 1-wiringpi.digitalRead(self._pin_state['pin'])
        self._pin_state = bounce_check(self._pin_state)

        return self._pin_state['stable']

    def poll(self):
        self.check_state()
        if (self._valve_state['changed'] == True):
#            print ('Notify')
            self._notifier(self, self.get_name(), self.get_state())
            self._valve_state['changed'] = False

    def open(self):
        self._relay.on()
        switch_made = (self.get_limit_switch_state() == 1)
        if switch_made:
            self._motor_on_time = time.time()
            self._motor_off_time = 0
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('%s Motor Relay ON',self.get_name())
        self.poll()

    def close(self):
        self._relay.off()
        switch_made = (self.get_limit_switch_state() == 1)
        if switch_made == False:
            self._motor_off_time = time.time()
            self._motor_on_time = 0
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug('%s Motor Relay OFF',self.get_name())
        self.poll()

    def toggle(self):
        self._relay.toggle()
        self.poll()

    def warn(self, secs):
        msg = '{} valve failed to {} within {}s'.format(self.get_name(), self.get_state(), secs)
#        self._logger.warn(msg)
#        self._pushover_client.send_message(msg, title="Warning")


# Tests

def printState(valve, name, state):
    print ('Valve:', valve.get_channel(), name, '-', state)
    #if (state == "open" or state == "closed"):
    #    valve.toggle()


if __name__ == "__main__":
    import time

    wiringpi.wiringPiSetup()
    zv1 = ZoneValve(1, 'ufh', printState)
    zv2 = ZoneValve(2, 'downstairs', printState)
    zv3 = ZoneValve(3, 'upstairs', printState)
    valves = [zv1,zv2,zv3]

    print ('UFH: %d, Downstairs: %d, Upstairs: %d', zv1.get_pin_state(), zv2.get_pin_state(), zv3.get_pin_state())
#    for v in valves:
#        v.close()
#    time.sleep(2)
#    for v in valves:
#        v.open()
#    time.sleep(2)

#    while True:
#        for v in valves:
#            v.poll()
#        time.sleep(.5)
