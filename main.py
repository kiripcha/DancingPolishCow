import pygame
from ball import Ball
from random import randint
import time

pygame.mixer.pre_init(44100, -16, 1, 512)  # важно прописать до pygame.init()
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

pygame.mixer.music.load('sounds/Krowa.mp3')
pygame.mixer.music.play(-1)

s_catch = pygame.mixer.Sound('sounds/catch.ogg')
l_catch = pygame.mixer.Sound('sounds/krik.ogg')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
W, H = 900, 600
ground = H - 5
FPS = 60
game_score = 0
lives = 9

black = pygame.image.load('images/black.png')
g_rect = black.get_rect(centerx=W // 2, top=ground)

heart = pygame.image.load('images/heart.png')
final = pygame.image.load('images/final.png')

walkLeft = [pygame.image.load('images/l_0.png'), pygame.image.load('images/l_19.png'),
            pygame.image.load('images/l_1.png'), pygame.image.load('images/l_2.png'),
            pygame.image.load('images/l_3.png'), pygame.image.load('images/l_4.png'),
            pygame.image.load('images/l_5.png'), pygame.image.load('images/l_6.png'),
            pygame.image.load('images/l_7.png'), pygame.image.load('images/l_8.png'),
            pygame.image.load('images/l_9.png'), pygame.image.load('images/l_10.png'),
            pygame.image.load('images/l_11.png'), pygame.image.load('images/l_12.png'),
            pygame.image.load('images/l_13.png'), pygame.image.load('images/l_14.png'),
            pygame.image.load('images/l_15.png'), pygame.image.load('images/l_16.png'),
            pygame.image.load('images/l_17.png'), pygame.image.load('images/l_18.png'), ]

walkRight = [pygame.image.load('images/r_0.png'), pygame.image.load('images/r_19.png'),
             pygame.image.load('images/r_1.png'), pygame.image.load('images/r_2.png'),
             pygame.image.load('images/r_3.png'), pygame.image.load('images/r_4.png'),
             pygame.image.load('images/r_5.png'), pygame.image.load('images/r_6.png'),
             pygame.image.load('images/r_7.png'), pygame.image.load('images/r_8.png'),
             pygame.image.load('images/r_9.png'), pygame.image.load('images/r_10.png'),
             pygame.image.load('images/r_11.png'), pygame.image.load('images/r_12.png'),
             pygame.image.load('images/r_13.png'), pygame.image.load('images/r_14.png'),
             pygame.image.load('images/r_15.png'), pygame.image.load('images/r_16.png'),
             pygame.image.load('images/r_17.png'), pygame.image.load('images/r_18.png'), ]

pygame.display.set_caption("DancingPolishCow")
pygame.display.set_icon(pygame.image.load('images/cow_right.png'))
sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()

score = pygame.image.load('images/score_fon.png').convert_alpha()
f = pygame.font.SysFont('arial', 30)

cow = pygame.image.load('images/cow.png').convert_alpha()
cow = pygame.transform.scale(cow, (cow.get_width() // 2, cow.get_height() // 2))
t_rect = cow.get_rect(centerx=W // 2, bottom=ground)
cow_right = cow
cow_left = pygame.transform.flip(cow, 1, 0)

balls_data = ({'path': 'bottle_1.png', 'score': -500},
              {'path': 'bottle_2.png', 'score': 50},
              {'path': 'bottle_3.png', 'score': 200})

balls_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in balls_data]


def create_ball(group):
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Ball(x, speed, balls_surf[indx], balls_data[indx]['score'], group)

END = True
is_end = False

def collide_balls():
    global game_score, lives
    for ball in balls:
        if t_rect.collidepoint(ball.rect.center):
            s_catch.play()
            game_score += ball.score
            ball.kill()
        elif g_rect.collidepoint(ball.rect.center):
            l_catch.play()
            lives -= 3
            ball.kill()


balls = pygame.sprite.Group()

bg = pygame.image.load('images/back.jpg').convert()

speed = 10
jump = 20
tmp_jump = jump + 1
create_ball(balls)

left = False
right = False
animationCount = 0


def draw_window():
    global is_end, END, lives, animationCount

    sc.blit(heart, (0, 300))
    collide_balls()
    sc.blit(bg, (0, 0))
    sc.blit(score, (0, 0))
    sc_text = f.render(str(game_score), 1, (94, 138, 14))
    sc.blit(sc_text, (20, 10))

    tmp = lives // 3
    x = 150
    while tmp > 0:
        tmp -= 1
        sc.blit(heart, (x, 0))
        x += 50

    balls.draw(sc)
    if animationCount + 1 >= 120: # or FPS
        animationCount = 0
    if left:
        cow_tmp = walkLeft[animationCount // 6]
        sc.blit(pygame.transform.scale(cow_tmp, (cow_tmp.get_width() * 2.5, cow_tmp.get_height() * 2.5)), t_rect)
        animationCount += 1
    elif right:
        cow_tmp = walkRight[animationCount // 6]
        sc.blit(pygame.transform.scale(cow_tmp, (cow_tmp.get_width() * 2.5, cow_tmp.get_height() * 2.5)), t_rect)
        animationCount += 1
    else:
        sc.blit(cow, t_rect)

    if lives == 0:
        sc.blit(pygame.transform.scale(final, (final.get_width() // 1.25, final.get_height() // 1.5)), (0, 0))
        sc.blit(sc_text, (20, 10))
        is_end = True
    # сделать финальный экран с возможностью повторить игру. во время его отбражения, игра должна остановиться

    pygame.display.update()
    clock.tick(FPS)
    balls.update(H)
    if is_end:
        time.sleep(2)
        END = False


while END:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            create_ball(balls)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and t_rect.bottom == ground:
                tmp_jump = -jump

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not left:
            animationCount = 0
        left = True
        right = False
        cow = cow_left
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        if not right:
            animationCount = 0
        left = False
        right = True
        cow = cow_right
        t_rect.x += speed
        if t_rect.x > W - t_rect.width:
            t_rect.x = W - t_rect.width
    elif tmp_jump <= jump:
        if t_rect.bottom + tmp_jump < ground:
            t_rect.y += tmp_jump
            if tmp_jump < jump:
                tmp_jump += 1
        else:
            t_rect.bottom = ground
            tmp_jump = jump + 1

    draw_window()
