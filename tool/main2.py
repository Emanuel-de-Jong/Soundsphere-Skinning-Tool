import sys, random, os, copy
from shutil import copy, copyfile

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt, QRect, QSize, QRectF, QMetaType, pyqtSignal, QPoint, QMimeData
from PyQt5.QtGui import QBrush, QPen, QFont, QPixmap, QFontDatabase, QDragMoveEvent, QDragEnterEvent, QDropEvent, QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QGraphicsScene, QGraphicsView,
                             QGraphicsObject, QGraphicsItem, QGraphicsRectItem, QGraphicsLineItem,
                             QGraphicsTextItem, QGraphicsPixmapItem, QListView, QGridLayout, QVBoxLayout,
                             QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QTableWidget,
                             QTableWidgetItem, QAbstractItemView)



user_interface, QtBaseClass = uic.loadUiType("user_interface.ui")

class MainWindow (QMainWindow, user_interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_interface.__init__(self)



class MyQGraphicsScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MyQGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ToolBox(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ObjectTree(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Properties(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Resources(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ToolBoxItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ObjectTreeItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PropertiesItem(QTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ResourcesItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Score(QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ShortNote(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())