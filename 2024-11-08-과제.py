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
ball_a = 0
ball_size = 10

# 시간 및 점수 초기화 (사용되지 않거나 수정됨)
t = 0
tJump = 0
point = 0

# 벽 배열 초기화
wall_arr = []

# 메인 게임 루프
while run:
    # 프레임 레이트 설정 (60 FPS)
    clock.tick(60)
    # 화면 초기화
    display.fill((0, 0, 0))

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # 게임 종료
        elif event.type == pygame.KEYDOWN:

#직접 작성해보세요!_____________________________________________________________________
공 움직임 처리 과정

1.키를 누르면 공을 위로 가속

2. 키를 떼덴 중력 적용 예) 키를 늘면 공의 가속도를 -9.8로 정함 키를 떼면 공의 가속도를 9.8로 정함
(y좌표가 반대로 작용하기 때문)
(이벤트: pygame.KEYDOWN
               pygame.KEYUP)

3. 가속도에 따라 공의 속도 및 위치 업데이트
(공이 화면 밖으로 나가면 반대쪽에서 나타나도록 처리하면 더욱 좋아용)

4. 공 그리기(pygame.draw.circle0) 














    # 일정 시간마다 벽 생성
    if point % 30 == 0:
        # 벽은 화면 오른쪽 끝에서 생성되어 왼쪽으로 이동
        wall_x = WIDTH
        wall_y = random.randint(0, HEIGHT - 90)
        wall_size = random.randint(10, 90)
        wall_arr.append([wall_x, wall_y, wall_size])

    # 삭제할 벽의 인덱스를 저장할 리스트
    del_arr = []

    # 벽 이동 및 그리기
    for i in range(len(wall_arr)):
        wall = wall_arr[i]
        wall_rect = pygame.Rect(int(wall[0]), int(wall[1]), wall[2], wall[2])
        pygame.draw.rect(display, (255, 255, 255), wall_rect)
        wall[0] -= 10 # 벽을 왼쪽으로 이동

        # 공과 벽의 충돌 감지
        ball_rect = pygame.Rect(int(ball_pos[0] - ball_size), int(ball_pos[1] - ball_size), ball_size * 2, ball_size * 2)
        if ball_rect.colliderect(wall_rect):
            time.sleep(1) # 충돌 시 잠시 대기
            run = False # 게임 종료

        # 벽이 화면 밖으로 나가면 삭제 목록에 추가
        if wall[0] + wall[2] <= 0:
            del_arr.append(i)

    # 화면 밖으로 나간 벽 삭제
    for i in reversed(del_arr):
        del wall_arr[i]

    # 점수 증가 (현재는 프레임당 1점 증가)
    point += 1

    # 점수 표시
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(str(point), True, (255, 255, 255))
    display.blit(score_text, (100, 100))

    # 화면 업데이트
    pygame.display.update()

# 게임 종료 처리
pygame.quit()
sys.exit()
