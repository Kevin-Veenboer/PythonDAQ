import pyvisa

# Function to display devices
def list_devices():
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports


class ArduinoVISADevice:
    def __init__(self, port) -> None:
        # Make connection with device
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

        # Initialize the channel values
        self.channel_0_value = None
        self.channel_1_value = None
        self.channel_2_value = None

    # Method to get device identification string
    def get_identification(self) -> None:
        print(self.device.query("*IDN?"))

    # Defining conversion functions
    def convert_analog_digital(self, value):
        steps = 1023
        step_value = 3.3 / steps
        return round(float(value) / step_value)

    def convert_digital_analog(self, value):
        steps = 1023
        step_value = 3.3 / steps
        return round(float(value) * step_value, 2)

    # Method to set output values (0-1023 input expected)
    def set_output_value(self, value) -> None:
        self.device.query(f"OUT:CH0 {value}")

    # Functions to get output value (CH0) or input values (CH1 or CH2)
    def get_output_value(self) -> int:
        # if no value is set then return 0
        if self.channel_0_value == None:
            return 0
        return self.channel_0_value

    # Function to get the value on channel 1 or 2 of the device as a digital value
    def get_input_value(self, channel) -> float:
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        elif channel == 1:
            return float(self.device.query("MEAS:CH1?"))
        else:
            return float(self.device.query("MEAS:CH1?"))

    # Function to get the value on channel 1 or 2 of the device as an analog value
    def get_input_voltage(self, channel) -> float:
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        if channel == 1:
            return self.convert_digital_analog(int(self.device.query("MEAS:CH1?")))
        else:
            return self.convert_digital_analog(int(self.device.query("MEAS:CH2?")))
