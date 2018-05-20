#  -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5 import uic

import os
import sys

from modeling import MathModelingSolver


class Modeling(QTabWidget):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'tabwidget.ui')
        uic.loadUi(ui_path, self)

        self.__init__tab1__stuff__()
        self.__init__tab2__stuff__()
        self.__init__tab3__stuff__()
        self.__init__tab4__stuff__()
        self.__init__tab5__stuff__()

    def __init__tab1__stuff__(self):
        def calc():
            L = self.lineEdit_L.text()
            c = 5
            y_sol = self.lineEdit_y.text()
            self.model = MathModelingSolver(L, y_sol)
            u = self.model.perturbation
            self.lineEdit_G.setText("diff(f, t, t) - %s**2*(diff(f, x1, x1) \
+ diff(f, x2, x2))" % c)
            # self.lineEdit_G.setText("to_calc: " + L)
            self.lineEdit_u.setText(str(u))
        self.tab1_button_calc.clicked.connect(calc)

        self.tab1_button_next.clicked.connect(lambda: self.setCurrentIndex(1))

    def __init__tab2__stuff__(self):
        self.tab2_graphics_scene = QGraphicsScene()
        self.tab2_graphics.setScene(self.tab2_graphics_scene)
        self.stop_drow = False

        def graphics_draw():
            self.tab2_graphics_scene.clear()
            for x1, x2 in self.model.spatial_area:
                self.tab2_graphics_scene.addItem(
                    QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2))
            for i in range(1, len(self.model.spatial_area)):
                self.tab2_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[i - 1][0], self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0], self.model.spatial_area[i][1]))
            if self.stop_drow and len(self.model.spatial_area) > 0:
                self.tab2_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[len(self.model.spatial_area) - 1][0],
                    self.model.spatial_area[len(self.model.spatial_area) - 1][1],
                    self.model.spatial_area[0][0],
                    self.model.spatial_area[0][1]))

        def add_point(x1, x2):
            self.tab2_table.setRowCount(len(self.model.spatial_area) + 1)
            self.tab2_table.setItem(len(self.model.spatial_area), 0, QTableWidgetItem(str(x1)))
            self.tab2_table.setItem(len(self.model.spatial_area), 1, QTableWidgetItem(str(x2)))
            self.model.spatial_area.append((x1, x2))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            self.tab2_graphics_scene.setSceneRect(
                0, 0, self.tab2_graphics.size().width(), self.tab2_graphics.size().height())
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab2_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse2_click(QMouseEvent):
            self.stop_drow = True
            graphics_draw()
        self.tab2_graphics.mouseDoubleClickEvent = graphics_mouse2_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
            if len(self.model.spatial_area) > 0 and not self.stop_drow:
                line = QGraphicsLineItem(
                    self.model.spatial_area[-1][0], self.model.spatial_area[-1][1], QMouseEvent.pos().x(), QMouseEvent.pos().y())
                self.tab2_graphics_scene.addItem(line)
        self.tab2_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 2:
                del self.model.spatial_area[row]
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
            for x1, x2 in self.model.spatial_area:
                self.tab3_graphics_scene.addItem(QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2))
            for i in range(1, len(self.model.spatial_area)):
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[i - 1][0], self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0], self.model.spatial_area[i][1]))
            if len(self.model.spatial_area) > 1:
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[0][0], self.model.spatial_area[0][1],
                    self.model.spatial_area[-1][0], self.model.spatial_area[-1][1]))
            for x1, x2, _, _ in self.model.initial_conditions:
                self.tab3_graphics_scene.addItem(QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2))

        def add_point(x1, x2):
            self.tab3_table.setRowCount(len(self.model.initial_conditions) + 1)
            self.tab3_table.setItem(len(self.model.initial_conditions), 0, QTableWidgetItem(str(x1)))
            self.tab3_table.setItem(len(self.model.initial_conditions), 1, QTableWidgetItem(str(x2)))
            exact = self.model.exact_solution_at_point(x1, x2)
            self.tab3_table.setItem(len(self.model.initial_conditions), 2, QTableWidgetItem(str(exact)))
            self.tab3_table.setItem(len(self.model.initial_conditions), 3, QTableWidgetItem(str(exact)))
            self.model.initial_conditions.append((x1, x2, exact, exact))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab3_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
        self.tab3_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 4:
                del self.model.initial_conditions[row]
                self.tab3_table.removeRow(row)
                graphics_draw()
        self.tab3_table.cellClicked.connect(table_cell_click)

        self.tab3_button_prev.clicked.connect(lambda: self.setCurrentIndex(1))  # because of page index start from 0
        self.tab3_button_next.clicked.connect(lambda: self.setCurrentIndex(3))

    def __init__tab4__stuff__(self):
        self.tab4_graphics_scene = QGraphicsScene()
        self.tab4_graphics.setScene(self.tab4_graphics_scene)

        def graphics_draw():
            self.tab4_graphics_scene.setSceneRect(
                0, 0, self.tab4_graphics.size().width(), self.tab4_graphics.size().height())
            self.tab4_graphics_scene.clear()
            for x1, x2 in self.model.spatial_area:
                self.tab4_graphics_scene.addItem(QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2))
            for i in range(1, len(self.model.spatial_area)):
                self.tab4_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[i - 1][0], self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0], self.model.spatial_area[i][1]))
            if len(self.model.spatial_area) > 1:
                self.tab4_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[0][0], self.model.spatial_area[0][1],
                    self.model.spatial_area[-1][0], self.model.spatial_area[-1][1]))
            for x1, x2, _, _, _ in self.model.boundary_conditions:
                self.tab4_graphics_scene.addItem(QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2))

        def add_point(x1, x2):
            self.tab4_table.setRowCount(len(self.model.boundary_conditions) + 1)
            self.tab4_table.setItem(len(self.model.boundary_conditions), 0, QTableWidgetItem(str(x1)))
            self.tab4_table.setItem(len(self.model.boundary_conditions), 1, QTableWidgetItem(str(x2)))
            t = self.doubleSpinBox_t.value()
            self.tab4_table.setItem(len(self.model.boundary_conditions), 2, QTableWidgetItem(str(t)))
            exact = self.model.exact_solution_at_point(x1, x2, t)
            self.tab4_table.setItem(len(self.model.boundary_conditions), 3, QTableWidgetItem(str(exact)))
            self.tab4_table.setItem(len(self.model.boundary_conditions), 4, QTableWidgetItem(str(exact)))
            self.model.boundary_conditions.append((x1, x2, t, exact, exact))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            add_point(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        self.tab4_graphics.mousePressEvent = graphics_mouse_click

        def graphics_mouse_move(QMouseEvent):
            graphics_draw()
        self.tab4_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 5:
                del self.model.boundary_conditions[row]
                self.tab4_table.removeRow(row)
                graphics_draw()
        self.tab4_table.cellClicked.connect(table_cell_click)

        self.tab4_button_prev.clicked.connect(lambda: self.setCurrentIndex(2))  # because of page index start from 0
        self.tab4_button_next.clicked.connect(lambda: self.setCurrentIndex(4))

    def __init__tab5__stuff__(self):
        def calc():
            print('clicked: {}'.format(self.lineEdit_y.text()))

            from subprocess import Popen, call

            dir_path = os.path.dirname(os.path.realpath(__file__))
            print(os.path.join(dir_path, 'vpython_example.py'))
            if os.name != 'nt':  # not windows
                call(["pkill python {}".format(os.path.join(dir_path, 'vpython_example.py'))], shell=True)
            Popen(["python", os.path.join(dir_path, 'vpython_example.py'), self.lineEdit_y.text()], shell=True)

        self.showResults.clicked.connect(calc)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
