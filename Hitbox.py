import sys

import pygame
import pygame.locals
WIDTH = HEIGHT = 1000

class boxer:
    def __init__(self, x, handle, controls=None, color=(60, 120, 255)):
        self.x = x
        self.y = 500
        self.vx = 0
        self.vy = 0
        self.on_ground = True

        self.color = color
        self.facing = handle 

        self.max_health = 100
        self.health = 100

        self.max_stamina = 100
        self.stamina = 100

        self.dodging = False

        self.hurtbox = (self.x-10, self.y-10, 120, 220)
        self.hitbox = None
        self.hitstun = 0

        self.attack_time = 0
        self.attack_duration = 30
        self.attack_cooldown = 0
        self.attack_cooldown_duration = 50

        self.attack_type = None  # "light" or "heavy"

        self.controls = controls
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,100,200))
        self.hurtbox = (self.x-10, self.y-10, 120, 220)
        pygame.draw.rect(screen, (0,0,0), self.hurtbox, 1,2)

        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y - 45, 100, 10))
        health_width = int((self.health / self.max_health) * 100)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 45, health_width, 10))

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
        if self.attack_time > 0:
            self.vx = 0

        if (self.x + self.vx)>0 and (self.x + self.vx+100<=1010):
            self.x += self.vx

        if self.attack_time > 0:
            self.attack_time -= 1

            if self.facing == 1:
                pygame.draw.rect(screen,"#FFFF00", (self.x+100, self.y +60, 50,30))

                self.hitbox = (self.x + 95, self.y +55, 60,40)
                pygame.draw.rect(screen, (0,0,0),(self.hitbox),1,2)
            elif self.facing ==-1:
                pygame.draw.rect(screen,"#FFFF00", (self.x-50, self.y +60, 50,30))

                self.hitbox = (self.x - 55, self.y +55, 60,40)
                pygame.draw.rect(screen, (0,0,0),(self.hitbox),1,2)
            
        else:
            self.hitbox = None
            self.attack_type = None

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

def collision(box1, box2):
    if box1.hitbox and box2.hurtbox:
        x1, y1, w1, h1 = box1.hitbox
        x2, y2, w2, h2 = box2.hurtbox
        
        if (x1 < x2 + w2 and x1 + w1 > x2 and 
            y1 < y2 + h2 and y1 + h1 > y2):
            
            if box1.attack_type == "light":
                damage = 5
            else:  
                damage = 15
            
            box2.health = max(0, box2.health - damage)
            box1.hitbox = None  
            box1.attack_time = 0
            box1.attack_type = None
            return True
    return False

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    box1 = boxer(100,1,controls={
        "left1": pygame.K_a,
        "right1": pygame.K_d,
        "L_punch1": pygame.K_w,
        "H_punch1": pygame.K_e,
        "dodge1": pygame.K_s,
    })

    box2 = boxer(800,-1,controls = {
        "left2": pygame.K_LEFT,
        "right2": pygame.K_RIGHT,
        "L_punch2": pygame.K_UP,
        "H_punch2": pygame.K_RSHIFT,
        "dodge2": pygame.K_DOWN,
    }, color = (0,255,255))

    speed = 10

    while True:
        screen.fill("#ffffff")
        pygame.draw.rect(screen, "#7B2E16",(0,700,1000,200))
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()

        held = pygame.key.get_pressed()
       
        if box1.attack_time == 0:
            if held[box1.controls["right1"]]:
                box1.vx=speed
                box1.facing = 1
            elif held[box1.controls["left1"]]:
                box1.vx=-speed
                box1.facing=-1
            else:
                box1.vx=0

        if held[box1.controls["L_punch1"]]:
            box1.punch("light")
        if held[box1.controls["H_punch1"]]:
            box1.punch("heavy")
        
        if box2.attack_time == 0:
            if held[box2.controls["right2"]]:  
                box2.vx = speed
                box2.facing = 1
            elif held[box2.controls["left2"]]:  
                box2.vx = -speed
                box2.facing = -1
            else:
                box2.vx = 0

        if held[box2.controls["L_punch2"]]:  
            box2.punch("light")
        if held[box2.controls["H_punch2"]]:
            box2.punch("heavy")

        box1.update(screen)
        box1.draw(screen)

        box2.update(screen)
        box2.draw(screen)

        collision(box1,box2)
        collision(box2,box1)

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()