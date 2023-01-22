"""View controller.
"""

from typing import Optional

from PySide6 import QtWidgets

from homes.config.controller.view_config import ViewConfig


class View(QtWidgets.QGraphicsView):
    """Show the scene through the graphics view.

    Args:
        QtWidgets.QGraphicsView (class): Parent class.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        # View configuration.
        self.__view_config: Optional[ViewConfig] = None

        # Scene property.
        self.__current_scene: Optional[QtWidgets.QGraphicsScene] = None

    def set_current_scene(self, scene: QtWidgets.QGraphicsScene) -> "View":
        """Set current scene property.

        Args:
            scene (QtWidgets.QGraphicsScene): The scene which will be associated with the view.
        """
        self.__current_scene = scene

        return self

    def set_view_config(self, view_config: ViewConfig) -> "View":
        """Set configuration of view.

        Args:
            view_config (ViewConfig): Configuration.

        Returns:
            Self: Self.
        """
        self.__view_config = view_config

        return self

    def get_current_scene(self) -> Optional[QtWidgets.QGraphicsScene]:
        """Get current scene property.

        Returns:
            QtWidgets.QGraphicsScene: The scene which is associated with the view.
        """
        return self.__current_scene

    def get_view_config(self) -> Optional[ViewConfig]:
        """Get configuration of view.

        Returns:
            ViewConfig: Configuration.
        """
        return self.__view_config
