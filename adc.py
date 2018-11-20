# Reads the analog values from the MCP3008
import time
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 18
MISO = 25
MOSI = 26
CS   = 27
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def read_analog():
    # Read all the ADC channel values in a list.
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    return values

# Run tests
if __name__ == "__main__":

    import time

    # Main program loop.
    while True:
        # Read all the ADC channel values in a list.
        values = read_analog()

        # Print the ADC values.
        print(values)
        # Pause for half a second.
        time.sleep(.5)
