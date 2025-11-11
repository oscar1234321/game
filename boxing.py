import sys

import pygame
import pygame.locals
WIDTH = HEIGHT = 1000

class boxer:
    def __init__(self, x, handle, color):
        self.x = x
        self.y = 500
        self.vx = 4
        self.handle=handle
        self.acc=0.1
        self.punch=0

        self.color = color

        self.max_health = 100
        self.health = 100

        self.max_stamina = 100
        self.stamina = 100

        self.dodging = False

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
            minus = 50
        pygame.draw.rect(screen, "#FFFFFF" , (self.x-25,self.y-50,150,25))
        pygame.draw.rect(screen, "#FF0000" , (self.x-20,self.y-45,140,15))
        pygame.draw.rect(screen, self.color , (self.x,self.y+minus,100,200-minus))
        if self.vx==0 and self.punch==0:
            pygame.draw.rect(screen, "#E03BA6", (self.x+25, self.y+50, 50,100))
        elif self.vx>0 and self.punch==1:
            pygame.draw.rect(screen, "#E03BA6", (self.x+50, self.y+50, 100,50))
        elif self.punch==1:
            pygame.draw.rect(screen, "#E03BA6", (self.x+50-100, self.y+50, 100,50))

def main():
    fps = 120
    fps_clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    box1 = boxer(1,1,"#49E03B")
    box2 = boxer(WIDTH-100,0,"#672EBC")
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
                elif held[pygame.K_LEFT]:
                    person.vx-=person.acc
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
                elif held[pygame.K_a]:
                    person.vx-=person.acc
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