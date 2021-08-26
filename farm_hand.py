from lib.game import Game
import pygame
import pytmx

original_pygame_image_load = pygame.image.load

def proxy_image_load(filename):
    if not filename.endswith('.png'):
        return original_pygame_image_load(filename + '.png')
    
pygame.image.load = proxy_image_load
        
farm_file = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)\Maps\Farm.tmx"

game = Game()
game.start(farm_file)
game.game_loop()
game.stop()