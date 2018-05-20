#  -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QTableWidgetItem
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem
from PyQt5 import uic

import os
import sys
import pickle

from modeling import MathModelingSolver

data_path = 'data'


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

        self.model = None

    def __init__tab1__stuff__(self):
        def calc():
            c = self.doubleSpinBox_c.text()
            try:
                c = int(c)
            except:
                pass
            L = self.lineEdit_L.text().replace('^', '**')
            L = (
                ' '.join(L.split('**')[0].split(' ')[:-1]) + ' ' +
                str(c) + '**' + L.split('**')[-1]
            )
            self.lineEdit_L.setText(L.replace('c', str(c)).replace('**', '^'))
            self.lineEdit_G.setText(
                "H(c*(t-t')-r)/(2*pi*c*(c^2*(t-t')**2-r^2))"
                .replace('c', str(c))
            )

            y_sol = self.lineEdit_y.text().replace('^', '**')
            self.model = MathModelingSolver(L, y_sol)
            u = self.model.perturbation
            self.lineEdit_u.setText(str(u))

        def button_next():
            if not self.model:
                calc()
            self.setCurrentIndex(1)

        self.tab1_button_calc.clicked.connect(calc)

        self.tab1_button_next.clicked.connect(button_next)

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
                    self.model.spatial_area[i - 1][0],
                    self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0],
                    self.model.spatial_area[i][1]))
            if self.stop_drow and len(self.model.spatial_area) > 0:
                self.tab2_graphics_scene.addItem(
                    QGraphicsLineItem(
                        self.model.spatial_area[
                            len(self.model.spatial_area) - 1
                        ][0],
                        self.model.spatial_area[
                            len(self.model.spatial_area) - 1
                        ][1],
                        self.model.spatial_area[0][0],
                        self.model.spatial_area[0][1]
                    )
                )

        def add_point(x1, x2):
            self.tab2_table.setRowCount(len(self.model.spatial_area) + 1)
            self.tab2_table.setItem(
                len(self.model.spatial_area),
                0,
                QTableWidgetItem(str(x1))
            )
            self.tab2_table.setItem(
                len(self.model.spatial_area),
                1,
                QTableWidgetItem(str(x2))
            )
            self.model.spatial_area.append((x1, x2))
            graphics_draw()

        def graphics_mouse_click(QMouseEvent):
            self.tab2_graphics_scene.setSceneRect(
                0,
                0,
                self.tab2_graphics.size().width(),
                self.tab2_graphics.size().height()
            )
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
                    self.model.spatial_area[-1][0],
                    self.model.spatial_area[-1][1],
                    QMouseEvent.pos().x(),
                    QMouseEvent.pos().y()
                )
                self.tab2_graphics_scene.addItem(line)
        self.tab2_graphics.mouseMoveEvent = graphics_mouse_move

        def table_cell_click(row, column):
            if column == 2:
                del self.model.spatial_area[row]
                self.tab2_table.removeRow(row)
                graphics_draw()
        self.tab2_table.cellClicked.connect(table_cell_click)

        def table_cell_change(row, column):
            if len(self.model.spatial_area) > row:
                if column < 2:
                    r = self.model.spatial_area[row]
                    to_edit = int(self.tab2_table.item(row, column).text())
                    res = tuple((v if i != column else to_edit) for i, v in
                                enumerate(r))
                    self.model.spatial_area[row] = res
                    graphics_draw()
        self.tab2_table.cellChanged.connect(table_cell_change)

        self.tab2_button_prev.clicked.connect(lambda: self.setCurrentIndex(0))
        self.tab2_button_next.clicked.connect(lambda: self.setCurrentIndex(2))

    def __init__tab3__stuff__(self):
        self.tab3_graphics_scene = QGraphicsScene()
        self.tab3_graphics.setScene(self.tab3_graphics_scene)

        def graphics_draw():
            self.tab3_graphics_scene.setSceneRect(
                0,
                0,
                self.tab3_graphics.size().width(),
                self.tab3_graphics.size().height()
            )
            self.tab3_graphics_scene.clear()
            for x1, x2 in self.model.spatial_area:
                self.tab3_graphics_scene.addItem(
                    QGraphicsEllipseItem(x1 - 1, x2 - 1, 2, 2)
                )
            for i in range(1, len(self.model.spatial_area)):
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[i - 1][0],
                    self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0],
                    self.model.spatial_area[i][1]
                ))
            if len(self.model.spatial_area) > 1:
                self.tab3_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[0][0],
                    self.model.spatial_area[0][1],
                    self.model.spatial_area[-1][0],
                    self.model.spatial_area[-1][1]
                ))
            for x1, x2, _, _ in self.model.initial_conditions:
                self.tab3_graphics_scene.addItem(QGraphicsEllipseItem(
                    x1 - 1, x2 - 1, 2, 2
                ))

        def add_point(x1, x2):
            self.tab3_table.setRowCount(len(self.model.initial_conditions) + 1)
            self.tab3_table.setItem(
                len(self.model.initial_conditions),
                0,
                QTableWidgetItem(str(x1))
            )
            self.tab3_table.setItem(
                len(self.model.initial_conditions),
                1,
                QTableWidgetItem(str(x2))
            )
            exact = self.model.exact_solution_at_point(x1, x2)
            self.tab3_table.setItem(
                len(self.model.initial_conditions),
                2,
                QTableWidgetItem(str(exact))
            )
            self.tab3_table.setItem(
                len(self.model.initial_conditions),
                3,
                QTableWidgetItem(str(exact))
            )
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

        def table_cell_change(row, column):
            if len(self.model.initial_conditions) > row:
                if column < 4:
                    r = self.model.initial_conditions[row]
                    to_edit = int(self.tab3_table.item(row, column).text())
                    res = tuple((v if i != column else to_edit) for i, v in
                                enumerate(r))
                    if column < 2:
                        exact = self.model.exact_solution_at_point(
                            res[0], res[1]
                        )
                        self.tab3_table.setItem(
                            row,
                            2,
                            QTableWidgetItem(str(exact))
                        )
                        res = tuple((v if i != 2 else exact) for i, v in
                                    enumerate(res))
                    self.model.initial_conditions[row] = res
                if column < 2:
                    graphics_draw()
        self.tab3_table.cellChanged.connect(table_cell_change)

        self.tab3_button_prev.clicked.connect(lambda: self.setCurrentIndex(1))
        self.tab3_button_next.clicked.connect(lambda: self.setCurrentIndex(3))

    def __init__tab4__stuff__(self):
        self.tab4_graphics_scene = QGraphicsScene()
        self.tab4_graphics.setScene(self.tab4_graphics_scene)

        def graphics_draw():
            self.tab4_graphics_scene.setSceneRect(
                0,
                0,
                self.tab4_graphics.size().width(),
                self.tab4_graphics.size().height()
            )
            self.tab4_graphics_scene.clear()
            for x1, x2 in self.model.spatial_area:
                self.tab4_graphics_scene.addItem(QGraphicsEllipseItem(
                    x1 - 1, x2 - 1, 2, 2
                ))
            for i in range(1, len(self.model.spatial_area)):
                self.tab4_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[i - 1][0],
                    self.model.spatial_area[i - 1][1],
                    self.model.spatial_area[i][0],
                    self.model.spatial_area[i][1]
                ))
            if len(self.model.spatial_area) > 1:
                self.tab4_graphics_scene.addItem(QGraphicsLineItem(
                    self.model.spatial_area[0][0],
                    self.model.spatial_area[0][1],
                    self.model.spatial_area[-1][0],
                    self.model.spatial_area[-1][1]
                ))
            for x1, x2, _, _, _ in self.model.boundary_conditions:
                self.tab4_graphics_scene.addItem(QGraphicsEllipseItem(
                    x1 - 1, x2 - 1, 2, 2
                ))

        def add_point(x1, x2):
            self.tab4_table.setRowCount(
                len(self.model.boundary_conditions) + 1
            )
            self.tab4_table.setItem(
                len(self.model.boundary_conditions),
                0,
                QTableWidgetItem(str(x1))
            )
            self.tab4_table.setItem(
                len(self.model.boundary_conditions),
                1,
                QTableWidgetItem(str(x2))
            )
            t = self.doubleSpinBox_t.value()
            self.tab4_table.setItem(
                len(self.model.boundary_conditions),
                2,
                QTableWidgetItem(str(t))
            )
            exact = self.model.exact_solution_at_point(x1, x2, t)
            self.tab4_table.setItem(
                len(self.model.boundary_conditions),
                3,
                QTableWidgetItem(str(exact))
            )
            self.tab4_table.setItem(
                len(self.model.boundary_conditions),
                4,
                QTableWidgetItem(str(exact))
            )
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

        def table_cell_change(row, column):
            if len(self.model.boundary_conditions) > row:
                if column < 5:
                    r = self.model.boundary_conditions[row]
                    to_edit = float(self.tab4_table.item(row, column).text())
                    res = tuple((v if i != column else to_edit) for i, v in
                                enumerate(r))
                    if column < 3:
                        exact = self.model.exact_solution_at_point(
                            res[0], res[1], res[2]
                        )
                        self.tab4_table.setItem(
                            row,
                            3,
                            QTableWidgetItem(str(exact))
                        )
                        res = tuple((v if i != 3 else exact) for i, v in
                                    enumerate(res))
                    self.model.boundary_conditions[row] = res
                if column < 2:
                    graphics_draw()
        self.tab4_table.cellChanged.connect(table_cell_change)

        self.tab4_button_prev.clicked.connect(lambda: self.setCurrentIndex(2))
        self.tab4_button_next.clicked.connect(lambda: self.setCurrentIndex(4))

    def __init__tab5__stuff__(self):
        def create_files():
            with open(data_path + '/spatial_area', 'wb') as fp:
                pickle.dump(self.model.spatial_area, fp)
            x_1 = []
            x_2 = []
            t = []
            exact = []
            sensor = []
            for item in (
                self.model.initial_conditions +
                self.model.boundary_conditions
            ):
                x_1.append(item[0])
                x_2.append(item[1])
                i = len(item) - 4
                t.append(0 if not i else item[2])
                exact.append(item[2 + i])
                sensor.append(item[3 + i])
            with open(data_path + '/x_1', 'wb') as fp:
                pickle.dump(x_1, fp)
            with open(data_path + '/x_2', 'wb') as fp:
                pickle.dump(x_2, fp)
            with open(data_path + '/t', 'wb') as fp:
                pickle.dump(t, fp)
            with open(data_path + '/exact', 'wb') as fp:
                pickle.dump(exact, fp)
            with open(data_path + '/sensor', 'wb') as fp:
                pickle.dump(sensor, fp)

        def calc():
            y = self.lineEdit_y.text()
            print('clicked: {}'.format(y))
            create_files()

            from subprocess import Popen, call

            dir_path = os.path.dirname(os.path.realpath(__file__))
            print(os.path.join(dir_path, 'vpython_example.py'))
            if os.name != 'nt':  # not windows
                call(["pkill python {}"
                      .format(os.path.join(dir_path, 'vpython_example.py'))],
                     shell=True)
            Popen(["python", os.path.join(dir_path, 'vpython_example.py'),
                   y.replace('^', '**').replace('x1', 'x').replace('x2', 'y')],
                  shell=True)

        self.showResults.clicked.connect(calc)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    modeling = Modeling()
    modeling.show()
    sys.exit(app.exec_())
