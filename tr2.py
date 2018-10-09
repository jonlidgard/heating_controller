import adc
tr2_sensed_bias_resistance = 3000.0
tr2_mode_bias_resistance = 15000.0
tr2_mode_schedule_resistance = 6220
tr2_mode_comfort_resistance = 8960
tr2_mode_frost_resistance = 12650
tr2_mode_night_resistance = 13960
tr2_max_setpoint_resistance = 2200
tr2_max_sensed_resistance = 3000
tr2_setpoint_factor= 30.0 / tr2_max_setpoint_resistance
tr2_sensed_factor = 30.0 / tr2_max_sensed_resistance

resistance_error_margin = 200

tr2_night_mode_raw = 492
tr2_frost_mode_raw = 467
tr2_comfort_mode_low_raw = 382
tr2_comfort_mode_high_raw = 437
tr2_schedule_mode_low_raw = 299
tr2_schedule_mode_high_raw = 369
raw_hysteresis = 5
tr2_setpoint_range_degc = 30.0

tr2_schedule_setpoint_factor = tr2_setpoint_range_degc / (tr2_schedule_mode_high_raw - tr2_schedule_mode_low_raw+5.0)
tr2_comfort_setpoint_factor = tr2_setpoint_range_degc / (tr2_comfort_mode_high_raw - tr2_comfort_mode_low_raw+5.0)

class TR2:
    def __init__(self):
        _mode = "unknown"
        _setpoint = -99.0
        _sensed = -99.0

    def get_mode_and_setpoint_from_raw(self, raw_val):
        setpoint = -99.0

        if (raw_val + raw_hysteresis > tr2_schedule_mode_low_raw) and \
        (raw_val - raw_hysteresis < tr2_schedule_mode_low_raw):
            mode = "scheduled"

        if raw_val > (tr2_night_mode_raw - raw_hysteresis) and \
            raw_val < (tr2_mode_night_resistance + raw_hysteresis):
            mode = 'night'
            setpoint = -99.0

        elif raw_val > (tr2_frost_mode_raw - raw_hysteresis) and \
            raw_val < (tr2_frost_mode_raw + raw_hysteresis):
            mode = "frost"
            setpoint = -99.0

        elif raw_val > (tr2_comfort_mode_low_raw - raw_hysteresis) and \
            raw_val < (tr2_comfort_mode_high_raw + raw_hysteresis):
            mode = "comfort"
            setpoint_raw = raw_val - tr2_comfort_mode_low_raw + 0.0
#            setpoint = tr2_setpoint_range_degc - tr2_comfort_setpoint_factor * setpoint_raw + 5.0
            setpoint = tr2_setpoint_range_degc - setpoint_raw / 2.3

        elif raw_val > (tr2_schedule_mode_low_raw - raw_hysteresis) and \
            raw_val < (tr2_schedule_mode_high_raw + raw_hysteresis):
            mode = "schedule"
            setpoint_raw = raw_val - tr2_schedule_mode_low_raw + 0.0
            setpoint = tr2_setpoint_range_degc - setpoint_raw / 2.9
#            setpoint = tr2_setpoint_range_degc - tr2_schedule_setpoint_factor * setpoint_raw + 5.0

        if setpoint != -99.0 and setpoint < 0 : setpoint = 0
        if setpoint > 30 : setpoint = 30

        return (mode, int(setpoint))

    def read(self):
        raw_values = [0]*8
        v = adc.read_analog()
        sensed_raw = v[0]
        mode_raw = v[1]
        _mode, _setpoint = self.get_mode_and_setpoint_from_raw(mode_raw)

        sensed_resistance = tr2_sensed_bias_resistance * sensed_raw / (1024.0 - sensed_raw)
        _sensed = int(sensed_resistance * tr2_sensed_factor)
        # Need to get this to increase as resistance decreases
        return {"mode": _mode, "setpoint": _setpoint, "sensed": _sensed}


    def get_mode(self):
        return _mode

    def get_setpoint(self):
        return _setpoint

    def get_sensed(self):
        return get_sensed