# performs a debounce function by only changing state after BOUNCE_COUNT calls

BOUNCE_COUNT = 5

def bounce_check(pin_state):
    # only change state after 5 stable samples
    # When first called after startup callee doesn't know BOUNCE_COUNT so is set to -1

    # When samples is zero we are not doing a bounce check
    if pin_state['samples'] == 0:
        if pin_state['new'] == pin_state['stable']:
            return pin_state
    
    # if we've detected a state change do the bounce timeout

    # dec bounce count if a stable sample
    if pin_state['new'] != pin_state['stable']:
        if (pin_state['samples'] < 1):
            pin_state['samples'] = BOUNCE_COUNT
        else:
            pin_state['samples'] -= 1
    else:
        # if here we are in a boune_timeout as a change of state detected between
        # new & stable but now stable == new so we must have had a bounce during
        # this period so reset the timeout count
        pin_state['samples'] = BOUNCE_COUNT

    # if not yet finised sampling just return the old state
    if pin_state['samples'] == 0:
        # if here we've had a period of stability on the pin so update state
        pin_state['changed'] = True

        pin_state['stable'] = pin_state['new']

    return pin_state