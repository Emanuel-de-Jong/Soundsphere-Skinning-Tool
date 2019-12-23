#   IMPORTS
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






#   GLOBAL VARIABLES
VIEW_WIDTH = 0
VIEW_HEIGHT = 0
DEFAULT_FONT = ""
user_interface, QtBaseClass = uic.loadUiType("user_interface.ui")






#   PROGRAM
#is run before anything else. used for loading resources and executing non window commands that are always needed
def startup():
    font_id = QFontDatabase.addApplicationFont("DefaultResources/DefaultFont.ttf")
    DEFAULT_FONT = QFontDatabase.applicationFontFamilies(font_id)[0]






#the main window
class MainWindow (QMainWindow, user_interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_interface.__init__(self)
        self.setupUi(self)

        self.fourKScene = MyQGraphicsScene()

        self.objectTree = ObjectTree(self.centralwidget)
        self.initObjectTree()

        self.fourKView = MyQGraphicsView(self.fourKTab)
        self.initFourKView()

        self.properties = MyQTableWidget(self.centralwidget)
        self.initProperties()

        self.resources = Resources(self.centralwidget)
        self.initResources()


        self.toolBox.addItem(ToolBoxItem(Score))
        self.toolBox.addItem(ToolBoxItem(ShortNote))


        self.fourKScene.selectionChanged.connect(self.sceneSelectionChanged)
        self.fourKScene.objectAddedToScene.connect(self.objectAddedToScene)
        self.fourKScene.mouseReleased.connect(self.mouseReleasedInScene)
        self.fourKScene.deletePressedInScene.connect(self.deleteSelectedObjects)
        self.objectTree.deletePressedInObjectTree.connect(self.deleteSelectedObjects)
        self.objectTree.itemPressed.connect(self.treeItemPressed)


        self.viewWidthTextbox.textChanged.connect(self.viewWidthTextboxChanged)
        self.viewHeightTextbox.textChanged.connect(self.viewHeightTextboxChanged)

    def deleteSelectedObjects(self):
        rowsToDelete = []
        for rowNumber in range(self.objectTree.count()):
            item = self.objectTree.item(rowNumber)
            if item.isSelected():
                rowsToDelete.append(rowNumber)
                self.fourKScene.removeItem(item.customClass)

        rowsToDelete.reverse()
        for rowNumber in rowsToDelete:
            self.objectTree.takeItem(rowNumber)

    def mouseReleasedInScene(self):
        self.properties.updateData()

    def sceneSelectionChanged(self):
        onlyOnce = True
        for rowNumber in range(self.objectTree.count()):
            item = self.objectTree.item(rowNumber)
            if item.customClass.isSelected():
                item.setSelected(True)
                if onlyOnce:
                    onlyOnce = False
                    self.properties.selectedClassChange(item.customClass)
            else:
                item.setSelected(False)


    def treeItemPressed(self, pressedItem):
        self.fourKScene.clearSelection()
        pressedItem.customClass.setSelected(True)

    def objectAddedToScene(self, newObject):
        item = ObjectTreeItem()
        item.setCustomClass(newObject)
        item.setText(newObject.name)
        self.objectTree.addItem(item)

        #self.fourKScene.clearSelection()
        #newObject.setSelected(True)




    def viewWidthTextboxChanged(self, value):
        self.fourKView.setMinimumWidth(int(value))
        self.fourKView.setMaximumWidth(int(value))
        self.keymodeTabs.setMinimumWidth(int(value) + 30)
        self.keymodeTabs.setMaximumWidth(int(value) + 30)

    def viewHeightTextboxChanged(self, value):
        self.fourKView.setMinimumHeight(int(value))
        self.fourKView.setMaximumHeight(int(value))
        self.keymodeTabs.setMinimumHeight(int(value) + 50)
        self.keymodeTabs.setMaximumHeight(int(value) + 50)




    def initObjectTree(self):
        self.objectTree.setMinimumSize(QtCore.QSize(150, 0))
        self.objectTree.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.objectTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.objectTree.setDragEnabled(False)
        self.objectTree.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.objectTree.setSelectionRectVisible(False)
        self.objectTree.setObjectName("objectTree")
        self.objectTree.setSortingEnabled(True)
        self.objectTree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.topright.addWidget(self.objectTree)

    def initFourKView(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fourKView.sizePolicy().hasHeightForWidth())
        self.fourKView.setSizePolicy(sizePolicy)
        self.fourKView.setMinimumSize(QtCore.QSize(500, 500))
        self.fourKView.setMaximumSize(QtCore.QSize(500, 500))
        self.fourKView.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.fourKView.setAutoFillBackground(False)
        self.fourKView.setDragMode(QGraphicsView.RubberBandDrag)
        self.fourKView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fourKView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(230, 230, 230))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.fourKView.setBackgroundBrush(brush)
        self.fourKView.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.fourKView.setObjectName("fourKView")
        self.gridLayout_2.addWidget(self.fourKView, 0, 0, 1, 1)
        self.fourKView.setScene(self.fourKScene)
        self.fourKView.setSceneRect(QRectF(self.fourKView.rect()))

    def initProperties(self):
        self.properties.setMinimumSize(QtCore.QSize(150, 0))
        self.properties.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.properties.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.properties.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.properties.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.properties.setDragEnabled(False)
        self.properties.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.properties.setAlternatingRowColors(True)
        self.properties.setShowGrid(False)
        self.properties.setGridStyle(QtCore.Qt.SolidLine)
        self.properties.setWordWrap(True)
        self.properties.setCornerButtonEnabled(True)
        self.properties.setObjectName("properties")
        self.properties.setColumnCount(1)
        self.properties.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.properties.setHorizontalHeaderItem(0, item)
        self.properties.horizontalHeader().setVisible(False)
        self.properties.horizontalHeader().setCascadingSectionResizes(False)
        self.properties.horizontalHeader().setDefaultSectionSize(100)
        self.properties.horizontalHeader().setHighlightSections(True)
        self.topleft.addWidget(self.properties)
        self.properties.setSortingEnabled(False)
        _translate = QtCore.QCoreApplication.translate
        item = self.properties.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))

    def initResources(self):
        self.resources.setMinimumSize(QtCore.QSize(150, 0))
        self.resources.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.resources.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.resources.setDragEnabled(True)
        self.resources.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.resources.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.resources.setViewMode(QtWidgets.QListView.ListMode)
        self.resources.setUniformItemSizes(False)
        self.resources.setObjectName("resources")
        self.setIconSize(QSize(72, 72))
        self.resources.setAcceptDrops(True)
        self.bottomleft.addWidget(self.resources)
        self.resources.setSortingEnabled(False)










