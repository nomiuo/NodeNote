"""Configuration of view.
"""


from PySide6 import QtCore, QtGui, QtWidgets
from typing_extensions import Self


class ViewConfig:
    """Configuration of view.
    Can init ViewConfig and set configuration of view
    such as update mode, render hints, context menu
    policy, attribute and drag mode.

    Please ensure that the specific configuration is not
    none.
    """

    __CONFIG_ERROR: str = "Please ensure view and config not none."

    def __init__(self) -> None:
        super().__init__()

        self.__update_mode: QtWidgets.QGraphicsView.ViewportUpdateMode = None
        self.__render_hints: QtGui.QPainter.RenderHints = None
        self.__context_menu_policy: QtCore.Qt.ContextMenuPolicy = None
        self.__attribute: QtCore.Qt.WidgetAttribute = None
        self.__drag_mode: QtWidgets.QGraphicsView.DragMode = None

    def update_mode_config(self, view: QtWidgets.QGraphicsView) -> None:
        """Set the update mode of graphics view.

        Args:
            view (QtWidgets.QGraphicsView): Window used to show scene.
        """

        # For security.
        assert view and self.__update_mode, self.__CONFIG_ERROR

        # Set update mode.
        view.setViewportUpdateMode(self.__update_mode)

    def render_hints_config(self, view: QtWidgets.QGraphicsView) -> None:
        """Set the render hints of graphics view.

        Args:
            view (QtWidgets.QGraphicsView): Window used to show scene.
        """

        # For security.
        assert view and self.__render_hints, self.__CONFIG_ERROR

        # Set render hints.
        view.setRenderHints(self.__render_hints)

    def context_menu_policy_config(
        self, view: QtWidgets.QGraphicsView
    ) -> None:
        """Set the context menu policy of graphics view.

        Args:
            view (QtWidgets.QGraphicsView): Window used to show scene.
        """

        # For security.
        assert view and self.__context_menu_policy, self.__CONFIG_ERROR

        # Set render hints.
        view.setContextMenuPolicy(self.__context_menu_policy)

    def attribute_config(
        self, view: QtWidgets.QGraphicsView, target: bool
    ) -> None:
        """Set the context menu policy of graphics view.

        Args:
            view (QtWidgets.QGraphicsView): Window used to show scene.
        """

        # For security.
        assert view and self.__attribute, self.__CONFIG_ERROR

        # Set render hints.
        view.setAttribute(self.__attribute, target)

    def drag_mode_config(self, view: QtWidgets.QGraphicsView) -> None:
        """Set the drag mode of graphics view.

        Args:
            view (QtWidgets.QGraphicsView): Drag mode.
        """

        # For security.
        assert view and self.__drag_mode, self.__CONFIG_ERROR

        # Set drag mode.
        view.setDragMode(self.__drag_mode)

    def set_update_mode(
        self, update_mode: QtWidgets.QGraphicsView.ViewportUpdateMode
    ) -> Self:
        """Set update mode of config.

        Args:
            update_mode (QtWidgets.QGraphicsView.ViewportUpdateMode): Update mode.

        Returns:
            Self: Self.
        """
        self.__update_mode = update_mode
        return self

    def set_render_hints(
        self, render_hints: QtGui.QPainter.RenderHints
    ) -> Self:
        """Set render hints.

        Args:
            render_hints (QtGui.QPainter.RenderHints): Render hints.

        Returns:
            Self: Self.
        """
        self.__render_hints = render_hints
        return self

    def set_context_menu_policy(
        self, context_menu_policy: QtCore.Qt.ContextMenuPolicy
    ) -> Self:
        """Set context menu policy.

        Args:
            context_menu_policy (QtCore.Qt.ContextMenuPolicy): Context menu policy.

        Returns:
            Self: Self.
        """
        self.__context_menu_policy = context_menu_policy
        return self

    def set_attribute(self, attribute: QtCore.Qt.WidgetAttribute) -> Self:
        """Set attribute.

        Args:
            attribute (QtCore.Qt.WidgetAttribute): Window attribute.

        Returns:
            Self: Self.
        """
        self.__attribute = attribute
        return self

    def set_drag_mode(
        self, drag_mode: QtWidgets.QGraphicsView.DragMode
    ) -> Self:
        """Set drag mode.

        Args:
            drag_mode (QtWidgets.QGraphicsView.DragMode): Drag mode.

        Returns:
            Self: Self.
        """
        self.__drag_mode = drag_mode
        return self
