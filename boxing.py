import sys
import pygame
import pygame.locals

WIDTH = HEIGHT = 1000

class boxer:
    def __init__(self, x, handle, color):
        self.x = x
        self.y = 500
        self.vx = 4
        self.handle = handle
        self.acc = 0.1
        self.punch = 0

        self.color = color

        self.max_health = 100
        self.health = 100
        self.lives = 3

        self.max_stamina = 100
        self.stamina = 100
        self.stamina_regen_delay = 0

        self.dodging = False
        self.dodge_timer = 0

        self.hitstun = 0

        self.attack_windup = 0
        self.attack_type = None
        
    def update(self, screen: pygame.surface):
        if self.vx > 7:
            self.vx = 6
        if (self.x + self.vx) > 0 and (self.x + self.vx + 100 <= WIDTH):
            self.x += self.vx
        minus = 0
        if self.dodging:
            minus = 50
        pygame.draw.rect(screen, "#FFFFFF", (self.x - 25, self.y - 70, 150, 45))
        stamina_ratio = self.stamina / self.max_stamina
        pygame.draw.rect(screen, "#0000FF", (self.x - 20, self.y - 65, 140 * stamina_ratio, 15))
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, "#FF0000", (self.x - 20, self.y - 45, 140 * health_ratio, 15))
        pygame.draw.rect(screen, self.color, (self.x, self.y + minus, 100, 200 - minus))
        if self.vx == 0 or self.punch == 0:
            pygame.draw.rect(screen, "#E03BA6", (self.x + 25, self.y + 50, 50, 100))
        elif self.vx > 0 and self.punch == 1:
            pygame.draw.rect(screen, "#E03BA6", (self.x + 50, self.y + 50, 100, 50))
        elif self.punch == 1:
            pygame.draw.rect(screen, "#E03BA6", (self.x + 50 - 100, self.y + 50, 100, 50))

def draw_lives(screen, box1, box2):
    font = pygame.font.SysFont(None, 40)
    text1 = font.render("Boxer 1:", True, (255, 255, 255))
    screen.blit(text1, (20, 20))
    for i in range(box1.lives):
        pygame.draw.rect(screen, "#FF0000", (140 + i * 40, 20, 30, 30))
    
    text2 = font.render("Boxer 2:", True, (255, 255, 255))
    screen.blit(text2, (WIDTH - 250, 20))
    for i in range(box2.lives):
        pygame.draw.rect(screen, "#FF0000", (WIDTH - 130 + i * 40, 20, 30, 30))

def main():
    fps = 120
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    box1 = boxer(1, 1, "#49E03B")
    box2 = boxer(WIDTH - 100, 0, "#672EBC")
    boxers = [box1, box2]

    while True:
        screen.fill("#000000")
        pygame.draw.rect(screen, "#7B2E16", (0, 700, 1000, 200))
        draw_lives(screen, box1, box2)
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
        held = pygame.key.get_pressed()
        for person in boxers:
            if person.stamina > 0:
                if person.handle == 0:
                    if held[pygame.K_RIGHT]:
                        person.vx += person.acc
                    elif held[pygame.K_LEFT]:
                        person.vx -= person.acc
                    else:
                        person.vx = 0
                    if held[pygame.K_UP]:
                        person.punch = 1
                        person.stamina -= 0.6
                        person.stamina_regen_delay = 60 # because game is 120 FPS so 0.5 of a second
                    else:
                        person.punch = 0
                    if held[pygame.K_DOWN]:
                        person.dodging = True
                        person.stamina -= 0.6
                        person.stamina_regen_delay = 60
                    else:
                        person.dodging = False
                elif person.handle == 1:
                    if held[pygame.K_d]:
                        person.vx += person.acc
                    elif held[pygame.K_a]:
                        person.vx -= person.acc
                    else:
                        person.vx = 0
                    if held[pygame.K_w]:
                        person.punch = 1
                        person.stamina -= 0.6
                        person.stamina_regen_delay = 60 
                    else:
                        person.punch = 0
                    if held[pygame.K_s]:
                        person.dodging = True
                        person.stamina -= 0.6
                        person.stamina_regen_delay = 60
                    else:
                        person.dodging = False
            else:
                person.vx = 0
                person.punch = 0
                person.dodging = False

            if person.stamina_regen_delay > 0:
                person.stamina_regen_delay -= 1
            elif not person.punch and not person.dodging:
                person.stamina += 0.4
            if person.stamina > person.max_stamina:
                person.stamina = person.max_stamina
            if person.stamina < 0:
                person.stamina = 0
            person.update(screen)
        pygame.display.flip()
        fps_clock.tick(fps)

if __name__ == "__main__":
    main()