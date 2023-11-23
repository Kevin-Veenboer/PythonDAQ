from pythondaq.models.diode_experiment import DiodeExperiment
import csv
from os import listdir, path, mkdir, getcwd
import matplotlib.pyplot as plt
import click


@click.group()
def cmd_group():
    pass


@cmd_group.command(name="list")
@click.option(
    "-s",
    "--search",
    default=None,
    help="only return devices which match with given search value",
    show_default=True,
)
def click_list(search=None):
    """Function that prints a list of the connected devices

    Args:
        search (string, optional): search term to match connected devices to. Defaults to None.
    """
    list_devices(search, display=True)


def list_devices(search=None, display=False):
    """Function that prints a list of the connected devices

    Args:
        search (string, optional): search term to match connected devices to. Defaults to None.
        display (bool, optional): flag to toggle printing the device list. Defaults to False.

    Returns:
        list: list containing the ports of connected devices
    """
    if not search:
        print(DiodeExperiment().get_connected_devices())
        return DiodeExperiment().get_connected_devices()
    else:
        matching = []
        for device in DiodeExperiment().get_connected_devices():
            if search in device:
                matching.append(device)
        # This makes sure that nothing is printed when the function is called in info() or scan()
        if display:
            print(matching)
            return
        return matching


@cmd_group.command()
@click.option(
    "-p",
    "--port",
    default=None,
    help="port of the device from which info is requested",
    show_default=None,
)
def info(port):
    """Function that requests the identification string from a device

    Args:
        port (string): port of a connected device. Partial ports are attempted to be matched.
    """
    if not port:
        print("No device port was given")

    else:
        ports = list_devices(port)
        assert (
            len(ports) < 2
        ), f"More than one device matches the given port value: {ports}"
        assert len(ports) > 0, "No devices match the given port value"
        port = ports.pop()
        DiodeExperiment().device_info(port=port)


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
@click.option(
    "-n",
    "--number",
    default=5,
    help="sample size of measurments per voltage",
    show_default=True,
)
@click.argument("port", type=str)
def scan(port, begin, end, output, graph, number):
    """Function that starts an experiment

    Args:
        port (string): port of the experiment controller device. Partial ports are attempted to be matched.
        begin (float): analog voltage at which the experiment starts. Defaults to 0.0.
        end (float): analog voltage at which the experiment stops. Defaults to 3.3.
        output (string): path at which data should be stored. Defaults to None.
        graph (bool): flag variable to determine whether output needs to be plotted. Defaults to False.
        number (int): number of samples to take at each voltage level. Defaults to 5.
    """
    assert begin <= end, "Cannot have the begin value be greater then the end value"
    assert number > 0, "Cannot have a sample size of less then one"

    # This uses the searh functionality of the list function to match incomplete port inputs
    ports = list_devices(port)
    assert len(ports) < 2, f"More than one device matches the given port value: {ports}"
    assert len(ports) > 0, "No devices match the given port value"
    port = ports.pop()

    header, data = DiodeExperiment().scan(
        port=port, start=begin, stop=end, sample_size=number
    )

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
            plt.show()

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
            plt.show()

    return


if __name__ == "main":
    cmd_group()
