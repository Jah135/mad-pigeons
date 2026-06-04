from __future__ import annotations

from pygame import draw, Surface, Rect, SRCALPHA

from ..udim2 import UDim2
from ..vec2 import Vec2
from ..eventsignal import EventSignal
from ..enums import UIState


class GuiObject:
    """An abstract class for all UI objects"""

    _parent: GuiObject | None
    _anchor_point: Vec2
    _position: UDim2
    _size: UDim2
    _visible: bool
    _clips_descendants: bool = False

    _is_stale: bool
    _rawtexture: Surface

    mouse_state: UIState

    children: set[GuiObject]

    mouse_down: EventSignal
    mouse_up: EventSignal
    mouse_enter: EventSignal
    mouse_leave: EventSignal

    def __init__(
        self,
        parent: GuiObject | None = None,
        *,
        anchor_point: Vec2 = Vec2(),
        position: UDim2 = UDim2(),
        size: UDim2 = UDim2(),
    ) -> None:
        self._parent = None
        self._anchor_point = anchor_point
        self._position = position
        self._size = size
        self._visible = True
        self._is_stale = True

        self.mouse_state = UIState.Idle

        self.children = set()
        self.parent = parent

        # signals
        self.mouse_down = EventSignal()
        self.mouse_up = EventSignal()
        self.mouse_enter = EventSignal()
        self.mouse_leave = EventSignal()


    # properties

    @property
    def parent(self) -> GuiObject | None:
        return self._parent
    
    @parent.setter
    def parent(self, new_parent: GuiObject | None):
        self.invalidate()

        old_parent = self._parent

        if old_parent is not None:
            old_parent.children.remove(self)
            old_parent.invalidate()

        self._parent = new_parent

        if new_parent is not None:
            new_parent.children.add(self)
            new_parent.invalidate()
    
    @property
    def anchor_point(self) -> Vec2:
        return self._anchor_point

    @anchor_point.setter
    def anchor_point(self, new_value: Vec2):
        self._anchor_point = new_value
        self.invalidate()
    
    @property
    def position(self) -> UDim2:
        return self._position
    
    @position.setter
    def position(self, new_value: UDim2):
        self._position = new_value
        self.invalidate()
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, new_value: UDim2):
        self._size = new_value
        self.invalidate()
    
    @property
    def visible(self) -> bool:
        return self._visible
    
    @visible.setter
    def visible(self, new_value: bool):
        self._visible = new_value
        self.invalidate()
    
    @property
    def clips_descendants(self) -> bool:
        return self._clips_descendants
    
    @clips_descendants.setter
    def clips_descendants(self, new_value: bool):
        self._clips_descendants = new_value
        self.invalidate()

    # derived properties
    @property
    def absolute_size(self) -> Vec2:
        """The absolute size of this GuiObject, in pixels as a Vec2."""

        if self._parent == None:
            return self._size.offsets

        return self._size.offsets + self._size.scales * self._parent.absolute_size

    @property
    def absolute_position(self) -> Vec2:
        """The absolute position of this GuiObject, relative to it's oldest ancestor, in pixels as a Vec2."""

        if self._parent == None:
            return self._position.offsets

        return (
            self._parent.absolute_position
            + self._position.offsets
            + self._parent.absolute_size * self._position.scales
        ) - (self.absolute_size * self._anchor_point)

    @property
    def content_bounds(self) -> Rect:
        """The bounds of this GuiObject, including all of it's descendants, relative to it's oldest ancestor."""
        if self._clips_descendants:
            return self.bounds

        top_left = self.absolute_position
        size = self.absolute_size

        for child in self.children:
            if not child._visible:
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

        if self._is_stale:
            self._reconcile()

        return self._rawtexture

    def invalidate(self):
        """
        Marks this Gui object and all of it's ancestors as stale.

        ask me about push-pull based reactive signals
        """

        if self._is_stale:
            return

        self._is_stale = True

        if self._parent is not None:
            self._parent.invalidate()

    def draw_to(self, out: Surface):
        out.blit(self.modern_texture, self.content_bounds)

    def debug_draw_descendants(self, out: Surface):
        draw.rect(out, "red", self.bounds, 1)
        draw.circle(out, "red", self.absolute_position.xy, 2)
        # draw.rect(out, "yellow" if self.is_visible else "black", self.content_bounds, 1)
        draw.circle(out, "yellow", self.content_bounds.topleft, 2)

        for child in self.children:
            child.debug_draw_descendants(out)

    def clear_children(self):
        """Removes all GuiObjects parented directly under this GuiObject."""
        for child in self.children:
            child._parent = None

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
    def _propagate_on_mouse_down(self, x: int, y: int):
        if not self._visible:
            return

        if self.mouse_state == UIState.Hover:
            self.mouse_state = UIState.Press
            self.mouse_down.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propagate_on_mouse_down(x, y)

    def _propagate_on_mouse_up(self, x: int, y: int):
        if not self._visible:
            return

        if self.mouse_state == UIState.Press:
            self.mouse_state = UIState.Hover
            self.mouse_up.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propagate_on_mouse_up(x, y)

    def _propagate_on_mouse_move(self, x: int, y: int):
        if not self._visible:
            return

        if self.check_is_in_bounds(x, y):
            if self.mouse_state == UIState.Idle:
                self.mouse_state = UIState.Hover
                self.mouse_enter.fire(x, y)
        elif self.mouse_state != UIState.Idle:
            self.mouse_state = UIState.Idle
            self.mouse_leave.fire(x, y)

        # propogate to children
        for child in self.children:
            child._propagate_on_mouse_move(x, y)

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
            if not child._visible:
                child._is_stale = False
                continue

            contents_texture.blit(
                child.modern_texture,
                (Vec2(*child.content_bounds.topleft) - full_bounds.topleft).xy,
            )

        self._rawtexture = contents_texture
        self._is_stale = False

    def render(self, render_texture: Surface):
        """
        An abstract method that is overridden by subclasses to generate a Surface for rendering to the screen.
        """
        ...
