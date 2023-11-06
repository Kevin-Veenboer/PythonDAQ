class ElectronicLoadMeasurement:
    def __init__(self):
        self.Loads = list()
        self.Voltages = list()
        self.Currents = list()
        self.Powers = list()

    # Method to add measurement to instance
    def add_Measurement(self, R, U):
        assert R != 0, "Loads of zero are not allowed"

        # Append load and volatage to storage lists directly
        self.Loads.append(R)
        self.Voltages.append(U)

        # Calculate the current with voltage/load and store teh result
        self.Currents.append(U / R)

        # Calculate the power with (U**2/R) this is equal to (I**2 * R), store the result
        self.Powers.append(U**2 / R)

    # Methods to retrieve the measurements from an instance
    def get_loads(self):
        return self.Loads

    def get_voltages(self):
        return self.Voltages

    def get_currents(self):
        return self.Currents

    def get_powers(self):
        return self.Powers

    # Method to clear the measurements of instance
    def clear(self):
        self.Loads = list()
        self.Voltages = list()
        self.Currents = list()
        self.Powers = list()


## Testing the class

# Creating and adding a few measurement
ELM = ElectronicLoadMeasurement()
for volt in range(2, 102, 2):
    ELM.add_Measurement(200, volt)

# Testing the data retrieval
print("\nLists with data:")
print(
    f"Loads: {ELM.get_loads()}\n\nVoltages: {ELM.get_voltages()}\n\nCurrents: {ELM.get_currents()}\n\nPowers: {ELM.get_powers()}"
)

# Testing clear function by making sure data retrieval gives empty lists after using the method
ELM.clear()
print("\nLists are empty after .clear() method was used")
print(
    f"Loads: {ELM.get_loads()}\n\nVoltages: {ELM.get_voltages()}\n\nCurrents: {ELM.get_currents()}\n\nPowers: {ELM.get_powers()}"
)
