import sys

from Components.window import NoteWindow
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


if __name__ == '__main__':
    app = QApplication([])

    # slash
    splash = QSplashScreen(QPixmap("Resources/splash.jpg"))
    splash.showMessage("start loading", Qt.AlignCenter | Qt.AlignBottom, Qt.white)
    splash.setFont(QFont("New York Large", 10))
    splash.show()
    app.processEvents()

    # main
    window = NoteWindow(sys.argv)
    window.load_data(splash)
    window.show()
    splash.finish(window)
    splash.deleteLater()

    app.exec_()