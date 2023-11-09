from diode_experiment import DiodeExperiment
import csv
from os import listdir
import matplotlib.pyplot as plt

# File path waar de CSV opgeslagen wordt
storage_path = "C:/Users/12604275/Desktop/ECPC/DataStore/"
file_name = f"ExperimentData_{len(listdir(storage_path))}.csv"

Experiment = DiodeExperiment()
Header, Data = Experiment.scan()

# sla de data op als CSV
with open(storage_path + file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(Header)
    for T_V, T_V_err, R_V, R_V_err, L_V, L_V_err, I, I_err, R in Data:
        writer.writerow([T_V, T_V_err, R_V, R_V_err, L_V, L_V_err, I, I_err, R])

# Extract LED Volt and Current plus their errors
LED_volt = list()
LED_volt_err = list()
Current = list()
Current_err = list()

for _, _, _, _, L_V, L_V_err, I, I_err, _ in Data[1]:
    LED_volt.append(L_V)
    LED_volt_err.append(L_V_err)
    Current.append(I)
    Current_err.append(I_err)


# plot de data
plt.errorbar(
    LED_volt, Current, xerr=LED_volt_err, yerr=Current_err, linestyle="None", marker="o"
)
plt.show()
