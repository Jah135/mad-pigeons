from pygame import draw, font, transform, Surface, Rect, SRCALPHA

from .vec2 import Vec2
from .udim2 import UDim2
from .enums import UIState, HorizontalAlignment, VerticalAlignment
from .eventsignal import EventSignal

Color = tuple[int, int, int, int]


class GuiObject:
    """An abstract class for all UI objects"""

    parent: "GuiObject | None"
    children: set["GuiObject"]

    anchor_point: Vec2
    position: UDim2
    size: UDim2
    visible: bool

    is_stale: bool
    texture: Surface

    def __init__(
        self,
        parent: "GuiObject | None" = None,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
    ) -> None:
        self.parent = None
        self.children = set()

        self.anchor_point = anchor_point
        self.position = position
        self.size = size
        self.visible = True

        self.state = UIState.Idle
        self.is_stale = True

        # signals
        self.mouse_down = EventSignal()
        self.mouse_up = EventSignal()
        self.mouse_enter = EventSignal()
        self.mouse_leave = EventSignal()

        self.set_parent(parent)

    @property
    def absolute_size(self) -> Vec2:
        """The absolute size of this GuiObject, in pixels as a Vec2."""

        if self.parent == None:
            return self.size.offsets

        return self.size.offsets + self.size.scales * self.parent.absolute_size

    @property
    def absolute_position(self) -> Vec2:
        """The absolute position of this GuiObject, relative to it's oldest ancestor, in pixels as a Vec2."""

        if self.parent == None:
            return self.position.offsets

        return (
            self.parent.absolute_position
            + self.position.offsets
            + self.parent.absolute_size * self.position.scales
        ) - (self.absolute_size * self.anchor_point)

    @property
    def relative_position(self) -> Vec2:
        """The relative position of this GuiObject to it's parent, in pixels as a Vec2."""

        if self.parent == None:
            return self.position.offsets

        return self.absolute_position - self.parent.absolute_position

    @property
    def content_bounds(self) -> Rect:
        """The bounds of this GuiObject, including all of it's descendants, relative to it's oldest ancestor."""

        top_left = self.absolute_position
        size = self.absolute_size

        for child in self.children:
            child_bounds = child.content_bounds
            child_topleft = Vec2(*child_bounds.topleft)
            child_dimensions = Vec2(*child_bounds.size)

            top_left = top_left.min(child_topleft)
            size = size.max((child_topleft - self.absolute_position) + child_dimensions)

        return Rect(top_left.tup, (size + (self.absolute_position - top_left)).tup)

    @property
    def bounds(self) -> Rect:
        """The bounds of this GuiObject, relative to it's oldest ancestor."""

        return Rect(self.absolute_position.tup, self.absolute_size.tup)

    @property
    def modern_texture(self) -> Surface:
        """Guaranteed to be the most up to date texture for rendering."""

        if self.is_stale:
            self._reconcile()

        return self.texture

    # actual methods you might be using
    def draw_to(self, out: Surface):
        out.blit(self.modern_texture, self.content_bounds)

    def debug_draw_descendants(self, out: Surface):
        draw.rect(out, "blue", self.bounds, 2)
        draw.rect(out, "yellow", self.content_bounds, 2)
        draw.circle(out, "blue", self.absolute_position.tup, 4)

        for child in self.children:
            child.debug_draw_descendants(out)

    def set_parent(self, new_parent: "GuiObject | None"):
        """Sets the parent of this GuiObject."""

        self.invalidate()

        current_parent = self.parent

        if current_parent != None:
            current_parent.children.remove(self)

        self.parent = new_parent

        if new_parent != None:
            new_parent.children.add(self)

    def check_is_in_bounds(self, x: int, y: int) -> bool:
        """Returns whether the specified point is within the bounds of this GuiObject."""

        top_left = self.absolute_position
        size = self.absolute_size

        return (
            x > top_left.x
            and x < top_left.x + size.x
            and y > top_left.y
            and y < top_left.y + size.y
        )

    # event entry points
    def _propogate_on_mouse_down(self, x: int, y: int):
        if self.state == UIState.Hover:
            self.state = UIState.Press
            self.mouse_down.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propogate_on_mouse_down(x, y)

    def _propogate_on_mouse_up(self, x: int, y: int):
        if self.state == UIState.Press:
            self.state = UIState.Hover
            self.mouse_up.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propogate_on_mouse_up(x, y)

    def _propogate_on_mouse_move(self, x: int, y: int):
        if self.check_is_in_bounds(x, y):
            if self.state == UIState.Idle:
                self.state = UIState.Hover
                self.mouse_enter.fire(x, y)
        elif self.state != UIState.Idle:
            self.state = UIState.Idle
            self.mouse_leave.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propogate_on_mouse_move(x, y)

    # rendering stuff
    def invalidate(self):
        """
        Marks this Gui object and all of it's ancestors as stale.

        ask me about push-pull based reactive signals
        """

        if self.is_stale:
            return

        self.is_stale = True

        if self.parent != None:
            self.parent.invalidate()

    def _reconcile(self):
        full_bounds = self.content_bounds

        contents_texture = Surface(full_bounds.size, SRCALPHA)
        render_texture = Surface(self.absolute_size.tup, SRCALPHA)

        self.render(render_texture)

        contents_texture.blit(
            render_texture, (self.absolute_position - full_bounds.topleft).tup
        )

        for child in self.children:
            if not child.visible:
                child.is_stale = False
                continue

            contents_texture.blit(
                child.modern_texture,
                (Vec2(*child.content_bounds.topleft) - full_bounds.topleft).tup,
            )

        self.texture = contents_texture
        self.is_stale = False

    def render(self, render_texture: Surface):
        """
        An abstract method that is overridden by subclasses to generate a Surface for rendering to the screen.
        """
        ...


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
        self.color = (255, 255, 255, 255)

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        render_texture.fill(self.color)

    def set_color(self, new_color: Color):
        self.color = new_color
        self.invalidate()


