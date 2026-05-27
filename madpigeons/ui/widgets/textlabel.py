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

    text: str
    text_size: int
    text_color: Color
    text_font: font.Font

    text_x_alignment: enums.HorizontalAlignment
    text_y_alignment: enums.VerticalAlignment

    text_outline_color: Color
    text_outline_thickness: int

    def __init__(
        self,
        parent: GuiObject | None = None,
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
        self.text = text
        self.text_color = text_color
        self.text_x_alignment = text_x_alignment
        self.text_y_alignment = text_y_alignment
        self.text_outline_color = text_outline_color
        self.text_outline_thickness = text_outline_thickness
        self.font = text_font

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        text_surface = self.font.render(self.text, True, self.text_color.rgb)

        total_width, total_height = self.absolute_size.xy

        blit_x = 0
        blit_y = 0

        match self.text_x_alignment:
            case enums.HorizontalAlignment.Center:
                blit_x = total_width // 2 - (text_surface.width // 2)
            case enums.HorizontalAlignment.Right:
                blit_x = total_height - text_surface.height

        match self.text_y_alignment:
            case enums.VerticalAlignment.Center:
                blit_y = total_height / 2 - text_surface.height / 2
            case enums.VerticalAlignment.Bottom:
                blit_y = total_height - text_surface.height

        if self.text_outline_color.a != 0 and self.text_outline_thickness > 0:
            thickness = self.text_outline_thickness

            outline_surface = self.font.render(
                self.text, True, self.text_outline_color.rgb
            )

            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx == 0 and dy == 0:
                        continue
                    render_texture.blit(outline_surface, (blit_x + dx, blit_y + dy))

        render_texture.blit(text_surface, (blit_x, blit_y))
