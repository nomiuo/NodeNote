from collections import OrderedDict
from PyQt5 import QtWidgets, QtCore
from Components import effect_background, effect_cutline, attribute, pipe, container
from Model import serializable

__all__ = ["Scene"]


class Scene(QtWidgets.QGraphicsScene, serializable.Serializable):
    def __init__(self, sub_scene_flag, view, attribute_widget=None, parent=None):
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

    def serialize(self):
        attribute_widgets = list()
        logic_widgets = list()
        pipe_widgets = list()
        container_widgets = list()

        for item in self.items():
            if isinstance(item, attribute.AttributeWidget):
                attribute_widgets.append(item.serialize())
            elif isinstance(item, attribute.LogicWidget):
                logic_widgets.append(item.serialize())
            elif isinstance(item, pipe.Pipe):
                pipe_widgets.append(item.serialize())
            elif isinstance(item, container.Container):
                container_widgets.append(item.serialize())

        return OrderedDict([
            ('id', self.id),
            ('attribute widgets', attribute_widgets),
            ('logic widgets', logic_widgets),
            ('pipe widgets', pipe_widgets),
            ('container widgets', container_widgets)
        ])

    def deserialize(self, data, hashmap: dict, view=None):
        self.id = data['id']
        hashmap[data['id']] = self

        for attribute_data in data['attribute widgets']:
            attribute.AttributeWidget().deserialize(attribute_data, hashmap, view)
        return True
