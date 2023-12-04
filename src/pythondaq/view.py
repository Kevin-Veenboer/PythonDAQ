import sys

import numpy as np

from PySide6 import QtWidgets, QtCore
import pyqtgraph as pg

from pythondaq.model import Experiment


class UserInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        vbox = QtWidgets.QVBoxLayout(central_widget)
        self.plot_widget = pg.PlotWidget()
        vbox.addWidget(self.plot_widget)
        start_button = QtWidgets.QPushButton("Start")
        vbox.addWidget(start_button)

        start_button.clicked.connect(self.start_scan)

        # Plot Timer
        self.plot_timer = QtCore.QTimer()
        # Roep plot function ieder 100ms aan
        self.plot_timer.timeout.connect(self.plot)
        self.plot_timer.start(100)

        # Maak een instance aan van Experiment
        self.experiment = Experiment()

    def start_scan(self):
        self.experiment.start_scan(0, np.pi, 50)

    def plot(self):
        """Clear the plot widget and display experimental data."""
        self.plot_widget.clear()
        self.plot_widget.plot(
            self.experiment.x, self.experiment.y, symbol="o", symbolSize=5, pen=None
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
