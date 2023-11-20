from pythondaq.models.diode_experiment import DiodeExperiment
import csv
from os import listdir, path, mkdir, getcwd
import matplotlib.pyplot as plt

# File path where the CSV will be saved (this will always create folders in de directory where it is run, it not a bug but a feature)
storage_path = f"{getcwd()}/DataStore/"
image_path = f"{getcwd()}/ImageStore/"


def main():
    # Check if given directories exist, if not create them
    if not path.isdir(storage_path):
        mkdir(storage_path)
    if not path.isdir(image_path):
        mkdir(image_path)

    # Create list to store the iteration numbers
    experiment_iterations = []
    for file in listdir(storage_path):
        # This is so unusual names do not cause an error
        try:
            experiment_iterations.append(int(file[15:-4]))
        except:
            pass
    # Sort list and get last number
    experiment_iterations.sort()

    # if there are no previous iteration set value to -1 (then suffix becomes 0)
    last_experiment_iteration = (
        experiment_iterations[-1] if len(experiment_iterations) != 0 else -1
    )

    # Only check the data file so that the saved plots always have the same number
    file_name = f"ExperimentData_{last_experiment_iteration+1}.csv"
    image_name = f"ExperimentPlot_{last_experiment_iteration+1}.jpg"

    # Initialize model and run experiment
    experiment = DiodeExperiment()
    header, data = experiment.scan()

    # Create lists to extract LED Volt and Current plus their errors
    led_volts = []
    led_volt_errors = []
    currents = []
    current_errors = []

    # save the data as CSV
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

            # save values to plot/print later
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
        markersize=3,
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

    if __name__ == "__main__":
        main()
