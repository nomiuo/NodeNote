from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class w(QWidget):
    # function3: left button beauty
    def set_left_btn_beauty(self, event):
        # set widget
        self.effect_container = QLabel(self)
        self.left_btn_effect = QMovie("Templates/left_btn_effect.gif")

        # set style
        self.effect_container.setScaledContents(True)
        self.effect_container.resize(150, 150)
        self.effect_container.move(int(event.pos().x() - self.effect_container.width() / 2),
                                   int(event.pos().y() - self.effect_container.height() / 2))

        # set function
        self.effect_container.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.effect_container.setMovie(self.left_btn_effect)
        self.left_btn_effect.start()
        self.effect_container.show()
        print('done')

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.set_left_btn_beauty(event)


app = QApplication([])
wa = w()
wa.show()
app.exec_()