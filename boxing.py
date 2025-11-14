import sys
import pygame
import pygame.locals

WIDTH = HEIGHT = 1000
boxer1 = pygame.image.load('fighter1.png')

class boxer:
    def __init__(self, x, handle, facing, color, image):
        self.x = x
        self.y = 500
        # self.vx = 4
        self.vx=0
        self.image=image

        self.handle = handle
        # self.acc = 0.1
        self.speed = 8
        self.punch_pos = 0

        self.color = color

        self.max_health = 100
        self.health = 100
        self.lives = 3

        self.max_stamina = 100
        self.stamina = 100
        self.stamina_regen_delay = 0

        self.handle=handle
        self.facing=facing

        self.dodging = False
        self.dodge_timer = 0

        self.hurtbox = None
        self.hitbox = None
        self.hitstun = 0

        self.attack_time = 0
        self.attack_duration = 30
        self.attack_cooldown = 0
        self.attack_cooldown_duration = 50

        self.attack_type = None

        self.light_pressed = False
        self.heavy_pressed = False

        self.knockback_velocity = 0
        self.knockback_duration = 0

    def punch(self, punch_type):
        if self.attack_time == 0 and self.attack_cooldown == 0:
            self.attack_type = punch_type
                
            if punch_type == "light":
                self.attack_duration = 25  # Faster
                self.attack_cooldown_duration = 40  # Shorter cooldown
            elif punch_type == "heavy":
                self.attack_duration = 50  # Slower
                self.attack_cooldown_duration = 60  # Lo

            self.attack_time = self.attack_duration
            self.attack_cooldown = self.attack_cooldown_duration
        
    def update(self, screen: pygame.surface):
        # if self.vx > 7:
        #     self.vx = 6
        # if (self.x + self.vx) > 0 and (self.x + self.vx + 100 <= WIDTH):
        #     self.x += self.vx
        # minus = 0
        # if self.dodging:
        #     minus = 50

        if self.knockback_duration > 0:
            if (self.x + self.knockback_velocity) > 0 and (self.x + self.knockback_velocity + 100 <= WIDTH):
                self.x += self.knockback_velocity
            self.knockback_duration -= 1
        elif (self.x + self.vx) > 0 and (self.x + self.vx + 100 <= WIDTH):
            self.x += self.vx
        minus = 0
        if self.dodging:
            minus = 50

        self.hurtbox = (self.x, self.y + minus, 150, 200 - minus)
        self.image=pygame.transform.scale(self.image, (150,200-minus))
        screen.blit(self.image, (self.x,self.y+minus))
        
        health_ratio = self.health / self.max_health
        stamina_ratio = self.stamina / self.max_stamina

        if self.handle == 1:
            pygame.draw.rect(screen, "#FFFFFF", (20, 80, 250, 40))
            pygame.draw.rect(screen, "#0000FF", (20, 105, 250 * stamina_ratio, 10))

            pygame.draw.rect(screen, "#FFFFFF", (20, 75, 400, 25))
            pygame.draw.rect(screen, "#FF0000", (20, 75, 400 * health_ratio, 25))
        
        else:
            pygame.draw.rect(screen, "#FFFFFF", (730, 80, 250, 40))
            stamina_width = 250 * stamina_ratio
            pygame.draw.rect(screen, "#0000FF", (980-stamina_width, 105, stamina_width, 10))

            pygame.draw.rect(screen, "#FFFFFF", (580, 75, 400, 25))
            health_width = 400 * health_ratio
            pygame.draw.rect(screen, "#FF0000", (980-health_width, 75, health_width, 25))

        self.image=pygame.transform.scale(self.image, (150,200-minus))
        screen.blit(self.image, (self.x,self.y+minus))
        # pygame.draw.rect(screen, self.color, (self.x, self.y + minus, 100, 200 - minus))

        if self.punch_pos == 0:
            pygame.draw.rect(screen, "#E03BA6", (self.x+50, self.y+50, 50,100))
        elif self.facing == 1:
            self.hitbox = (self.x + 50, self.y +50, 100,50)
            pygame.draw.rect(screen, "#E03BA6", self.hitbox)
        elif self.facing == -1:
            self.hitbox = (self.x - 50, self.y +50, 100,50)
            pygame.draw.rect(screen, "#E03BA6", self.hitbox)

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

