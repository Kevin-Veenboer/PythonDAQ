import pyvisa


def list_devices():
    """This function shows which devices are connected

    Returns:
        list: a list containing strings of the ports from the connected devices
    """
    rm = pyvisa.ResourceManager("@py")
    ports = rm.list_resources()
    return ports


class ArduinoVISADevice:
    """This class allows users to manage their arduino experiment controller"""

    def __init__(self, port) -> None:
        """Creates an instance of the ArduinoVISADevice class and connect to the controller

        Args:
            port (string): the port of the device to connect with
        """
        # Make connection with device
        self.rm = pyvisa.ResourceManager("@py")
        self.device = self.rm.open_resource(
            port, read_termination="\r\n", write_termination="\n"
        )

    def get_identification(self) -> None:
        """Prints the identification string of the device"""
        try:
            print(self.device.query("*IDN?"))

        # If the request is made to a device which does not support this query then handle the error
        except pyvisa.errors.VisaIOError:
            print(
                "The device at the given port does not respond to this query please try anoher port"
            )

    def convert_analog_digital(self, value):
        """Converts an analog value to digital value

        Args:
            value (float): the analog value to be converted

        Returns:
            int: digital value between 0 - 1023
        """
        steps = 1023
        step_value = 3.3 / steps
        return round(float(value) / step_value)

    def convert_digital_analog(self, value):
        """Converts a digital value to an analog value

        Args:
            value (int): the digital value to be converted

        Returns:
            float: analog value between 0.0-3.3
        """
        steps = 1023
        step_value = 3.3 / steps
        return round(float(value) * step_value, 2)

    def set_output_value(self, value) -> None:
        """This function sets the value of the output channel on the device

        Args:
            value (int): value to set the output channel to, ranging from 0-1023
        """
        self.device.query(f"OUT:CH0 {value}")

    def get_output_value(self) -> int:
        """This function reads the current value on the output channel

        Returns:
            int: current value of the output channel
        """
        return self.device.query(f"OUT:CH0?")

    def get_input_value(self, channel) -> float:
        """This function measures the digital values on the input channels

        Args:
            channel (int): the channel from which the value has to be read

        Returns:
            int: digital value on the measured input channel
        """
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        elif channel == 1:
            return int(self.device.query("MEAS:CH1?"))
        else:
            return int(self.device.query("MEAS:CH1?"))

    def get_input_voltage(self, channel) -> float:
        """This function measures the digital values on the input channels

        Args:
            channel (int): the channel from which the value has to be read

        Returns:
            float: analog value on the measured input channel
        """
        if channel not in [1, 2]:
            print("Available channels are 1 and 2!")
        if channel == 1:
            return self.convert_digital_analog(int(self.device.query("MEAS:CH1?")))
        else:
            return self.convert_digital_analog(int(self.device.query("MEAS:CH2?")))
