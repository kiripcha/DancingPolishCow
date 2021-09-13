import pygame
from ball import Ball
from random import randint

pygame.mixer.pre_init(44100, -16, 1, 512)  # важно прописать до pygame.init()
pygame.init()
pygame.time.set_timer(pygame.USEREVENT, 2000)

pygame.mixer.music.load('sounds/Krowa.mp3')
pygame.mixer.music.play(-1)

s_catch = pygame.mixer.Sound('sounds/catch.ogg')
l_catch = pygame.mixer.Sound('sounds/krik.ogg')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
W, H = 1200, 900
ground = H-5

black = pygame.image.load('images/black.png')
g_rect = black.get_rect(centerx=W // 2, top=ground)

heart = pygame.image.load('images/heart.png')
final = pygame.image.load('images/final.png')

pygame.display.set_caption("DancingPolishCow")
pygame.display.set_icon(pygame.image.load('images/cow_right.png'))
sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60

score = pygame.image.load('images/score_fon.png').convert_alpha()
f = pygame.font.SysFont('arial', 30)

cow = pygame.image.load('images/cow.png').convert_alpha()
cow = pygame.transform.scale(cow, (cow.get_width()//2, cow.get_height()//2))
t_rect = cow.get_rect(centerx=W // 2, bottom=ground)
cow_right = cow
cow_left = pygame.transform.flip(cow, 1, 0)

balls_data = ({'path': 'bottle_1.png', 'score': -100},
              {'path': 'bottle_2.png', 'score': 50},
              {'path': 'bottle_3.png', 'score': 200})

balls_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in balls_data]


def createBall(group):
    indx = randint(0, len(balls_surf) - 1)
    x = randint(20, W - 20)
    speed = randint(1, 4)

    return Ball(x, speed, balls_surf[indx], balls_data[indx]['score'], group)


game_score = 0
lives = 9

def collideBalls():
    global game_score
    global lives
    for ball in balls:
        if t_rect.collidepoint(ball.rect.center):
            s_catch.play()
            game_score += ball.score
            ball.kill()
        elif g_rect.collidepoint(ball.rect.center):
            l_catch.play()
            lives -= 1


balls = pygame.sprite.Group()

bg = pygame.image.load('images/back.jpg').convert()

speed = 10
jump = 20
tmp_jump = jump + 1
createBall(balls)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createBall(balls)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and t_rect.bottom == ground:
                tmp_jump = -jump

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cow = cow_left
        t_rect.x -= speed
        if t_rect.x < 0:
            t_rect.x = 0
    elif keys[pygame.K_RIGHT]:
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


    sc.blit(heart, (0, 300))
    collideBalls()
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

    # if lives == 0:
    #     sc.blit(final, (0, 0))
# сделать финальный экран с возможностью повторить игру. во время его отбражения, игра должна остановиться

    balls.draw(sc)
    sc.blit(cow, t_rect)
    pygame.display.update()

    clock.tick(FPS)

    balls.update(H)
