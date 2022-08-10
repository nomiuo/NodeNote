"""Add message handler and start the application.
"""


from smiley.config.handler.handler_config import HandlerConfig
from smiley.handler.logger_handler import LoggerHandler

CONFIG_LIST = [
    LoggerHandler,
]


HandlerConfig.config(CONFIG_LIST)
