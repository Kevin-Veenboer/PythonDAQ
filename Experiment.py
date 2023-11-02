import pyvisa
import time
import matplotlib.pyplot as plt


rm = pyvisa.ResourceManager("@py")
ports = rm.list_resources()

device = rm.open_resource(
    "ASRL5::INSTR", read_termination="\r\n", write_termination="\n"
)

Output_values = list(range(0, 1024))
MeasurementsT = list()
MeasurementsR = list()
MeasurementsL = list()
for val in Output_values:
    # Setting value of Arduino then measuring
    device.query(f"OUT:CH0 {val}")
    Resistor_Voltage = float(device.query("MEAS:CH2?"))
    Total_Voltage = float(device.query("MEAS:CH1?"))

    # Storing the measurements in lists
    MeasurementsT.append(Total_Voltage)
    MeasurementsR.append(Resistor_Voltage)
    MeasurementsL.append(Total_Voltage - Resistor_Voltage)

    # Debug print
    print(
        f"Total: {Total_Voltage}, Resistor: {Resistor_Voltage}, LED: {Total_Voltage-Resistor_Voltage}"
    )
