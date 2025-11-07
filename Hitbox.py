import sys

import pygame
import pygame.locals
WIDTH = HEIGHT = 1000

class boxer:
    def __init__(self, x, controls=None, color=(60, 120, 255)):
        self.x = x
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.on_ground = True

        self.color = color

        self.max_health = 100
        self.health = 100

        self.max_stamina = 100
        self.stamina = 100

        self.dodging = False

        self.hitstun = 0

        self.attack_windup = 0
        self.attack_type = None  # "light" or "heavy"


        # controls mapping for human
        self.controls = controls or {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "punch": pygame.K_w,
            "dodge": pygame.K_s,
        }
    
    def update(self, screen: pygame.surface):
        self.x += self.vx
        self.y += self.vy
        pygame.draw.rect(screen, "#E03B3B",(self.x,self.y,100,100))


def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    box1 = boxer(1)
    speed = 10

    while True:
        screen.fill("#000000")
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            box1.update(screen)

        held = pygame.key.get_pressed()
        if held[pygame.K_RIGHT]:
            box1.vx=speed
        elif held[pygame.K_LEFT]:
            box1.vx=-speed
        else:
            box1.vx=0
        box1.update(screen)
        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()