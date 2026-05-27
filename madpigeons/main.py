import pygame
import pymunk
from enum import Enum
from typing import Callable
from pygame import mouse, key, transform

from game import Game
from ui import GuiObject, TextLabel, Frame, ImageLabel, UDim2, Vec2, Color
import objects
import assets

WINDOW_DIMENSIONS = (1000, 564)

BACKGROUND_IMAGE = transform.smoothscale(assets.BACKGROUND_3, WINDOW_DIMENSIONS)


class GameMode(Enum):
    Edit = "Edit"
    Play = "Play"


class InventoryItem:
    name: str
    image: pygame.Surface
    create: Callable[[objects.Level], objects.CorporealEntity]

    def __init__(
        self,
        name: str,
        image: pygame.Surface,
        create: Callable[[objects.Level], objects.CorporealEntity],
    ) -> None:
        self.name = name
        self.display_image = image
        self.create_entity = create


HOTBARS = {
    "Wood": [
        InventoryItem("Wood Box", assets.WOOD_BOX_0, objects.wood.Box),
        InventoryItem("Wood Wedge", assets.WOOD_WEDGE_0, objects.wood.Wedge),
        InventoryItem(
            "Large Wood Plank", assets.LARGE_WOOD_PLANK_0, objects.wood.LargePlank
        ),
        InventoryItem("Wood Triangle", assets.WOOD_TRIANGLE_0, objects.wood.Triangle),
        InventoryItem("Wood Slab", assets.WOOD_SLAB_0, objects.wood.Slab),
        InventoryItem(
            "Large Wood Ball", assets.LARGE_WOOD_BALL_0, objects.wood.LargeBall
        ),
        InventoryItem(
            "Small Wood Ball", assets.SMALL_WOOD_BALL_0, objects.wood.SmallBall
        ),
    ],
    "Stone": [
        InventoryItem("Stone Box", assets.STONE_BOX_0, objects.stone.Box),
        InventoryItem("Stone Wedge", assets.STONE_WEDGE_0, objects.stone.Wedge),
        InventoryItem(
            "Large Stone Plank", assets.LARGE_STONE_PLANK_0, objects.stone.LargePlank
        ),
        InventoryItem(
            "Stone Triangle", assets.STONE_TRIANGLE_0, objects.stone.Triangle
        ),
        InventoryItem("Stone Slab", assets.STONE_SLAB_0, objects.stone.Slab),
        InventoryItem(
            "Large Stone Ball", assets.LARGE_STONE_BALL_0, objects.stone.LargeBall
        ),
        InventoryItem(
            "Small Stone Ball", assets.SMALL_STONE_BALL_0, objects.stone.SmallBall
        ),
    ],
    "Glass": [
        InventoryItem("Glass Box", assets.GLASS_BOX_0, objects.glass.Box),
        InventoryItem("Glass Wedge", assets.GLASS_WEDGE_0, objects.glass.Wedge),
        InventoryItem(
            "Large Glass Plank", assets.LARGE_GLASS_PLANK_0, objects.glass.LargePlank
        ),
        InventoryItem(
            "Glass Triangle", assets.GLASS_TRIANGLE_0, objects.glass.Triangle
        ),
        InventoryItem("Glass Slab", assets.GLASS_SLAB_0, objects.glass.Slab),
        InventoryItem(
            "Large Glass Ball", assets.LARGE_GLASS_BALL_0, objects.glass.LargeBall
        ),
        InventoryItem(
            "Small Glass Ball", assets.SMALL_GLASS_BALL_0, objects.glass.SmallBall
        ),
    ],
    "Pigs": [
        InventoryItem("Regular Pig", assets.MEDIUM_PIG, objects.pig.MinionPig),
        InventoryItem("Foreman Pig", assets.FOREMAN_PIG, objects.pig.ForemanPig),
        InventoryItem("Corporal Pig", assets.CORPORAL_PIG, objects.pig.CorporalPig),
        InventoryItem("King Pig", assets.KING_PIG, objects.pig.KingPig),
    ],
}
HOTBAR_SLOT_SIZE = 60
HOTBAR_SLOT_PADDING = 5


