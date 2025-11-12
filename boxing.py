import sys

import pygame
import pygame.locals
WIDTH = HEIGHT = 1000

class boxer:
    def __init__(self, x, handle, facing, color):
        self.x = x
        self.y = 500
        self.vx = 4
        self.acc=0.1
        self.punch=0

        self.color = color

        self.max_health = 100
        self.health = 100

        self.max_stamina = 100
        self.stamina = 100

        self.handle=handle
        self.facing=facing

        self.dodging = False

        self.hurtbox = None
        self.hitbox = None
        self.hitstun = 0

        self.attack_windup = 0
        self.attack_type = None  
    
    def update(self, screen: pygame.surface):
        if self.vx>7:
            self.vx=6
        if (self.x + self.vx)>0 and (self.x + self.vx+100<=WIDTH):
            self.x += self.vx
        minus=0
        if self.dodging:
            minus = 5

        pygame.draw.rect(screen, "#FFFFFF" , (self.x-25,self.y-50,150,25))
        pygame.draw.rect(screen, "#FF0000" , (self.x-20,self.y-45,140,15))
        pygame.draw.rect(screen, self.color , (self.x,self.y+minus,100,200-minus))

        if self.punch == 0:
            pygame.draw.rect(screen, "#E03BA6", (self.x+25, self.y+50, 50,100))
        elif self.facing == 1:
            self.hitbox = (self.x + 50, self.y +50, 100,50)
            pygame.draw.rect(screen, "#E03BA6", self.hitbox)
        elif self.facing == -1:
            self.hitbox = (self.x - 50, self.y +50, 100,50)
            pygame.draw.rect(screen, "#E03BA6", self.hitbox)

def collision(box1,box2):
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
    fps = 120
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    box1 = boxer(1,1,1,"#49E03B")
    box2 = boxer(WIDTH-100,0,-1,"#672EBC")
    boxers=[]
    boxers.append(box1)
    boxers.append(box2)

    while True:
        screen.fill("#000000")
        pygame.draw.rect(screen, "#7B2E16",(0,700,1000,200))
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                sys.exit()
            box1.update(screen)
            box2.update(screen)

        held = pygame.key.get_pressed()
        for person in boxers:
            if person.handle==0:
                if held[pygame.K_RIGHT]:
                    person.vx+=person.acc
                    person.facing == 1
                elif held[pygame.K_LEFT]:
                    person.vx-=person.acc
                    person.facing==-1
                else:
                    person.vx=0
                if held[pygame.K_UP]:
                    person.punch=1
                else:
                    person.punch=0
                if held[pygame.K_DOWN]:
                    person.dodging=True
                else:
                    person.dodging=False
            elif person.handle==1:
                if held[pygame.K_d]:
                    person.vx+=person.acc
                    person.facing = 1
                elif held[pygame.K_a]:
                    person.vx-=person.acc
                    person.facing = -1
                else:
                    person.vx=0
                if held[pygame.K_w]:
                    person.punch=1
                else:
                    person.punch=0
                if held[pygame.K_s]:
                    person.dodging=True
                else:
                    person.dodging=False
            person.update(screen)
        pygame.display.flip()
        fps_clock.tick(fps)


if __name__ == "__main__":
    main()