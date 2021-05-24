__all__ = ["NoteWindow"]

from PyQt5 import QtWidgets, QtCore, QtGui
from Components.effect_snow import EffectSkyWidget
from Components import attribute
from Model import stylesheet
from GraphicsView.view import View


class NoteWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(NoteWindow, self).__init__()

        self.UI_MainWindow()

        # tool bar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setStyleSheet(stylesheet.STYLE_QTOOLBAR)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

        # scene
        self.scene_list = QtWidgets.QTreeWidget()
        self.scene_list.setStyleSheet(stylesheet.STYLE_QTREEWIDGET)
        self.scene_list.setAlternatingRowColors(True)
        self.scene_list.setHeaderLabel("Scene List")
        self.scene_list.setIndentation(8)

        # style
        self.style_control = QtWidgets.QWidget()
        self.style_control_layout = QtWidgets.QGridLayout()
        self.style_control.setLayout(self.style_control_layout)
        #   attribute
        self.attribute_style = QtWidgets.QLabel("Attribute Widgets")
        self.style_control_layout.addWidget(self.attribute_style, 0, 0, 1, -1)

        #   font
        self.attribute_style_font = None
        self.attribute_style_font_color_type = None

        self.attribute_style_font_label = QtWidgets.QLabel("Font")
        self.attribute_style_font_select = QtWidgets.QPushButton("Select Font")
        self.attribute_style_font_color = QtWidgets.QLabel("Current Font Color")
        self.attribute_style_font_color_select = QtWidgets.QPushButton("Select Font Color")

        self.attribute_style_font_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.attribute_style_font_select.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_font_color.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.attribute_style_font_color_select.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)

        self.attribute_style_font_select.clicked.connect(lambda: self.font_changed(False))
        self.attribute_style_font_color_select.clicked.connect(lambda: self.color_changed("Font"))

        self.style_control_layout.addWidget(self.attribute_style_font_label, 1, 0, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_select, 1, 1, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_color, 2, 0, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_color_select, 2, 1, 1, 1)

        self.font_changed(True)

        #       color
        self.attribute_style_color = None
        self.attribute_style_selected_color = None

        self.attribute_style_color_select = QtWidgets.QPushButton("Select Background Color")
        self.attribute_style_color_label = QtWidgets.QLabel("Current Color")
        self.attribute_style_color_selected = QtWidgets.QPushButton("Select Selected Color")
        self.attribute_style_color_label_selected = QtWidgets.QLabel("Current Background Color")

        self.attribute_style_color_select.clicked.connect(lambda: self.color_changed("Attribute Widget", False, False))
        self.attribute_style_color_selected.clicked.connect(lambda: self.color_changed("Attribute Widget", True, False))
        self.attribute_style_color_label.setAutoFillBackground(True)
        self.attribute_style_color_label_selected.setAutoFillBackground(True)

        self.attribute_style.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_select.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_selected.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_label_selected.setStyleSheet(stylesheet.STYLE_QLABEL)

        self.color_changed("Attribute Widget", False, True)
        self.color_changed("Attribute Widget", True, True)

        self.style_control_layout.addWidget(self.attribute_style_color_label, 3, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_select, 3, 1)
        self.style_control_layout.addWidget(self.attribute_style_color_label_selected, 4, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_selected, 4, 1)

        self.toolbar.addWidget(self.scene_list)
        self.toolbar.addWidget(self.style_control)

        self.central_widget = QtWidgets.QWidget()  # central widget
        self.view_widget = View(self, self.central_widget)  # view widget
        self.scene_list.itemClicked.connect(self.view_widget.change_current_scene)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)  # layout contains two widgets
        self.sky_widget = EffectSkyWidget(self.view_widget, self.central_widget)  # snow falling widget
        self.UI_Widget()

    def UI_MainWindow(self):
        self.setWindowIcon(QtGui.QIcon('Resources/snow3.svg'))  # set icon
        self.setWindowTitle("Snow")  # set title
        self.resize(1200, 1000)  # set size
        self.move(  # set geometry
            (QtWidgets.QDesktopWidget().screenGeometry().width() - self.geometry().width()) // 2,
            (QtWidgets.QDesktopWidget().screenGeometry().height() - self.geometry().height()) // 2
        )

    def UI_Widget(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.view_widget)
        self.central_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setCentralWidget(self.central_widget)

    def color_changed(self, widget, selected_flag=False, init_flag=False):
        if widget == "Attribute Widget":
            if selected_flag is False:
                if not init_flag:
                    self.attribute_style_color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None, "Select Color",
                                                                                 QtWidgets.QColorDialog.ShowAlphaChannel)
                else:
                    self.attribute_style_color = attribute.AttributeWidget.color

                color_style = '''
                QLabel {
                    background-color: #%s;
                    border-style: outset;
                    border-width: 1px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 8px;
                    padding: 6px;
                }
                ''' % str(hex(self.attribute_style_color.rgba()))[2:]
                self.attribute_style_color_label.setStyleSheet(color_style)

                attribute.AttributeWidget.color = self.attribute_style_color
            else:
                if not init_flag:
                    self.attribute_style_selected_color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                                                          "Select Color",
                                                                                          QtWidgets.QColorDialog. \
                                                                                          ShowAlphaChannel)
                else:
                    self.attribute_style_selected_color = attribute.AttributeWidget.selected_color

                color_style = '''
                QLabel {
                    background-color: #%s;
                    border-style: outset;
                    border-width: 1px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 8px;
                    padding: 6px;
                }
                ''' % str(hex(self.attribute_style_selected_color.rgba()))[2:]
                self.attribute_style_color_label_selected.setStyleSheet(color_style)

                attribute.AttributeWidget.selected_color = self.attribute_style_selected_color
        elif widget == "Font":
            self.attribute_style_font_color_type = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                                                   "Select Color",
                                                                                   QtWidgets.QColorDialog. \
                                                                                   ShowAlphaChannel)
            attribute.InputTextField.font_color = self.attribute_style_font_color_type
            font_style_color = '''
            QLabel {
                background-color: rgba(204, 255, 255, 200);
                border-style: outset;
                border-width: 1px;
                border-radius: 10px;
                border-color: beige;
                font: bold 8px;
                padding: 6px;
                color: #%s;
            }
            ''' % str(hex(self.attribute_style_font_color_type.rgba()))[2:]
            self.attribute_style_font_color.setStyleSheet(font_style_color)

    def font_changed(self, init_flag: bool):
        if not init_flag:
            self.attribute_style_font, _ = QtWidgets.QFontDialog.getFont()
            attribute.InputTextField.font = self.attribute_style_font

            for item in self.view_widget.attribute_widgets:
                item.attribute_widget.label_item.document().setDefaultFont(self.attribute_style_font)
                item.text_change_node_shape()
                item.update_pipe_position()
        else:
            self.attribute_style_font = attribute.InputTextField.font

        self.attribute_style_font_label.setText("Font: %s %d" % (self.attribute_style_font.family(),
                                                                 self.attribute_style_font.pointSize()))

    def resizeEvent(self, a0) -> None:
        super(NoteWindow, self).resizeEvent(a0)
        self.sky_widget.resize(self.width(), self.height())

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_B and int(a0.modifiers()) & QtCore.Qt.ControlModifier:
            self.toolbar.setVisible(not self.toolbar.isVisible())
        if a0.key() == QtCore.Qt.Key_Delete and len(self.scene_list.selectedItems()) == 1:
            self.view_widget.delete_sub_scene(self.scene_list.selectedItems()[0])
        super(NoteWindow, self).keyPressEvent(a0)
