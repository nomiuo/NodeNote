from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPixmap, QBrush


class MyScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(MyScene, self).__init__(parent)
        self.scene = scene

    # 1. interface resize
    def set_my_scene_rect(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    # 2. interface background
    def set_background_img(self, img_name="Resources/night.jpg"):
        background_img = QPixmap(img_name)
        self.setBackgroundBrush(QBrush(background_img))


class Scene:
    def __init__(self, my_view):
        # 1. set MyScene
        self.my_scene = MyScene(self)
        self.my_view = my_view
        self.set_my_scene_rect()
        self.set_my_scene_background_img()

        # 3. store item in the my_scene
        self.basic_widget = list()

    # 1. set scene size
    def set_my_scene_rect(self):
        width = 64000
        height = 64000
        self.my_scene.set_my_scene_rect(width, height)

    # 2. set scene background img
    def set_my_scene_background_img(self):
        img_name = "Resources/night.jpg"
        self.my_scene.set_background_img(img_name)

    # 3. store item in the my_scene
    def add_basic_widget(self, basic_widget):
        self.basic_widget.append(basic_widget)

    def remove_basic_widget(self, basic_widget):
        self.basic_widget.remove(basic_widget)
