from arduino_device import list_devices, ArduinoVISADevice
import numpy as np


class DiodeExperiment:
    def __init__(self) -> None:
        # TA said I did not have to use resistor errors
        self.resistor_loads = []
        self.total_voltages = []
        self.total_voltages_errors = []
        self.resistor_voltages = []
        self.resistor_voltages_errors = []
        self.led_voltages = []
        self.led_voltages_errors = []
        self.currents = []
        self.currents_errors = []

    # Method to start an experiment
    def scan(self, device_range=1024, resistor_load=220, sample_size=5) -> tuple:
        # Make sure to clear the old results first
        self.clear()

        port = list_devices()[0]
        device = ArduinoVISADevice(port=port)

        for output_val in range(0, device_range):
            device.set_output_value(value=output_val)

            measurement_total_volt = []
            measurement_resistor_volt = []
            # Take measurements (take a few to determine the error)
            for _ in range(sample_size):
                measurement_total_volt.append(device.get_input_value(channel=1))
                measurement_resistor_volt.append(device.get_input_value(channel=2))

            # Calculate the total volt and resister volt
            total_volt = np.mean(measurement_total_volt)
            resistor_volt = np.mean(measurement_resistor_volt)

            # Note standard error = Standard Deviation / sqrt(sample_size)
            total_volt_error = np.std(measurement_total_volt) / np.sqrt(sample_size)
            resistor_volt_error = np.std(measurement_resistor_volt) / np.sqrt(
                sample_size
            )

            # Add the measurement
            self.add_measurement(
                resistor_load,
                total_volt,
                resistor_volt,
                total_volt_error,
                resistor_volt_error,
            )

        # Return the experiment data as tuple with headers and data
        return self.export_experiment_data()

    # Method to add measurement to instance
    def add_measurement(
        self, R, total_volt, resistor_volt, total_volt_error, resistor_volt_error
    ) -> None:
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

    def clear(self):
        self.resistor_loads = []
        self.total_voltages = []
        self.total_voltages_errors = []
        self.resistor_voltages = []
        self.resistor_voltages_errors = []
        self.led_voltages = []
        self.led_voltages_errors = []
        self.currents = []
        self.currents_errors = []
