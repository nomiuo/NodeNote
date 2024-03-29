# -*- coding: utf-8 -*-
"""
Example.py -  run the application
Copyright 2021 ye tao
Distributed under MPL-2.0 license. See LICENSE for more information

# v2.7.4:
## Debug:
- Restore the scene rect.
- Delete pipes correctly.
"""

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../../../")))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../../../")))

from PyQt5.QtCore import QLocale, QTranslator, qInstallMessageHandler
from PyQt5 import QtWidgets, QtCore
from src.NodeNotePackage.NodeNote.Components import work_dir_interface
from src.NodeNotePackage.NodeNote.GraphicsView.app import TabletApplication


def message_output(msg_type, context, msg):
    try:
        if msg_type >= 2:
            with open("exception_log.txt", "a", encoding="utf-8") as log:
                log.write(
                    f"{msg}, type: {msg_type} at {time.asctime(time.localtime(time.time()))}\n"
                )
    except Exception as e:
        pass


if __name__ == "__main__":
    qInstallMessageHandler(message_output)

    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_EnableHighDpiScaling, True
    )  # enable highdpi scaling
    QtWidgets.QApplication.setAttribute(
        QtCore.Qt.AA_UseHighDpiPixmaps, True
    )  # use highdpi icons

    app = TabletApplication(["", "--no-sandbox"])

    # load language
    local = QLocale()
    lan = QLocale.language(local)
    trans = QTranslator()
    if lan == QLocale.Chinese:
        trans.load("src/NodeNotePackage/NodeNote/Resources/MultiLanguages/zh_CN.qm")
        app.installTranslator(trans)

    # work dir interface
    work_dir_widget = work_dir_interface.WorkDirInterface(app, trans)
    work_dir_widget.show()

    app.exec_()
