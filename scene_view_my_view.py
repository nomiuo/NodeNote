from PyQt5.QtWidgets import QGraphicsView, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QMovie
from scene_view_scene import Scene


class MyView(QGraphicsView):
    def __init__(self, parent=None):
        super(MyView, self).__init__(parent)

        # function1: show scene
        self.scene = Scene(self)
        self.set_scene()

        # function2: beauty
        self.set_beauty()

    # function1: show scene
    def set_scene(self):
        self.setScene(self.scene.my_scene)

    # function2: interface beauty
    def set_beauty(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # function3: left button beauty
    def set_left_btn_beauty(self, event):
        # set widget
        effect_container = QLabel(self)
        left_btn_effect = QMovie("Templates/left_btn_effect2.gif")

        # set style
        effect_container.setScaledContents(True)
        effect_container.resize(25, 25)
        effect_container.move(int(event.pos().x() - effect_container.width() / 2),
                              int(event.pos().y() - effect_container.height() / 2))

        # set function
        effect_container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        effect_container.setMovie(left_btn_effect)
        left_btn_effect.start()
        effect_container.show()

        # set done
        left_btn_effect.frameChanged.connect(lambda frame_number: self.set_left_btn_beauty_down(
                                                        frame_number=frame_number,
                                                        left_btn_effect=left_btn_effect,
                                                        effect_container=effect_container))

    @staticmethod
    def set_left_btn_beauty_down(frame_number, left_btn_effect, effect_container):
        if frame_number == left_btn_effect.frameCount() - 1:
            effect_container.close()

    # function 4: todo-list
    def set_todo_list(self, event):
        print('hello')

    def mousePressEvent(self, event) -> None:
        super(MyView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_left_btn_beauty(event)

    def keyPressEvent(self, event) -> None:
        super(MyView, self).keyPressEvent(event)
        if event.key() == Qt.Key_M and event.modifiers() & Qt.ControlModifier:
            self.set_todo_list(event)
