import pygame, random


class Emeny(pygame.sprite.Sprite):
    image = pygame.image.load('data/apple.png')
    def __init__(self, *group):
        super().__init__(*group)
        self.image = Emeny.image
        self.rect = self.image.get_rect()
        self.rect.x = 346
        self.rect.y = 346
        self.point = (random.randint(16, 704), random.randint(16, 704))
    def update(self):
        if self.rect.x + 16 < self.point[0]:
            self.rect = self.rect.move(1, 0)
        if self.rect.x + 16 > self.point[0]:
            self.rect = self.rect.move(-1, 0)
        if self.rect.y + 16 < self.point[1]:
            self.rect = self.rect.move(0, 1)
        if self.rect.y + 16 > self.point[1]:
            self.rect = self.rect.move(0, -1)
        pygame.draw.circle(screen, 'white', self.point, 3)
        if self.rect.x + 16 == self.point[0] and self.rect.y + 16 == self.point[1]:
            self.point = (random.randint(16, 704), random.randint(16, 704))


pygame.init()
pygame.display.set_caption('PyG')
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((720, 720), pygame.FULLSCREEN)
MainLoop = True
clock = pygame.time.Clock()

AS = pygame.sprite.Group()
Emeny(AS)

while MainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            MainLoop = False
    AS.update()
    AS.draw(screen)
    pygame.display.flip()
    clock.tick(150)