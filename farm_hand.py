import pygame
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

class MapCursor:
    def __init__(self, width, height, color = Colors.RED, border_width = 2):
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.cursor_pos = (mouse_pos[0] - (mouse_pos[0] % self.width), mouse_pos[1] - (mouse_pos[1] % self.height))

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect(self.cursor_pos[0], self.cursor_pos[1], self.width, self.height), self.border_width)

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
    
    def start(self):
        self.window = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.set_caption("2d Game")
        self.is_running = True
    
    def game_loop(self):

        # load map data
        tile_map_data = pytmx.load_pygame("C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)\Maps\Farm.tmx")

        map_cursor = MapCursor(
            width=TILE_SIZE,
            height=TILE_SIZE
        )
        
        tiles = {}
        
        is_painting = False
        is_still_down = False
        
        while self.is_running:
            map_cursor.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break
                if pygame.mouse.get_pressed()[0]:
                    if is_painting:
                        is_still_down = True
                    is_painting = True
                    tiles[map_cursor.cursor_pos] = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if not is_still_down:
                        del tiles[map_cursor.cursor_pos]
                    is_painting = False
                    is_still_down = False

            # draw map data on screen
            for layer in tile_map_data.visible_layers:
                for x, y, gid, in layer:
                    tile = tile_map_data.get_tile_image_by_gid(gid)
                    if tile:
                        self.window.blit(tile, (x * tile_map_data.tilewidth,
                                                y * tile_map_data.tileheight))
            
            for pos, do_render in tiles.items():
                if do_render:
                    highlight = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    highlight.set_alpha(100)
                    highlight.fill(Colors.WHITE)
                    self.window.blit(highlight, pos)
            
            map_cursor.draw(self.window)
            
            pygame.display.update()
            self.clock.tick(30)
            
    def stop(self):
        pygame.quit()
        
game = Game()
game.start()
game.game_loop()
game.stop()