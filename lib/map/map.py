import pytmx
from lib.util import Observable
from lib.constants import Colors, TILE_SIZE
import pygame


class MapCursor(Observable):
    def __init__(self, width, height, color = Colors.RED, border_width = 2):
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        # self.is_dragging = False
        # self.single_clicked = False
        self.mouse_down = False
        super().__init__()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_pos = (mouse_pos[0] - (mouse_pos[0] % self.width), mouse_pos[1] - (mouse_pos[1] % self.height))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            self.fire("click", pos=self.cursor_pos)
            # # If a single click
            # if not self.is_dragging and not self.single_clicked:
            #     self.single_clicked = True
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                self.fire("drag", pos=self.cursor_pos)
            # # If a click and drag
            # if not self.is_dragging and self.single_clicked:
            #     self.single_clicked = False
            #     self.is_dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False
            # # End dragging
            # self.is_dragging = False
            # self.single_clicked = False
        # print((self.is_dragging, self.single_clicked))

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.cursor_pos[0], self.cursor_pos[1], self.width, self.height), self.border_width)

class HighlightMode:
    ADDITIVE = True
    SUBTRACTIVE = False
    
class Map:
    def __init__(self, file_path, cursor: MapCursor):
        # load map data
        self.tile_data = pytmx.load_pygame(file_path)
        self.highlighted_tiles = {}
        self.highlight_mode = HighlightMode.ADDITIVE
        cursor.subscribe('click', self.handleClick)
        cursor.subscribe('drag', self.handleDrag)

    def draw(self, window):
        # draw map data on screen
        for layer in self.tile_data.visible_layers:
            for x, y, gid, in layer:
                tile = self.tile_data.get_tile_image_by_gid(gid)
                if tile:
                    window.blit(tile, (x * self.tile_data.tilewidth,
                                            y * self.tile_data.tileheight))
        
        for pos, do_render in self.highlighted_tiles.items():
            # if do_render:
            highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
            highlight.set_alpha(100)
            highlight.fill(Colors.WHITE if do_render else Colors.RED)
            window.blit(highlight, pos)

    def handleClick(self, event):
        self.highlighted_tiles[event.pos] = not self.highlighted_tiles.get(event.pos, False)
        self.highlight_mode = self.highlighted_tiles[event.pos]
        if not self.highlight_mode and self.highlighted_tiles.get(event.pos) is not None:
            del self.highlighted_tiles[event.pos]
    
    def handleDrag(self, event):
        self.highlighted_tiles[event.pos] = self.highlight_mode
        if not self.highlight_mode and self.highlighted_tiles.get(event.pos) is not None:
            del self.highlighted_tiles[event.pos]