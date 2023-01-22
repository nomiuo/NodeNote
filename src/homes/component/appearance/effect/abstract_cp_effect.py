"""Base component effect.
"""

from homes.component.appearance.effect.item_effect.abstract_item_effect import (
    AbstractItemEffect,
)
from homes.component.appearance.effect.mouse_effect.abstract_mouse_effect import (
    AbstractMouseEffect,
)


class AbstractCpEffect(AbstractMouseEffect, AbstractItemEffect):
    """Basic component effect.

    Args:
        AbstractMouseEffect (class): Mouse effect.
        AbstractItemEffect (class): Item effect.
    """
