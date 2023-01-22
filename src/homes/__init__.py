"""Add message handler and start the application.
"""


from homes.config.handler.handler_config import HandlerConfig
from homes.handler.logger_handler import LoggerHandler

CONFIG_LIST = [
    LoggerHandler,
]


HandlerConfig.config(CONFIG_LIST)
