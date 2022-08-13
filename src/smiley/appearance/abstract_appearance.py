from abc import ABC

from ..constant.enum.appearance.level import AppearanceLevel


class AbstractAppearance(ABC):
    def __init__(self) -> None:
        super().__init__()

        # Different levels for different situations.
        self.__level = AppearanceLevel(AppearanceLevel.Level)

        # Appearance settings.

    def set_level(self, level):
        self.__level = level
        return self

    def get_level(self):
        return self.__level
