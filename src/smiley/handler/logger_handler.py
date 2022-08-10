"""logger_handler.py

This module contains one class named LoggerHandler Which is
used to log.
"""


import time
from typing import Dict, Final

from PySide6.QtCore import (
    QMessageLogContext,
    QMutex,
    QtMsgType,
    qInstallMessageHandler,
)

from smiley.handler.abstract_handler import AbstractHandler
from smiley.util.file_util import FileUtil

__all__ = ["LoggerHandler"]


class LoggerHandler(AbstractHandler):
    """LoggerHandler is used to catch qInfo|qDebug information.

    This handler will save the information into specific file.
    The default log file is log/log.text of your project.
    """

    # File name.
    __LOG_DIR_NAME: Final[str] = "log"
    __LOG_FILE_NAME: Final[str] = FileUtil.concat_path(
        __LOG_DIR_NAME, "log.txt"
    )

    # Log level.
    __LOG_LEVEL: int = QtMsgType.QtInfoMsg
    __LOG_LEVEL_DICT: Final[Dict[QtMsgType, str]] = {
        QtMsgType.QtInfoMsg: "[INFO]",
        QtMsgType.QtDebugMsg: "[DEBUG]",
        QtMsgType.QtWarningMsg: "[WARNING]",
        QtMsgType.QtCriticalMsg: "[CRITICAL]",
        QtMsgType.QtSystemMsg: "[SYSTEM]",
        QtMsgType.QtFatalMsg: "[FATAL]",
    }

    # Log lock.
    __LOG_LOCK: QMutex = QMutex()

    @classmethod
    def install_handler(cls) -> None:
        """Install message handler into application."""
        qInstallMessageHandler(cls.__logger_handler)

    @classmethod
    def __logger_handler(
        cls,
        qt_msg_type: QtMsgType,
        _: QMessageLogContext,
        content: str,
    ) -> None:
        """Catch exceptions and log different type of information
        into specific file.

        Args:
            qt_msg_type (QtMsgType): The type of message.
            content (str): Information.
        """

        # For security.
        assert qt_msg_type in cls.__LOG_LEVEL_DICT

        # Lock.
        cls.__LOG_LOCK.lock()

        # Create log dir in project.
        FileUtil.make_dirs(
            FileUtil.splice_project_location(cls.__LOG_DIR_NAME), 0o666
        )

        # Create log file in project.
        if qt_msg_type <= cls.__LOG_LEVEL:
            with open(
                FileUtil.splice_project_location(cls.__LOG_FILE_NAME),
                "a",
                encoding="utf-8",
            ) as log_file:
                log_file.write(
                    "\n".join(
                        [
                            f"\nLOG_LEVEL: {cls.__LOG_LEVEL_DICT[qt_msg_type]}",
                            f"CURRENT_TIME: {time.asctime( time.localtime(time.time()))}",
                            f"MESSAGE: {content}\n",
                        ]
                    )
                )

        # Unlock.
        cls.__LOG_LOCK.unlock()
