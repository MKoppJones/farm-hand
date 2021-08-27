import pytmx
from lib.util import Observable
from lib.constants import Colors, TILE_SIZE, DISPLAY_SIZE
import pygame


class MapCursor(Observable):
    def __init__(self, width, height, color = Colors.RED, border_width = 2):
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        self.mouse_down = False
        super().__init__()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < DISPLAY_SIZE[0] - TILE_SIZE * 25:
            self.cursor_pos = (mouse_pos[0] - (mouse_pos[0] % self.width), mouse_pos[1] - (mouse_pos[1] % self.height))

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
            self.fire("click", pos=self.cursor_pos)
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_down:
                self.fire("drag", pos=self.cursor_pos)
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False

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

    def getTile(self, pos):
        print(f'Looking at {pos[0]/TILE_SIZE, pos[1]/TILE_SIZE}')
        tile = None
        for i in self.tile_data.visible_tile_layers:
            try:
                tile = self.tile_data.get_tile_properties(x=pos[0]/TILE_SIZE, y=pos[1]/TILE_SIZE, layer=i)
                break
            except Exception as e:
                print(f'tile not found on layer {i}')
        return tile

    def handleClick(self, event):
        tile = self.getTile(event.pos)
        if tile:
            if tile.get('Diggable') == 'T':
                self.highlighted_tiles[event.pos] = not self.highlighted_tiles.get(event.pos, False)
                self.highlight_mode = self.highlighted_tiles[event.pos]
                if not self.highlight_mode and self.highlighted_tiles.get(event.pos) is not None:
                    del self.highlighted_tiles[event.pos]
    
    def handleDrag(self, event):
        tile = self.getTile(event.pos)
        if tile:
            if tile.get('Diggable') == 'T':
                self.highlighted_tiles[event.pos] = self.highlight_mode
                if not self.highlight_mode and self.highlighted_tiles.get(event.pos) is not None:
                    del self.highlighted_tiles[event.pos]