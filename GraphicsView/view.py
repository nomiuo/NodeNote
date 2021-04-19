from PyQt5.QtWidgets import QGraphicsView, QMenu
from PyQt5.QtGui import QPainter, QIcon, QKeyEvent
from GraphicsView.scene import Scene
from Components.effect_water import EffectWater
from Components.tuple_node import *


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyView, self).__init__(parent)
        # BASIC SETTINGS
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene = Scene(self)
        self.setScene(self.scene.my_scene)

        # SCALE FUNCTION
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 0.8
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def set_leftbtn_beauty(self, event):
        water_drop = EffectWater()
        property_water_drop = QGraphicsProxyWidget()
        property_water_drop.setWidget(water_drop)
        self.scene.my_scene.addItem(property_water_drop)
        water_drop.move(self.mapToScene(event.pos()))
        water_drop.show()

    def change_scale(self, event):
        if DEBUG_VIEW_CHANGE_SCALE:
            print("View is zooming! Current zoom: ", self.zoom)
            print(event.key())
        if event.key() == Qt.Key_Equal and event.modifiers() & Qt.ControlModifier:
            self.zoom += self.zoomStep  # 放大次数增加一次
            if self.zoom <= self.zoomRange[1]:
                self.scale(self.zoomInFactor, self.zoomInFactor)
            else:
                self.zoom = self.zoomRange[1]
        elif event.key() == Qt.Key_Minus and event.modifiers() & Qt.ControlModifier:
            self.zoom -= self.zoomStep  # 缩小次数增加一次
            if self.zoom >= self.zoomRange[0]:
                self.scale(self.zoomOutFactor, self.zoomOutFactor)
            else:
                self.zoom = self.zoomRange[0]

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

    def mousePressEvent(self, event) -> None:
        super(MyView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_leftbtn_beauty(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (event.key() == Qt.Key_Equal and event.modifiers() & Qt.ControlModifier) or \
                (event.key() == Qt.Key_Minus and event.modifiers() & Qt.ControlModifier):
            self.change_scale(event)
        else:
            super(MyView, self).keyPressEvent(event)
