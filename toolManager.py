import pygame

from buffalo import utils

import tile
import chunk
import camera
import mapManager

class ToolManager(object):
    
    # DEFINE CONSTANTS

    # ONLY ONE FUNC STATE CAN BE SELECTED AT A TIME
    FUNC_FILL   = 1
    FUNC_SELECT = 2

    # ONLY ONE EFFECT STATE CAN BE SELECTED AT A TIME
    EFFECT_DRAW = 1
    EFFECT_AREA = 2

    func_state   = None
    effect_state = None

    tiles = dict()

    @staticmethod
    def blit():
        for (chcx, chcy), (tcx, tcy) in ToolManager.tiles.keys():
            cx, cy = camera.Camera.pos
            tx, ty = (chcx * chunk.Chunk.CHUNK_WIDTH + tcx) * tile.Tile.TILE_SIZE, (chcy * chunk.Chunk.CHUNK_HEIGHT + tcy) * tile.Tile.TILE_SIZE
            utils.screen.blit(
                ToolManager.tiles[(chcx, chcy), (tcx, tcy)],
                (tx - cx, ty - cy),
            )

    @staticmethod
    def update(mouse_buttons, mouse_pos, click_pos, trays):
        if ToolManager.func_state == ToolManager.FUNC_SELECT:
            if ToolManager.effect_state == ToolManager.EFFECT_DRAW:
                if mouse_buttons[0] and not any([tray.contains(mouse_pos) for tray in trays]):
                    mwx, mwy = (mouse_pos[0] + camera.Camera.pos[0], mouse_pos[1] + camera.Camera.pos[1])
                    cx, cy = chunk_coords = mapManager.MapManager.get_chunk_coords((mwx, mwy))
                    tile_coords = (
                        int((mwx - cx * chunk.Chunk.CHUNK_WIDTH * tile.Tile.TILE_SIZE) / tile.Tile.TILE_SIZE),
                        int((mwy - cy * chunk.Chunk.CHUNK_HEIGHT * tile.Tile.TILE_SIZE) / tile.Tile.TILE_SIZE),
                    )
                    if (chunk_coords, tile_coords) not in ToolManager.tiles.keys():
                        ToolManager.tiles[(chunk_coords, tile_coords)] = utils.empty_surface(
                            (tile.Tile.TILE_SIZE, tile.Tile.TILE_SIZE)
                        )
                        ToolManager.tiles[(chunk_coords, tile_coords)].fill((75, 255, 75, 225))
                        ToolManager.tiles[(chunk_coords, tile_coords)].fill((75, 255, 75, 150), pygame.Rect(1, 1, tile.Tile.TILE_SIZE - 2, tile.Tile.TILE_SIZE - 2))
            elif ToolManager.effect_state == ToolManager.EFFECT_AREA:
                if mouse_buttons[0] and not any([tray.contains(mouse_pos) for tray in trays]):
                    ToolManager.tiles = dict()
                    mwx, mwy = (mouse_pos[0] + camera.Camera.pos[0], mouse_pos[1] + camera.Camera.pos[1])
                    cmwx, cmwy = (click_pos[0] + camera.Camera.pos[0], click_pos[1] + camera.Camera.pos[1])
                    x_delta = tile.Tile.TILE_SIZE if mwx > cmwx else -tile.Tile.TILE_SIZE
                    y_delta = tile.Tile.TILE_SIZE if mwy > cmwy else -tile.Tile.TILE_SIZE
                    for y_val in range(cmwy, mwy + y_delta - (mwy % y_delta), y_delta):
                        for x_val in range(cmwx, mwx + x_delta - (mwx % x_delta), x_delta):
                            cx, cy = chunk_coords = mapManager.MapManager.get_chunk_coords((x_val, y_val))
                            tile_coords = (
                                int((x_val - cx * chunk.Chunk.CHUNK_WIDTH * tile.Tile.TILE_SIZE) / tile.Tile.TILE_SIZE),
                                int((y_val - cy * chunk.Chunk.CHUNK_HEIGHT * tile.Tile.TILE_SIZE) / tile.Tile.TILE_SIZE),
                            )
                            if (chunk_coords, tile_coords) not in ToolManager.tiles.keys():
                                ToolManager.tiles[(chunk_coords, tile_coords)] = utils.empty_surface(
                                    (tile.Tile.TILE_SIZE, tile.Tile.TILE_SIZE)
                                )
                            ToolManager.tiles[(chunk_coords, tile_coords)].fill((75, 255, 75, 225))
                            ToolManager.tiles[(chunk_coords, tile_coords)].fill((75, 255, 75, 150), pygame.Rect(1, 1, tile.Tile.TILE_SIZE - 2, tile.Tile.TILE_SIZE - 2))
        elif ToolManager.func_state == ToolManager.FUNC_FILL:
            if ToolManager.effect_state == ToolManager.EFFECT_DRAW:
                pass
            elif ToolManager.effect_state == ToolManager.EFFECT_AREA:
                pass

    @staticmethod
    def verify_state(func_state, effect_state):
        assert(
            func_state == ToolManager.FUNC_FILL or \
            func_state == ToolManager.FUNC_SELECT
        )
        assert(
            effect_state == ToolManager.EFFECT_DRAW or \
            effect_state == ToolManager.EFFECT_AREA
        )

    @staticmethod
    def set_func_state(other_state):
        ToolManager.tiles = dict()
        ToolManager.verify_state(other_state, ToolManager.effect_state)
        ToolManager.func_state = other_state
        if ToolManager.func_state == ToolManager.FUNC_FILL:
            ToolManager.BUTTON_FUNC_FILL.bg_color = ToolManager.BUTTON_FUNC_FILL_SEL_COLOR
            ToolManager.BUTTON_FUNC_FILL.render()
            ToolManager.BUTTON_FUNC_SELECT.bg_color = ToolManager.BUTTON_FUNC_SELECT_BG_COLOR
            ToolManager.BUTTON_FUNC_SELECT.render()
        elif ToolManager.func_state == ToolManager.FUNC_SELECT:
            ToolManager.BUTTON_FUNC_SELECT.bg_color = ToolManager.BUTTON_FUNC_SELECT_SEL_COLOR
            ToolManager.BUTTON_FUNC_SELECT.render()
            ToolManager.BUTTON_FUNC_FILL.bg_color = ToolManager.BUTTON_FUNC_FILL_BG_COLOR
            ToolManager.BUTTON_FUNC_FILL.render()

    @staticmethod
    def set_effect_state(other_state):
        ToolManager.tiles = dict()
        ToolManager.verify_state(ToolManager.func_state, other_state)
        ToolManager.effect_state = other_state
        if ToolManager.effect_state == ToolManager.EFFECT_AREA:
            ToolManager.BUTTON_EFFECT_AREA.bg_color = ToolManager.BUTTON_EFFECT_AREA_SEL_COLOR
            ToolManager.BUTTON_EFFECT_AREA.render()
            ToolManager.BUTTON_EFFECT_DRAW.bg_color = ToolManager.BUTTON_EFFECT_DRAW_BG_COLOR
            ToolManager.BUTTON_EFFECT_DRAW.render()
        elif ToolManager.effect_state == ToolManager.EFFECT_DRAW:
            ToolManager.BUTTON_EFFECT_DRAW.bg_color = ToolManager.BUTTON_EFFECT_DRAW_SEL_COLOR
            ToolManager.BUTTON_EFFECT_DRAW.render()
            ToolManager.BUTTON_EFFECT_AREA.bg_color = ToolManager.BUTTON_EFFECT_AREA_BG_COLOR
            ToolManager.BUTTON_EFFECT_AREA.render()

    @staticmethod
    def initialize_states(func_state, effect_state, buttons):
        assert(type(buttons) == tuple and len(buttons) == 4)
        ToolManager.BUTTON_FUNC_FILL   = buttons[0]
        ToolManager.BUTTON_FUNC_FILL_BG_COLOR = ToolManager.BUTTON_FUNC_FILL.bg_color
        ToolManager.BUTTON_FUNC_FILL_SEL_COLOR = ToolManager.BUTTON_FUNC_FILL.sel_color
        ToolManager.BUTTON_FUNC_SELECT = buttons[1]
        ToolManager.BUTTON_FUNC_SELECT_BG_COLOR = ToolManager.BUTTON_FUNC_SELECT.bg_color
        ToolManager.BUTTON_FUNC_SELECT_SEL_COLOR = ToolManager.BUTTON_FUNC_SELECT.sel_color
        ToolManager.BUTTON_EFFECT_DRAW = buttons[2]
        ToolManager.BUTTON_EFFECT_DRAW_BG_COLOR = ToolManager.BUTTON_EFFECT_DRAW.bg_color
        ToolManager.BUTTON_EFFECT_DRAW_SEL_COLOR = ToolManager.BUTTON_EFFECT_DRAW.sel_color
        ToolManager.BUTTON_EFFECT_AREA = buttons[3]
        ToolManager.BUTTON_EFFECT_AREA_BG_COLOR = ToolManager.BUTTON_EFFECT_AREA.bg_color
        ToolManager.BUTTON_EFFECT_AREA_SEL_COLOR = ToolManager.BUTTON_EFFECT_AREA.sel_color
        ToolManager.verify_state(func_state, effect_state)
        ToolManager.func_state = func_state
        ToolManager.effect_state = effect_state
        ToolManager.set_func_state(ToolManager.func_state)
        ToolManager.set_effect_state(ToolManager.effect_state)
