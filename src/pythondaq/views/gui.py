import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
from pythondaq.models.diode_experiment import DiodeExperiment
import numpy as np
import pandas as pd


# PyQtGraph global options
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Create plot widget
        self.plot_window = pg.PlotWidget()

        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # Create vertical layout
        vbox = QtWidgets.QVBoxLayout(central_widget)
        vbox.addWidget(self.plot_window)

        # Create Horizontal layout
        hbox = QtWidgets.QHBoxLayout()
        vbox.addLayout(hbox)

        # Create Vbox for start value
        self.start_box = QtWidgets.QVBoxLayout()
        start_label = QtWidgets.QLabel("Start voltage")
        self.start_input = QtWidgets.QDoubleSpinBox()
        self.start_input.setRange(0.0, 3.3)
        self.start_input.setSingleStep(0.01)
        self.start_input.setValue(0.0)
        self.start_box.addWidget(start_label)
        self.start_box.addWidget(self.start_input)

        # Create Vbox for start value
        self.stop_box = QtWidgets.QVBoxLayout()
        stop_label = QtWidgets.QLabel("Stop voltage")
        self.stop_input = QtWidgets.QDoubleSpinBox()
        self.stop_input.setRange(0.0, 3.3)
        self.stop_input.setSingleStep(0.01)
        self.stop_input.setValue(3.3)
        self.stop_box.addWidget(stop_label)
        self.stop_box.addWidget(self.stop_input)

        # Create Vbox for start value
        self.sample_box = QtWidgets.QVBoxLayout()
        sample_label = QtWidgets.QLabel("Sample size")
        self.sample_input = QtWidgets.QSpinBox()
        self.sample_input.setRange(1, 25)
        self.sample_input.setValue(5)
        self.sample_box.addWidget(sample_label)
        self.sample_box.addWidget(self.sample_input)

        # Create Vbox for start and save button
        self.button_box = QtWidgets.QVBoxLayout()
        self.start_button_label = QtWidgets.QLabel("")
        self.start_button = QtWidgets.QPushButton("start")
        self.start_button_box.addWidget(self.start_button_label)
        self.start_button_box.addWidget(self.start_button)

        # Add boxes to hbox
        hbox.addLayout(self.start_box)
        hbox.addLayout(self.stop_box)
        hbox.addLayout(self.sample_box)
        hbox.addLayout(self.button_box)

        # plot data on button click
        self.start_button.clicked.connect(self.run_measurement)

    @Slot()
    def run_measurement(self):
        # Clear old results
        self.plot_window.clear()

        # Get data
        headers, data = DiodeExperiment().scan(
            port="ASRL5::INSTR",
            start=self.start_input.value(),
            stop=self.stop_input.value(),
            sample_size=self.sample_input.value(),
        )

        # Create lists to extract LED Volt and Current plus their errors
        self.led_volts = []
        self.led_volt_errors = []
        self.currents = []
        self.current_errors = []

        for (
            _,
            _,
            _,
            _,
            led_volt,
            led_volt_error,
            current,
            current_error,
            _,
        ) in data:
            led_volts.append(led_volt)
            led_volt_errors.append(led_volt_error)
            currents.append(current)
            current_errors.append(current_error)

        self.plot_window.plot(led_volts, currents, symbol="o", symbolSize=5, pen=None)
        error_items = pg.ErrorBarItem(
            x=np.array(led_volts),
            y=np.array(currents),
            width=2 * np.array(led_volt_errors),
            height=2 * np.array(current_errors),
        )

        self.plot_window.addItem(error_items)

        self.plot_window.setLabel("left", "Current (A)")
        self.plot_window.setLabel("bottom", "Volt (V)")

    def save_data(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(filter="CSV files (*.csv)")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
