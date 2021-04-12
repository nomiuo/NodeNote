from PyQt5.QtWidgets import QGraphicsView, QLabel, QMenu
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QIcon
from scene_view_scene import Scene
from component_property_grwidget import PropertyGrwidget
from component_water import Water


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
        water_drop = Water(self)
        water_drop.move(self.mapToGlobal(event.pos()))
        water_drop.show()

    # function 3: add basic widget
    def add_basic_widget(self, event):
        basic_widget = PropertyGrwidget()
        basic_widget.setPos(self.mapToScene(event.pos()))
        self.scene.my_scene.addItem(basic_widget)
        self.scene.add_basic_widget(basic_widget)

    def keyPressEvent(self, event) -> None:
        super(MyView, self).keyPressEvent(event)
        if event.key() == Qt.Key_M and event.modifiers() & Qt.ControlModifier:
            self.add_basic_widget(event)

    def contextMenuEvent(self, event) -> None:
        super(MyView, self).contextMenuEvent(event)
        context_menu = QMenu(self)
        # basic widget
        create_todo_widget = context_menu.addAction("Create Basic Widget")
        create_todo_widget.setIcon(QIcon("Templates/life_green.png"))
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action == create_todo_widget:
            self.add_basic_widget(event)

    def mousePressEvent(self, event) -> None:
        super(MyView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_leftbtn_beauty(event)

