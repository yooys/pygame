import pygame
import sys
import random
import time
from pygame.locals import *

# Pygame 초기화
pygame.init()

# 화면 크기 설정
WIDTH = 1000
HEIGHT = 600

# 디스플레이 생성 및 설정
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Title")
clock = pygame.time.Clock()

# 색상 배열 (사용되지 않음)
col_arr = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
col = 0

# 게임 실행 여부 플래그
run = True

# 카메라 위치 (사용되지 않음)
cam_pos = [0, 0]

# 공의 초기 위치, 속도, 가속도, 크기 설정
ball_pos = [100, 300]
ball_v = 0
ball_a = 0.5
ball_size = 10

# 시간 및 점수 초기화 (사용되지 않거나 수정됨)
t = 0
tJump = 0
point = 0

# 벽 배열 초기화
wall_arr = []

key_pressed = False

# 메인 게임 루프
while run:
    clock.tick(60)
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                key_pressed = True
                ball_v = -6.7  # 점프 강도를 3분의 2로 낮춤
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                key_pressed = False

    if key_pressed:
        ball_v -= 0.2
    else:
        ball_v += ball_a

    ball_pos[1] += ball_v

    # 바닥에 닿았을 때 탄성 효과 추가
    if ball_pos[1] >= HEIGHT - ball_size:
        ball_pos[1] = HEIGHT - ball_size
        ball_v = -ball_v * 0.7

    # 천장에 닿았을 때
    if ball_pos[1] <= ball_size:
        ball_pos[1] = ball_size
        ball_v = -ball_v * 0.7

    # 공 그리기
    pygame.draw.circle(display, (255, 0, 0), (int(ball_pos[0]), int(ball_pos[1])), ball_size)

    if point % 30 == 0:
        wall_x = WIDTH
        wall_y = random.randint(0, HEIGHT - 90)
        wall_size = random.randint(10, 90)
        wall_arr.append([wall_x, wall_y, wall_size])

    del_arr = []

    for i in range(len(wall_arr)):
        wall = wall_arr[i]
        wall_rect = pygame.Rect(int(wall[0]), int(wall[1]), wall[2], wall[2])
        pygame.draw.rect(display, (255, 255, 255), wall_rect)
        wall[0] -= 10

        ball_rect = pygame.Rect(int(ball_pos[0] - ball_size), int(ball_pos[1] - ball_size), ball_size * 2, ball_size * 2)
        if ball_rect.colliderect(wall_rect):
            time.sleep(1)
            run = False

        if wall[0] + wall[2] <= 0:
            del_arr.append(i)

    for i in reversed(del_arr):
        del wall_arr[i]

    point += 1

    font = pygame.font.SysFont(None, 30)
    score_text = font.render(str(point), True, (255, 255, 255))
    display.blit(score_text, (100, 100))

    pygame.display.update()

pygame.quit()
sys.exit()

