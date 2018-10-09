# performs a debounce function by only changing state after BOUNCE_COUNT calls

BOUNCE_COUNT = 5

def bounce_check(pin_state):
    # only change state after 5 stable samples
    # When first called after startup callee doesn't know BOUNCE_COUNT so is set to -1
    if (pin_state['samples'] < 1):
#        print ('Setting sample count on first call')
        pin_state['samples'] = BOUNCE_COUNT

    # only on startup as old_state = -1 as unknown
    if pin_state['old'] !=0 and pin_state['old'] != 1:
#        print ('Setting pin_state on 1st call')
        pin_state['old'] = pin_state['new']

#    if pin_state['stable'] >-1 and :

    # dec bounce count if a stable sample
    if pin_state['new'] == pin_state['old']:
#        print ('Stable')
        pin_state['samples'] -= 1
    else:
        # else reset the count
#        print ('Unstable')
        pin_state['samples'] = BOUNCE_COUNT

    # if not yet finised sampling just return the old state
    if pin_state['samples'] > 0:
#        print ('Waiting for stable')
        pin_state['stable'] = pin_state['old']
    else:
        # if here we've had a period of stability on the pin so update state
        print ('Updating stable')
        pin_state['stable'] = pin_state['new']
        pin_state['samples'] = BOUNCE_COUNT

    return pin_state