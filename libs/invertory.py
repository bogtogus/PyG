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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PyG')
    print(pygame.display.Info().current_w, pygame.display.Info().current_h)
    screen = pygame.display.set_mode((720, 720), pygame.FULLSCREEN)
    b = inv()
    b.extend((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 12, 12, 12, 12, 87, 8787, 78, 78, 65, 45, 4, 4, 1, 5))
    print(draw(screen, b, 128, 64))
    clock = pygame.time.Clock()
