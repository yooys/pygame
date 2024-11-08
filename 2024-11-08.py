import pygame, sys
from pygame.locals import *

# 라이브러리 초기화
pygame.init()

# 화면 설정
WIDTH = 700
HEIGHT = 600
DISPLAYSF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Title")
clock = pygame.time.Clock()

# 메인 함수
def main():
    col_arr = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    col = 0
    run = True
    ball_pos = [0, 500-100]
    jump = False
    t = 0
    
    while run:
        clock.tick(900)
        DISPLAYSF.fill((0, 0, 0))

        if ball_pos[1] >= 500 - 100:
            jump = False
            pygame.draw.line(DISPLAYSF, (255, 255, 255), (0,500), (700,500))
            
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                col += 1
            if event.type == pygame.KEYDOWN:
                col += 1
                if jump == False:
                    t = 0
                    jump = True
        if jump == True:
            t += 0.017
            ball_pos[1] = 500 - 100 + 0.5 * 9.8 * t ** 2 + (-100) * t
 
        keys = pygame.key.get_pressed()
        
        rect = pygame.Rect(ball_pos[0], ball_pos[1], 100, 100)
        pygame.draw.rect(DISPLAYSF, col_arr[col % 3], rect)
        pygame.display.update()
    

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
