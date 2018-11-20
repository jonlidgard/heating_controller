# Relay 1: UFH Pump
# Relay 2: UFH Valve
# Relay 3: Downstairs
# Relay 4: Upstairs

import logging, time, TR2, Boiler, zonevalve, cfh, relays, wiringpi
import pushover 


def setup():
    wiringpi.wiringPiSetup()

    global boiler
    global tr2 
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
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.info('Heating Program Started')

    # Pushover
    pushover_client = pushover.Client("u1nntc8b4zqy9p565krjpnq2wqfp6t", api_token="ayexnq66ykz79gdr8q4wx2tto6qri7")
    pushover_client.send_message("Heating Started", title="Info")


    boiler = Boiler.Boiler()
    tr2 = TR2.TR2()
    ufh_valve = zonevalve.ZoneValve(1, 'UFH', zone_valve_state_changed)
    downstairs_valve = zonevalve.ZoneValve(2, 'Downstairs', zone_valve_state_changed)
    upstairs_valve = zonevalve.ZoneValve(3, 'Upstairs', zone_valve_state_changed)
    valves = [ufh_valve, downstairs_valve, upstairs_valve]

    kitchen_cfh = cfh.CFH(1, 'Kitchen', cfh_state_changed)
    lounge_cfh = cfh.CFH(2, 'Lounge', cfh_state_changed)
    landing_cfh = cfh.CFH(3, 'Landing', cfh_state_changed)
    call_for_heats = [kitchen_cfh, lounge_cfh, landing_cfh]

    ufh_pump = relays.Relay(1)
    ufh_pump.off()
    logger.info('UFH Pump: Stoppped')
    
    # boiler.set_temp(2000) 
    boiler.off()
   
    for v in valves:
        v.close()

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
    return result1 | result2 | result3


def cfh_state_changed(cfh):
    if cfh.get_name() == 'Kitchen': # UFH
        if cfh.get_state() == True:
            ufh_valve.open()
            downstairs_valve.open() # Temp to ensure boiler has somewhere to pump the heat
        else:
            ufh_pump.off()
            logger.info('UFH Pump: Stopped')
            ufh_valve.close()
    elif cfh.get_name()  == 'Lounge': # Lounge
        if cfh.get_state() == True:
            downstairs_valve.open()
            upstairs_valve.open()
        else:
            downstairs_valve.close()
            upstairs_valve.close()


def zone_valve_state_changed(zv):
    if zv.get_name() == 'UFH':
        if zv.get_state() == 'open':
            ufh_pump.on()
            logger.info('UFH Pump: Started')

    if boiler_needs_on():
       boiler.on()
    else:
       boiler.off()


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
