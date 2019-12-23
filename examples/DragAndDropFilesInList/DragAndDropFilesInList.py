import sys, random, os

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt, QRect, QSize, QRectF, QMetaType, pyqtSignal, QPoint, QMimeData, QSize
from PyQt5.QtGui import QBrush, QPen, QFont, QPixmap, QFontDatabase, QDragMoveEvent, QDragEnterEvent, QDropEvent, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QGraphicsScene, QGraphicsView,
                             QGraphicsObject, QGraphicsItem, QGraphicsRectItem, QGraphicsLineItem,
                             QGraphicsTextItem, QGraphicsPixmapItem, QListView, QGridLayout, QVBoxLayout,
                             QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QTableWidget,
                             QTableWidgetItem, QAbstractItemView)

class TestListView(QListWidget):
    dropped = pyqtSignal(list)

    def __init__(self, type, parent=None):
        super(TestListView, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setIconSize(QSize(72, 72))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.dropped.emit(links)
        else:
            event.ignore()

class MainForm(QMainWindow):
    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.view = TestListView(self)
        self.view.dropped.connect(self.pictureDropped)
        self.setCentralWidget(self.view)

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                icon = QtGui.QIcon(url)
                pixmap = icon.pixmap(72, 72)
                icon = QIcon(pixmap)
                item = QListWidgetItem(url, self.view)
                item.setIcon(icon)
                item.setStatusTip(url)

def main():
    app = QApplication(sys.argv)
    form = MainForm()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()