from diode_experiment import DiodeExperiment
import csv
from os import listdir
import matplotlib.pyplot as plt

# File path waar de CSV opgeslagen wordt
storage_path = "C:/Users/12604275/Desktop/ECPC/DataStore/"
image_path = "C:/Users/12604275/Desktop/ECPC/ImageStore/"

# Set names for the experiment by checking how many experiments came before
file_name = f"ExperimentData_{len(listdir(storage_path))}.csv"
image_name = f"ExperimentPlot_{len(listdir(storage_path))}.jpg"

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

    # write the header into the file first
    writer.writerow(header)

    # unpack the zip object (data) with a for loop
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

        # write all values into a the CSV file
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

# plotting the data
plt.errorbar(
    led_volts,
    currents,
    xerr=led_volt_errors,
    yerr=current_errors,
    linestyle="None",
    marker="o",
)

# formatting the plot
plt.xlim(0, 3)
plt.ylim(0, 0.003)
plt.title("U,I-characteristic plot for an LED", fontsize=17)
plt.xlabel("LED volage (V)", fontsize=14)
plt.ylabel("LED current (A)", fontsize=14)
plt.tight_layout()

# saving and showing the plot
plt.savefig(image_path + image_name)
plt.show()
