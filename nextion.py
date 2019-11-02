import serial
import logging
import time

class StateWriter:
    def output(self, state):
        return

class OnOffStateWriter(StateWriter):
    def output(self, state):
        return " ON" if state else "OFF"

class ValveStateWriter(StateWriter):
    def output(self, state):
        return state.upper()


class TextWidget:
    def __init__(self, widget_id, static, state_writer):
        self._dirty_flag = True
        self._state = ''
        self._id = id
        self._static = static
        self._state_writer= state_writer

    def update(self, state):
        self._state = self._state_writer.output(state)
        self._dirty_flag = True

    def output(self):
        self._dirty_flag = False
        output = self._static + ":" + self._state
        return 't' + str(self._id) +'.txt="' + output + '"'

    def is_dirty(self):
        return self._dirty_flag


class Nextion:
    END_COMM=b"\xff\xff\xff"

    def __init__(self):
        self._logger = logging.getLogger('heating')
        self._logger.addHandler(logging.NullHandler())

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
        for widget in self._widgets:
            if all or widget.is_dirty():
                self.output(widget.output())


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
    


