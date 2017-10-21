from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsWidget

from PyQt5 import uic

import os
import sys


class Modeling(QTabWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), "tabwidget.ui")
        uic.loadUi(ui_path, self)

        self.__init__common__stuff__()
        self.__init__tab2__stuff__()

    def __init__common__stuff__(self):
        self.points = []

    def __init__tab2__stuff__(self):
        self.tab2_graphics_scene = QGraphicsScene()
        self.tab2_graphics.setScene(self.tab2_graphics_scene)

        def graphics_draw():
            self.tab2_graphics_scene.clear()
            for x, y in self.points:
                self.tab2_graphics_scene.addItem(QGraphicsEllipseItem(x - 1, y - 1, 2, 2))
            for i in range(1, len(self.points)):
                self.tab2_graphics_scene.addItem(QGraphicsLineItem(
                    self.points[i - 1][0], self.points[i - 1][1], self.points[i][0], self.points[i][1]))

        def add_point(x, y):
            self.tab2_table.setRowCount(len(self.points) + 1)
            self.tab2_table.setItem(len(self.points), 0, QTableWidgetItem(str(x)))
            self.tab2_table.setItem(len(self.points), 1, QTableWidgetItem(str(y)))
            self.points.append((x, y))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            self.tab2_graphics_scene.setSceneRect(
                0, 0, self.tab2_graphics.size().width(), self.tab2_graphics.size().height())
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab2_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
            if len(self.points) > 0:
                line = QGraphicsLineItem(
                    self.points[-1][0], self.points[-1][1], QMouseEvent.pos().x(), QMouseEvent.pos().y())
                self.tab2_graphics_scene.addItem(line)
        self.tab2_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_clicked(row, column):
            if column == 2:
                self.points = self.points[:row] + self.points[row + 1:]
                self.tab2_table.removeRow(row)
                graphics_draw()
        self.tab2_table.cellClicked.connect(table_cell_clicked)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
