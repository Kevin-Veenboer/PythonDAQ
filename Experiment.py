import pyvisa
import time
import matplotlib.pyplot as plt
import pandas as pd

# function to display devices
def list_devices():
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports


# Defining conversion functions
def convert_Analog_Digital(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) / step_value)


def convert_Digital_Analog(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) * step_value, 2)


class ArduinoVISADevice:
    def __init__(self, port) -> None:
        # Make connection with device
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

        # Initialize the channel values
        self.CH0_value = None
        self.CH1_value = None
        self.CH2_value = None

    def get_identification(self) -> None:
        print(self.device.query("*IDN?"))

    # Method to set output values (0-1023 input expected)
    def set_output_value(self, value) -> None:
        self.device.query(f"OUT:CH0 {value}")

    # functions to get output value (CH0) or input values (CH1 or CH2)
    def get_output_value(self) -> int:
        # if no value is set then return 0
        if self.CH0_value == None:
            return 0
        return self.CH0_value

    def get_input_value(self, channel) -> int:
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        elif channel == 1:
            return int(self.device.query("MEAS:CH1?"))
        else:
            return int(self.device.query("MEAS:CH2?"))


# VIEW thingy

# Defining storage path for data
path = "C:/Users/12604275/Desktop/ECPC/DataStore/"


port = list_devices()[0]

Device = ArduinoVISADevice(port=port)

# Intitializing the measurement lists
Output_values = list(range(0, 1024))
MeasurementsT = list()
MeasurementsR = list()
MeasurementsL = list()
MeasurementsI = list()

for val in Output_values:
    # Setting value of Arduino then measuring
    Device.set_output_value(value=val)
    Resistor_Voltage = convert_Digital_Analog(float(Device.get_input_value(channel=2)))
    Total_Voltage = convert_Digital_Analog(float(Device.get_input_value(channel=1)))
    LED_Voltage = round(Total_Voltage - Resistor_Voltage, 2)

    # Storing the measurements in lists
    MeasurementsT.append(Total_Voltage)
    MeasurementsR.append(Resistor_Voltage)
    MeasurementsL.append(LED_Voltage)

    # Current is in mA !
    MeasurementsI.append(round(1000 * (Resistor_Voltage / 220), 2))

    # Debug print
    print(
        f"Total: {Total_Voltage}, Resistor: {Resistor_Voltage}, LED: {LED_Voltage}, Current(mV): {round(1000 * (Resistor_Voltage / 220), 2)}"
    )

# # CSV met pandas library (mocht blijkbaar niet)

# DF_dict = {
#     "Total Voltage (V)": MeasurementsT,
#     "Resistor Voltage (V)": MeasurementsR,
#     "LED Voltage (V)": MeasurementsL,
#     "Current (mA)": MeasurementsI,
# }
# # storing the data as CSV
# pd.DataFrame(DF_dict).to_csv(path + "ExperimentData.csv")

# data = zip(MeasurementsT)


# plotting the result
plt.plot(MeasurementsL, MeasurementsI, marker="o", linestyle="None")
plt.show()
