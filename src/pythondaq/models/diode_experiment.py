from pythondaq.controllers.arduino_device import list_devices, ArduinoVISADevice
import numpy as np


class DiodeExperiment:
    # Initialize the lists for storing results
    def __init__(self) -> None:
        # Clear method called to initialize the list for storing data
        self.clear()

    # Method to start an experiment
    def scan(self, start=0.0, stop=3.3, resistor_load=220, sample_size=5) -> tuple:
        """
        This function is used to start a U,I-experiment with the LED. It makes sure to clear the old data and connects to the experiment controller.
        It will scan over the entire range given with the start and stop parameters. For each value in this range it will take a sample.
        The size of this sample can be altered with the sample_size parameter.

        The function parameters are set by default but can be altered if the experiment setup is different.

        The function returns a tuple containing the experiment data. For details on the format of the data see the export_experiment_data method.
        """

        # Make sure to clear the old results first
        self.clear()

        # connect with the controller
        port = list_devices()[0]
        device = ArduinoVISADevice(port=port)

        # start / stop are given in analog, convert this to digital first
        start_digital = device.convert_analog_digital(start)
        stop_digital = device.convert_analog_digital(stop)

        # scan across the given experiment range
        for output_val in range(start_digital, stop_digital + 1):
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

            # Note standard error = standard deviation / sqrt(sample_size)
            total_volt_error = np.std(measurement_total_volt) / np.sqrt(sample_size)
            resistor_volt_error = np.std(measurement_resistor_volt) / np.sqrt(
                sample_size
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

        # Return the experiment data
        return self.export_experiment_data()

    # Method to add measurement to instance
    def add_measurement(
        self, R, total_volt, resistor_volt, total_volt_error, resistor_volt_error
    ) -> None:
        """
        This function is used to store the measured experiment data. First it stores the values that do not require calculation.
        Then it contuinues by calculating the current, LED voltage and their errors. Finally it stores these values as well.

        The function takes as parameters the resistor load, total volatage, resitor voltage, the error on the total voltage and
        the error on the resistor voltage.

        The function does not return a value
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
        """
        This funcion exports the data stored in an instance of the DiodeExperiment class. It returns a tuple containing two objects.
        The first object is a list containing headers for the data, this can be used to easily store the data in something like a CSV file.
        The second object is a zip object of all the lists that contain the data from the DiodeExperiment instance.
        The headers are in the same order as the data lists are zipped.
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
        self.resistor_loads = []
        self.total_voltages = []
        self.total_voltages_errors = []
        self.resistor_voltages = []
        self.resistor_voltages_errors = []
        self.led_voltages = []
        self.led_voltages_errors = []
        self.currents = []
        self.currents_errors = []
