from PyQt5 import QtGui, QtCore, QtWidgets
from GraphicsView.scene import Scene
from Components import effect_water, attribute, port, pipe, effect_background
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
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.scene = Scene(self)
        self.background_image = effect_background.EffectBackground(self)
        self.background_image.resize(self.size().width(), self.size().height())
        self.background_image.setPos(self.mapToScene(0, 0).x(), self.mapToScene(0, 0).y())
        self.scene.addItem(self.background_image)
        self.setScene(self.scene)

        # SCALE FUNCTION
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 0.8
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        # SCROLLBAR
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.horizontal_scrollbar = QtWidgets.QScrollBar()
        self.horizontal_scrollbar.setStyleSheet('''
                QScrollBar:horizontal {
                    border: 2px solid grey;
                    background: #32CC99;
                    height: 8px;
                    margin: 0px 20px 0 20px;
                }
                QScrollBar::handle:horizontal {
                    background: rgba(204, 255, 255, 200);
                    min-width: 20px;
                }
                QScrollBar::add-line:horizontal {
                    border: 2px solid grey;
                    background: #32CC99;
                    width: 20px;
                    subcontrol-position: right;
                    subcontrol-origin: margin;
                }
                
                QScrollBar::sub-line:horizontal {
                    border: 2px solid grey;
                    background: #32CC99;
                    width: 20px;
                    subcontrol-position: left;
                    subcontrol-origin: margin;
                }
    ''')
        self.setHorizontalScrollBar(self.horizontal_scrollbar)
        self.vertical_scrollbar = QtWidgets.QScrollBar()
        self.vertical_scrollbar.setStyleSheet('''
             QScrollBar:vertical {
                 border: 2px solid grey;
                 background: #32CC99;
                 width: 8px;
                 margin: 22px 0 22px 0;
             }
             QScrollBar::handle:vertical {
                 background: rgba(204, 255, 255, 200);
                 min-height: 20px;
             }
             QScrollBar::add-line:vertical {
                 border: 2px solid grey;
                 background: #32CC99;
                 height: 20px;
                 subcontrol-position: bottom;
                 subcontrol-origin: margin;
             }
            
             QScrollBar::sub-line:vertical {
                 border: 2px solid grey;
                 background: #32CC99;
                 height: 20px;
                 subcontrol-position: top;
                 subcontrol-origin: margin;
             }
             QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                 border: 2px solid grey;
                 width: 3px;
                 height: 3px;
                 background: white;
             }
            
             QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                 background: none;
             }
            ''')
        self.setVerticalScrollBar(self.vertical_scrollbar)

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

    def change_svg_image(self, event):
        image_name, image_type = QtWidgets.QFileDialog.getOpenFileName(self, "select svg", "", "*.svg")
        if image_name != "":
            self.background_image.change_svg(image_name)

    def contextMenuEvent(self, event) -> None:
        super(View, self).contextMenuEvent(event)
        if not event.isAccepted():
            context_menu = QtWidgets.QMenu(self)
            # context list
            create_truth_widget = context_menu.addAction("Create Attribute Widget")
            create_truth_widget.setIcon(QtGui.QIcon("Resources/ViewContextMenu/Attribute Widget.png"))
            change_background_image = context_menu.addAction("Change Background Image")
            change_background_image.setIcon(QtGui.QIcon("Resources/ViewContextMenu/Change Background Image.png"))

            action = context_menu.exec_(self.mapToGlobal(event.pos()))
            if action == create_truth_widget:
                self.add_basic_widget(event)
            elif action == change_background_image:
                self.change_svg_image(event)

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

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        self.background_image.setPos(self.mapToScene(0, 0).x(), self.mapToScene(0, 0).y())
        self.background_image.resize(self.size().width(), self.size().height())
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
