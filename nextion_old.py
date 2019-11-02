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
        self._id = id
        self._static = static
        self._state_writer= state_writer

    def output(self, state):
        output = self._static + ":" + self._state_writer(state)
        return 't' + str(self._id) +'.txt="' + output + '"'


class Nextion:
    NAME='name'
    ID='id'
    OUTPUT='output'
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
        # print(self._ser.name)
        # print('True' if self._ser.is_open else 'False')
        self._endcomm = b"\xff\xff\xff"
        self._ser.write(b'rest' + self._endcomm)
        time.sleep(1)
        self._ser.write(b'dims=40' + self._endcomm)
        self._ser.write(b'thsp=30' + self._endcomm)
        self._ser.write(b'thup=1' + self._endcomm)
        self._ser.write(b'usup=1' + self._endcomm)
        # self._ser.write(b't0.txt="XXX"' + self._endcomm)

        self._cfhs = [{self.NAME:'Kitchen CFH', self.ID:1},{self.NAME:'Lounge CFH', self.ID:0}, {self.NAME:'Landing CFH', self.ID:-1}]
        self._valves = [{self.NAME:'UFH Valve', self.ID:4},{self.NAME:'UP Valve', self.ID:5}, {self.NAME:'DN Valve', self.ID:6}]

        self._logger.debug('Nextion Module Starting..')

    def __del__(self):
        self._ser.close()

    def getSerial(self):
        return self._ser

    def output(self,str):
        self._logger.debug('Nextion: ' + str)
        self._ser.write(str.encode('utf-8') + self._endcomm)
        # print (str + self._endcomm)

    def updateLine(self, widget):
        if widget[self.ID] < 0:
            return
        line = 't' + str(widget[self.ID]) +'.txt="' + widget[self.OUTPUT] + '"'
        self.output(line)

    def updateWidget(self, widget_index, value):
        assert (widget_index >= 0 and widget_index < widgets.length()), "Nextion: Widget' out of range"

        widget = self._widgets[widget_index]
        str = widget[self.NAME] + ':'
        str = str + value
        widget = {self.ID:valve[self.ID], self.OUTPUT:str}
        self.updateLine(widget)


    def updateValveState(self, valve_no, valve_state):
        assert (valve_no > 0 and valve_no < 4), "Nextion: Valve no' out of range"

        valve = self._valves[valve_no -1]
        str = valve[self.NAME] + ':'
        str = str + valve_state.upper()
        widget = {self.ID:valve[self.ID], self.OUTPUT:str}
        self.updateLine(widget)

    def updateCfhState(self, cfh_no, state):
        assert (cfh_no > 0 and cfh_no < 4), "Nextion: CFH no' out of range"

        cfh = self._cfhs[cfh_no -1]
        str = cfh[self.NAME] + ':'
        str = str + " ON" if state else str + "OFF"
        widget = {self.ID:cfh[self.ID], self.OUTPUT:str}
        self.updateLine(widget)

if __name__ == "__main__":
    nextion = Nextion()
    widget = {"id":1, "output":"Testing2"}
    # nextion.output('t0.txt="Hellos"')
    nextion.updateLine(widget)
    


