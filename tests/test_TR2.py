import time
from tr2 import TR2
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    my_tr2 = TR2() 
    values = my_tr2.read()

    # Print the ADC values.
    print(values)
    # Pause for half a second.
    time.sleep(.5)