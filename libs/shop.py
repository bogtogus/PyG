import pygame
from libs.invertory import draw, inv
from libs.items import *

def shoplist(money: list, invr: inv):
    forsale = inv()
    forsale.extend((WoodenStick(), IronSword(), RicardoArmor()))
    r = draw(pygame.display.get_surface(), forsale, pygame.display.get_surface().get_size()[0] // 2,
        pygame.display.get_surface().get_size()[1] // 2)
    if r != -1 and r[1] == 1:
        if money[0] > forsale[r[0]-1].cost:
            money[0] -= forsale[r[0]-1].cost
            invr.append(forsale[r[0]-1])