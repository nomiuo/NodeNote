from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: setConrnerWidget
# todo: clone node
# todo: change control point with pipe
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
