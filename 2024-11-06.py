import pygame, sys
from pygame.locals import *

# 라이브러리 초기화
pygame.init()

# 화면 설정
WIDTH = 700
HEIGHT = 600
DISPLAYSF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Title")

# 메인 함수
def main():
    col_arr = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    col = 0
    run = True
    player_pos = [300,250]
    
    while run:
        DISPLAYSF.fill((255, 255, 255))
        
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                col += 1
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player_pos[0] += 0.5
        elif keys[pygame.K_LEFT]:
            player_pos[0] -= 0.5
        elif keys[pygame.K_UP]:
            player_pos[1] -= 0.5
        elif keys[pygame.K_DOWN]:
            player_pos[1] += 0.5
            
        
        rect = pygame.Rect(player_pos[0], player_pos[1], 100, 100)
        pygame.draw.rect(DISPLAYSF, col_arr[col % 3], rect)  

        pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
