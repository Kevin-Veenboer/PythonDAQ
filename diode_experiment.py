from arduino_device import list_devices, ArduinoVISADevice
import numpy as np


class DiodeExperiment:
    def __init__(self) -> None:
        self.Resistor_Loads = list()
        self.LED_Loads = list()

        self.Total_Voltages = list()
        self.Total_Voltages_Error = list()
        self.Resistor_Voltages = list()
        self.Resistor_Voltages_Error = list()

        self.LED_Voltages = list()
        self.Currents = list()
        self.LED_Powers = list()

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

            self.Total_Voltages.append(np.mean(Measurement_T_U))
            self.Resistor_Voltages.append(np.mean(Measurement_R_U))

            # Note standard error > Standard Deviation / sqrt(sample_size)
            self.Total_Voltages_Error.append(
                np.std(Measurement_T_U) / np.sqrt(sample_size)
            )
            self.Resistor_Voltages_Error.append(
                np.std(Measurement_R_U) / np.sqrt(sample_size)
            )

    # Method to add measurement to instance
    def add_Measurement(self, R, Total_U, Resistor_U, T_U_Err, R_U_Err) -> None:
        assert R != 0, "Loads of zero are not allowed"

        # Append load and volatage to storage lists directly
        self.Resistor_Loads.append(R)
        self.Total_Voltages.append(Total_U)
        self.Resistor_Voltages.append(Resistor_U)

        # Calculate the current with voltage/load and store teh result
        circuit_current = Resistor_U / R
        self.Currents.append(circuit_current)

        # Calculate LED voltage and load and power
        LED_U = Total_U - Resistor_U
        LED_R = LED_U / circuit_current
        LED_P = (LED_U**2) / LED_R

        # Store results
        self.LED_Voltages(LED_U)
        self.LED_Loads.append(LED_R)
        self.LED_Powers(LED_P)

    # # Might delete
    # # Methods to retrieve the measurements from an instance
    # def get_loads(self):
    #     return self.Loads

    # def get_voltages(self):
    #     return self.Voltages

    # def get_currents(self):
    #     return self.Currents

    # def get_powers(self):
    #     return self.Powers

    # Method to clear the measurements of instance
    def clear(self):
        self.Resistor_Loads = list()
        self.LED_Loads = list()
        self.Total_Voltages = list()
        self.Resistor_Voltages = list()
        self.LED_Voltages = list()
        self.Currents = list()
        self.LED_Powers = list()
