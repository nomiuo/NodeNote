from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QPushButton, QTextEdit
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from scene_view_scene import Scene


class MyView(QGraphicsView):
    def __init__(self):
        super(MyView, self).__init__()

        # function1: show scene
        self.scene = Scene()
        self.setScene(self.scene.my_scene)

        self.add_DebugContent()

    def add_DebugContent(self):
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        greenBrush = QBrush(Qt.green)
        rect = self.scene.my_scene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        text = self.scene.my_scene.addText("this is my awesome text!", QFont("Manjaro"))
        text.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(0, 0, 0))

        pushBtn = QPushButton("Hello World")
        proxy1 = self.scene.my_scene.addWidget(pushBtn)
        proxy1.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        proxy1.setPos(0, 30)

        text = QTextEdit()
        proxy2 = self.scene.my_scene.addWidget(text)
        proxy2.setPos(0, 60)

        line = self.scene.my_scene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
