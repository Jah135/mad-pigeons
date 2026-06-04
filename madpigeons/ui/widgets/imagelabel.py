from pygame import transform, Surface

from .guiobject import GuiObject
from ..vec2 import Vec2
from ..udim2 import UDim2


class ImageLabel(GuiObject):
    """A label for displaying images maybe"""

    _display_image: Surface

    def __init__(
        self,
        parent: GuiObject | None = None,
        *,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        image: Surface = Surface((1, 1)),
    ) -> None:
        self._display_image = image

        super().__init__(parent, anchor_point=anchor_point, position=position, size=size)

    @property
    def image(self) -> Surface:
        return self._display_image
    
    @image.setter
    def image(self, new_image: Surface):
        self._display_image = new_image
        self.invalidate()

    def render(self, render_texture: Surface):
        # using smoothscale here, as point resampling looks kinda horrible on images with alpha
        scaled_image = transform.smoothscale_by(
            self._display_image, min(self.absolute_size.xy) / max(self._display_image.size)
        )
        render_texture.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).xy
        )