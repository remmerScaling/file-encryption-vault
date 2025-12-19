from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPolygonItem
from PyQt5.QtCore import QTimer, Qt, QPointF
from PyQt5.QtGui import QPolygonF, QTransform, QColor, QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class HexagonWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)

        size = 60
        points = [
            QPointF(size * 0.5, 0),
            QPointF(size, size * 0.25),
            QPointF(size, size * 0.75),
            QPointF(size * 0.5, size),
            QPointF(0, size * 0.75),
            QPointF(0, size * 0.25),
        ]
        hexagon = QPolygonF(points)
        self.item = QGraphicsPolygonItem(hexagon)

        self.item.setBrush(QBrush(QColor("#39ff14")))
        self.item.setPen(QPen(QColor("#39ff14"), 2))
        self.item.setTransformOriginPoint(self.item.boundingRect().center())
        self.scene.addItem(self.item)

        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate_hex)
        self.timer.start(30)
        self.rotation_speed = 1.0

    def rotate_hex(self):
        self.item.setRotation(self.item.rotation() + self.rotation_speed)

    def set_rotation_speed(self, speed):
        self.rotation_speed = speed

    def stop_rotation(self, duration_ms=3000):
        self.timer.stop()
        QTimer.singleShot(duration_ms, lambda: self.timer.start(30))
