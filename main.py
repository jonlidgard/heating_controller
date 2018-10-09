import time, tr2, boiler, zonevalve, cfh

def setup:
    wiringpi.wiringPiSetup()

    boiler = boiler.Boiler()
    tr2 = tr2.TR2()
    zv1 = zonevalve.ZoneValve(1, zone_valve_state_changed)
    zv2 = zonevalve.ZoneValve(2, zone_valve_state_changed)
    zv3 = zonevalve.ZoneValve(3, zone_valve_state_changed)
    valves = [zv1,zv2,zv3]

    cfh1 = cfh.CFH(1,cfh_state_changed)
    cfh2 = cfh.CFH(2,cfh_state_changed)
    cfh3 = cfh.CFH(3,cfh_state_changed)
    call_for_heats = [cfh1,cfh2,cfh3]

    boiler.set_mode("comfort", 10) #no call for heat

    for v in valves:
        v.close()

def zone_valve_state_changed(zv):

def cfh_state_changed(cfh):
        ch = cfh.get_channel()
        zv = valves[ch]
    if cfh.get_current_state() == True:
        zv.open()
    else:
        zv.close()

def zone_valve_state_changed(zv):
    any_valve_open = False
    for ch in range( len(valves) ):
        cfh = call_for_heats[ch]
        zv = valves[ch]
        # Only want boiler on if valve is open & a valid call for heat on that channel
        if zv.get_current_state() == "open" and \
            cfh.get_current_state == True
        any_valve_open = True
        break

    if any_valve_open:
        boiler.set_mode("comfort", 30) #ensure boiler comes on
    else
        boiler.set_mode("frost", 0) #revert to frost protection


def loop():
    for v in valves:
        v.poll()
    
    for cfh in call_for_heats:
        cfh.poll()


