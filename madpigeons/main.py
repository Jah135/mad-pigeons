import pygame
import pymunk
from typing import Callable
from pygame import mouse, key

from game import Game
from ui import GuiObject, TextLabel, Frame, ImageLabel, UDim2, Vec2, Color
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

MODE_EDIT = "edit"
MODE_PLAY = "play"


def point_in_body(point: tuple[float, float], body: pymunk.Body):
    for shape in body.shapes:
        if shape.point_query(point).distance <= 0:
            return True


class TheGame(Game):
    window_width = 1000
    window_height = 564
    title = "Mad Pigeons™ (not angry birds)"
    icon = assets.RED_BIRD

    mode: str
    birds: list[objects.bird.Bird]

    mouse_down_start: tuple[int, int] | None = None

    def setup(self):
        test_level = objects.Level()

        self.mode = MODE_EDIT
        self.birds = [
            objects.bird.BirdRed(test_level),
            objects.bird.BirdRed(test_level),
            objects.bird.BirdRed(test_level),
        ]

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

        self.background_image = pygame.transform.smoothscale(
            assets.BACKGROUND_1,
            (self.window_width, self.window_height),
        )

    def set_mode(self, new_mode: str):
        if new_mode == MODE_PLAY:
            self.hotbar_container.visible = False
            self.hotbar_container.invalidate()
            self.mode_button.set_image(assets.EDIT_BUTTON)
        elif new_mode == MODE_EDIT:
            self.hotbar_container.visible = True
            self.hotbar_container.invalidate()
            self.mode_button.set_image(assets.PLAY_BUTTON)

        self.mode = new_mode

    def setup_ui(self):
        screen_ui_container = GuiObject(
            size=UDim2(x_offset=self.window_width, y_offset=self.window_height)
        )
        self.screen_ui_container = screen_ui_container

        def button_down(*_):
            self.set_mode(MODE_EDIT if self.mode == MODE_PLAY else MODE_PLAY)

        mode_button = ImageLabel(
            screen_ui_container,
            anchor_point=Vec2(1, 1),
            position=UDim2(-5, 1, -5, 1),
            size=UDim2(75, 0, 75, 0),
            image=assets.PLAY_BUTTON,
        )
        mode_button.mouse_down.connect(button_down)

        self.mode_button = mode_button

        # setup hotbar
        hotbar_count = len(HOTBARS["Wood"])
        hotbar_container = GuiObject(
            screen_ui_container,
            size=UDim2(0, 0.6, HOTBAR_SLOT_SIZE, 0),
            position=UDim2(0, 0.5, -5, 1),
            anchor_point=Vec2(0.5, 1),
        )

        self.hotbar_container = hotbar_container

        for index, item in enumerate(HOTBARS["Wood"]):
            frame = Frame(
                hotbar_container,
                Vec2(index / (hotbar_count - 1), 0),
                UDim2(x_scale=index / (hotbar_count - 1)),
                UDim2(x_offset=HOTBAR_SLOT_SIZE, y_offset=HOTBAR_SLOT_SIZE),
            )
            frame.color = Color(0, 0, 0, 80)
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
                Vec2(0.5, 1),
                UDim2(x_scale=0.5),
                size=UDim2(0, 2, 20, 0),
                text=item.name,
                text_color=Color(0, 0, 0, 255),
                text_outline_color=Color(255, 255, 255, 10),
                text_outline_thickness=1,
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

    def on_update(self, dt: float):
        if self.mode == MODE_EDIT:
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

                # apparently this fixes the problem where dragging while paused wouldnt actually update the position of the shape
                # yay
                self.current_level.space.reindex_shapes_for_body(body)
        elif self.mode == MODE_PLAY:
            self.current_level.update(dt)
            self.current_level.update_physics(dt)

    def on_draw_scene(self, out: pygame.Surface):
        out.blit(self.background_image)

        # self.current_level.display(out, True)
        self.current_level.display(out)

    def on_draw_interface(self, out: pygame.Surface):
        # NOAH TEST ASSETS HERE
        # out.blit(assets.BLAST, (100, 100))

        self.screen_ui_container.draw_to(out)

    def on_mouse_left_down(self, pos: tuple[int, int]):
        if self.mode == MODE_EDIT:
            for entity in self.current_level.entities:
                if not isinstance(entity, objects.CorporealEntity):
                    continue

                if point_in_body(pos, entity.body):
                    self.current_dragging_entity = entity
                    break
        elif self.mode == MODE_PLAY:
            self.mouse_down_start = pos

        self.screen_ui_container._propogate_on_mouse_down(*pos)

    def on_mouse_left_up(self, pos: tuple[int, int]):
        if self.mode == MODE_EDIT:
            if self.current_dragging_entity is not None:
                self.current_dragging_entity = None
        elif self.mode == MODE_PLAY:
            if self.mouse_down_start is not None and len(self.birds) > 0:
                delta_x = pos[0] - self.mouse_down_start[0]
                delta_y = pos[1] - self.mouse_down_start[1]

                new_bird = self.birds.pop()
                new_bird.body.position = (20, 400)
                new_bird.body.velocity = (delta_x, delta_y)

                self.current_level.add_entity(new_bird)

        self.screen_ui_container._propogate_on_mouse_up(*pos)

    def on_mouse_move(self, pos: tuple[int, int]):
        self.screen_ui_container._propogate_on_mouse_move(*pos)


game = TheGame()
game.start()
