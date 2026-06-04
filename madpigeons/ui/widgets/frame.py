from pygame import draw, Surface

from .guiobject import GuiObject
from ..color import Color
from ..vec2 import Vec2
from ..udim2 import UDim2


class Frame(GuiObject):
    """A basic rectangular frame."""

    _background_color: Color
    _border_color: Color
    _border_thickness: int
    _roundness: int

    def __init__(
        self,
        parent: GuiObject | None = None,
        *,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        color: Color = Color(255, 255, 255, 255),
        border_color: Color = Color(0, 0, 0, 0),
        border_thickness: int = 0,
        roundness: int = 0,
    ) -> None:
        self._background_color = color
        self._border_color = border_color
        self._border_thickness = border_thickness
        self._roundness = roundness

        super().__init__(parent, anchor_point=anchor_point, position=position, size=size)

    @property
    def background_color(self) -> Color:
        return self._background_color
    
    @background_color.setter
    def background_color(self, new_value: Color):
        self._background_color = new_value
        self.invalidate()
    
    @property
    def border_color(self) -> Color:
        return self._border_color
    
    @border_color.setter
    def border_color(self, new_value: Color):
        self._border_color = new_value
        self.invalidate()
    
    @property
    def border_thickness(self) -> int:
        return self._border_thickness
    
    @border_thickness.setter
    def border_thickness(self, new_value: int):
        self._border_thickness = new_value
        self.invalidate()
    
    @property
    def roundness(self) -> int:
        return self._roundness
    
    @roundness.setter
    def roundness(self, new_value: int):
        self._roundness = new_value
        self.invalidate()

    def render(self, render_texture: Surface):
        # render_texture.fill(self.color.rgba)
        draw.rect(
            render_texture,
            self._background_color.rgba,
            (0, 0, *self.absolute_size.xy),
            0,
            self._roundness,
            self._roundness,
            self._roundness,
            self._roundness,
        )

        if self._border_color.a > 0 and self._border_thickness > 0:
            draw.rect(
                render_texture,
                self._border_color.rgba,
                (0, 0, *self.absolute_size.xy),
                self._border_thickness,
                self._roundness,
                self._roundness,
                self._roundness,
                self._roundness,
            )
