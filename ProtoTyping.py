import pyvisa
import time


rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
)
# Debug print
# print(device.query("*IDN?"))

# Query statements
# device.query(f"OUT:CH0 {value}")
# measurement = device.query("MEAS:CH2?")


def convert_Analog_Digital(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) / step_value)


def convert_Digital_Analog(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) * step_value, 2)


print(f"spanning D700: {convert_Digital_Analog(700)}")
print(f"D value voor 2.0V: {convert_Analog_Digital(2.0)}")
print(f"D value voor 2.28V: {convert_Analog_Digital(2.28)}")
