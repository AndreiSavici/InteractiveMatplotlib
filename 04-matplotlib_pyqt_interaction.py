import sys
import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets
try:
    from matplotlib.backends.qt_compat import is_pyqt5
except ImportError:
    def is_pyqt5():
        return False

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
        #text inputs
        self._edit_color=QtWidgets.QLineEdit()
        self._edit_symbol=QtWidgets.QLineEdit()
        #buttons
        self._btn_ok=QtWidgets.QPushButton('OK')
        self._btn_cancel=QtWidgets.QPushButton('Cancel')
        #layout
        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self._label_color,0,0)
        grid.addWidget(self._edit_color,0,1)
        grid.addWidget(self._label_symbol,1,0)
        grid.addWidget(self._edit_symbol,1,1)
        grid.addWidget(self._btn_ok,2,0)
        grid.addWidget(self._btn_cancel,2,1)        
        #connections
        self._btn_ok.clicked.connect(self.process_inputs)
        self._btn_cancel.clicked.connect(self.close)
        
        self.update_from_line(self.line)
        
    def update_from_line(self,line):
        if line is not None:
            self._edit_color.setText(line.get_c())
            self._edit_symbol.setText(line.get_marker())
            self.line=line
            self.show()

    def process_inputs(self):
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
        self.line.figure.canvas.draw()
        self.close()


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
        t = np.linspace(0, 10, 51)
        self._static_ax.plot(t, np.sin(t), ".", picker=5)
        self._static_ax.plot(t, np.cos(t), "o", picker=5)
        self.cid=static_canvas.mpl_connect('pick_event', self.on_pick)
        self.curve_dialog=CurvePropertiesDialog()

    def on_pick(self,event):
        self.curve_dialog.update_from_line(event.artist)
        

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
