from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication


# todo: 1. clone node
# todo: 2. use time
# todo: 3. print
# todo: 4. ball
# todo: 5. paste debug
# todo: 6. style
if __name__ == '__main__':
    app = QApplication([])
    window = NoteWindow()
    window.show()
    app.exec_()
