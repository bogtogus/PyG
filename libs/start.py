import pygame
from time import sleep
def init():
    screen = pygame.display.get_surface()
    print('На линуксе перед запуском следует отключить параметр full screen в гланой файле')

    for i in range(256):
        screen.fill('black')
        font = pygame.font.Font('data/font.ttf', 20)
        screen.blit(font.render('PyG - это игровой движок', True, (i, i, i)), (100, 100))
        screen.blit(font.render('На данный момент мы реализовали инвертарь, магазин, врагов и ЭнПиСи', True,
                                (i, i, i)), (100, 150))
        screen.blit(font.render('Немного об управлении:', True, (i, i, i)), (100, 200))
        screen.blit(font.render('E - инвертарь', True, (i, 0, 0)), (150, 250))
        screen.blit(font.render('T - магазин', True, (0, i, 0)), (150, 300))
        screen.blit(font.render('WASD и space - перемещение', True, (0, 0, i)), (150, 350))
        font = pygame.font.SysFont('Consolas', 100)
        screen.blit(font.render('Желательно звук', True, (0, i, i)), (100, 400))
        font = pygame.font.SysFont('Consolas', 20)
        screen.blit(font.render('Подсказка: для боя с боссом прикупите(кнопка Т) броню', True, (255-i, 255-i, 255-i)), (100, 500))
        sleep(0.01)
        pygame.display.flip()
    sleep(5)