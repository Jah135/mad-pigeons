from pygame import transform, Surface

from .guiobject import GuiObject
from ..vec2 import Vec2
from ..udim2 import UDim2


class ImageLabel(GuiObject):
    """A label for displaying images maybe"""

    image: Surface

    def __init__(
        self,
        parent: GuiObject | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        image: Surface = Surface((1, 1)),
    ) -> None:
        self.image = image

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        # using smoothscale here, as point resampling looks kinda horrible on images with alpha
        scaled_image = transform.smoothscale_by(
            self.image, min(self.absolute_size.xy) / max(self.image.size)
        )
        render_texture.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).xy
        )

    def set_image(self, new_image: Surface):
        self.image = new_image
        self.invalidate()
