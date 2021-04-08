from PyQt5.QtWidgets import QGraphicsScene


class MyScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(MyScene, self).__init__(parent)

        # 1. Contact with the outside scene
        self.scene = scene

    # 2. Set background
    def drawBackground(self, painter, rect):
        pass

    def set_my_scene_rect(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)