class TextLabel(GuiObject):
    """A label for displaying text maybe"""

    text: str
    text_size: int
    text_color: Color
    text_font: str | None

    text_x_alignment: HorizontalAlignment
    text_y_alignment: VerticalAlignment

    text_outline_color: Color
    text_outline_thickness: int

    def __init__(
        self,
        parent: GuiObject | None = None,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
        text: str = "Label",
        text_size: int = 16,
        text_color: Color = (0, 0, 0, 255),
        text_font: str | None = None,
        text_x_alignment: HorizontalAlignment = HorizontalAlignment.Center,
        text_y_alignment: VerticalAlignment = VerticalAlignment.Center,
        text_outline_color: Color = (0, 0, 0, 0),
        text_outline_thickness: int = 1,
    ) -> None:
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_x_alignment = text_x_alignment
        self.text_y_alignment = text_y_alignment
        self.text_outline_color = text_outline_color
        self.text_outline_thickness = text_outline_thickness

        self._font = font.Font(text_font, self.text_size)

        super().__init__(parent, anchor_point, position, size)

    def render(self, render_texture: Surface):
        text_surface = self._font.render(self.text, True, self.text_color)

        total_width, total_height = self.absolute_size.tup

        blit_x = 0
        blit_y = 0

        match self.text_x_alignment:
            case HorizontalAlignment.Center:
                blit_x = total_width // 2 - (text_surface.width // 2)
            case HorizontalAlignment.Right:
                blit_x = total_height - text_surface.height

        match self.text_y_alignment:
            case VerticalAlignment.Center:
                blit_y = total_height / 2 - text_surface.height / 2
            case VerticalAlignment.Bottom:
                blit_y = total_height - text_surface.height

        if self.text_outline_color[3] != 0 and self.text_outline_thickness > 0:
            thickness = self.text_outline_thickness

            outline_surface = self._font.render(
                self.text, True, self.text_outline_color
            )

            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx == 0 and dy == 0:
                        continue
                    render_texture.blit(outline_surface, (blit_x + dx, blit_y + dy))

        render_texture.blit(text_surface, (blit_x, blit_y))


class ImageLabel(GuiObject):
    """A label for displaying images maybe"""

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
        scaled_image = transform.scale_by(
            self.image, min(self.absolute_size.tup) / max(self.image.size)
        )
        render_texture.blit(
            scaled_image, ((self.absolute_size / 2) - Vec2(*scaled_image.size) / 2).tup
        )

    def set_image(self, new_image: Surface):
        self.image = new_image
        self.invalidate()
