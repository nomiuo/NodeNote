__all__ = ["NoteWindow"]

from PyQt5 import QtWidgets, QtCore, QtGui
from Components.effect_snow import EffectSkyWidget
from Components import attribute, pipe, port, container
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

        # tab widget
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.scene_list, "Scene")
        self.tab_widget.addTab(self.style_control, "Style")

        # ================ Style ==============================
        self.style_switch_widget = QtWidgets.QComboBox()
        self.style_switch_widget.addItems(("All Scene", "Current Scene", "Selected Items"))
        self.style_switch_widget.setStyleSheet(stylesheet.STYLE_QCOMBOBOX)

        self.style_switch_layout = QtWidgets.QVBoxLayout()
        self.style_control.setLayout(self.style_switch_layout)
        self.style_switch_layout.addWidget(self.style_switch_widget)
        self.style_switch_layout.addLayout(self.style_control_layout)

        #   =============== attribute widget========================
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
        self.attribute_style_font_color_select.clicked.connect(lambda: self.color_changed("Font", None))

        self.style_control_layout.addWidget(self.attribute_style_font_label, 1, 0, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_select, 1, 1, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_color, 2, 0, 1, 1)
        self.style_control_layout.addWidget(self.attribute_style_font_color_select, 2, 1, 1, 1)

        self.font_changed(True)

        #       color
        self.attribute_style_color = None
        self.attribute_style_selected_color = None
        self.attribute_style_border_color = None
        self.attribute_style_border_selected_color = None

        self.attribute_style_color_select = QtWidgets.QPushButton("Select Background Color")
        self.attribute_style_color_label = QtWidgets.QLabel("Current Background Color")
        self.attribute_style_color_selected = QtWidgets.QPushButton("Select Selected Color")
        self.attribute_style_color_label_selected = QtWidgets.QLabel("Current Selected Color")
        self.attribute_style_color_border_selected = QtWidgets.QPushButton("Select Border Color")
        self.attribute_style_color_border = QtWidgets.QLabel("Current Border Color")
        self.attribute_style_color_selected_border_selected = QtWidgets.QPushButton("Select Selected Border Color")
        self.attribute_style_color_selected_border = QtWidgets.QLabel("Current SelectedBorder Color")

        self.attribute_style_color_select.clicked.connect(lambda: self.color_changed("Attribute Widget",
                                                                                     "Background", False))
        self.attribute_style_color_selected.clicked.connect(lambda: self.color_changed("Attribute Widget",
                                                                                       "Selected", False))
        self.attribute_style_color_border_selected.clicked.connect(lambda: self.color_changed("Attribute Widget",
                                                                                              "Border", False))
        self.attribute_style_color_selected_border_selected.clicked.connect(
            lambda: self.color_changed("Attribute Widget",
                                       "Selected Border", False))

        self.attribute_style_color_label.setAutoFillBackground(True)
        self.attribute_style_color_label_selected.setAutoFillBackground(True)
        self.attribute_style_color_border.setAutoFillBackground(True)
        self.attribute_style_color_selected_border.setAutoFillBackground(True)

        self.attribute_style.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_select.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_selected.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_label_selected.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_border_selected.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_border.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.attribute_style_color_selected_border_selected.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.attribute_style_color_selected_border.setStyleSheet(stylesheet.STYLE_QLABEL)

        self.color_changed("Attribute Widget", "Background", True)
        self.color_changed("Attribute Widget", "Selected", True)
        self.color_changed("Attribute Widget", "Border", True)
        self.color_changed("Attribute Widget", "Selected Border", True)

        self.style_control_layout.addWidget(self.attribute_style_color_label, 3, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_select, 3, 1)
        self.style_control_layout.addWidget(self.attribute_style_color_label_selected, 4, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_selected, 4, 1)
        self.style_control_layout.addWidget(self.attribute_style_color_border, 5, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_border_selected, 5, 1)
        self.style_control_layout.addWidget(self.attribute_style_color_selected_border, 6, 0)
        self.style_control_layout.addWidget(self.attribute_style_color_selected_border_selected, 6, 1)
        # ==========================================================

        # ================ Logic Widget =================================
        # Color
        self.logic_style_background_color = None
        self.logic_style_selected_background_color = None
        self.logic_style_border_color = None
        self.logic_style_selected_border_color = None
        # Widgets
        #   label widgets
        self.logic_style = QtWidgets.QLabel("Logic Widgets")
        self.logic_style_background_color_label = QtWidgets.QLabel("Current Background Color")
        self.logic_style_selected_background_color_label = QtWidgets.QLabel("Current Selected Background Color")
        self.logic_style_border_color_label = QtWidgets.QLabel("Current Border Color")
        self.logic_style_selected_border_color_label = QtWidgets.QLabel("Current Selected Border Color")
        #   button widgets
        self.logic_style_background_color_button = QtWidgets.QPushButton("Select Background Color")
        self.logic_style_selected_background_color_button = QtWidgets.QPushButton("Select Selected Background Color")
        self.logic_style_border_color_button = QtWidgets.QPushButton("Select Border Color")
        self.logic_style_selected_border_color_button = QtWidgets.QPushButton("Select Selected Border Color")
        #   added
        self.style_control_layout.addWidget(self.logic_style, 7, 0, 1, -1)
        self.style_control_layout.addWidget(self.logic_style_background_color_label, 8, 0)
        self.style_control_layout.addWidget(self.logic_style_selected_background_color_label, 9, 0)
        self.style_control_layout.addWidget(self.logic_style_border_color_label, 10, 0)
        self.style_control_layout.addWidget(self.logic_style_selected_border_color_label, 11, 0)
        self.style_control_layout.addWidget(self.logic_style_background_color_button, 8, 1)
        self.style_control_layout.addWidget(self.logic_style_selected_background_color_button, 9, 1)
        self.style_control_layout.addWidget(self.logic_style_border_color_button, 10, 1)
        self.style_control_layout.addWidget(self.logic_style_selected_border_color_button, 11, 1)
        # Stylesheet
        #   label stylesheet
        self.logic_style.setAutoFillBackground(True)
        self.logic_style_background_color_label.setAutoFillBackground(True)
        self.logic_style_selected_background_color_label.setAutoFillBackground(True)
        self.logic_style_border_color_label.setAutoFillBackground(True)
        self.logic_style_selected_border_color_label.setAutoFillBackground(True)
        self.logic_style.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.logic_style_background_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.logic_style_selected_background_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.logic_style_border_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.logic_style_selected_border_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        #   button stylesheet
        self.logic_style_background_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.logic_style_selected_background_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.logic_style_border_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.logic_style_selected_border_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        # Slots
        self.logic_style_background_color_button.clicked.connect(lambda: self.color_changed(
            "Logic Widget",
            "Background",
            False))
        self.logic_style_selected_background_color_button.clicked.connect(lambda: self.color_changed(
            "Logic Widget",
            "Selected Background",
            False
        ))
        self.logic_style_border_color_button.clicked.connect(lambda: self.color_changed(
            "Logic Widget",
            "Border",
            False
        ))
        self.logic_style_selected_border_color_button.clicked.connect(lambda: self.color_changed(
            "Logic Widget",
            "Selected Border",
            False
        ))
        # Init
        self.color_changed(
            "Logic Widget",
            "Background",
            True
        )
        self.color_changed(
            "Logic Widget",
            "Selected Background",
            True
        )
        self.color_changed(
            "Logic Widget",
            "Border",
            True
        )
        self.color_changed(
            "Logic Widget",
            "Selected Border",
            True
        )
        # =========================================================
        # ==================== Pipe =================================
        #   Parameters
        self.pipe_style_width = None
        self.pipe_style_background_color = None
        self.pipe_style_selected_background_color = None
        #   Widgets
        #       label
        self.pipe_style_label = QtWidgets.QLabel("Pipe Widgets")
        self.pipe_style_width_label = QtWidgets.QLabel("Current Width")
        self.pipe_style_background_color_label = QtWidgets.QLabel("Current Background Color")
        self.pipe_style_selected_background_color_label = QtWidgets.QLabel("Current Selected Background Color")
        #       button
        self.pipe_style_width_button = QtWidgets.QPushButton("Select Width")
        self.pipe_style_background_color_button = QtWidgets.QPushButton("Select Background Color")
        self.pipe_style_selected_background_color_button = QtWidgets.QPushButton("Select Selected Background Color")
        #       added
        self.style_control_layout.addWidget(self.pipe_style_label, 12, 0, 1, -1)
        self.style_control_layout.addWidget(self.pipe_style_width_label, 13, 0)
        self.style_control_layout.addWidget(self.pipe_style_background_color_label, 14, 0)
        self.style_control_layout.addWidget(self.pipe_style_selected_background_color_label, 15, 0)
        self.style_control_layout.addWidget(self.pipe_style_width_button, 13, 1)
        self.style_control_layout.addWidget(self.pipe_style_background_color_button, 14, 1)
        self.style_control_layout.addWidget(self.pipe_style_selected_background_color_button, 15, 1)
        #   Stylesheeet
        #       label stylesheet
        self.pipe_style_label.setAutoFillBackground(True)
        self.pipe_style_width_label.setAutoFillBackground(True)
        self.pipe_style_background_color_label.setAutoFillBackground(True)
        self.pipe_style_selected_background_color_label.setAutoFillBackground(True)
        self.pipe_style_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.pipe_style_width_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.pipe_style_background_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.pipe_style_selected_background_color_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        #       button stylesheet
        self.pipe_style_width_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.pipe_style_background_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.pipe_style_selected_background_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        #   Slots
        self.pipe_style_width_button.clicked.connect(lambda: self.width_changed("Pipe Widget", False))
        self.pipe_style_background_color_button.clicked.connect(lambda: self.color_changed("Pipe Widget", "Background",
                                                                                           False))
        self.pipe_style_selected_background_color_button.clicked.connect(lambda:
                                                                         self.color_changed("Pipe Widget",
                                                                                            "Selected Background",
                                                                                            False))
        #   Init
        self.width_changed("Pipe Widget", True)
        self.color_changed("Pipe Widget", "Background", True)
        self.color_changed("Pipe Widget", "Selected Background", True)
        # ==========================================================
        # ==================== Port ===================================
        #   Parameters
        self.port_style_width = None
        self.port_style_color = None
        self.port_style_border_color = None
        self.port_style_hovered_color = None
        self.port_style_hovered_border_color = None
        self.port_style_activated_color = None
        self.port_style_activated_border_color = None
        #   Widgets
        #       label widgets
        self.port_style_label = QtWidgets.QLabel("Port Widgets")
        self.port_style_width_label = QtWidgets.QLabel("Current Width")
        self.port_style_color_label = QtWidgets.QLabel("Current Background Color")
        self.port_style_border_color_label = QtWidgets.QLabel("Current Border Color")
        self.port_style_hovered_color_label = QtWidgets.QLabel("Current Hovered Background Color")
        self.port_style_hovered_border_color_label = QtWidgets.QLabel("Current Hovered Border Color")
        self.port_style_activated_color_label = QtWidgets.QLabel("Current Activated Background Color")
        self.port_style_activated_border_color_label = QtWidgets.QLabel("Current Activated Border Color")
        #       button widgets
        self.port_style_width_button = QtWidgets.QPushButton("Select Width")
        self.port_style_color_button = QtWidgets.QPushButton("Select Background Color")
        self.port_style_border_color_button = QtWidgets.QPushButton("Select Border Color")
        self.port_style_hovered_color_button = QtWidgets.QPushButton("Select Hovered Background Color")
        self.port_style_hovered_border_color_button = QtWidgets.QPushButton("Select Hovered Border Color")
        self.port_style_activated_color_button = QtWidgets.QPushButton("Select Activated Background Color")
        self.port_style_activated_border_color_button = QtWidgets.QPushButton("Select Activated Border Color")
        #       added
        self.style_control_layout.addWidget(self.port_style_label, 16, 0, 1, -1)
        self.style_control_layout.addWidget(self.port_style_width_label, 17, 0)
        self.style_control_layout.addWidget(self.port_style_color_label, 18, 0)
        self.style_control_layout.addWidget(self.port_style_border_color_label, 19, 0)
        self.style_control_layout.addWidget(self.port_style_hovered_color_label, 20, 0)
        self.style_control_layout.addWidget(self.port_style_hovered_border_color_label, 21, 0)
        self.style_control_layout.addWidget(self.port_style_activated_color_label, 22, 0)
        self.style_control_layout.addWidget(self.port_style_activated_border_color_label, 23, 0)
        self.style_control_layout.addWidget(self.port_style_width_button, 17, 1)
        self.style_control_layout.addWidget(self.port_style_color_button, 18, 1)
        self.style_control_layout.addWidget(self.port_style_border_color_button, 19, 1)
        self.style_control_layout.addWidget(self.port_style_hovered_color_button, 20, 1)
        self.style_control_layout.addWidget(self.port_style_hovered_border_color_button, 21, 1)
        self.style_control_layout.addWidget(self.port_style_activated_color_button, 22, 1)
        self.style_control_layout.addWidget(self.port_style_activated_border_color_button, 23, 1)
        #   Stylesheet
        #       label stylesheet
        self.port_style_label.setAutoFillBackground(True)
        self.port_style_width_label.setAutoFillBackground(True)
        self.port_style_color_label.setAutoFillBackground(True)
        self.port_style_border_color_label.setAutoFillBackground(True)
        self.port_style_hovered_color_label.setAutoFillBackground(True)
        self.port_style_hovered_border_color_label.setAutoFillBackground(True)
        self.port_style_activated_color_label.setAutoFillBackground(True)
        self.port_style_activated_border_color_label.setAutoFillBackground(True)
        self.port_style_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.port_style_width_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_border_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_hovered_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_hovered_border_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_activated_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.port_style_activated_border_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        #       button stylesheet
        self.port_style_width_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_border_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_hovered_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_hovered_border_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_activated_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.port_style_activated_border_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        #   Slots
        self.port_style_width_button.clicked.connect(lambda: self.width_changed("Port Widget", False))
        self.port_style_color_button.clicked.connect(lambda: self.color_changed("Port Widget", "Background", False))
        self.port_style_border_color_button.clicked.connect(lambda: self.color_changed("Port Widget", "Border", False))
        self.port_style_hovered_color_button.clicked.connect(lambda: self.color_changed("Port Widget",
                                                                                        "Hovered Background", False))
        self.port_style_hovered_border_color_button.clicked.connect(lambda: self.color_changed("Port Widget",
                                                                                               "Hovered Border", False))
        self.port_style_activated_color_button.clicked.connect(lambda: self.color_changed("Port Widget",
                                                                                          "Activated Background",
                                                                                          False))
        self.port_style_activated_border_color_button.clicked.connect(lambda: self.color_changed("Port Widget",
                                                                                                 "Activated Border",
                                                                                                 False))
        #   Init
        self.width_changed("Port Widget", True)
        self.color_changed("Port Widget", "Background", True)
        self.color_changed("Port Widget", "Border", True)
        self.color_changed("Port Widget", "Hovered Background", True)
        self.color_changed("Port Widget", "Hovered Border", True)
        self.color_changed("Port Widget", "Activated Background", True)
        self.color_changed("Port Widget", "Activated Border", True)
        # ==========================================================
        # ====================== Container =============================
        #   Parameters
        self.container_style_width = None
        self.container_style_color = None
        self.container_style_selected_color = None
        #   Widgets
        #       label widget
        self.container_style_label = QtWidgets.QLabel("Container Widgets")
        self.container_style_width_label = QtWidgets.QLabel("Current Width")
        self.container_style_color_label = QtWidgets.QLabel("Current Color")
        self.container_style_selected_color_label = QtWidgets.QLabel("Current Selected Color")
        #       button widget
        self.container_style_width_button = QtWidgets.QPushButton("Select Width")
        self.container_style_color_button = QtWidgets.QPushButton("Select Color")
        self.container_style_selected_color = QtWidgets.QPushButton("Select Selected Color")
        #       added
        self.style_control_layout.addWidget(self.container_style_label, 24, 0, 1, -1)
        self.style_control_layout.addWidget(self.container_style_width_label, 25, 0)
        self.style_control_layout.addWidget(self.container_style_color_label, 26, 0)
        self.style_control_layout.addWidget(self.container_style_selected_color_label, 27, 0)
        self.style_control_layout.addWidget(self.container_style_width_button, 25, 1)
        self.style_control_layout.addWidget(self.container_style_color_button, 26, 1)
        self.style_control_layout.addWidget(self.container_style_selected_color, 27, 1)
        #   Stylesheeet
        #       label stylesheet
        self.container_style_label.setAutoFillBackground(True)
        self.container_style_width_label.setAutoFillBackground(True)
        self.container_style_color_label.setAutoFillBackground(True)
        self.container_style_selected_color_label.setAutoFillBackground(True)
        self.container_style_label.setStyleSheet(stylesheet.STYLE_QLABEL)
        self.container_style_width_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.container_style_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        self.container_style_selected_color_label.setStyleSheet(stylesheet.STYLE_QLABEL_NOCOLOR)
        #       button stylesheet
        self.container_style_width_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.container_style_color_button.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        self.container_style_selected_color.setStyleSheet(stylesheet.STYLE_QPUSHBUTTON)
        #   Slots
        self.container_style_width_button.clicked.connect(lambda: self.width_changed("Container Widget", False))
        self.container_style_color_button.clicked.connect(lambda: self.color_changed("Container Widget",
                                                                                     "Color", False))
        self.container_style_selected_color.clicked.connect(lambda: self.color_changed("Container Widget",
                                                                                       "Selected Color", False))
        #   Init
        self.width_changed("Container Widget", True)
        self.color_changed("Container Widget", "Color", True)
        self.color_changed("Container Widget", "Selected Color", True)
        # ==========================================================
        # ============================   Style  =========================
        #   init
        self.font_changed(True, self.style_switch_widget.currentIndex())
        #   slots
        self.style_switch_widget.currentIndexChanged.connect(
            lambda combox_index: self.font_changed(False, combox_index))
        # ==========================================================
        self.toolbar.addWidget(self.tab_widget)

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

    def color_changed(self, widget, content, init_flag=False):
        if widget == "Attribute Widget":
            if content == "Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None, "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.attribute_style_color = color
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
            elif content == "Selected":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.attribute_style_selected_color = color
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

            elif content == "Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.attribute_style_border_color = color
                else:
                    self.attribute_style_border_color = attribute.AttributeWidget.border_color

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
                                ''' % str(hex(self.attribute_style_border_color.rgba()))[2:]
                self.attribute_style_color_border.setStyleSheet(color_style)

                attribute.AttributeWidget.border_color = self.attribute_style_border_color

            elif content == "Selected Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.attribute_style_border_selected_color = color
                else:
                    self.attribute_style_border_selected_color = attribute.AttributeWidget.selected_border_color

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
                                                ''' % str(hex(self.attribute_style_border_selected_color.rgba()))[2:]
                self.attribute_style_color_selected_border.setStyleSheet(color_style)

                attribute.AttributeWidget.selected_border_color = self.attribute_style_border_selected_color

        elif widget == "Font":
            font_type = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                        "Select Color",
                                                        QtWidgets.QColorDialog.ShowAlphaChannel)
            if font_type:
                self.attribute_style_font_color_type = font_type
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

            for attribute_widget in self.view_widget.attribute_widgets:
                attribute_widget.attribute_widget.label_item.font_color = self.attribute_style_font_color_type
                attribute_widget.attribute_widget.label_item.setDefaultTextColor(self.attribute_style_font_color_type)

        elif widget == "Logic Widget":

            if content == "Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.logic_style_background_color = color
                else:
                    self.logic_style_background_color = attribute.LogicWidget.background_color

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
                                        ''' % str(
                    hex(self.logic_style_background_color.rgba()))[2:]
                self.logic_style_background_color_label.setStyleSheet(color_style)

                attribute.LogicWidget.background_color = self.logic_style_background_color

            elif content == "Selected Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.logic_style_selected_background_color = color
                else:
                    self.logic_style_selected_background_color = attribute.LogicWidget.selected_background_color

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
                                        ''' % str(
                    hex(self.logic_style_selected_background_color.rgba()))[2:]
                self.logic_style_selected_background_color_label.setStyleSheet(color_style)

                attribute.LogicWidget.selected_background_color = self.logic_style_selected_background_color

            elif content == "Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.logic_style_border_color = color
                else:
                    self.logic_style_border_color = attribute.LogicWidget.border_color

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
                                        ''' % str(
                    hex(self.logic_style_border_color.rgba()))[2:]
                self.logic_style_border_color_label.setStyleSheet(color_style)

                attribute.LogicWidget.border_color = self.logic_style_border_color

            elif content == "Selected Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.logic_style_selected_border_color = color
                else:
                    self.logic_style_selected_border_color = attribute.LogicWidget.selected_border_color

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
                                        ''' % str(
                    hex(self.logic_style_selected_border_color.rgba()))[2:]
                self.logic_style_selected_border_color_label.setStyleSheet(color_style)

                attribute.LogicWidget.selected_border_color = self.logic_style_selected_border_color
        elif widget == "Pipe Widget":
            if content == "Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.pipe_style_background_color = color
                else:
                    self.pipe_style_background_color = pipe.Pipe.color

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
                                            ''' % str(
                    hex(self.pipe_style_background_color.rgba()))[2:]
                self.pipe_style_background_color_label.setStyleSheet(color_style)

                pipe.Pipe.color = self.pipe_style_background_color

            elif content == "Selected Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.pipe_style_selected_background_color = color
                else:
                    self.pipe_style_selected_background_color = pipe.Pipe.selected_color

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
                                            ''' % str(
                    hex(self.pipe_style_selected_background_color.rgba()))[2:]
                self.pipe_style_selected_background_color_label.setStyleSheet(color_style)

                pipe.Pipe.selected_color = self.pipe_style_selected_background_color

        elif widget == "Port Widget":
            if content == "Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_color = color
                else:
                    self.port_style_color = port.Port.color

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
                                                            ''' % str(
                    hex(self.port_style_color.rgba()))[2:]
                self.port_style_color_label.setStyleSheet(color_style)

                port.Port.color = self.port_style_color

            elif content == "Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_border_color = color
                else:
                    self.port_style_border_color = port.Port.border_color

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
                                                            ''' % str(
                    hex(self.port_style_border_color.rgba()))[2:]
                self.port_style_border_color_label.setStyleSheet(color_style)

                port.Port.border_color = self.port_style_border_color

            elif content == "Hovered Background":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_hovered_color = color
                else:
                    self.port_style_hovered_color = port.Port.hovered_color

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
                                                            ''' % str(
                    hex(self.port_style_hovered_color.rgba()))[2:]
                self.port_style_hovered_color_label.setStyleSheet(color_style)

                port.Port.hovered_color = self.port_style_hovered_color

            elif content == "Hovered Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_hovered_border_color = color
                else:
                    self.port_style_hovered_border_color = port.Port.hovered_border_color

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
                                                            ''' % str(
                    hex(self.port_style_hovered_border_color.rgba()))[2:]
                self.port_style_hovered_border_color_label.setStyleSheet(color_style)

                port.Port.hovered_border_color = self.port_style_hovered_border_color

            elif content == "Activated Color":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_activated_color = color
                else:
                    self.port_style_activated_color = port.Port.activated_color

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
                                                            ''' % str(
                    hex(self.port_style_activated_color.rgba()))[2:]
                self.port_style_activated_color_label.setStyleSheet(color_style)

                port.Port.activated_color = self.port_style_activated_color

            elif content == "Activated Border":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.port_style_activated_border_color = color
                else:
                    self.port_style_activated_border_color = port.Port.activated_border_color

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
                                                            ''' % str(
                    hex(self.port_style_activated_border_color.rgba()))[2:]
                self.port_style_activated_border_color_label.setStyleSheet(color_style)

                port.Port.activated_border_color = self.port_style_activated_border_color

        elif widget == "Container Widget":
            if content == "Color":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.container_style_color = color
                else:
                    self.container_style_color = container.Container.color

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
                                                                           ''' % str(
                    hex(self.container_style_color.rgba()))[2:]
                self.container_style_color_label.setStyleSheet(color_style)

                container.Container.color = self.container_style_color

            elif content == "Selected Color":
                if not init_flag:
                    color = QtWidgets.QColorDialog.getColor(QtCore.Qt.red, None,
                                                            "Select Color",
                                                            QtWidgets.QColorDialog.ShowAlphaChannel)
                    if color:
                        self.container_style_selected_color = color
                else:
                    self.container_style_selected_color = container.Container.selected_color

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
                                                                           ''' % str(
                    hex(self.container_style_selected_color.rgba()))[2:]
                self.container_style_selected_color_label.setStyleSheet(color_style)

                container.Container.selected_color = self.container_style_selected_color

    def font_changed(self, init_flag: bool, combox_index=0):
        if combox_index == 0:
            if not init_flag:
                font_type, ok = QtWidgets.QFontDialog.getFont()
                if font_type and ok:
                    self.attribute_style_font = font_type
                attribute.InputTextField.font = self.attribute_style_font

                for item in self.view_widget.attribute_widgets:
                    item.attribute_widget.label_item.document().setDefaultFont(self.attribute_style_font)
                    item.text_change_node_shape()
                    item.update_pipe_position()
            else:
                self.attribute_style_font = attribute.InputTextField.font

            self.attribute_style_font_label.setText("Font: %s %d" % (self.attribute_style_font.family(),
                                                                     self.attribute_style_font.pointSize()))
        elif combox_index == 1:
            if not init_flag:
                font_type, ok = QtWidgets.QFontDialog.getFont()
                if font_type and ok:
                    self.view_widget.current_scene.attribute_style_font = font_type

                for item in self.view_widget.current_scene.items():
                    if isinstance(item, attribute.AttributeWidget):
                        item.attribute_widget.label_item.document().setDefaultFont(self.attribute_style_font)
                        item.text_change_node_shape()
                        item.update_pipe_position()

            else:
                self.view_widget.current_scene.attribute_style_font = attribute.InputTextField.font

            self.attribute_style_font_label.setText("Font: %s %d" % (self.attribute_style_font.family(),
                                                                     self.attribute_style_font.pointSize()))

    def width_changed(self, widget, init_flag: bool):
        if widget == "Pipe Widget":
            if not init_flag:
                width, ok = QtWidgets.QInputDialog.getDouble(self, "Get Double Width",
                                                             "Width", 2, 0.1, 15.0, 2, QtCore.Qt.WindowFlags(), 0.5)
                if ok and width:
                    self.pipe_style_width = width
            else:
                self.pipe_style_width = pipe.Pipe.width

            pipe.Pipe.width = self.pipe_style_width
            self.pipe_style_width_label.setText("Current Width: %s" % str(self.pipe_style_width))

        elif widget == "Port Widget":
            if not init_flag:
                width, ok = QtWidgets.QInputDialog.getDouble(self, "Get Double Width",
                                                             "Width", 22.0, 2.0, 40.0, 2, QtCore.Qt.WindowFlags(), 2)
                if width and ok:
                    self.port_style_width = width
            else:
                self.port_style_width = port.Port.width

            port.Port.width = self.port_style_width
            self.port_style_width_label.setText("Current Width: %s" % str(self.port_style_width))

        elif widget == "Container Widget":
            if not init_flag:
                width, ok = QtWidgets.QInputDialog.getDouble(self, "Get Double Width",
                                                             "Width", 4.0, 0.5, 8.0, 2, QtCore.Qt.WindowFlags(), 0.5)
                if width and ok:
                    self.container_style_width = width
            else:
                self.container_style_width = container.Container.width

            container.Container.width = self.container_style_width
            self.container_style_width_label.setText("Current Width: %s" % str(self.container_style_width))

    def resizeEvent(self, a0) -> None:
        super(NoteWindow, self).resizeEvent(a0)
        self.sky_widget.resize(self.width(), self.height())

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_B and int(a0.modifiers()) & QtCore.Qt.ControlModifier:
            self.toolbar.setVisible(not self.toolbar.isVisible())
        if a0.key() == QtCore.Qt.Key_Delete and len(self.scene_list.selectedItems()) == 1:
            self.view_widget.delete_sub_scene(self.scene_list.selectedItems()[0])
        super(NoteWindow, self).keyPressEvent(a0)
