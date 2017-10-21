from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsWidget

from PyQt5 import uic

import os
import sys


class Modeling(QTabWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'tabwidget.ui')
        uic.loadUi(ui_path, self)

        self.__init__common__stuff__()
        self.__init__tab2__stuff__()
        self.__init__tab3__stuff__()

    def __init__common__stuff__(self):
        self.spatial_area = []
        self.initial_conditions = []

    def __init__tab2__stuff__(self):
        self.tab2_graphics_scene = QGraphicsScene()
        self.tab2_graphics.setScene(self.tab2_graphics_scene)

        def graphics_draw():
            self.tab2_graphics_scene.clear()
            for x, y in self.spatial_area:
                self.tab2_graphics_scene.addItem(QGraphicsEllipseItem(x - 1, y - 1, 2, 2))
            for i in range(1, len(self.spatial_area)):
                self.tab2_graphics_scene.addItem(QGraphicsLineItem(
                    self.spatial_area[i - 1][0], self.spatial_area[i - 1][1],
                    self.spatial_area[i][0], self.spatial_area[i][1]))

        def add_point(x, y):
            self.tab2_table.setRowCount(len(self.spatial_area) + 1)
            self.tab2_table.setItem(len(self.spatial_area), 0, QTableWidgetItem(str(x)))
            self.tab2_table.setItem(len(self.spatial_area), 1, QTableWidgetItem(str(y)))
            self.spatial_area.append((x, y))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            self.tab2_graphics_scene.setSceneRect(
                0, 0, self.tab2_graphics.size().width(), self.tab2_graphics.size().height())
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab2_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
            if len(self.spatial_area) > 0:
                line = QGraphicsLineItem(
                    self.spatial_area[-1][0], self.spatial_area[-1][1], QMouseEvent.pos().x(), QMouseEvent.pos().y())
                self.tab2_graphics_scene.addItem(line)
        self.tab2_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 2:
                del self.spatial_area[row]
                self.tab2_table.removeRow(row)
                graphics_draw()
        self.tab2_table.cellClicked.connect(table_cell_click)

        self.tab2_button_prev.clicked.connect(lambda: self.setCurrentIndex(0))  # because of page index start from 0
        self.tab2_button_next.clicked.connect(lambda: self.setCurrentIndex(2))

    def __init__tab3__stuff__(self):
        self.tab3_graphics_scene = QGraphicsScene()
        self.tab3_graphics.setScene(self.tab3_graphics_scene)

        def graphics_draw():
            self.tab3_graphics_scene.setSceneRect(
                0, 0, self.tab3_graphics.size().width(), self.tab3_graphics.size().height())
            self.tab3_graphics_scene.clear()
            for x, y in self.spatial_area:
                self.tab3_graphics_scene.addItem(QGraphicsEllipseItem(x - 1, y - 1, 2, 2))
            for i in range(1, len(self.spatial_area)):
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.spatial_area[i - 1][0], self.spatial_area[i - 1][1],
                    self.spatial_area[i][0], self.spatial_area[i][1]))
            if len(self.spatial_area) > 1:
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.spatial_area[0][0], self.spatial_area[0][1],
                    self.spatial_area[-1][0], self.spatial_area[-1][1]))
            for x, y, _, _ in self.initial_conditions:
                self.tab3_graphics_scene.addItem(QGraphicsEllipseItem(x - 1, y - 1, 2, 2))

        def add_point(x, y):
            self.tab3_table.setRowCount(len(self.initial_conditions) + 1)
            self.tab3_table.setItem(len(self.initial_conditions), 0, QTableWidgetItem(str(x)))
            self.tab3_table.setItem(len(self.initial_conditions), 1, QTableWidgetItem(str(y)))
            self.tab3_table.setItem(len(self.initial_conditions), 2, QTableWidgetItem('-1'))
            self.tab3_table.setItem(len(self.initial_conditions), 3, QTableWidgetItem('0'))
            self.initial_conditions.append((x, y, -1, 0))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab3_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
        self.tab3_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 4:
                del self.initial_conditions[row]
                self.tab3_table.removeRow(row)
                graphics_draw()
        self.tab3_table.cellClicked.connect(table_cell_click)

        self.tab3_button_prev.clicked.connect(lambda: self.setCurrentIndex(1))  # because of page index start from 0
        self.tab3_button_next.clicked.connect(lambda: self.setCurrentIndex(3))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
