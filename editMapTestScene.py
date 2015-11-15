import os
import os.path
import sys

import pygame

from buffalo import utils
from buffalo.scene import Scene
from buffalo.label import Label
from buffalo.button import Button
from buffalo.input import Input
from buffalo.tray import Tray

from camera import Camera
from mapManager import MapManager
from pluginManager import PluginManager
from toolManager import ToolManager

class CameraController:
    def __init__(self):
        self.fPos = (0.0, 0.0)
        self.pos = (int(self.fPos[0]), int(self.fPos[1]))
        self.xv, self.yv = 0.0, 0.0
        self.speed = 1.2
        self.shift_speed = self.speed * 5.0

    def update(self, keys):
        w, a, s, d, shift = (
            keys[pygame.K_w],
            keys[pygame.K_a],
            keys[pygame.K_s],
            keys[pygame.K_d],
            keys[pygame.K_LSHIFT],
        )

        if shift:
            speed = self.shift_speed
        else:
            speed = self.speed

        speed *= utils.delta / 16.0

        self.xv = 0.0
        self.yv = 0.0

        if w:
            self.yv -= speed
        if a:
            self.xv -= speed
        if s:
            self.yv += speed
        if d:
            self.xv += speed

        x, y = self.fPos
        x += self.xv
        y += self.yv
        self.fPos = x, y
        self.pos = (int(self.fPos[0]), int(self.fPos[1]))

class EditMapTestScene(Scene):
    def on_escape(self):
        sys.exit()

    def blit(self):
        Camera.blitView()
        ToolManager.blit()

    def update(self):
        super(EditMapTestScene, self).update()
        keys = pygame.key.get_pressed()
        self.camera_controller.update(keys)
        Camera.update()
        ToolManager.update(self.mouse_buttons, self.mouse_pos, self.click_pos, self.trays)
        MapManager.soft_load_writer()

    def __init__(self):
        Scene.__init__(self)
        self.BACKGROUND_COLOR = (0, 0, 0, 255)
        PluginManager.loadPlugins()
        self.camera_controller = CameraController()
        Camera.lock(self.camera_controller, initial_update=True)

        Button.DEFAULT_SEL_COLOR = (50, 50, 100, 255)
        self.tool_tray = Tray(
            (utils.SCREEN_W - 270, 20),
            (250, 800),
            min_width=250, max_width=250,
            min_height=250, max_height=800,
            color=(100, 50, 50, 100),
        )
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 10),
                "Tool Tray",
                color=(255,255,255,255),
                x_centered=True,
                font="default24",
            )
        )
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 25),
                "________________",
                color=(255,255,255,255),
                x_centered=True,
                font="default18",
            )
        )
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 50),
                "Function",
                color=(255,255,255,255),
                x_centered=True,
                font="default18",
            )
        )
        def set_func_state_to_select():
            ToolManager.set_func_state(ToolManager.FUNC_SELECT)
            self.tool_tray.render()
        self.button_select_mode = Button(
            (15, 80),
            " Select Mode ",
            color=(255,255,255,255),
            bg_color=(100,100,200,255),
            font="default12",
            func=set_func_state_to_select,
        )
        self.tool_tray.buttons.add(self.button_select_mode)
        def set_func_state_to_fill():
            ToolManager.set_func_state(ToolManager.FUNC_FILL)
            self.tool_tray.render()
        self.button_fill_mode = Button(
            (self.tool_tray.width - 15, 80),
            "   Fill Mode   ",
            color=(255,255,255,255),
            bg_color=(100,100,200,255),
            invert_x_pos=True,
            font="default12",
            func=set_func_state_to_fill,
        )
        self.tool_tray.buttons.add(self.button_fill_mode)
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 120),
                "________________",
                color=(255,255,255,255),
                x_centered=True,
                font="default18",
            )
        )
        self.tool_tray.labels.add(
            Label(
                (int(self.tool_tray.width / 2), 150),
                "Area of Effect",
                color=(255,255,255,255),
                x_centered=True,
                font="default18",
            )
        )
        def set_effect_state_to_draw():
            ToolManager.set_effect_state(ToolManager.EFFECT_DRAW)
            self.tool_tray.render()
        self.button_draw_mode = Button(
            (15, 180),
            "  Draw Mode  ",
            color=(255,255,255,255),
            bg_color=(100,100,200,255),
            font="default12",
            func=set_effect_state_to_draw,
        )
        self.tool_tray.buttons.add(self.button_draw_mode)
        def set_effect_state_to_area():
            ToolManager.set_effect_state(ToolManager.EFFECT_AREA)
            self.tool_tray.render()
        self.button_area_mode = Button(
            (self.tool_tray.width - 15, 180),
            "  Area Mode  ",
            color=(255,255,255,255),
            bg_color=(100,100,200,255),
            invert_x_pos=True,
            font="default12",
            func=set_effect_state_to_area,
        )
        self.tool_tray.buttons.add(self.button_area_mode)

        ToolManager.initialize_states(
            ToolManager.FUNC_SELECT, ToolManager.EFFECT_DRAW,
            (
                self.button_fill_mode,
                self.button_select_mode,
                self.button_draw_mode,
                self.button_area_mode,
            ),
        )
        
        self.tool_tray.render()
        self.trays.add(self.tool_tray)
