from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter
from GraphicsView.scene import Scene
from Components.effect_water import EffectWater
from Components.tuple_node import *


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyView, self).__init__(parent)

        # function1: show scene
        self.scene = Scene(self)
        self.set_scene()

        # function2: beauty
        self.set_function()

    # function1: show scene
    def set_scene(self):
        self.setScene(self.scene.my_scene)

    # function2: interface beauty
    def set_function(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    # function3: left button beauty
    def set_leftbtn_beauty(self, event):
        water_drop = EffectWater()
        property_water_drop = QGraphicsProxyWidget()
        property_water_drop.setWidget(water_drop)
        self.scene.my_scene.addItem(property_water_drop)
        water_drop.move(self.mapToScene(event.pos()))
        water_drop.show()

    # function 4: add basic widget
    def add_basic_widget(self, event):
        basic_widget = Node()
        self.scene.my_scene.addItem(basic_widget)
        basic_widget.setPos(self.mapToScene(event.pos()))
        self.scene.add_basic_widget(basic_widget)

    def contextMenuEvent(self, event) -> None:
        super(MyView, self).contextMenuEvent(event)
        context_menu = QMenu(self)
        # context list
        create_truth_widget = context_menu.addAction("Create Truth Widget")
        create_truth_widget.setIcon(QIcon("Resources/context_menu/truth.png"))

        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == create_truth_widget:
            self.add_basic_widget(event)
        # elif action ==

    def mousePressEvent(self, event) -> None:
        super(MyView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_leftbtn_beauty(event)


