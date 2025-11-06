import pygame
import random
import math

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Parry Game")

# 색상
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)

font = pygame.font.SysFont(None, 36)

# 배경 이미지 불러오기
background = pygame.image.load("우주배경1.PNG")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# 플레이어
player_size = 50  
player_pos = [WIDTH // 2, HEIGHT // 2]
player_radius = player_size // 2

# 지구 이미지 
earth_image = pygame.image.load("지구.png").convert_alpha()
earth_image = pygame.transform.scale(earth_image, (player_size, player_size))

# 패링 범위
parry_range = 120
range_reduced = False  

# 투사체
projectiles = []
PROJECTILE_SPEED = 4
SPAWN_INTERVAL = 1000
last_spawn_time = 0

meteor_image = pygame.image.load("운석.png").convert()
meteor_image.set_colorkey((255, 255, 255)) 
meteor_size = 32
meteor_image = pygame.transform.scale(meteor_image, (meteor_size, meteor_size))

# 변수
score = 0
hp = 5
last_space_pressed = False
PARRY_COOLDOWN = 200  
last_parry_time = 0

# 시간 관련
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()  

# 게임 루프
while running:
    dt = clock.tick(60)
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 10초 후 패링 범위 감소
    if not range_reduced and elapsed_time >= 10:
        parry_range = int(parry_range * 0.8)  
        range_reduced = True  
        print(f"⚠️ 패링 범위 감소! 현재 범위: {parry_range}")

    # 투사체 생성
    if current_time - last_spawn_time > SPAWN_INTERVAL:
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x, y = random.randint(0, WIDTH), 0
        elif side == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT
        elif side == "left":
            x, y = 0, random.randint(0, HEIGHT)
        else:
            x, y = WIDTH, random.randint(0, HEIGHT)

        dx, dy = player_pos[0] - x, player_pos[1] - y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        projectiles.append({
            "x": x, "y": y, "dx": dx, "dy": dy, "reversed": False
        })
        last_spawn_time = current_time
        
    # 투사체 이동
    for p in projectiles:
        p["x"] += p["dx"] * PROJECTILE_SPEED
        p["y"] += p["dy"] * PROJECTILE_SPEED
        
    # 패링 입력
    parry_pressed = keys[pygame.K_SPACE] and not last_space_pressed
    if parry_pressed and current_time - last_parry_time > PARRY_COOLDOWN:
        parry_success = False
        for p in projectiles:
            dist = math.hypot(p["x"] - player_pos[0], p["y"] - player_pos[1])
            if dist < parry_range and not p["reversed"]:
                p["dx"] *= -1
                p["dy"] *= -1
                p["reversed"] = True
                parry_success = True
                score += 1  
        if not parry_success:
            hp -= 1  
        last_parry_time = current_time

    last_space_pressed = keys[pygame.K_SPACE]

    # 투사체 충돌 (HP 감소)
    for p in projectiles:
        dist = math.hypot(p["x"] - player_pos[0], p["y"] - player_pos[1])
        if dist < player_radius and not p["reversed"]:
            hp -= 1
            projectiles.remove(p)
            break

    # 화면 그리기
    screen.blit(background, (0, 0))

    # 지구 (플레이어)
    screen.blit(earth_image, (player_pos[0] - player_radius, player_pos[1] - player_radius))

    # 패링 범위 원
    pygame.draw.circle(screen, (255, 255, 0), player_pos, parry_range, 2)

    # 운석 (투사체)
    for p in projectiles:
        meteor_rect = meteor_image.get_rect(center=(int(p["x"]), int(p["y"])))
        screen.blit(meteor_image, meteor_rect)

    # 점수 / HP / 시간 표시
    score_text = font.render(f"Score: {score}", True, WHITE)
    hp_text = font.render(f"HP: {hp}", True, WHITE)
    time_text = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
    screen.blit(score_text, (20, 20))
    screen.blit(hp_text, (20, 60))
    screen.blit(time_text, (20, 100))

    # 게임 오버
    if hp <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()

pygame.quit()
