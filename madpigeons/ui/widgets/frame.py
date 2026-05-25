from pygame import Surface

from .guiobject import GuiObject
from ..color import Color
from ..vec2 import Vec2
from ..udim2 import UDim2


class Frame(GuiObject):
    """A basic rectangular frame."""

    color: Color

    def __init__(
        self,
        parent: GuiObject | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
    ) -> None:
        self.color = Color(255, 255, 255, 255)

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        render_texture.fill(self.color.rgba)

    def set_color(self, new_color: Color):
        self.color = new_color
        self.invalidate()
