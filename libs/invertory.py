import pygame


class inv(list):
    def __init__(self):
        super(inv, self).__init__()

    def append(self, __object) -> None:
        if len(self) < 32:
            super(inv, self).append(__object)
            return None
        else:
            return None

    def extend(self, iterable) -> None:
        if len(self) + len(iterable) < 32:
            super(inv, self).extend(iterable)
            return None
        else:
            return None


def draw(SCREEN: pygame.surface, back: inv, x, y):
    pygame.draw.rect(SCREEN, (255, 255, 255), (0 + x, 0 + y, 265, 133), width=1)
    pygame.draw.rect(SCREEN, (255, 255, 255), (0 + x, 33 + y, 265, 67), width=1)
    pygame.draw.line(SCREEN, (255, 255, 255), (0 + x, 66 + y), (264 + x, 66 + y))
    for i in range(4):
        pygame.draw.rect(SCREEN, (255, 255, 255), (33 + 33 * i * 2 + x, 0 + y, 34, 133), width=1)
    for i in range(len(back)):
        back[i].draw(SCREEN, 1 + i % 8 * 32 + i % 8 + x, 1 + i // 8 * 32 + i // 8 + y)
    pygame.display.flip()
    MainLoop = True
    pygame.mouse.set_visible(True)
    while MainLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MainLoop = False
            if event.type == pygame.MOUSEBUTTONUP:
                MainLoop = False
                c = event.pos
                pygame.mouse.set_visible(False)
                if x < c[0] < x + 265 and y < c[1] < y + 133:
                    r = ((c[0] - x) // 33) + 1 + (((c[1] - y) // 33)) * 8
                    if r <= len(back):
                        return (r, event.button)
                return -1
        pygame.display.flip()