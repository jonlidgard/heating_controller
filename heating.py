# Relay 1: UFH Pump
# Relay 2: UFH Valve
# Relay 3: Downstairs
# Relay 4: Upstairs

import logging, time, Boiler, zonevalve, cfh, relays, wiringpi
import pushover
# import webserver
import nextion

import time
import struct



def setup():
    wiringpi.wiringPiSetup()

    global nextion
    global boiler
    # global tr2 
    global valves
    global call_for_heats
    global ufh_pump
    global kitchen_cfh
    global lounge_cfh
    global landing_cfh
    global ufh_valve
    global downstairs_valve
    global upstairs_valve
    global logger
    global pushover_client
    
    # create logger
    logger = logging.getLogger('heating')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.FileHandler(filename='/var/log/heating.log') #StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.info('Heating Program Started')

    # Display
    nextion = nextion.Nextion()

    # Pushover
    pushover_client = pushover.Client("u1nntc8b4zqy9p565krjpnq2wqfp6t", api_token="ayexnq66ykz79gdr8q4wx2tto6qri7")
    pushover_client.send_message("Heating Started", title="Info")

    boiler = Boiler.Boiler()
    # tr2 = TR2.TR2()
    ufh_valve_widget = TextWidget(4,"UFH Valve", new ValveStateWriter())
    ufh_valve = zonevalve.ZoneValve(1, 'UFH', zone_valve_state_changed)

    downstairs_valve_widget = TextWidget(6,"DN Valve", new ValveStateWriter())
    downstairs_valve = zonevalve.ZoneValve(2, 'Downstairs', zone_valve_state_changed)

    upstairs_valve_widget = TextWidget(5,"UP Valve", new ValveStateWriter())
    upstairs_valve = zonevalve.ZoneValve(3, 'Upstairs', zone_valve_state_changed)

    valves = [ufh_valve, downstairs_valve, upstairs_valve]

    kitchen_cfh_widget = TextWidget(1,"Kitchen CFH", new OnOffStateWriter())
    kitchen_cfh = cfh.CFH(1, 'Kitchen', 'Kitchen CFH', 1, cfh_state_changed)
    
    lounge_cfh_widget = TextWidget(0,"Lounge CFH", new OnOffStateWriter())
    lounge_cfh = cfh.CFH(2, 'Lounge', 'Lounge CFH', 0, cfh_state_changed)
    
    landing_cfh_widget = TextWidget(-1,"Landing CFH", new OnOffStateWriter())
    landing_cfh = cfh.CFH(3, 'Landing', 'Landind CFH', -1, cfh_state_changed)

    call_for_heats = [kitchen_cfh, lounge_cfh, landing_cfh]

    ufh_pump_widget = TextWidget(3,"UFH Pump", new OnOffStateWriter())
    boiler_widget = TextWidget(2,"Boiler", new OnOffStateWriter())

    nextion
        .add(kitchen_cfh_widget)
        .add(lounge_cfh_widget)
        .add(landing_cfh_widget)
        .add(upstairs_valve_widget)
        .add(downstairs_valve_widget)
        .add(ufh_valve_widget)
        .add(ufh_pump_widget)

    ufh_pump = relays.Relay(1)
    ufh_pump_widget.update(0)
    ufh_pump.off()
    logger.info('UFH Pump: Stoppped')
    
    # boiler.set_temp(2000) 
    boiler_widget.update(0)
    boiler.off()
   
    nextion.refresh(True) // Refresh all
    for v in valves:
        v.close()

    # Start the Web Server
    # webserver.run()
    
    logger.debug('Setup Done')

def calling_for_heat():
    result = FALSE
    for cfh in call_for_heats:
        result = result | cfh.get_state()
    logger.debug(result)
    return result


def any_valve_open():
    result = FALSE
    for zv in valves:
        result = result | (zv.get_state() == 'open')
    logger.debug(result)
    return result


def boiler_needs_on():
    result1 = kitchen_cfh.get_state() == True and ufh_valve.get_state() == 'open' 
    result2 = lounge_cfh.get_state() == True and (downstairs_valve.get_state() == 'open')
    result3 = lounge_cfh.get_state() == True and (upstairs_valve.get_state() == 'open')
    result = result1 | result2 | result3
    logger.debug('Boiler Needs On: %d, Kitchen-%d, Lounge1-%d, Lounge2-%d',result,result1,result2,result3)
    return result

def cfh_state_changed(cfh, name, state):
        if state == True:
            ufh_valve.open()
        else:
            ufh_pump_widget.update(0)
            ufh_pump.off()
            logger.info('UFH Pump: Stopped')
            ufh_valve.close()
    elif name  == 'Lounge': # Lounge
        if state == True:
            downstairs_valve.open()
        else:
            ufh_state = ufh_valve.get_state()
            if ufh_state == 'closed' or ufh_state == 'closing':
                downstairs_valve.close()
    nextion.refresh()


def zone_valve_state_changed(zv, name, state):
    if name == 'UFH':
        if state == 'open':
            ufh_pump_widget.update(1)
            ufh_pump.on()
            logger.info('UFH Pump: Started')
            upstairs_valve.open() # Temp to ensure boiler has somewhere to pump the heat
            logger.info('Downstairs Valve: Opened')

    elif name == 'Downstairs':
        if state == 'open':
            upstairs_state = upstairs_valve.get_state()
            if upstairs_state == 'closed' or upstairs_state == 'closing':            
                upstairs_valve.open()
                logger.info('Upstairs Valve: Opened')

    if boiler_needs_on():
       boiler_widget.update(1)
       boiler.on()
    else:
       boiler_widget.update(0)
       boiler.off()

    nextion.refresh()


def loop():
    for v in valves:
        v.poll()
    
    for cfh in call_for_heats:
        cfh.poll()



if __name__ == "__main__":
    setup()

    while True:
        loop()
        time.sleep(1)
