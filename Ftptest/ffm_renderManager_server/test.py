# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/3/22 12:01"
__all__ = ["__version__", "MyPaint", "MyView"]
__version__ = "1.0.0"
import os, sys
from PySide import QtGui
from PySide import QtCore


class MyPaint(QtGui.QGraphicsItem):
    def __init__(self, parent=None):
        super(MyPaint, self).__init__(parent)
        self._width = 2000.0
        self._height = 2000.0

    def boundingRect(self, *args, **kwargs):
        return QtCore.QRectF(0.0, 0.0, self._width, self._height)

    def paint(self, painter, option, widget):
        # painter: QPainter
        # option: QStyleOptionGraphicsItem
        # widget: QWidget
        border_color = QtGui.QColor(255, 150, 15)
        path = QtGui.QPainterPath()
        pen = QtGui.QPen(border_color, 2)

        path.addEllipse(10, 10, 100, 100)

        point = QtCore.QPoint(180, 180)
        path.lineTo(point)

        painter.setPen(pen)
        painter.drawPath(path)

        text_rect = QtCore.QRectF(150, 100, 100, 100)
        painter.drawText(text_rect, QtCore.Qt.AlignLeft, "test")


class MyView(QtGui.QWidget):
    def __init__(self):
        super(MyView, self).__init__()
        self.resize(500, 500)

        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView(self)
        self.view.setScene(self.scene)

        self.scene.addItem(MyPaint())


def copyDB():
    from ffm.db.Jzmongo import mongoDB

    oldDB = mongoDB("192.168.1.93")
    newDB = mongoDB("192.168.1.93")

    db_name = "ffm_user"
    coll_name = "users"

    for i in oldDB.connect(db_name, coll_name).find():
        newDB.connect(db_name, coll_name).save(i)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = MyView()
    t.show()
    sys.exit(app.exec_())
