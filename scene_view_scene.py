from scene_view_my_scene import MyScene


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
        img_name = "Templates/night.jpg"
        self.my_scene.set_background_img(img_name)

    # 3. store item in the my_scene
    def add_basic_widget(self, basic_widget):
        self.basic_widget.append(basic_widget)

    def remove_basic_widget(self, basic_widget):
        self.basic_widget.remove(basic_widget)