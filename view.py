from diode_experiment import DiodeExperiment
import csv
from os import listdir
import matplotlib.pyplot as plt

# File path waar de CSV opgeslagen wordt
storage_path = "C:/Users/12604275/Desktop/ECPC/DataStore/"
file_name = f"ExperimentData_{len(listdir(storage_path))}.csv"

experiment = DiodeExperiment()
header, data = experiment.scan()

# Create lists to extract LED Volt and Current plus their errors
led_volts = []
led_volt_errors = []
currents = []
current_errors = []


# sla de data op als CSV
with open(storage_path + file_name, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for (
        total_volt,
        total_volt_resistance,
        resistor_volt,
        resistor_volt_resistance,
        led_volt,
        led_volt_resistance,
        current,
        current_resistance,
        resistance,
    ) in data:
        writer.writerow(
            [
                total_volt,
                total_volt_resistance,
                resistor_volt,
                resistor_volt_resistance,
                led_volt,
                led_volt_resistance,
                current,
                current_resistance,
                resistance,
            ]
        )

        # save values to plot later
        led_volts.append(led_volt)
        led_volt_errors.append(led_volt_resistance)
        currents.append(current)
        current_errors.append(current_resistance)

# plot de data
plt.errorbar(
    led_volts,
    currents,
    xerr=led_volt_errors,
    yerr=current_errors,
    linestyle="None",
    marker="o",
)
plt.show()
