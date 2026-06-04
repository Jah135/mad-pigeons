from pygame import font, Surface

from .guiobject import GuiObject
from .. import enums
from ..color import Color
from ..vec2 import Vec2
from ..udim2 import UDim2

font.init()

DEFAULT_FONT = font.Font(None, 16)


class TextLabel(GuiObject):
    """A label for displaying text maybe"""

    _text: str
    _text_color: Color
    _text_font: font.Font

    _text_x_alignment: enums.HorizontalAlignment
    _text_y_alignment: enums.VerticalAlignment

    _text_outline_color: Color
    _text_outline_thickness: int

    def __init__(
        self,
        parent: GuiObject | None = None,
        *,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        text: str = "Label",
        text_color: Color = Color(0, 0, 0, 255),
        text_font: font.Font = DEFAULT_FONT,
        text_x_alignment: enums.HorizontalAlignment = enums.HorizontalAlignment.Center,
        text_y_alignment: enums.VerticalAlignment = enums.VerticalAlignment.Center,
        text_outline_color: Color = Color(0, 0, 0, 0),
        text_outline_thickness: int = 1,
    ) -> None:
        self._text = text
        self._text_color = text_color
        self._text_x_alignment = text_x_alignment
        self._text_y_alignment = text_y_alignment
        self._text_outline_color = text_outline_color
        self._text_outline_thickness = text_outline_thickness
        self._text_font = text_font

        super().__init__(parent, anchor_point=anchor_point, position=position, size=size)

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_value: str):
        self._text = new_value
        self.invalidate()
    
    @property
    def text_color(self) -> Color:
        return self._text_color
    
    @text_color.setter
    def text_color(self, new_value: Color):
        self._text_color = new_value
        self.invalidate()
    
    @property
    def text_font(self) -> font.Font:
        return self._text_font
    
    @text_font.setter
    def text_font(self, new_value: font.Font):
        self._text_font = new_value
        self.invalidate()
    
    @property
    def text_x_alignment(self) -> enums.HorizontalAlignment:
        return self._text_x_alignment
    
    @text_x_alignment.setter
    def text_x_alignment(self, new_value: enums.HorizontalAlignment):
        self._text_x_alignment = new_value
        self.invalidate()
    
    @property
    def text_y_alignment(self) -> enums.VerticalAlignment:
        return self._text_y_alignment
    
    @text_y_alignment.setter
    def text_y_alignment(self, new_value: enums.VerticalAlignment):
        self._text_y_alignment = new_value
        self.invalidate()
    
    @property
    def text_outline_color(self) -> Color:
        return self._text_outline_color
    
    @text_outline_color.setter
    def text_outline_color(self, new_value: Color):
        self._text_outline_color = new_value
        self.invalidate()
    
    @property
    def text_outline_thickness(self) -> int:
        return self._text_outline_thickness
    
    @text_outline_thickness.setter
    def text_outline_thickness(self, new_value: int):
        self._text_outline_thickness = new_value
        self.invalidate()
    

    def render(self, render_texture: Surface):
        text_surface = self._text_font.render(self._text, True, self._text_color.rgb)

        total_width, total_height = self.absolute_size.xy

        blit_x = 0
        blit_y = 0

        match self._text_x_alignment:
            case enums.HorizontalAlignment.Center:
                blit_x = total_width // 2 - (text_surface.width // 2)
            case enums.HorizontalAlignment.Right:
                blit_x = total_height - text_surface.height

        match self._text_y_alignment:
            case enums.VerticalAlignment.Center:
                blit_y = total_height / 2 - text_surface.height / 2
            case enums.VerticalAlignment.Bottom:
                blit_y = total_height - text_surface.height

        if self._text_outline_color.a != 0 and self._text_outline_thickness > 0:
            thickness = self._text_outline_thickness

            outline_surface = self._text_font.render(
                self._text, True, self._text_outline_color.rgb
            )

            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx == 0 and dy == 0:
                        continue
                    render_texture.blit(outline_surface, (blit_x + dx, blit_y + dy))

        render_texture.blit(text_surface, (blit_x, blit_y))
