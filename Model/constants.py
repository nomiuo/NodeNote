from PyQt5.QtWidgets import QGraphicsItem


DEBUG_EFFECT_SNOW = False
DEBUG_TUPLE_NODE_SCALE = False

# === DRAW STACK ORDER ===
Z_VAL_PIPE = -1
Z_VAL_NODE = 1
Z_VAL_PORT = 2
Z_VAL_NODE_WIDGET = 3


# === NODE ===
NODE_WIDTH = 170
NODE_HEIGHT = 80
NODE_LAYOUT_MARGINS = 5
NODE_ICON_SIZE = 24
NODE_SEL_COLOR = (255, 255, 255, 30)
NODE_SEL_BORDER_COLOR = (254, 207, 42, 255)

# === ITEM CACHE MODE ===
ITEM_CACHE_MODE = QGraphicsItem.DeviceCoordinateCache

# === NODE PROPERTY ===

#: Property type will hidden in the properties bin (default).
NODE_PROP = 0
#: Property type represented with a QLabel widget in the properties bin.
NODE_PROP_QLABEL = 2
#: Property type represented with a QLineEdit widget in the properties bin.
NODE_PROP_QLINEEDIT = 3
#: Property type represented with a QTextEdit widget in the properties bin.
NODE_PROP_QTEXTEDIT = 4
#: Property type represented with a QComboBox widget in the properties bin.
NODE_PROP_QCOMBO = 5
#: Property type represented with a QCheckBox widget in the properties bin.
NODE_PROP_QCHECKBOX = 6
#: Property type represented with a QSpinBox widget in the properties bin.
NODE_PROP_QSPINBOX = 7
#: Property type represented with a ColorPicker widget in the properties bin.
NODE_PROP_COLORPICKER = 8
#: Property type represented with a Slider widget in the properties bin.
NODE_PROP_SLIDER = 9
#: Property type represented with a file selector widget in the properties bin.
NODE_PROP_FILE = 10
#: Property type represented with a file save widget in the properties bin.
NODE_PROP_FILE_SAVE = 11
#: Property type represented with a vector2 widget in the properties bin.
NODE_PROP_VECTOR2 = 12
#: Property type represented with vector3 widget in the properties bin.
NODE_PROP_VECTOR3 = 13
#: Property type represented with vector4 widget in the properties bin.
NODE_PROP_VECTOR4 = 14
#: Property type represented with float widget in the properties bin.
NODE_PROP_FLOAT = 15
#: Property type represented with int widget in the properties bin.
NODE_PROP_INT = 16
#: Property type represented with button widget in the properties bin.
NODE_PROP_BUTTON = 17