def collision(box1,box2):
    if box1.hitbox and box2.hurtbox and not box2.dodging:
        x1, y1, w1, h1 = box1.hitbox
        x2, y2, w2, h2 = box2.hurtbox
        
        if (x1 < x2 + w2 and x1 + w1 > x2 and 
            y1 < y2 + h2 and y1 + h1 > y2):
            
            if box1.attack_type == "light":
                damage = 5
                knockback = 3
                knockback_frames = 10
            else:  
                damage = 15
                knockback = 8
                knockback_frames = 20
    
            knockback_direction = 1 if box2.x > box1.x else -1
            box2.knockback_velocity = knockback * knockback_direction
            box2.knockback_duration = knockback_frames

            box2.health = max(0, box2.health - damage)

            box1.hitbox = None  
            box1.punch_pos = 0
            box1.attack_time = 0
            box1.attack_type = None
            return True
    return False

def main():
    fps = 120
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    box1 = boxer(1,1,1,"#49E03B", boxer1)
    box2 = boxer(WIDTH-100,0,-1,"#672EBC", boxer1)
    boxers=[box1,box2]


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
                if person.attack_time == 0:
                    if person.handle == 0:
                        if held[pygame.K_RIGHT]:
                            # person.vx += person.acc
                            person.vx = person.speed
                            person.facing = 1
                        elif held[pygame.K_LEFT]:
                            # person.vx -= person.acc
                            person.vx = -person.speed
                            person.facing = -1
                        else:
                            person.vx = 0
                        
                        if held[pygame.K_UP]:
                            if not person.light_pressed:
                                person.punch("light")
                                person.punch_pos = 1
                                person.stamina -= 2
                                person.stamina_regen_delay = 60 
                                person.light_pressed = True
                        else:
                            person.light_pressed = False

                        if held[pygame.K_RSHIFT]:
                            if not person.heavy_pressed:
                                person.punch("heavy")
                                person.punch_pos = 1
                                person.stamina -= 4
                                person.stamina_regen_delay = 60
                                person.heavy_pressed = True
                        else:
                            person.heavy_pressed = False
                        
                        if not held[pygame.K_UP] and not held[pygame.K_RSHIFT]:
                            person.punch_pos = 0

                        if held[pygame.K_DOWN]:
                            person.dodging = True
                            person.stamina -= 0.6
                            person.stamina_regen_delay = 60
                        else:
                            person.dodging = False

                    elif person.handle == 1:
                        if held[pygame.K_d]:
                            # person.vx += person.acc
                            person.vx = person.speed
                            person.facing = 1
                        elif held[pygame.K_a]:
                            # person.vx -= person.acc
                            person.vx = -person.speed
                            person.facing = -1
                        else:
                            person.vx = 0

                        if held[pygame.K_w]:
                            if not person.light_pressed:
                                person.punch("light")
                                person.punch_pos = 1
                                person.stamina -= 2
                                person.stamina_regen_delay = 60 
                                person.light_pressed = True
                        else:
                            person.light_pressed = False

                        if held[pygame.K_e]:
                            if not person.heavy_pressed:
                                person.punch("heavy")
                                person.punch_pos=1
                                person.stamina -= 4
                                person.stamina_regen_delay = 60 
                                person.heavy_pressed = True
                        else:
                            person.heavy_pressed = False
                        
                        if not held[pygame.K_w] and not held[pygame.K_e]:
                            person.punch_pos = 0

                        if held[pygame.K_s]:
                            person.dodging = True
                            person.stamina -= 0.6
                            person.stamina_regen_delay = 60
                        else:
                            person.dodging = False
                else:
                    person.vx = 0
                    person.dodging = False

            else:
                person.vx = 0
                person.punch_pos = 0
                person.dodging = False

            if person.attack_time == 1:
                person.vx = 0

            if person.attack_time > 0:
                person.attack_time -= 1
                if person.attack_time == 0:
                    person.punch_pos = 0
                    person.hitbox = None
                    person.attack_type = None
            
            if person.attack_cooldown > 0:
                person.attack_cooldown -= 1

            if person.stamina_regen_delay > 0:
                person.stamina_regen_delay -= 1
            elif not person.punch_pos and not person.dodging:
                person.stamina += 0.4
            if person.stamina > person.max_stamina:
                person.stamina = person.max_stamina
            if person.stamina < 0:
                person.stamina = 0
            person.update(screen)
        
        collision(box1, box2)
        collision(box2, box1)

        pygame.display.flip()
        fps_clock.tick(fps)

if __name__ == "__main__":
    main()