from PyQt5 import QtGui, QtCore, QtWidgets
from GraphicsView.scene import Scene
from Components import effect_water, attribute, port, pipe
from Model import constants


__all__ = ["View"]


class View(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        # BASIC SETTINGS
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing |
                            QtGui.QPainter.TextAntialiasing | QtGui.QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.scene = Scene(self)
        self.setScene(self.scene)

        # SCALE FUNCTION
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 0.8
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        # DRAW LINE
        self.mode = constants.MODE_NOOP

    def set_leftbtn_beauty(self, event):
        water_drop = effect_water.EffectWater()
        property_water_drop = QtWidgets.QGraphicsProxyWidget()
        property_water_drop.setWidget(water_drop)
        self.scene.addItem(property_water_drop)
        water_drop.move(self.mapToScene(event.pos()))
        water_drop.show()

    def change_scale(self, event):
        if constants.DEBUG_VIEW_CHANGE_SCALE:
            print("View is zooming! Current zoom: ", self.zoom)
        if event.key() == QtCore.Qt.Key_Equal and event.modifiers() & QtCore.Qt.ControlModifier:
            self.zoom += self.zoomStep
            if self.zoom <= self.zoomRange[1]:
                self.scale(self.zoomInFactor, self.zoomInFactor)
            else:
                self.zoom = self.zoomRange[1]
        elif event.key() == QtCore.Qt.Key_Minus and event.modifiers() & QtCore.Qt.ControlModifier:
            self.zoom -= self.zoomStep
            if self.zoom >= self.zoomRange[0]:
                self.scale(self.zoomOutFactor, self.zoomOutFactor)
            else:
                self.zoom = self.zoomRange[0]

    def add_basic_widget(self, event):
        basic_widget = attribute.AttributeWidget()
        self.scene.addItem(basic_widget)
        basic_widget.setPos(self.mapToScene(event.pos()))
        self.scene.add_tuple_node_widget(basic_widget)

    def contextMenuEvent(self, event) -> None:
        super(View, self).contextMenuEvent(event)
        if not event.isAccepted():
            context_menu = QtWidgets.QMenu(self)
            # context list
            create_truth_widget = context_menu.addAction("Create Attribute Widget")
            create_truth_widget.setIcon(QtGui.QIcon("Resources/ViewContextMenu/Attribute Widget.png"))

            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == create_truth_widget:
                self.add_basic_widget(event)

    def mousePressEvent(self, event) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.set_leftbtn_beauty(event)
            super(View, self).mousePressEvent(event)
            item = self.itemAt(event.pos())
            if type(item) is port.Port and self.mode == constants.MODE_NOOP:
                if constants.DEBUG_DRAW_PIPE:
                    print("enter the drag mode and set input port")
                self.mode = constants.MODE_PIPE_DRAG
                self.drag_pip = pipe.Pipe(input_port=item, output_port=None, parent=None)
                return
            if self.mode == constants.MODE_PIPE_DRAG:
                self.mode = constants.MODE_NOOP
        else:
            super(View, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.mode == constants.MODE_PIPE_DRAG:
            scene_pos = self.mapToScene(event.pos())
        super(View, self).mouseMoveEvent(event)

    def keyPressEvent(self, event) -> None:
        if (event.key() == QtCore.Qt.Key_Equal and event.modifiers() & QtCore.Qt.ControlModifier) or \
                (event.key() == QtCore.Qt.Key_Minus and event.modifiers() & QtCore.Qt.ControlModifier):
            self.change_scale(event)
        else:
            super(View, self).keyPressEvent(event)
