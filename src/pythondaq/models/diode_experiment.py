from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np
from rich.progress import track


class DiodeExperiment:
    """This class allows users to run their diode experiment"""

    def __init__(self) -> None:
        """Creates an instance of the DiodeExperiment class and runs the clear()-method to initialize the lists where data is stored."""
        self.clear()

    def device_info(self, port):
        """Gets the identification string of the device

        Args:
            port (string): port of the device from which info is requested

        Returns:
            string: identification string of device at requested port
        """
        return ArduinoVISADevice(port=port).get_identification()

    def get_connected_devices(self):
        """Lists connected devices

        Returns:
            list: a list containing the ports of the connected devices
        """
        return list_devices()

    # Method to start an experiment
    def scan(
        self, port, start=0.0, stop=3.3, resistor_load=220, sample_size=5
    ) -> tuple:
        """Function to start an experiment with the diode

        Args:
            port (string): port of the device controlling the experiment
            start (float, optional): analog voltage at which the experiment starts. Defaults to 0.0.
            stop (float, optional): analog voltage at which the experiment stops. Defaults to 3.3.
            resistor_load (int, optional): resistance of the resistor in the experiment in ohm. Defaults to 220.
            sample_size (int, optional): number of samples to take at each volatage level. Defaults to 5.

        Returns:
            tuple: tuple object containing a list of headers and a zip object containing the lists with the experiment data
        """

        # Make sure to clear the old results first
        self.clear()

        # connect with the controller
        device = ArduinoVISADevice(port=port)

        # start / stop are given in analog, convert this to digital first
        start_digital = device.convert_analog_digital(start)
        stop_digital = device.convert_analog_digital(stop)

        # scan across the given experiment range
        for output_val in track(
            range(start_digital, stop_digital + 1), description="Running experiment..."
        ):
            device.set_output_value(value=output_val)

            measurement_total_volt = []
            measurement_resistor_volt = []
            # Take measurements (take a few to determine the error)
            for _ in range(sample_size):
                measurement_total_volt.append(device.get_input_voltage(channel=1))
                measurement_resistor_volt.append(device.get_input_voltage(channel=2))

            # Calculate the total volt and resister volt by taking the mean of the sample
            total_volt = np.mean(measurement_total_volt)
            resistor_volt = np.mean(measurement_resistor_volt)

            # Note standard error = standard deviation / sqrt(sample_size), if sample_size is 1 no errors can be determined
            total_volt_error = (
                np.std(measurement_total_volt) / np.sqrt(sample_size)
                if sample_size > 1
                else 0
            )
            resistor_volt_error = (
                np.std(measurement_resistor_volt) / np.sqrt(sample_size)
                if sample_size > 1
                else 0
            )

            # save the measurement
            self.add_measurement(
                resistor_load,
                total_volt,
                resistor_volt,
                total_volt_error,
                resistor_volt_error,
            )
        # After the experiment we turn the LED off
        device.set_output_value(value=0)

        # After experiment we close the connection to the controller
        device.close_connection()

        # Return the experiment data
        return self.export_experiment_data()

    # Method to add measurement to instance
    def add_measurement(
        self, R, total_volt, resistor_volt, total_volt_error, resistor_volt_error
    ) -> None:
        """Function to store measurements in the lists for experiment data

        Args:
            R (int): resistance of the resistor in the experiment in ohm
            total_volt (float): total voltage drop across the experiment setup
            resistor_volt (float): voltage drop across the resistor
            total_volt_error (float): error on total voltage drop across the experiment setup
            resistor_volt_error (float): error on voltage drop across the resistor
        """

        # make sure the load is not set to zero to avoid zero division errors
        assert R != 0, "Loads of zero are not allowed"

        # Append the values that do not need calculation
        self.resistor_loads.append(R)
        self.total_voltages.append(total_volt)
        self.total_voltages_errors.append(total_volt_error)
        self.resistor_voltages.append(resistor_volt)
        self.resistor_voltages_errors.append(resistor_volt_error)

        # Calculate the current with voltage/load and store the result
        circuit_current = resistor_volt / R
        current_error = resistor_volt_error / R
        self.currents.append(circuit_current)
        self.currents_errors.append(current_error)

        # Calculate LED voltage and load and power
        led_volt = total_volt - resistor_volt
        led_volt_error = np.sqrt((total_volt_error) ** 2 + (resistor_volt_error) ** 2)

        # Store results
        self.led_voltages.append(led_volt)
        self.led_voltages_errors.append(led_volt_error)

    def export_experiment_data(self) -> tuple:
        """Function to export the stored experiment data

        Returns:
            tuple: tuple object containing a list of headers and a zip object containing the lists with the experiment data
        """

        headers = [
            "Total voltage (V)",
            "Total V error",
            "Resistor Voltage (V)",
            "Resistor V error",
            "LED voltage (V)",
            "LED V error",
            "Current (A)",
            "Current error",
            "Resistor load (Ohm)",
        ]
        data = zip(
            self.total_voltages,
            self.total_voltages_errors,
            self.resistor_voltages,
            self.resistor_voltages_errors,
            self.led_voltages,
            self.led_voltages_errors,
            self.currents,
            self.currents_errors,
            self.resistor_loads,
        )

        return (headers, data)

    # Method to clear the stored data
    def clear(self) -> None:
        """This function clears lists containing the experiment data"""
        self.resistor_loads = []
        self.total_voltages = []
        self.total_voltages_errors = []
        self.resistor_voltages = []
        self.resistor_voltages_errors = []
        self.led_voltages = []
        self.led_voltages_errors = []
        self.currents = []
        self.currents_errors = []
