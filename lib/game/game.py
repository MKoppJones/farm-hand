import pygame
from lib.constants import DISPLAY_SIZE, TILE_SIZE
from lib.map import Map, MapCursor

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
    
    def start(self, farm_file):
        self.window = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.set_caption("Farm Hand - Stardew Valley planner and helper")
        self.is_running = True
        self.map_cursor = MapCursor(
            width=TILE_SIZE,
            height=TILE_SIZE
        )
        self.game_map: Map = Map(file_path=farm_file, cursor=self.map_cursor)
        
    def game_loop(self):
        
        while self.is_running:
            self.map_cursor.update()
            for event in pygame.event.get():
                self.map_cursor.handleEvent(event)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    break
            
            self.game_map.draw(self.window)
            self.map_cursor.draw(self.window)
            
            pygame.display.update()
            self.clock.tick(60)
            
    def stop(self):
        pygame.quit()
        