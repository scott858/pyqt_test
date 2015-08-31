import sys
import random

from PyQt5.QtCore import Qt, QObject, pyqtSignal, QBasicTimer, QDate
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QTextEdit, QLineEdit, QLabel,
                             QVBoxLayout, QLCDNumber, QSlider, QPushButton, QMainWindow, QInputDialog, QFrame,
                             QColorDialog, QSizePolicy, QFontDialog, QAction, QFileDialog, QCheckBox, QProgressBar,
                             QCalendarWidget)
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFont, QPainter


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Simple Drag and Drop')
        self.setGeometry(300, 300, 300, 150)
        self.show()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        qp.setPen(QColor(168, 34, 3))
        size = self.size()

        for i in range(1000):
            x = random.randint(1, size.width() - 1)
            y = random.randint(1, size.height() - 1)
            qp.drawPoint(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
