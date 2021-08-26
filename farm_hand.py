import pygame
from pygame import event
import pytmx

SCREEN_TILES_WIDTH = 80
SCREEN_TILES_HEIGHT = 65
TILE_SIZE = 16
DISPLAY_SIZE = SCREEN_TILES_WIDTH * TILE_SIZE, SCREEN_TILES_HEIGHT * TILE_SIZE

original_pygame_image_load = pygame.image.load

def proxy_image_load(filename):
    if not filename.endswith('.png'):
        return original_pygame_image_load(filename + '.png')
    
pygame.image.load = proxy_image_load
        
farm_file = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)\Maps\Farm.tmx"
class Colors:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

class Event(object):
    pass

class Observable(object):
    def __init__(self):
        self.callbacks = {}
        
    def subscribe(self, event_name, callback):
        if not self.callbacks.get(event_name):
            self.callbacks[event_name] = []
        self.callbacks[event_name].append(callback)
        
    def fire(self, event_type, **attrs):
        event = Event()
        event.source = self
        event.type = event_type
        for key, value in attrs.items():
            setattr(event, key, value)
        for func in self.callbacks.get(event_type, []):
            func(event)

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
    
    def update(self, cursor):
        # # If a click and drag
        # if cursor.is_dragging:
        #     self.highlighted_tiles[cursor.cursor_pos] = self.highlight_mode
        #     if not self.highlight_mode and self.highlighted_tiles.get(cursor.cursor_pos) is not None:
        #         del self.highlighted_tiles[cursor.cursor_pos]
        # # If a single click
        # elif cursor.single_clicked:
        #     self.highlighted_tiles[cursor.cursor_pos] = not self.highlighted_tiles.get(cursor.cursor_pos, False)
        #     self.highlight_mode = self.highlighted_tiles[cursor.cursor_pos]
        #     if not self.highlight_mode and self.highlighted_tiles.get(cursor.cursor_pos) is not None:
        #         del self.highlighted_tiles[cursor.cursor_pos]
        pass
    
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

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
    
    def start(self):
        self.window = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.set_caption("Farm Hand - Stardew Valley planner and helper")
        self.is_running = True
        self.map_cursor = MapCursor(
            width=TILE_SIZE,
            height=TILE_SIZE
        )
        self.game_map = Map(file_path=farm_file, cursor=self.map_cursor)
        
    def game_loop(self):
        
        while self.is_running:
            self.map_cursor.update()
            for event in pygame.event.get():
                self.map_cursor.handleEvent(event)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break
            self.game_map.update(self.map_cursor)
            
            self.game_map.draw(self.window)
            self.map_cursor.draw(self.window)
            
            pygame.display.update()
            self.clock.tick(60)
            
    def stop(self):
        pygame.quit()
        
game = Game()
game.start()
game.game_loop()
game.stop()