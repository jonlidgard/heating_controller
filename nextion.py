import serial
import logging
import time

class StatusFile:
    def __init__(self):
        self._fh = open("/home/pi/heatingStatus","w+")
        self._fh.write('')
        self._fh.close()

    def __del__(self):
        self._fh.close()

    def update(self, data):
        self._fh = open("/home/pi/heatingStatus","w+")
        old_data = self._fh.read()
        if old_data != data:
            self._fh.write(data)
        self._fh.close()


class StateWriter:
    def __init__(self):
        self._state = None

    def output(self, state):
        return None
    def colorForState(self, state):
        return None    

class OnOffStateWriter(StateWriter):

    def output(self, state):
        self._state = state
        return " ON" if state else "OFF"

    def colorForState(self):
        return 2016 if self._state else 33840    

class ValveStateWriter(StateWriter):
    STATE_COLORS={'open': 2016, 'opening': 63488, 'closed': 33840, 'closing': 63488}
    def output(self, state):
        self._state = state
        return state.upper()

    def colorForState(self):
        if self._state:
            return self.STATE_COLORS[self._state]
        else:
            return None

class TextWidget:
    def __init__(self, widget_id, static, state_writer):
        self._dirty_flag = True
        self._state = ''
        self._id = widget_id
        self._static = static
        self._state_writer= state_writer

    def update(self, state):
        self._state = self._state_writer.output(state)
        self._dirty_flag = True
#        print( self.text())

    def text(self):
        return self._static + ":" + self._state

    def makeCommand(self, cmd):
        return 't' + str(self._id) +'.' + cmd +'='

    def output(self):
        commands = []
        if self._id >= 0:
            self._dirty_flag = False            
            commands.append(self.makeCommand('txt') + '"' + self.text() + '"')
            commands.append(self.makeCommand('pco') + str(self._state_writer.colorForState()))
        return commands

    def is_dirty(self):
        return self._dirty_flag


class Nextion:
    END_COMM=b"\xff\xff\xff"

    def __init__(self):
        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())
        self._statusFile = StatusFile()

        self._ser = serial.Serial(
            port='/dev/ttyS0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )

        self.output("rest")
        time.sleep(1)
        self.output("dims=40")
        self.output("thsp=30")
        self.output("thup=1")
        self.output("usup=1")

        self._widgets=[]

        self._logger.debug('Nextion Module Starting..')

    def __del__(self):
        self._ser.close()

    def getSerial(self):
        return self._ser

    def refresh(self, all = False):
        new_data = ''
        for widget in self._widgets:
            new_data += widget.text() + '\n'
            if all or widget.is_dirty():
                for cmd in widget.output():
#                    print(cmd)
                    self.output(cmd)
        self._statusFile.update(new_data)


    def output(self,str):
        self._logger.debug('Nextion: ' + str)
        self._ser.write(str.encode('utf-8') + self.END_COMM)
        # print (str + self.END_COMM)


    def add(self, widget):
        self._widgets.append(widget)
        return self

if __name__ == "__main__":
    nextion = Nextion()
    widget = TextWidget(0,"UFH Valve", ValveStateWriter())
    widget.update("open")
    nextion.add(widget)
    nextion.refresh()
    


