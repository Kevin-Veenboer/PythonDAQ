from pythondaq.models.diode_experiment import DiodeExperiment
import csv
from os import listdir, path, mkdir, getcwd
import matplotlib.pyplot as plt
import click


@click.group()
def cmd_group():
    pass


@cmd_group.command(name="list")
def list_devices():
    print("test")
    return


@cmd_group.command()
@click.option(
    "-b",
    "--begin",
    default=0,
    type=click.FloatRange(0, 3.3),
    help="Voltage where scan should start",
    show_default=True,
)
@click.option(
    "-e",
    "--end",
    default=3.3,
    type=click.FloatRange(0, 3.3),
    help="Voltage where scan should end",
    show_default=True,
)
@click.option(
    "-o",
    "--output",
    default=None,
    help="File path where ouput should be saved if specified",
    show_default=True,
)
@click.option(
    "-g",
    "--graph/--no-graph",
    help="flag option to specify if results should be plotted",
)
def scan(begin, end, output, graph):
    assert begin <= end, "Cannot have the begin value be greater then the end value"
    header, data = DiodeExperiment().scan(start=begin, stop=end)

    # Create lists to extract LED Voltages and currents plus their errors
    led_volts = []
    led_volt_errors = []
    currents = []
    current_errors = []

    if not output:
        for (
            total_volt,
            total_volt_error,
            resistor_volt,
            resistor_volt_error,
            led_volt,
            led_volt_error,
            current,
            current_error,
            resistance,
        ) in data:
            led_volts.append(led_volt)
            led_volt_errors.append(led_volt_error)
            currents.append(current)
            current_errors.append(current_error)

        # print the lists containing the data
        print(led_volts)
        print(currents)

        if graph:
            pass

    else:
        with open(output, "w", newline="") as file:
            writer = csv.writer(file)

            # write the header into the file first
            writer.writerow(header)

            # unpack the zip object (data) with a for loop
            for (
                total_volt,
                total_volt_error,
                resistor_volt,
                resistor_volt_error,
                led_volt,
                led_volt_error,
                current,
                current_error,
                resistance,
            ) in data:

                # write all values into a the CSV file
                writer.writerow(
                    [
                        total_volt,
                        total_volt_error,
                        resistor_volt,
                        resistor_volt_error,
                        led_volt,
                        led_volt_error,
                        current,
                        current_error,
                        resistance,
                    ]
                )

                # save values to plot/print later
                led_volts.append(led_volt)
                led_volt_errors.append(led_volt_error)
                currents.append(current)
                current_errors.append(current_error)

        # print the lists containing the data
        print(led_volts)
        print(currents)

        if graph:
            pass

    return


if __name__ == "main":
    cmd_group()
