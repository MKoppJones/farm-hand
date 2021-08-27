from lib.game import Game
import pygame
from subprocess import Popen, PIPE

dll_loc = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Stardew Valley.exe"

out = Popen(
    args="DUMPBIN -EXPORTS " + dll_loc, 
    shell=True, 
    stdout=PIPE
).communicate()[0].decode("utf-8")

attrs = [
    i.split(" ")[-1].replace("\r", "") 
    for i in out.split("\n") if " T " in i
]

from ctypes import CDLL

original_pygame_image_load = pygame.image.load

def proxy_image_load(filename):
    if not filename.endswith('.png'):
        return original_pygame_image_load(filename + '.png')
    
pygame.image.load = proxy_image_load
        
farm_file = "C:\Program Files (x86)\Steam\steamapps\common\Stardew Valley\Content (unpacked)\Maps\Farm.tmx"



# lib = cdll.LoadLibrary(dll_loc)
# lib.DebugCommand()
functions = [i for i in attrs if hasattr(CDLL(dll_loc), i)]

print(functions)
game = Game()
game.start(farm_file)
game.game_loop()
game.stop()