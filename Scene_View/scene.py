from Scene_View.my_scene import MyScene


class Scene:
    def __init__(self):
        # 1. set MyScene
        self.my_scene = MyScene(self)
        self.set_my_scene_rect()

    # set scene size
    def set_my_scene_rect(self):
        width = 64000
        height = 64000
        self.my_scene.set_my_scene_rect(width, height)
