"""This module defines a standard for all handlers."""

from abc import ABC, abstractmethod

__all__ = ["AbstractHandler"]


class AbstractHandler(ABC):
    """Abstract interface for all handlers.

    Every handler should implement install_handler
    function.

    Args:
        ABC (class): Abstract class.
    """

    @classmethod
    @abstractmethod
    def install_handler(cls) -> None:
        """Install message handler into application."""
