from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QBrush


class MyScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(MyScene, self).__init__(parent)
        self.scene = scene

    # 1. interface resize
    def set_my_scene_rect(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    # 2. interface background
    def set_background_img(self, img_name="Templates/night.jpg"):
        background_img = QPixmap(img_name)
        self.setBackgroundBrush(QBrush(background_img))
