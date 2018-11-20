import time, TR2, Boiler, zonevalve, cfh, relays, wiringpi

def setup():
    wiringpi.wiringPiSetup()

    global boiler
    global tr2 
    global valves
    global call_for_heats
    global ufh_pump

    boiler = Boiler.Boiler()
    tr2 = TR2.TR2()
    zv1 = zonevalve.ZoneValve(1, zone_valve_state_changed)
    zv2 = zonevalve.ZoneValve(2, zone_valve_state_changed)
    zv3 = zonevalve.ZoneValve(3, zone_valve_state_changed)
    valves = {'ufh': zv1, 'downstairs':zv2, 'upstairs': zv3}

    cfh1 = cfh.CFH(1,cfh_state_changed)
    cfh2 = cfh.CFH(2,cfh_state_changed)
    cfh3 = cfh.CFH(3,cfh_state_changed)
    call_for_heats = {'kitchen':cfh1, 'lounge': cfh2, 'landing': cfh3}


    ufh_pump = relays.Relay(0)

    # boiler.set_temp(2000) 
    boiler.off()
   
    for v in valves:
        valves[v].close()


def calling_for_heat():
    result = FALSE:
    for cfh in call_for_heats:
        result = result | call_for_heats[cfh].get_state()
    return result


def cfh_state_changed(cfh):
    ch = cfh.get_channel()
#    zv = valves[ch-1]
    if ch == 1: # UFH
        if cfh.get_state() == True:
            valves['ufh'].open()
            print ('UFH Pump: Running')
        else:
            ufh_pump.off()
            print ('UFH Pump: Stopped')
            valves['ufh'].close()
    elif ch == 2: # Lounge
        if cfh.get_state() == True:
            valves['downstairs'].open()
            valves['upstaris'].open()
        else:
            valves['downstairs'].close()
            valves['upstaris'].close()


def zone_valve_state_changed(zv):
    if zv

    any_valve_open = False
    for ch in range( len(valves) ):
        cfh = call_for_heats[ch]
        zv = valves[ch]
        # Only want boiler on if valve is open & a valid call for heat on that channel
        print ('Valve',ch,zv.get_state(),'CFH',cfh.get_state())
        if zv.get_state() == "open" and cfh.get_state() == True:
            any_valve_open = True
            break

    if any_valve_open:
       print ('Boiler:ON')
       # boiler.on()
        
    else:
       print ('Boiler:OFF')
       # boiler.off()


def loop():
    for v in valves:
        valves[v].poll()
    
    for cfh in call_for_heats:
        call_for_heats[cfh].poll()



if __name__ == "__main__":
    setup()

    while True:
        loop()
        time.sleep(.5)
