from scene_view_my_scene import MyScene


class Scene:
    def __init__(self, my_view):
        # 1. set MyScene
        self.my_scene = MyScene(self)
        self.my_view = my_view
        self.set_my_scene_rect()
        self.set_my_scene_background_img()

    # 1. set scene size
    def set_my_scene_rect(self):
        width = 64000
        height = 64000
        self.my_scene.set_my_scene_rect(width, height)

    # 2. set scene background img
    def set_my_scene_background_img(self):
        img_name = "Templates/girl.jpeg"
        self.my_scene.set_background_img(img_name)