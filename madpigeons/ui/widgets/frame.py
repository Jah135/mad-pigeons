from pygame import draw, Surface

from .guiobject import GuiObject
from ..color import Color
from ..vec2 import Vec2
from ..udim2 import UDim2


class Frame(GuiObject):
    """A basic rectangular frame."""

    color: Color
    border_color: Color
    border_thickness: int
    roundness: int

    def __init__(
        self,
        parent: GuiObject | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        color: Color = Color(255, 255, 255, 255),
        border_color: Color = Color(0, 0, 0, 0),
        border_thickness: int = 0,
        roundness: int = 0,
    ) -> None:
        self.color = color
        self.border_color = border_color
        self.border_thickness = border_thickness
        self.roundness = roundness

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        # render_texture.fill(self.color.rgba)
        draw.rect(
            render_texture,
            self.color.rgba,
            (0, 0, *self.absolute_size.xy),
            0,
            self.roundness,
            self.roundness,
            self.roundness,
            self.roundness,
        )

        if self.border_color.a > 0 and self.border_thickness > 0:
            draw.rect(
                render_texture,
                self.border_color.rgba,
                (0, 0, *self.absolute_size.xy),
                self.border_thickness,
                self.roundness,
                self.roundness,
                self.roundness,
                self.roundness,
            )
