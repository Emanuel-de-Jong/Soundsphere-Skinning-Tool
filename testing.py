import sys

from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsItem,
                             QLabel)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setGeometry(500, 200, 500, 500)

        label = QLabel()
        label.setText("test")
        label.setFont(label.font().setPixelSize(80))

        font = QFont()
        label.setFont(font)

        self.setCentralWidget(label)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
