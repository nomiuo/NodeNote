"""This module contains HandlerConfig class.

Import this module and call HandlerConfig.config will
launch the specific handler passed by caller.
"""

from typing import Sequence, Type

from homes.handler.abstract_handler import AbstractHandler


class HandlerConfig:
    """Install the handlers."""

    @staticmethod
    def config(handlers: Sequence[Type[AbstractHandler]]) -> None:
        """Install the handlers passed by caller.

        Args:
            handlers (List[AbstractHandler]): A list contains handler.
        """
        # For security.
        assert handlers

        # Install handlers.
        for handler in handlers:
            handler.install_handler()
