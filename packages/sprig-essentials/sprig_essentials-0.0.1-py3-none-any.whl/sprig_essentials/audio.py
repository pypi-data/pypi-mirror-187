import board
import displayio, audiobusio

# Reset all pins to allow new connections
displayio.release_displays()

# To show return tooltips for functions
class pin_number:pass
class audiobusio__i2s:pass

def createI2S(bit_clock_pin: pin_number, word_select_pin: pin_number, data_pin: pin_number) -> audiobusio__i2s:
    i2s = audiobusio.I2SOut(bit_clock_pin, word_select_pin, data_pin)
    return i2s
