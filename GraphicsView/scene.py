from PyQt5 import QtWidgets, QtCore
from Components import effect_background, effect_cutline


__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, sub_scene_flag, view, attribute_widget = None, parent=None):
        super(Scene, self).__init__(parent)
        self.view = view
        self.attribute_widget = attribute_widget
        self.setSceneRect(QtCore.QRectF())
        self.sub_scene_flag = sub_scene_flag

        # background image
        self.background_image = effect_background.EffectBackground(self.view)
        self.background_image.resize(self.view.size().width(), self.view.size().height())
        self.background_image.setPos(self.view.mapToScene(0, 0).x(), self.view.mapToScene(0, 0).y())
        self.addItem(self.background_image)
        self.background_image.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)

        # CUT LINE
        self.cutline = effect_cutline.EffectCutline()
        self.addItem(self.cutline)