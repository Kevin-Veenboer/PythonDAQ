import pyvisa

# function to display devices
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
        self.CH0_value = None
        self.CH1_value = None
        self.CH2_value = None

    def get_identification(self) -> None:
        print(self.device.query("*IDN?"))

    # Method to set output values (0-1023 input expected)
    def set_output_value(self, value) -> None:
        self.device.query(f"OUT:CH0 {value}")

    # functions to get output value (CH0) or input values (CH1 or CH2)
    def get_output_value(self) -> int:
        # if no value is set then return 0
        if self.CH0_value == None:
            return 0
        return self.CH0_value

    def get_input_value(self, channel) -> int:
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        elif channel == 1:
            return int(self.device.query("MEAS:CH1?"))
        else:
            return int(self.device.query("MEAS:CH1?"))