#custom Qt classes
class Resources(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            rowNumber = self.currentRow()
            self.takeItem(rowNumber)

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

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                item = ResourcesItem()

                extension = os.path.splitext(url.fileName())[1]
                if extension == ".png" or extension == ".jpg" or extension == ".jpeg" or extension == ".bmp":
                    item.setWhatsThis("Image")
                    item.setIcon(QIcon(url.toLocalFile()))
                elif extension == ".ttf":
                    item.setWhatsThis("Font")
                    item.setIcon(QIcon("Images/FontIcon.png"))
                else:
                    return

                item.setText(os.path.splitext(url.fileName())[0])
                item.setUrl(url.toLocalFile())
                self.addItem(item)

        else:
            event.ignore()



class ResourcesItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = ""

    def setUrl(self, url):
        self.url = url



class ObjectTree(QListWidget):
    deletePressedInObjectTree = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            self.deletePressedInObjectTree.emit()



class MyQGraphicsView(QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        event.accept()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        event.accept()

    def dropEvent(self, event: QDropEvent) -> None:
        event.accept()

        print("source if statement")
        if isinstance(event.source(), QListWidget):
            print("item if statement")
            if isinstance(event.source().currentItem(), ToolBoxItem):
                print("getting new object from item")
                obj = event.source().currentItem().getNewCustomClass()
                print("adding object to scene")
                self.scene().addItem(obj)

                objRect = obj.boundingRect().center()

                position = QPoint(event.pos().x() - objRect.x(), event.pos().y() - objRect.y())
                obj.setPos(self.mapToScene(position))











class MyQGraphicsScene(QGraphicsScene):
    objectAddedToScene = pyqtSignal(QGraphicsItem)
    mouseReleased = pyqtSignal()
    deletePressedInScene = pyqtSignal()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete:
            self.deletePressedInScene.emit()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mouseReleaseEvent(event)
        self.mouseReleased.emit()



    def addItem(self, qGraphicsItem):
        super().addItem(qGraphicsItem)
        self.objectAddedToScene.emit(qGraphicsItem)







class ObjectTreeItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.customClass = object

        #self.setFlags(Qt.ItemIsEditable)

    def setCustomClass(self, value):
        self.customClass = value







class MyQTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selectedClass = object

        self.itemChanged.connect(self.valueChanged)

    def updatePos(self):
        for rowNumber in range(self.rowCount()):
            item = self.item(rowNumber, 0)
            if item.whatsThis() == "X":
                item.setText(str(self.selectedClass.x()))
            elif item.whatsThis() == "Y":
                item.setText(str(self.selectedClass.y()))

    def selectedClassChange(self, _class):
        if self.selectedClass != _class:
            self.selectedClass = _class
            self.updateData()

    def updateData(self):
        properties = self.selectedClass.sendProperties()

        self.clear()
        self.setRowCount(len(properties))

        i = 0
        for key, value in properties.items():
            item = QTableWidgetItem()
            item.setText(key)
            self.setVerticalHeaderItem(i, item)

            item = QTableWidgetItem()
            item.setText(value)
            item.setWhatsThis(key)
            self.setItem(i, 0, item)

            i += 1

    def valueChanged(self, item):
        pass
        getattr(self.selectedClass, "set" + item.whatsThis())(item.text())






#objects
class Score(QGraphicsTextItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Qfont = QFont(DEFAULT_FONT)
        self.Qfont.setPixelSize(40)
        self.setFont(self.Qfont)

        self.name = "Score"
        self.setPlainText("98.5%")

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def sendProperties(self):
        properties = dict()
        properties["X"] = str(self.x())
        properties["Y"] = str(self.y())
        properties["Size"] = str(self.font().pixelSize())
        return properties

    def setName(self, name: str):
        self.name = name

    def setX(self, x: str):
        super().setX(float(x))

    def setY(self, y: str):
        super().setY(float(y))

    def setSize(self, size: str):
        self.Qfont.setPixelSize(int(size))
        self.setFont(self.Qfont)





class ShortNote(QGraphicsPixmapItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPixmap(QPixmap("DefaultResources/DefaultShortNote.jpg"))

        self.name = "Short Note"

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def sendProperties(self):
        properties = dict()
        properties["X"] = str(self.x())
        properties["Y"] = str(self.y())
        properties["Width"] = str(self.pixmap().width())
        properties["Height"] = str(self.pixmap().height())
        return properties

    def setName(self, name: str):
        self.name = name

    def setX(self, x: str):
        super().setX(float(x))

    def setY(self, y: str):
        super().setY(float(y))

    def setWidth(self, width: str):
        self.setPixmap(self.pixmap().scaled(int(width), self.pixmap().height(), Qt.IgnoreAspectRatio))

    def setHeight(self, height: str):
        self.setPixmap(self.pixmap().scaled(self.pixmap().width(), int(height), Qt.IgnoreAspectRatio))






class ToolBoxItem(QListWidgetItem):
    def __init__(self, classType):
        super().__init__()
        self.classType = classType
        self.setText(classType().name)

    def getNewCustomClass(self):
        return self.classType()






#   EXECUTION
if __name__ == "__main__":
    app = QApplication(sys.argv)

    startup()

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
