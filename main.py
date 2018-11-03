import time, TR2, Boiler, zonevalve, cfh, wiringpi

def setup():
    wiringpi.wiringPiSetup()

    global boiler
    global tr2 
    global valves
    global call_for_heats
 
    boiler = Boiler.Boiler()
    tr2 = TR2.TR2()
    zv1 = zonevalve.ZoneValve(1, zone_valve_state_changed)
    zv2 = zonevalve.ZoneValve(2, zone_valve_state_changed)
    zv3 = zonevalve.ZoneValve(3, zone_valve_state_changed)
    valves = [zv1,zv2,zv3]

    cfh1 = cfh.CFH(1,cfh_state_changed)
    cfh2 = cfh.CFH(2,cfh_state_changed)
    cfh3 = cfh.CFH(3,cfh_state_changed)
    call_for_heats = [cfh1,cfh2,cfh3]
 
    # boiler.set_temp(2000) 
    boiler.off()
   
    for v in valves:
        v.close()


def cfh_state_changed(cfh):
    ch = cfh.get_channel()
    zv = valves[ch]
    if cfh.get_state() == True:
        zv.open()
    else:
        zv.close()


def zone_valve_state_changed(zv):
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
        v.poll()
    
    for cfh in call_for_heats:
        cfh.poll()



if __name__ == "__main__":
    setup()

    while True:
        loop()
        time.sleep(.5)
