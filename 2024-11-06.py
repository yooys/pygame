import pygame, sys
from pygame.locals import *

#라이브러리 초기화
pygame.init()

#화면 설정
WIDTH = 700
HEIGHT = 600
DISPLAYSF = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_captinon("Title")

#메인 함수
def main():
    col_arr = [(255, 0 , 0), (0, 255 , 0), (0, 0 , 255)]
    col = 0
    run = True
    
    while run:
        DISPLAYSF.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            col += 1
    
    rect = pygame.Rect(300, 250, 100, 100)
    pygame.draw.rect(DISPLAYSE, col_arr[col % 3], rect)

    pygame.display.update()

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
