from __future__ import annotations

from pygame import draw, Surface, Rect, SRCALPHA

from ..udim2 import UDim2
from ..vec2 import Vec2
from ..eventsignal import EventSignal
from ..enums import UIState


class GuiObject:
    """An abstract class for all UI objects"""

    parent: "GuiObject | None"
    children: set["GuiObject"]

    anchor_point: Vec2
    position: UDim2
    size: UDim2
    visible: bool
    clips_descendants: bool = False

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
        if self.clips_descendants:
            return self.bounds

        top_left = self.absolute_position
        size = self.absolute_size

        for child in self.children:
            if not child.visible:
                continue

            child_bounds = child.content_bounds
            child_topleft = Vec2(*child_bounds.topleft)
            child_dimensions = Vec2(*child_bounds.size)

            top_left = top_left.min(child_topleft)
            size = size.max((child_topleft - self.absolute_position) + child_dimensions)

        return Rect(top_left.xy, (size + (self.absolute_position - top_left)).xy)

    @property
    def bounds(self) -> Rect:
        """The bounds of this GuiObject, relative to it's oldest ancestor."""

        return Rect(self.absolute_position.xy, self.absolute_size.xy)

    @property
    def modern_texture(self) -> Surface:
        """Guaranteed to be the most up to date texture for rendering."""

        if self.is_stale:
            self._reconcile()

        return self.texture

    @property
    def is_visible(self) -> bool:
        """Returns whether this GuiObject is visible, based off of whether it's ancestor's are visible."""

        if not self.visible:
            return False

        for ancestor in self.get_ancestors():
            if not ancestor.visible:
                return False

        return True

    # actual methods you might be using
    def get_ancestors(self) -> list[GuiObject]:
        ancestors = []
        current = self

        while True:
            current = current.parent

            if current is None:
                break
            ancestors.append(current)

        return ancestors

    def invalidate(self):
        """
        Marks this Gui object and all of it's ancestors as stale.

        ask me about push-pull based reactive signals
        """

        if self.is_stale:
            return

        self.is_stale = True

        if self.parent is not None:
            self.parent.invalidate()

    def invalidate_parent(self):
        """
        Marks this GuiObject's parent as stale.
        """
        if self.parent is not None:
            self.parent.invalidate()

    def draw_to(self, out: Surface):
        out.blit(self.modern_texture, self.content_bounds)

    def debug_draw_descendants(self, out: Surface):
        draw.rect(out, "red", self.bounds, 1)
        draw.circle(out, "red", self.absolute_position.xy, 2)
        draw.rect(out, "yellow" if self.is_visible else "black", self.content_bounds, 1)
        draw.circle(out, "yellow", self.content_bounds.topleft, 2)

        for child in self.children:
            child.debug_draw_descendants(out)

    def set_parent(self, new_parent: "GuiObject | None"):
        """Sets the parent of this GuiObject."""

        self.invalidate()

        current_parent = self.parent

        if current_parent is not None:
            current_parent.children.remove(self)

        self.parent = new_parent

        if new_parent is not None:
            new_parent.children.add(self)

    def clear_children(self):
        """Removes all GuiObjects parented directly under this GuiObject."""
        for child in self.children:
            child.parent = None

        self.children.clear()
        self.invalidate()

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
        if not self.visible:
            return

        if self.state == UIState.Hover:
            self.state = UIState.Press
            self.mouse_down.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propogate_on_mouse_down(x, y)

    def _propogate_on_mouse_up(self, x: int, y: int):
        if not self.visible:
            return

        if self.state == UIState.Press:
            self.state = UIState.Hover
            self.mouse_up.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propogate_on_mouse_up(x, y)

    def _propogate_on_mouse_move(self, x: int, y: int):
        if not self.visible:
            return

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
    def _reconcile(self):
        full_bounds = self.content_bounds

        contents_texture = Surface(full_bounds.size, SRCALPHA)
        render_texture = Surface(self.absolute_size.xy, SRCALPHA)

        self.render(render_texture)

        contents_texture.blit(
            render_texture, (self.absolute_position - full_bounds.topleft).xy
        )

        for child in self.children:
            if not child.visible:
                child.is_stale = False
                continue

            contents_texture.blit(
                child.modern_texture,
                (Vec2(*child.content_bounds.topleft) - full_bounds.topleft).xy,
            )

        self.texture = contents_texture
        self.is_stale = False

    def render(self, render_texture: Surface):
        """
        An abstract method that is overridden by subclasses to generate a Surface for rendering to the screen.
        """
        ...
