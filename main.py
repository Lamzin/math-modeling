from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget

from PyQt5 import uic

import os
import sys


class Modeling(QTabWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "tabwidget.ui")
        uic.loadUi(ui_path, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
