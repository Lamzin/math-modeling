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

        self.points = []

        self.__init_scene__()

        self.graphicsView.mousePressEvent = self.graphics_view_mouse_click
        self.graphicsView.mouseMoveEvent = self.graphics_view_mouse_move

        self.tableWidget.itemClicked = self.table_item_click
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)

    def cell_was_clicked(self, row, column):
        if column == 2:
            self.points = self.points[:row] + self.points[row+1:]
            self.tableWidget.removeRow(row)
            self.draw()

    def __init_scene__(self):
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

    def graphics_view_mouse_click(self, QMouseEvent):
        self.scene.setSceneRect(0, 0, self.graphicsView.size().width(), self.graphicsView.size().height())
        self.add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())

    def graphics_view_mouse_move(self, QMouseEvent):
        self.draw()
        if len(self.points) > 0:
            line = QGraphicsLineItem(
                self.points[-1][0], self.points[-1][1], QMouseEvent.pos().x(), QMouseEvent.pos().y())
            self.scene.addItem(line)

    def table_item_click(self, QListWidgetItem):
        print(QListWidgetItem.row())

    def add_point(self, x, y):
        # w = QTableWidget()
        self.tableWidget.setRowCount(len(self.points) + 1)
        self.tableWidget.setItem(len(self.points), 0, QTableWidgetItem(str(x)))
        self.tableWidget.setItem(len(self.points), 1, QTableWidgetItem(str(y)))
        self.points.append((x, y))
        self.draw()

    def draw(self):
        self.scene.clear()
        for x, y in self.points:
            point = QGraphicsEllipseItem(x - 1, y - 1, 2, 2)
            self.scene.addItem(point)
        for i in range(1, len(self.points)):
            line = QGraphicsLineItem(
                self.points[i - 1][0], self.points[i - 1][1], self.points[i][0], self.points[i][1])
            self.scene.addItem(line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
