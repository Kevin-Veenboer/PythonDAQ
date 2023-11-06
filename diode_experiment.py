from arduino_device import list_devices, ArduinoVISADevice
import numpy as np


class DiodeExperiment:
    def __init__(self) -> None:
        # TA said I did not have to use resistor error
        self.Resistor_Loads = list()
        self.Total_Voltages = list()
        self.Total_Voltages_Error = list()
        self.Resistor_Voltages = list()
        self.Resistor_Voltages_Error = list()
        self.LED_Voltages = list()
        self.LED_Voltages_Error = list()
        self.Currents = list()
        self.Currents_Error = list()

    # Method to start an experiment
    def scan(self, device_range=1024, Resistor_Load=220, sample_size=5) -> list():
        # Make sure to clear the old results first
        self.clear()

        port = list_devices()[0]
        Device = ArduinoVISADevice(port=port)

        for output_val in range(0, device_range):
            Device.set_output_value(value=output_val)

            Measurement_T_U = list()
            Measurement_R_U = list()
            # Take measurements (take a few to determine the error)
            for _ in range(sample_size):
                Measurement_T_U.append(Device.get_input_value(channel=1))
                Measurement_R_U.append(Device.get_input_value(channel=2))

            # Calculate the total volt and resister volt
            Total_U = np.mean(Measurement_T_U)
            Resistor_U = np.mean(Measurement_R_U)

            # Note standard error > Standard Deviation / sqrt(sample_size)
            T_U_Err = np.std(Measurement_T_U) / np.sqrt(sample_size)
            R_U_Err = np.std(Measurement_R_U) / np.sqrt(sample_size)

            # Add the measurement
            self.add_Measurement(Resistor_Load, Total_U, Resistor_U, T_U_Err, R_U_Err)

        # Return the experiment data as tuple with headers and data
        return self.export_experiment_data()

    # Method to add measurement to instance
    def add_Measurement(self, R, Total_U, Resistor_U, T_U_Err, R_U_Err) -> None:
        assert R != 0, "Loads of zero are not allowed"

        # Append the values that do not need calculation
        self.Resistor_Loads.append(R)
        self.Total_Voltages.append(Total_U)
        self.Total_Voltages_Error.append(T_U_Err)
        self.Resistor_Voltages.append(Resistor_U)
        self.Resistor_Voltages.append(R_U_Err)

        # Calculate the current with voltage/load and store the result
        circuit_current = Resistor_U / R
        current_err = R_U_Err / R
        self.Currents.append(circuit_current)
        self.Currents_Error.append(current_err)

        # Calculate LED voltage and load and power
        LED_U = Total_U - Resistor_U
        LED_U_err = np.sqrt((T_U_Err) ** 2 + (R_U_Err) ** 2)

        # Store results
        self.LED_Voltages.append(LED_U)
        self.LED_Voltages_Error.append(LED_U_err)

    def export_experiment_data(self) -> list:
        headers = (
            "Total voltage (V)",
            "Total V error",
            "Resistor Voltage (V)",
            "Resistor V error",
            "LED voltage (V)",
            "LED V error",
            "Current (A)",
            "Current error",
            "Resistor load (Ohm)",
        )
        data = zip(
            self.Total_Voltages,
            self.Total_Voltages_Error,
            self.Resistor_Voltages,
            self.Resistor_Voltages_Error,
            self.LED_Voltages,
            self.LED_Voltages_Error,
            self.Currents,
            self.Currents_Error,
            self.Resistor_Loads,
        )

        return (headers, data)

    def clear(self):
        self.Resistor_Loads = list()
        self.Total_Voltages = list()
        self.Total_Voltages_Error = list()
        self.Resistor_Voltages = list()
        self.Resistor_Voltages_Error = list()
        self.LED_Voltages = list()
        self.LED_Voltages_Error = list()
        self.Currents = list()
        self.Currents_Error = list()


experiment = DiodeExperiment()
test = experiment.scan()
print(test)
print(type(test))
