import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Slot
import pyqtgraph as pg
from pythondaq.models.diode_experiment import DiodeExperiment


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


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
