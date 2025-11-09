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


        # controls mapping for human
        self.controls = controls
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,100,200))
        
        self.hurtbox = (self.x-10, self.y-10, 120, 220)

        pygame.draw.rect(screen, (0,0,0), self.hurtbox, 1,2)

    def punch(self):
        if self.attack_time == 0 and self.attack_cooldown == 0:
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

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    box1 = boxer(100,1,controls={
        "left1": pygame.K_a,
        "right1": pygame.K_d,
        "punch1": pygame.K_w,
        "dodge1": pygame.K_s,
    })

    box2 = boxer(800,-1,controls = {
        "left2": pygame.K_LEFT,
        "right2": pygame.K_RIGHT,
        "punch2": pygame.K_UP,
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

        if held[box1.controls["punch1"]]:
            box1.punch()
        
        if box2.attack_time == 0:
            if held[box2.controls["right2"]]:  
                box2.vx = speed
                box2.facing = 1
            elif held[box2.controls["left2"]]:  
                box2.vx = -speed
                box2.facing = -1
            else:
                box2.vx = 0

        if held[box2.controls["punch2"]]:  
            box2.punch()

        box1.update(screen)
        box1.draw(screen)

        box2.update(screen)
        box2.draw(screen)

        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()