def point_in_body(point: tuple[float, float], body: pymunk.Body):
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True


class TheGame(Game):
    window_width = WINDOW_DIMENSIONS[0]
    window_height = WINDOW_DIMENSIONS[1]
    title = "Mad Pigeons™"
    icon = assets.RED_BIRD

    remaining_birds: list[objects.bird.Bird]

    mouse_down_start: tuple[int, int] | None = None

    edit_snapshot: list[objects.EntitySnapshot]
    current_mode: GameMode
    current_hotbar: str = ""

    def set_mode(self, new_mode: GameMode):
        if new_mode == GameMode.Play:
            self.edit_snapshot = self.current_level.take_snapshot()

            self.remaining_birds = [
                objects.bird.BirdRed(self.current_level),
                objects.bird.BirdRed(self.current_level),
                objects.bird.BirdRed(self.current_level),
            ]

            self.current_dragging_entity = None
            self.hotbar_container.visible = False
            self.hotbar_container.invalidate()
            self.mode_button.set_image(assets.EDIT_BUTTON)
        elif new_mode == GameMode.Edit:
            self.current_level.load_snapshot(self.edit_snapshot)

            self.hotbar_container.visible = True
            self.hotbar_container.invalidate()
            self.mode_button.set_image(assets.PLAY_BUTTON)

        self.current_mode = new_mode

    def set_hotbar(self, new_hotbar: str):
        if self.current_hotbar == new_hotbar:
            return

        self.current_hotbar = new_hotbar

        hotbar_items = HOTBARS.get(new_hotbar, [])
        num_items = len(hotbar_items)

        self.hotbar_container.size = UDim2(
            x_offset=num_items * (HOTBAR_SLOT_SIZE + HOTBAR_SLOT_PADDING)
            - HOTBAR_SLOT_PADDING,
            y_offset=HOTBAR_SLOT_SIZE,
        )
        self.hotbar_container.clear_children()

        for index, item in enumerate(hotbar_items):
            item_container = GuiObject(
                self.hotbar_container,
                position=UDim2(
                    index * (HOTBAR_SLOT_SIZE + HOTBAR_SLOT_PADDING), 0, 0, 0
                ),
                size=UDim2(HOTBAR_SLOT_SIZE, 0, HOTBAR_SLOT_SIZE, 0),
            )
            background_frame = Frame(
                item_container,
                anchor_point=Vec2(0.5, 0.5),
                position=UDim2(0, 0.5, 0, 0.5),
                size=UDim2(0, 0.9, 0, 0.9),
                color=Color(20, 20, 30, 80),
                border_color=Color(0, 0, 0, 127),
                border_thickness=2,
                roundness=8,
            )
            ImageLabel(
                background_frame,
                anchor_point=Vec2(0.5, 0.5),
                position=UDim2(0, 0.5, 0, 0.5),
                size=UDim2(-8, 1, -8, 1),
                image=item.display_image,
            )
            hover_name_label = TextLabel(
                background_frame,
                anchor_point=Vec2(0.5, 0),
                position=UDim2(0, 0.5, 10, 1),
                size=UDim2(0, 2, 16, 0),
                text=item.name,
            )
            hover_name_label.visible = False

            def mouse_enter(*_, label=hover_name_label):
                label.visible = True
                label.invalidate()

            def mouse_leave(*_, label=hover_name_label):
                label.visible = False
                label.invalidate()

            def mouse_down(*_, item=item):
                new_entity = item.create_entity(self.current_level)
                self.current_dragging_entity = new_entity

            background_frame.mouse_down.connect(mouse_down)
            background_frame.mouse_enter.connect(mouse_enter)
            background_frame.mouse_leave.connect(mouse_leave)

    def setup(self):
        main_level = objects.Level()

        self.current_mode = GameMode.Edit

        floor_segment = pymunk.Segment(
            main_level.space.static_body,
            (-1e4, self.window_height * 0.9 + 130),
            (1e4, self.window_height * 0.9 + 130),
            90,
        )
        floor_segment.friction = 0.6
        floor_segment.elasticity = 0.4

        main_level.space.add(floor_segment)

        self.current_level = main_level
        self.current_dragging_entity: objects.CorporealEntity | None = None

        self.setup_ui()

    def setup_ui(self):
        screen_ui_container = GuiObject(
            size=UDim2(x_offset=self.window_width, y_offset=self.window_height)
        )
        self.screen_ui_container = screen_ui_container

        def button_down(*_):
            self.set_mode(
                GameMode.Play if self.current_mode == GameMode.Edit else GameMode.Edit
            )

        mode_button = ImageLabel(
            screen_ui_container,
            anchor_point=Vec2(1, 0),
            position=UDim2(-5, 1, 5, 0),
            size=UDim2(75, 0, 75, 0),
            image=assets.PLAY_BUTTON,
        )
        mode_button.mouse_down.connect(button_down)
        self.mode_button = mode_button

        # setup hotbar
        hotbar_container = Frame(  # size will be updated in set_hotbar
            screen_ui_container,
            anchor_point=Vec2(0.5, 0),
            position=UDim2(0, 0.5, 5, 0),
            color=Color(20, 20, 30, 127),
            roundness=8,
        )

        self.hotbar_container = hotbar_container
        self.set_hotbar("Wood")

    def on_update(self, dt: float):
        if self.current_mode == GameMode.Edit:
            entity = self.current_dragging_entity

            if entity is not None:
                keys = key.get_pressed()

                rotate_sign = (-1 if keys[pygame.K_q] else 0) + (
                    1 if keys[pygame.K_e] else 0
                )

                body = entity.body
                body.position = mouse.get_pos()
                body.velocity = (0, 0)
                body.angular_velocity = 0
                body.angle += dt * rotate_sign * 3.14

                self.current_level.space.reindex_shapes_for_body(body)
        elif self.current_mode == GameMode.Play:
            self.current_level.update(dt)
            self.current_level.update_physics(dt)

    def on_draw_scene(self, out: pygame.Surface):
        out.blit(BACKGROUND_IMAGE)

        # self.current_level.display(out, True)
        self.current_level.display(out)

    def on_draw_interface(self, out: pygame.Surface):
        self.screen_ui_container.draw_to(out)
        # self.screen_ui_container.debug_draw_descendants(out)

    # inputs
    def on_mouse_left_down(self, pos: tuple[int, int]):
        if self.current_mode == GameMode.Edit:
            for entity in self.current_level.entities:
                if not isinstance(entity, objects.CorporealEntity):
                    continue

                if point_in_body(pos, entity.body):
                    self.current_dragging_entity = entity
                    break
        elif self.current_mode == GameMode.Play:
            self.mouse_down_start = pos

        self.screen_ui_container._propogate_on_mouse_down(*pos)

    def on_mouse_left_up(self, pos: tuple[int, int]):
        if self.current_mode == GameMode.Edit:
            if self.current_dragging_entity is not None:
                self.current_dragging_entity = None
        elif self.current_mode == GameMode.Play:
            # TODO: make this better
            if self.mouse_down_start is not None and len(self.remaining_birds) > 0:
                delta_x = pos[0] - self.mouse_down_start[0]
                delta_y = pos[1] - self.mouse_down_start[1]

                new_bird = self.remaining_birds.pop()
                new_bird.body.position = (20, 400)
                new_bird.body.velocity = (delta_x, delta_y)

                self.current_level.add_entity(new_bird)

        self.screen_ui_container._propogate_on_mouse_up(*pos)

    def on_mouse_move(self, pos: tuple[int, int]):
        self.screen_ui_container._propogate_on_mouse_move(*pos)

    def on_key_down(self, key: str):
        if key == "1":
            self.set_hotbar("Wood")
        elif key == "2":
            self.set_hotbar("Stone")
        elif key == "3":
            self.set_hotbar("Glass")
        elif key == "4":
            self.set_hotbar("Pigs")


game = TheGame()
game.start()
