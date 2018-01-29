from __future__ import print_function

import sys
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.qt_compat import QtCore, QtWidgets, QtGui
try:
    from matplotlib.backends.qt_compat import is_pyqt5
except ImportError:
    def is_pyqt5():
        from matplotlib.backends.qt_compat import QT_API
        return QT_API == u'PyQt5'

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class CurvePropertiesDialog(QtWidgets.QWidget):
    def __init__(self, parent=None, line=None):
        super(CurvePropertiesDialog, self).__init__(parent)
        self.line=line
        #labels
        self._label_color=QtWidgets.QLabel('Color')
        self._label_symbol=QtWidgets.QLabel('Symbol')
        self._label_line_style = QtWidgets.QLabel('Line style')
        self._label_line_width = QtWidgets.QLabel('Line thickness')
        #text inputs
        self._edit_label = QtWidgets.QLineEdit()
        self._edit_color=QtWidgets.QLineEdit()
        self._edit_symbol=QtWidgets.QLineEdit()
        self._edit_line_style = QtWidgets.QComboBox()
        self._edit_line_style.addItems(['None', '-', '--', '-.', ':'])
        self._edit_line_width = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self._edit_line_width.setMinimum(0)
        self._edit_line_width.setMaximum(9)
        self._edit_line_width.setValue(0)
        self._edit_line_width.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self._edit_line_width.setTickInterval(1)
        #buttons
        self._btn_ok=QtWidgets.QPushButton('Apply')
        self._btn_cancel=QtWidgets.QPushButton('Close')
        #layout
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self._edit_label,0,0)
        grid.addWidget(self._label_color,1,0)
        grid.addWidget(self._edit_color,1,1)
        grid.addWidget(self._label_symbol,2,0)
        grid.addWidget(self._edit_symbol,2,1)
        grid.addWidget(self._label_line_style, 3, 0)
        grid.addWidget(self._edit_line_style, 3, 1)
        grid.addWidget(self._label_line_width, 4, 0)
        grid.addWidget(self._edit_line_width, 4, 1)
        grid.addWidget(self._btn_ok,5,0)
        grid.addWidget(self._btn_cancel,5,1)
        #connections
        self._btn_ok.clicked.connect(self.process_inputs)
        self._btn_cancel.clicked.connect(self.close)
        
        self.update_from_line(self.line)
        
    def update_from_line(self,line):
        if line is not None:
            self.setWindowTitle(line.get_label())
            self._edit_label.setText(line.get_label())
            self._edit_color.setText(line.get_c())
            self._edit_symbol.setText(line.get_marker())
            self._edit_line_style.setCurrentText(line.get_linestyle())
            self._edit_line_width.setValue(line.get_linewidth())
            self.line=line
            # connections requiring line object instantiated
            self._edit_line_width.valueChanged.connect(self.process_inputs)
            self.show()

    def process_inputs(self):
        self.setWindowTitle(self._edit_label.text())
        newcolor=str(self._edit_color.text())
        newsymbol=str(self._edit_symbol.text())
        try:
            self.line.set_c(newcolor)
        except ValueError:
            print('Did not understood the color')
        try:
            self.line.set_marker(newsymbol)
        except ValueError:
            print('Unrecognized symbol')
        self.line.set_linestyle(str(self._edit_line_style.currentText()))
        self.line.set_linewidth(self._edit_line_width.value())
        self.line.set_label(self._edit_label.text())
        self.line._axes.legend()
        self.line.figure.tight_layout()
        self.line.figure.canvas.draw()


class AxisMenu(QtWidgets.QMenu):
    r"""Popup menu for setting axis scale"""
    def __init__(self, axis, parent=None):
        super(AxisMenu, self).__init__(parent=parent)
        self._axis = axis

        # toggle the grid on major ticks
        grid_mutate = 'off' if axis._gridOnMajor else 'on'
        grid_action = QtWidgets.QAction('Grid ' + grid_mutate, self)
        grid_action.triggered.connect(
            self._act_now(lambda: axis.grid(not axis._gridOnMajor)))
        self.addAction(grid_action)

        # toggle linear and logarithm scale
        scale_mutate= 'log' if axis.get_scale() == 'linear' else 'linear'
        scale_action = QtWidgets.QAction(scale_mutate + ' scale ', self)
        change_scale = axis.axes.set_xscale if \
            isinstance(axis, mpl.axis.XAxis) else axis.axes.set_yscale
        scale_action.triggered.connect(
            self._act_now(lambda: change_scale(scale_mutate)))
        self.addAction(scale_action)

        # popup the menu at the mouse pointer position
        self.popup(QtGui.QCursor.pos())

    def _act_now(self, func):
        r"""Decorator calls the function and updates the plot"""
        def wrapped():
            func()
            self._axis.figure.canvas.draw_idle()
        return wrapped


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(static_canvas)
        self.addToolBar(NavigationToolbar(static_canvas, self))

        self._static_ax = static_canvas.figure.add_subplot(111)

        self._static_ax.xaxis.set_picker(5)
        self._static_ax.yaxis.set_picker(5)
        self._static_ax.set_xlabel('time (s)', picker=True)
        self._static_ax.set_ylabel('signal', picker=True)

        self.curve_dialog=CurvePropertiesDialog()
        self.cid=static_canvas.mpl_connect('pick_event', self.on_pick)

        # Initial plots
        t = np.linspace(0, 10, 51)
        self._static_ax.plot(t, np.sin(t), ".", label='first', picker=5)
        self._static_ax.plot(t, np.cos(t), "o:", label='second', picker=5)
        self._static_ax.legend()
        self._static_ax.get_legend().set_picker(5)
        self._static_ax.get_legend().draggable()

        static_canvas.figure.tight_layout()

    def on_pick(self, event):
        if isinstance(event.artist, mpl.lines.Line2D) and \
        event.mouseevent.dblclick:
            self.curve_dialog.update_from_line(event.artist)
        elif isinstance(event.artist, mpl.axis.Axis) and \
        event.mouseevent.button == 3:  # right-click
                AxisMenu(event.artist, parent=self)
        elif isinstance(event.artist, mpl.legend.Legend):
            print("Hi, I'm a", event.artist)
        else:
            print("I'm a", event.artist)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()

'''
Exercises:
- add inputs for linestyle, line thickness
- add legend, and modify it in the same dialog box. Set the title of the dialog box
  as the label for the curve
- add labels to x and y axis. Make axes pickable and create a dialog to modify the
  axis label, the minimum/maximum, and to be able to use logarithmic scale
'''
