from PyQt5.QtWidgets import QGraphicsView, QVBoxLayout, QGraphicsItem, QPushButton, QTextEdit
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from Scene_View.scene import Scene
from Components.sky_widget import SkyWidget


class MyView(QGraphicsView):
    def __init__(self):
        super(MyView, self).__init__()

        # function1: show scene
        self.scene = Scene()
        self.setScene(self.scene.my_scene)

        # function2: show snow falling
        # self.view_layout = QVBoxLayout(self)  # view layout
        # # print(self.view_layout.parent())
        # self.view_layout.setContentsMargins(0, 0, 0, 0)  # set view margins
        # self.sky_widget = SkyWidget(self)  # get sky widget
        # # self.sky_widget.show()
        # self.view_layout.addWidget(self.sky_widget)  # add snow falling widget
        # self.view_layout.
        self.add_DebugContent()

    def add_DebugContent(self):
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        greenBrush = QBrush(Qt.green)
        rect = self.scene.my_scene.addRect(-100, -100, 80, 100, outlinePen, greenBrush)
        rect.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        text = self.scene.my_scene.addText("this is my awesome text!", QFont("Manjaro"))
        text.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        text.setDefaultTextColor(QColor.fromRgbF(10.0, 7.0, 3.0))

        pushBtn = QPushButton("Hello World")
        proxy1 = self.scene.my_scene.addWidget(pushBtn)
        proxy1.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        proxy1.setPos(0, 30)

        text = QTextEdit()
        proxy2 = self.scene.my_scene.addWidget(text)
        proxy2.setPos(0, 60)

        line = self.scene.my_scene.addLine(-200, -100, 400, 200, outlinePen)
        line.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
