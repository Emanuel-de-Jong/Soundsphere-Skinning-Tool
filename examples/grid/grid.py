import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMenu
from PyQt5.QtGui import QKeySequence, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QLinearGradient
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtWidgets import QGraphicsItem


def create_action(parent, text, slot=None,
                  shortcut=None, shortcuts=None, shortcut_context=None,
                  icon=None, tooltip=None,
                  checkable=False, checked=False):
    action = QtWidgets.QAction(text, parent)

    if icon is not None:
        action.setIcon(QIcon(':/%s.png' % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if shortcuts is not None:
        action.setShortcuts(shortcuts)
    if shortcut_context is not None:
        action.setShortcutContext(shortcut_context)
    if tooltip is not None:
        action.setToolTip(tooltip)
        action.setStatusTip(tooltip)
    if checkable:
        action.setCheckable(True)
    if checked:
        action.setChecked(True)
    if slot is not None:
        action.triggered.connect(slot)

    return action


class Settings():

    WIDTH = 20
    HEIGHT = 15
    NUM_BLOCKS_X = 32
    NUM_BLOCKS_Y = 16


class CI(QGraphicsTextItem):

    def __init__(self, text, pos):
        QGraphicsTextItem.__init__(self)

        self.content = text
        self.setPlainText(text)

        self.setPos(pos)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setDefaultTextColor(Qt.black)
        self.setFlags(
            self.flags() | QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        self.setAcceptDrops(True)

    def boundingRect(self):
        # get the original width and height of boundingrect
        br = QGraphicsTextItem.boundingRect(self)
        brw = br.width()
        brh = br.height()
        # new width and height in "blocks"
        wblocks = int(brw / Settings.WIDTH) + 1
        hblocks = int(brh / Settings.HEIGHT) + 1
        w = wblocks * Settings.WIDTH
        h = hblocks * Settings.HEIGHT
        return QtCore.QRectF(0, 0, w, h)

    def setGridIntersection(self, pos):
        # get the next grid intersection top left of items top-left corner
        grid_x = int(pos.x() / Settings.WIDTH)
        grid_y = int(pos.y() / Settings.HEIGHT)
        self.setPos(grid_x * Settings.WIDTH, grid_y * Settings.HEIGHT)

    def paint(self, painter, option, widget):
        painter.save()
        painter.setBrush(QBrush(Qt.white))
        painter.drawRect(self.boundingRect())
        painter.restore()

        super().paint(painter, option, widget)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.content = self.toPlainText()

    def focusInEvent(self, event):
        self.scene().writing_comment = True
        # self.setPlainText(self.content)
        # print("Focusinevent")

    def focusOutEvent(self, event):
        self.scene().writing_comment = False
        # self.setHtml(self.content)
        # print("FocusOutevent")

    def contextMenuEvent(self, scme):
        super().contextMenuEvent(scme)


class QS(QtWidgets.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        width = Settings.NUM_BLOCKS_X * Settings.WIDTH
        height = Settings.NUM_BLOCKS_Y * Settings.HEIGHT
        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        pos = QPoint(
            5 * Settings.WIDTH,
            2 * Settings.HEIGHT
        )
        content = """<!DOCTYPE html>
                    <html>
                    <body>

                    <h1>This is heading 1</h1>
                    <h2>This is heading 2</h2>
                    <h3>This is heading 3</h3>
                    <h4>This is heading 4</h4>
                    <h5>This is heading 5</h5>
                    <h6>This is heading 6</h6>

                    </body>
                    </html>
                    """
        self.addItem(CI(content, pos))

    def mouseMoveEvent(self, event):
        QtWidgets.QGraphicsScene.mouseMoveEvent(self, event)
        for i in self.selectedItems():
            if type(i) == CI:
                i.setGridIntersection(i.pos())


class QV(QtWidgets.QGraphicsView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.view_menu = QMenu(self)
        self.create_actions()

    def create_actions(self):
        act = create_action(self.view_menu, "Zoom in",
                            slot=self.on_zoom_in,
                            shortcut=QKeySequence("+"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)

        act = create_action(self.view_menu, "Zoom out",
                            slot=self.on_zoom_out,
                            shortcut=QKeySequence("-"), shortcut_context=Qt.WidgetShortcut)
        self.view_menu.addAction(act)
        self.addActions(self.view_menu.actions())

    def on_zoom_in(self):
        if not self.scene():
            return

        self.scale(1.5, 1.5)

    def on_zoom_out(self):
        if not self.scene():
            return

        self.scale(1.0 / 1.5, 1.0 / 1.5)

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QPainter.Antialiasing, True)

        gr = rect.toRect()
        start_x = gr.left() + Settings.WIDTH - (gr.left() % Settings.WIDTH)
        start_y = gr.top() + Settings.HEIGHT - (gr.top() % Settings.HEIGHT)
        painter.save()

        for index, x in enumerate(range(start_x, gr.right(), Settings.WIDTH)):
            if index == Settings.NUM_BLOCKS_X:
                painter.setPen(QtGui.QColor(255, 70, 80).lighter(90))
                painter.setOpacity(0.7)
            else:
                painter.setPen(QtGui.QColor(60, 70, 80).lighter(90))
                painter.setOpacity(0.7)

            painter.drawLine(x, gr.top(), x, gr.bottom())

        for index, y in enumerate(range(start_y, gr.bottom(), Settings.HEIGHT)):
            if index == Settings.NUM_BLOCKS_Y:
                painter.setPen(QtGui.QColor(255, 70, 80).lighter(90))
                painter.setOpacity(0.7)
            else:
                painter.setPen(QtGui.QColor(60, 70, 80).lighter(90))
                painter.setOpacity(0.7)

            painter.drawLine(gr.left(), y, gr.right(), y)

        painter.restore()

        super().drawBackground(painter, rect)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    a = QS()
    b = QV()
    b.setScene(a)
    print(b.mapToScene(b.rect()))
    b.show()
    sys.exit(app.exec_())