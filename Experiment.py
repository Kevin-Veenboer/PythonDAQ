import pyvisa
import time
import matplotlib.pyplot as plt
import pandas as pd

# Deining storage path for data
path = "C:/Users/12604275/Desktop/ECPC/DataStore/"

# Defining conversion functions
def convert_Analog_Digital(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) / step_value)


def convert_Digital_Analog(value):
    steps = 1023
    step_value = 3.3 / steps
    return round(float(value) * step_value, 2)


rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
)

Output_values = list(range(0, 1024))
MeasurementsT = list()
MeasurementsR = list()
MeasurementsL = list()
MeasurementsI = list()

for val in Output_values:
    # Setting value of Arduino then measuring
    device.query(f"OUT:CH0 {val}")
    Resistor_Voltage = convert_Digital_Analog(float(device.query("MEAS:CH2?")))
    Total_Voltage = convert_Digital_Analog(float(device.query("MEAS:CH1?")))
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

DF_dict = {
    "Total Voltage (V)": MeasurementsT,
    "Resistor Voltage (V)": MeasurementsR,
    "LED Voltage (V)": MeasurementsL,
    "Current (mA)": MeasurementsI,
}
# storing the data as CSV
pd.DataFrame(DF_dict).to_csv(path + "ExperimentData.csv")

# plotting the result
plt.plot(MeasurementsL, MeasurementsI, marker="o", linestyle="None")
plt.show()
