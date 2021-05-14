from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: setConrnerWidget
# todo: clone node
# todo: animation added in the front
# todo: pipe + not set
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
