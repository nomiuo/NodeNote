import sys

from PySide6 import QtCore, QtWidgets

from smiley.config.controller.view_config import ViewConfig
from smiley.controller.view.view import View

app = QtWidgets.QApplication(sys.argv)
view = View()
config = ViewConfig().set_context_menu_policy(
    QtCore.Qt.ContextMenuPolicy.DefaultContextMenu
)
config.context_menu_policy_config(view)
view.show()
sys.exit(app.exec())
