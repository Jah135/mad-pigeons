import pygame
import pymunk
from typing import Any, Callable
from pygame import draw, mouse, key

from game import Game
from ui import GuiObject, TextLabel, Frame, ImageLabel, UDim2, Vec2
import objects
import assets


class InventoryItem:
    def __init__(
        self,
        name: str,
        image: pygame.Surface,
        create: Callable[[objects.Level], objects.CorporealEntity],
    ) -> None:
        self.name = name
        self.image = image

        self.create_entity = create


HOTBAR: list[InventoryItem] = [
    InventoryItem(
        "Box",
        assets.STONE_WEDGE_0,
        lambda scope: objects.stone.Wedge(scope),
    ),
    InventoryItem(
        "Ball",
        assets.STONE_BOX_0,
        lambda scope: objects.stone.Box(scope),
    ),
    InventoryItem(
        "Thin Plank",
        assets.STONE_TRIANGLE_0,
        lambda scope: objects.stone.Triangle(scope),
    ),
    InventoryItem(
        "Thick Plank",
        assets.WOOD_PLANK_THICK,
        lambda scope: objects.wood.PlankThick(scope),
    ),
    InventoryItem(
        "Triangle",
        assets.WOOD_TRIANGLE,
        lambda scope: objects.wood.Triangle(scope),
    ),
    InventoryItem(
        "Wedge",
        assets.WOOD_WEDGE,
        lambda scope: objects.wood.Wedge(scope),
    ),
    InventoryItem(
        "Pig",
        assets.BIG_PIG,
        lambda scope: objects.pig.Pig(scope),
    ),
    InventoryItem(
        "TNT",
        assets.TNT,
        lambda scope: objects.special.TNT(scope),
    ),
]
HOTBAR_SLOT_SIZE = 70


def point_in_body(point: tuple[float, float], body: pymunk.Body):
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True


class TheGame(Game):
    window_width = 1000
    window_height = 564
    title = "Mad Pigeons™ (not angry birds)"
    icon = assets.RED_BIRD

    def setup(self):
        test_level = objects.Level()

        floor_segment = pymunk.Segment(
            test_level.space.static_body,
            (-1e4, self.window_height * 0.9 + 70),
            (1e4, self.window_height * 0.9 + 70),
            90,
        )
        floor_segment.friction = 0.6
        floor_segment.elasticity = 0.4

        test_level.space.add(floor_segment)

        self.current_level = test_level
        self.current_dragging_entity: objects.CorporealEntity | None = None

        self.background_image = pygame.transform.scale(
            assets.BACKGROUND_1,
            (self.window_width, self.window_height),
        )

    def setup_ui(self):
        screen_ui_container = GuiObject(
            size=UDim2(x_offset=self.window_width, y_offset=self.window_height)
        )
        self.screen_ui_container = screen_ui_container

        # setup hotbar
        hotbar_count = len(HOTBAR)
        hotbar_container = GuiObject(
            screen_ui_container,
            size=UDim2(0, 0.6, HOTBAR_SLOT_SIZE, 0),
            position=UDim2(0, 0.5, -5, 1),
            anchor_point=Vec2(0.5, 1),
        )

        for index, item in enumerate(HOTBAR):
            frame = Frame(
                hotbar_container,
                Vec2(index / (hotbar_count - 1), 0),
                UDim2(x_scale=index / (hotbar_count - 1)),
                UDim2(x_offset=HOTBAR_SLOT_SIZE, y_offset=HOTBAR_SLOT_SIZE),
            )
            frame.color = (0, 0, 0, 80)
            frame.invalidate()

            ImageLabel(
                frame,
                Vec2(0.5, 0.5),
                UDim2(x_scale=0.5, y_scale=0.5),
                UDim2(x_scale=0.9, y_scale=0.9),
                image=item.image,
            )

            name_label = TextLabel(
                frame,
                Vec2(0, 1),
                size=UDim2(0, 1, 20, 0),
                text=item.name,
                text_color=(0, 0, 0, 255),
            )
            name_label.visible = False

            def on_mouse_down(*_, item=item):
                new_entity = item.create_entity(self.current_level)
                new_entity.body.position = mouse.get_pos()
                self.current_dragging_entity = new_entity

            def on_mouse_enter(*_, name_label=name_label):
                name_label.visible = True
                name_label.invalidate()

            def on_mouse_leave(*_, name_label=name_label):
                name_label.visible = False
                name_label.invalidate()

            frame.mouse_down.connect(on_mouse_down)
            frame.mouse_enter.connect(on_mouse_enter)
            frame.mouse_leave.connect(on_mouse_leave)

        self.screen_ui_container.invalidate()

    def on_update(self, dt: float):
        entity = self.current_dragging_entity

        if entity != None:
            keys = key.get_pressed()

            rotate_sign = (-1 if keys[pygame.K_q] else 0) + (
                1 if keys[pygame.K_e] else 0
            )

            body = entity.body
            body.position = mouse.get_pos()
            body.velocity = (0, 0)
            body.angular_velocity = 0
            body.angle += dt * rotate_sign * 3.14

            # apparently this fixes the problem where dragging while paused wouldnt actually update the position of the shape
            # yay
            self.current_level.space.reindex_shapes_for_body(body)

        self.current_level.update(dt)
        self.current_level.update_physics(dt)

    def on_draw_scene(self, out: pygame.Surface):
        out.blit(self.background_image)

        self.current_level.display(out)

    def on_draw_interface(self, out: pygame.Surface):
        # NOAH TEST ASSETS HERE
        out.blit(assets.LARGE_WOOD_BALL_0, (100, 100))

        self.screen_ui_container.draw_to(out)

    def on_mouse_left_down(self, pos: tuple[int, int]):
        for entity in self.current_level.entities:
            if not isinstance(entity, objects.CorporealEntity):
                continue

            if point_in_body(pos, entity.body):
                self.current_dragging_entity = entity
                break

    #     self.screen_ui_container._propogate_on_mouse_down(*pos)

    # def on_mouse_left_up(self, pos: tuple[int, int]):
    #     self.screen_ui_container._propogate_on_mouse_up(*pos)

    #     if self.current_dragging_entity != None:
    #         delta_x = pos[0] - self._last_mouse_pos[0]
    #         delta_y = pos[1] - self._last_mouse_pos[1]

            self.current_dragging_entity.body.position = pos
            self.current_dragging_entity.body.velocity += (delta_x * 20, delta_y * 20)
            self.current_dragging_entity = None

    def on_mouse_move(self, pos: tuple[int, int]):
        self.screen_ui_container._propogate_on_mouse_move(*pos)


game = TheGame()
game.start()
