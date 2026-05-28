import pygame
import pymunk
from enum import Enum
from typing import Callable
from pygame import mouse, transform, draw
from math import radians

from game import Game
from ui import (
    GuiObject,
    TextLabel,
    Frame,
    ImageLabel,
    UDim2,
    Vec2,
    Color,
    VerticalAlignment,
)
import objects
import assets

WINDOW_SCALE = 1
WINDOW_WIDTH = int(1000 * WINDOW_SCALE)
WINDOW_HEIGHT = int(564 * WINDOW_SCALE)

SLINGSHOT_SCALE = 0.7

BACKGROUND_IMAGE = transform.smoothscale(
    assets.BACKGROUND_3, (WINDOW_WIDTH, WINDOW_HEIGHT)
)
SLINGSHOT_BACK_IMAGE = transform.smoothscale_by(assets.SLINGSHOT_BACK, SLINGSHOT_SCALE)
SLINGSHOT_FRONT_IMAGE = transform.smoothscale_by(
    assets.SLINGSHOT_FRONT, SLINGSHOT_SCALE
)
SLINGSHOT_HEIGHT = SLINGSHOT_BACK_IMAGE.height
SLINGSHOT_POS = (200, WINDOW_HEIGHT - SLINGSHOT_HEIGHT - 10)


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
    "Other": [
        InventoryItem("Regular Pig", assets.MEDIUM_PIG, objects.pig.MinionPig),
        InventoryItem("Foreman Pig", assets.FOREMAN_PIG, objects.pig.ForemanPig),
        InventoryItem("Corporal Pig", assets.CORPORAL_PIG, objects.pig.CorporalPig),
        InventoryItem("King Pig", assets.KING_PIG, objects.pig.KingPig),
        InventoryItem("TNT", assets.TNT, objects.special.TNT),
    ],
}
HOTBAR_SLOT_SIZE = 60
HOTBAR_SLOT_PADDING = 5


def point_in_body(point: tuple[float, float], body: pymunk.Body):
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True


class TheGame(Game):
    window_width = WINDOW_WIDTH
    window_height = WINDOW_HEIGHT
    title = "Mad Pigeons™"
    icon = assets.RED_BIRD

    remaining_birds: list[objects.bird.Bird]

    edit_snapshot: list[objects.EntitySnapshot] | None = None
    current_mode: GameMode = GameMode.Edit
    current_hotbar: str = ""
    slingshot_engaged: bool = False

    def set_mode(self, new_mode: GameMode):
        if new_mode == GameMode.Play:
            self.edit_snapshot = self.current_level.take_snapshot()

            self.remaining_birds = [
                objects.bird.BirdRed(self.current_level),
                objects.bird.BirdRed(self.current_level),
                objects.bird.BirdRed(self.current_level),
            ]

            self.current_dragging_entity = None

            self.edit_gui.visible = False
            self.edit_gui.invalidate()

            self.mode_button.set_image(assets.EDIT_BUTTON)
        elif new_mode == GameMode.Edit:
            if self.edit_snapshot is not None:
                self.current_level.load_snapshot(self.edit_snapshot)

            self.edit_gui.visible = True
            self.edit_gui.invalidate()

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
                text_color=Color(255, 255, 255, 255),
                text_y_alignment=VerticalAlignment.Top,
                text_font=assets.LDF_COMIC_SANS_16PT,
                text_outline_color=Color(0, 0, 0, 255),
                text_outline_thickness=1,
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
            (-1e4, WINDOW_HEIGHT + 85),
            (1e4, WINDOW_HEIGHT + 85),
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
            size=UDim2(x_offset=WINDOW_WIDTH, y_offset=WINDOW_HEIGHT)
        )
        self.screen_ui_container = screen_ui_container

        def mode_button_down(*_):
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
        mode_button.mouse_down.connect(mode_button_down)
        self.mode_button = mode_button

        def clear_button_down(*_):
            self.current_level.clear()

        # edit mode gui

        edit_gui_container = GuiObject(screen_ui_container, size=UDim2(0, 1, 0, 1))
        self.edit_gui = edit_gui_container

        clear_button = ImageLabel(
            edit_gui_container,
            size=UDim2(70, 0, 70, 0),
            position=UDim2(5, 0, 5, 0),
            image=assets.TRASH_BUTTON,
        )
        clear_button.mouse_down.connect(clear_button_down)

        # setup hotbar
        hotbar_container = Frame(  # size will be updated in set_hotbar
            edit_gui_container,
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
                body = entity.body
                body.position = mouse.get_pos()
                body.velocity = (0, 0)
                body.angular_velocity = 0

                self.current_level.space.reindex_shapes_for_body(body)
        elif self.current_mode == GameMode.Play:
            if not self.slingshot_engaged:
                pass

            self.current_level.update(dt)
            self.current_level.update_physics(dt)

    def on_draw_scene(self, out: pygame.Surface):
        out.blit(BACKGROUND_IMAGE)

        out.blit(SLINGSHOT_BACK_IMAGE, SLINGSHOT_POS)

        # draw entities
        self.current_level.display(out, True)
        self.current_level.display(out)

        out.blit(
            SLINGSHOT_FRONT_IMAGE,
            (SLINGSHOT_POS[0] - SLINGSHOT_FRONT_IMAGE.width * 0.7, SLINGSHOT_POS[1]),
        )

    def on_draw_interface(self, out: pygame.Surface):
        # out.blit(assets.SMALL_WOOD_BALL_0)

        self.screen_ui_container.draw_to(out)
        self.screen_ui_container.debug_draw_descendants(out)

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
            self.mouse_down_start_position = pos

        self.screen_ui_container._propogate_on_mouse_down(*pos)

    def on_mouse_left_up(self, pos: tuple[int, int]):
        if self.current_mode == GameMode.Edit:
            if self.current_dragging_entity is not None:
                self.current_dragging_entity = None
        elif self.current_mode == GameMode.Play:
            # TODO: check if the mouse "activated" the slingshot and if so then launch the bird in the direction from the mouse to the slingshot
            pass

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
            self.set_hotbar("Other")

        entity = self.current_dragging_entity
        if entity is not None:
            if key == "e":
                entity.body.angle += radians(45)
            elif key == "q":
                entity.body.angle -= radians(45)

        # if key == "n" and self.edit_snapshot is not None:
        #     objects.save_snapshots_to_file(self.edit_snapshot, "hi.json")
        # elif key == "l":
        #     objects.load_entities_from_file("hi.json", self.current_level)


game = TheGame()
game.start()
