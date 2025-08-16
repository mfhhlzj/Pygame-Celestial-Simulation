import pygame
import math
import scipy
import random

pygame.init()#创建窗口

DISPLAY:pygame.Vector2 = pygame.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)
FPS = 60
offset:pygame.Vector2 = pygame.Vector2(0, 0)
scaling_ratio:float = 1274200
window_size:pygame.Vector2 = pygame.Vector2(DISPLAY.x*scaling_ratio, DISPLAY.y*scaling_ratio)

class Circle:
    r:float = 0
    m:float = 0
    color:tuple[int, int, int] = (0, 0, 0)
    pos:pygame.Vector2 = pygame.Vector2(0, 0)
    speed:pygame.Vector2 = pygame.Vector2(0, 0)
    is_show:bool = False
    join_compute:bool = False

    def __init__(self, r:float, m:float, color:tuple[int, int, int], pos:pygame.Vector2|None=None, speed:pygame.Vector2|None=None, is_show:bool = False, join_com:bool = True):
        self.r = abs(r)
        self.m = m
        self.color = color
        if pos is None:
            self.pos = pygame.Vector2(offset.x + m_random(0, int(window_size.x)), offset.y + m_random(0, int(window_size.y)))
        else:
            self.pos = pos
        if speed is None:
            self.speed = pygame.Vector2(0, 0)
        else:
            self.speed = speed
        self.is_show = is_show
        self.join_compute = join_com

    def show(self, screen:pygame.Surface) -> None:
        if not self.is_show:
            return
        win_pos:pygame.Vector2 = pygame.Vector2(self.pos.x - offset.x, self.pos.y-offset.y)
        if win_pos.x + self.r < 0 or win_pos.y + self.r < 0 or win_pos.x - self.r > window_size.x or win_pos.y - self.r > window_size.y:
            return
        pygame.draw.circle(screen, self.color, pygame.Vector2(win_pos.x/scaling_ratio, win_pos.y/scaling_ratio), self.r/scaling_ratio)

    def add_speed(self, spd:pygame.Vector2) -> None:
        self.speed += spd

    def move(self) -> None:
        self.pos += self.speed

circle_list:list[Circle] = []

def m_random(a:int, b:int) -> float:
    return random.randint(a, b+1) if random.randint(0, 2) == 0 else (random.randint(a, b)+random.random())

#万有引力公式  F=G*(m1m2)/r^2
def f_g(m1: float,m2: float,d_pos:pygame.Vector2) -> pygame.Vector2:
    R2 = math.pow(d_pos.x, 2)+math.pow(d_pos.y, 2)
    R = math.sqrt(R2)
    F = scipy.constants.G*(m1*m2)/R2
    return pygame.Vector2(F*(d_pos.x/R), F*(d_pos.y/R))

def compute(c1:Circle, c2:Circle) -> None:
    if not c1.join_compute or not c2.join_compute:
        return
    if(c1.pos == c2.pos):
        return
    f = f_g(c1.m, c2.m, c1.pos - c2.pos)
    c2.add_speed(pygame.Vector2(f[0]/c2.m, f[1]/c2.m))
    c1.add_speed(pygame.Vector2(-f[0]/c1.m, -f[1]/c1.m))

def add_circle(r:float, m: float, color:tuple[int, int, int], pos:pygame.Vector2|None = None, speed:pygame.Vector2|None=None, *, is_show:bool = False, join_com:bool = True) -> None:
    circle_list.append(Circle(r, m, color, pos, speed, is_show, join_com))

def add_circle_DisplayPos(r: float, m: float, color: tuple[int, int, int], pos: pygame.Vector2|None = None, speed: pygame.Vector2|None = None, *, is_show:bool = False, join_com:bool = True) -> None:
    _pos:pygame.Vector2|None = pos
    _spd:pygame.Vector2|None = speed
    if pos is not None:
        _pos = pygame.Vector2(offset.x + pos.x*scaling_ratio, offset.y + pos.y*scaling_ratio)
    if speed is not None:
        _spd = pygame.Vector2(speed.x*scaling_ratio, speed.y*scaling_ratio)
    circle_list.append(Circle(r*scaling_ratio, m, color, _pos, _spd, is_show, join_com))
def camera_move() -> None:
    global window_size, scaling_ratio
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        offset.y -= 10*scaling_ratio
    if keys[pygame.K_s]:
        offset.y += 10*scaling_ratio
    if keys[pygame.K_a]:
        offset.x -= 10*scaling_ratio
    if keys[pygame.K_d]:
        offset.x += 10*scaling_ratio
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scaling_ratio *= 0.9
            if event.button ==5:
                scaling_ratio *= 1.1
    window_size = pygame.Vector2(DISPLAY.x*scaling_ratio, DISPLAY.y*scaling_ratio)

def main():
    screen=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    #球1
    add_circle(69_550_000, 1_989_100_000_000_000_000_000_000_000_000, (0xff, 0, 0), pygame.Vector2(-1*scaling_ratio, 540*scaling_ratio), is_show=True)

    #球2
    add_circle(6_371_000, 5_972_168_000_000_000_000_000_000, (0 ,0xff, 0), pygame.Vector2(960*scaling_ratio-149598023,540*scaling_ratio), pygame.Vector2(0,496.384), is_show=True)
    
    while True :
        keys = pygame.key.get_pressed()

        screen.fill((0, 0, 0))

        for circle in circle_list:
            circle.show(screen)

        for i in range(len(circle_list)-1):
            for j in range(i+1, len(circle_list)):
                compute(circle_list[i], circle_list[j])

        for circle in circle_list:
            circle.move()

        #结束
        if keys[pygame.K_ESCAPE] :
            break
        if pygame.event.get(pygame.QUIT):
            break
        
        camera_move()
        
        pygame.display.flip()#渲染画面
        clock.tick(FPS)#游戏刻

if __name__ == "__main__":
    main()

pygame.quit()