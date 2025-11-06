import pygame

class boxer:
    def __init__(self, x, height, controls=None, color=(60, 120, 255), facing=1):
        self.x = x
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.on_ground = True

        self.color = color
        self.facing = facing 

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
