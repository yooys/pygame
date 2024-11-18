import pygame
import random
import pyautogui
from pygame.locals import *

class Tiles:
    # 다양한 변수를 초기화하는 메인 메서드
    def __init__(self, screen, start_position_x, 
                 start_position_y, num, mat_pos_x, mat_pos_y):
        self.color = (0, 255, 0)  # 타일의 기본 색상 (초록색)
        self.screen = screen  # 타일이 그려질 화면
        self.start_pos_x = start_position_x  # 타일의 초기 x 위치
        self.start_pos_y = start_position_y  # 타일의 초기 y 위치
        self.num = num  # 타일에 표시될 번호
        self.width = tile_width  # 타일의 너비
        self.depth = tile_depth  # 타일의 높이
        self.selected = False  # 타일이 선택되었는지 여부
        self.position_x = mat_pos_x  # 매트릭스에서의 x 위치
        self.position_y = mat_pos_y  # 매트릭스에서의 y 위치
        self.movable = False  # 타일이 이동 가능한지 여부

    # 타일을 그리는 메드서
    def draw_tyle(self):
        pygame.draw.rect(
            self.screen, self.color, 
            pygame.Rect(self.start_pos_x, self.start_pos_y, self.width, self.depth)
        )  # 타일 사각형 그리기
        numb = font.render(str(self.num), True, (125, 55, 100))  # 번호를 타일에 렌더링
        screen.blit(numb, (self.start_pos_x + 40, self.start_pos_y + 10))  # 타일에 번호 표시

    # 마우스가 타일 위에 있을 때 색상을 변경하는 메서드
    def mouse_hover(self, x_m_motion, y_m_motion):
        if x_m_motion > self.start_pos_x and x_m_motion < self.start_pos_x + self.width and \
           y_m_motion > self.start_pos_y and y_m_motion < self.start_pos_y + self.depth:
            self.color = (255, 255, 255)  # 마우스가 타일 위에 있으면 흰색으로 변경
        else:
            self.color = (255, 165, 0)  # 마우스가 벗어나면 주황색으로 변경

    # 마우스 클릭 시 타일이 선택되었는지 확인하는 메서드
    def mouse_click(self, x_m_click, y_m_click):
        if x_m_click > self.start_pos_x and x_m_click < self.start_pos_x + self.width and \
           y_m_click > self.start_pos_y and y_m_click < self.start_pos_y + self.depth:
            self.selected = True  # 클릭된 타일을 선택 상태로 설정
        else:
            self.selected = False  # 클릭되지 않으면 선택 해제

    # 마우스 클릭 해제 시 타일 선택을 해제하는 메서드
    def mouse_click_release(self, x_m_click_rel, y_m_click_rel):
        if x_m_click_rel > 0 and y_m_click_rel > 0:
            self.selected = False  # 마우스 클릭 해제로 선택 상태 해제

    # 타일을 마우스의 움직임에 따라 이동시키는 메서드
    def move_tyle(self, x_m_motion, y_m_motion):
        self.start_pos_x = x_m_motion  # 마우스의 x 좌표로 타일 이동
        self.start_pos_y = y_m_motion  # 마우스의 y 좌표로 타일 이동

#사용 가능한 타일 수에 따라 타일 생성

def create_tyles():
    i = 1
    while i <= tile_count:
        r = random.randint(1, tile_count)
        if r not in tile_no:
            tile_no.append(r)
            i += 1
    tile_no.append("")  # 마지막에 빈칸 추가
    k = 0
    for i in range(0, rows):
        for j in range(0, cols):
            if (i == rows - 1) and (j == cols - 1):  # 마지막 칸은 건너뜁니다.
                pass
            else:
                t = Tiles(screen, tile_print_position[(
                    i, j)][0], tile_print_position[(i, j)][1],
                        tile_no[k], i, j)
                tiles.append(t)  # 타일을 추가합니다.
            matrix[i][j] = tile_no[k]  # 타일 번호를 매트릭스에 저장
            k += 1
    check_mobility()  # 타일의 이동 가능 여부를 확인합니다.

# 타일을 생성합니다.
# 타일 수에 맞게 랜덤으로 타일 번호를 추가합니다.

def check_mobility():
    for i in range(tile_count):
        tile = tiles[i]
        row_index = tile.position_x
        col_index = tile.position_y
        adjacent_cells = []
        adjacent_cells.append([row_index-1, col_index, False]) # 위쪽
        adjacent_cells.append([row_index+1, col_index, False]) # 아래쪽
        adjacent_cells.append([row_index, col_index-1, False]) # 오른쪽
        adjacent_cells.append([row_index, col_index+1, False]) # 왼쪽
        for i in range(len(adjacent_cells)):
            if (adjacent_cells[i][0] >= 0 and adjacent_cells[i][0] < rows) and (adjacent_cells[i][1] >= 0 and adjacent_cells[i][1] < cols):
                adjacent_cells[i][2] = True

        for j in range(len(adjacent_cells)):
            if adjacent_cells[j][2]:
                adj_cell_row = adjacent_cells[j][0]
                adj_cell_col = adjacent_cells[j][1]
                for k in range(tile_count):
                    if adj_cell_row == tiles[k].position_x and adj_cell_col == tiles[k].position_y:
                        adjacent_cells[j][2] = False

                false_count = 0

                for m in range(len(adjacent_cells)):
                    if adjacent_cells[m][2]:
                        tile.movable = True
                        break
                    else:
                        false_count += 1

                if false_count == 4:
                    tile.movable = False

# 매트릭스를 순회한 후 타일 번호 문자열이 "12345678_"이면
# 플레이어가 승리한 것으로 간주하고 게임을 종료

def isGameOver():
	global game_over, game_over_banner
	allcelldata = ""
	for i in range(rows):
		for j in range(cols):
			allcelldata = allcelldata + str(matrix[i][j])

	if allcelldata == "12345678 ":
		game_over = True
		game_over_banner = "Game Over"

		print("Game Over")

		for i in range(tile_count):
			tiles[i].movable = False
			tiles[i].selected = False


# 창 크기 설정
page_width, page_depth = pyautogui.size()
page_width = int(page_width * .95)  # 화면 크기의 95%로 가로 크기 설정
page_depth = int(page_depth * .95)  # 화면 크기의 95%로 세로 크기 설정

# 타일 크기 설정
tiles = []  # 타일들을 저장할 빈 리스트
tile_width = 200  # 타일의 가로 크기 200px
tile_depth = 200  # 타일의 세로 크기 200px

# 퍼즐 크기 (행, 열 개수)
rows, cols = (3, 3)
tile_count = rows * cols - 1  # 타일의 개수 (빈 칸 제외)

# 퍼즐 상태를 저장할 매트릭스 초기화
matrix = [["" for i in range(cols)] for j in range(rows)]

# 타일 번호 리스트와 화면에 그려질 위치를 저장하는 딕셔너리
tile_no = []
tile_print_position = {(0, 0): (100, 50),
                       (0, 1): (305, 50),
                       (0, 2): (510, 50),
                       (1, 0): (100, 255),
                       (1, 1): (305, 255),
                       (1, 2): (510, 255),
                       (2, 0): (100, 460),
                       (2, 1): (305, 460),
                       (2, 2): (510, 460)}

# 초기 값 설정
mouse_press = False  # 마우스 클릭 여부
x_m_click, y_m_click = 0, 0  # 마우스 클릭 위치
x_m_click_rel, y_m_click_rel = 0, 0  # 마우스 클릭 해제 후 위치
game_over = False  # 게임 종료 여부
game_over_banner = ""  # 게임 종료 배너 텍스트


# pygame 초기화 및 설정
pygame.init()
game_over_font = pygame.font.Font('freesansbold.ttf', 70)
move_count_font = pygame.font.Font('freesansbold.ttf', 40)
font = pygame.font.Font('freesansbold.ttf', 200)
move_count = 0
move_count_banner = "Moves : "

# 게임 화면 크기 설정
screen = pygame.display.set_mode((page_width, page_depth))
pygame.display.set_caption("Slide Game")

# 타일 생성 함수 호출
create_tyles()

running = True
while running:
    screen.fill((0, 0, 0))  # 화면을 검은색으로 채움
    pygame.draw.rect(screen, (165, 42, 42), pygame.Rect(95, 45, 620, 620))
    game_over_print = game_over_font.render(
        game_over_banner, True, (255, 255, 0))  # 게임 오버 배너 텍스트 생성
    screen.blit(game_over_print, (950, 100))

    # 이동 횟수를 문자열로 렌더링하여 화면에 표시
    if move_count == 0:
        move_count_render = move_count_font.render(
            move_count_banner, True, (0, 255, 0))  # 이동 횟수 텍스트
    else:
        move_count_render = move_count_font.render(
            move_count_banner + str(move_count), True, (0, 255, 0))  # 이동 횟수와 숫자를 텍스트로 표시
    screen.blit(move_count_render, (1050, 200))

    # 이벤트 큐에서 이벤트를 가져오기
    for event in pygame.event.get():
        # 종료 이벤트가 발생하면 while 루프를 종료
        if event.type == pygame.QUIT:
            running = False
        # 마우스가 움직이면 (x, y) 좌표를 얻고, 이를 mouse_hover 함수에 전달
        if event.type == pygame.MOUSEMOTION:
            x_m_motion, y_m_motion = pygame.mouse.get_pos()
            for i in range(tile_count):
                tiles[i].mouse_hover(x_m_motion, y_m_motion)
            # 타일이 선택되고 마우스가 클릭되면 move_tyle 함수에 좌표를 전달
            for i in range(tile_count):
                if tiles[i].selected and mouse_press:
                    tiles[i].move_tyle(x_m_motion, y_m_motion)
        # 마우스 버튼이 눌리면 (x, y) 좌표를 얻고, 이를 mouse_click 함수에 전달
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_press = True
            x_m_click, y_m_click = pygame.mouse.get_pos()
            for i in range(tile_count):
                tiles[i].mouse_click(x_m_click, y_m_click)
        # 마우스 버튼을 떼면 (x, y) 좌표를 얻고, 타일을 이동시킬지 결정
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_press = False
            x_m_click_rel, y_m_click_rel = pygame.mouse.get_pos()
            x_m_click, y_m_click = 0, 0
            cell_found = False
            # 행과 열을 순회하면서 클릭한 위치에 타일이 맞는지 확인
            for i in range(0, rows):
                for j in range(0, cols):
                    tile_start_pos_x = tile_print_position[(i, j)][0]
                    tile_start_pos_y = tile_print_position[(i, j)][1]

                    if (x_m_click_rel > tile_start_pos_x and x_m_click_rel < tile_start_pos_x + tile_width) and (y_m_click_rel > tile_start_pos_y and y_m_click_rel < tile_start_pos_y + tile_depth):
                        if matrix[i][j] == "":
                            for k in range(tile_count):
                                if game_over == False:
                                    if tiles[k].selected:
                                        if tiles[k].movable:
                                            cell_found = True
                                            dummy = matrix[tiles[k].position_x][tiles[k].position_y]
                                            matrix[tiles[k].position_x][tiles[k].position_y] = matrix[i][j]
                                            matrix[i][j] = dummy
                                            tiles[k].position_x = i
                                            tiles[k].position_y = j
                                            tiles[k].start_pos_x = tile_print_position[(
                                                i, j)][0]
                                            tiles[k].start_pos_y = tile_print_position[(
                                                i, j)][1]
                                            move_count += 1
                                            isGameOver()
                                            check_mobility()

                    if cell_found == False:
                        for k in range(tile_count):
                            if tiles[k].selected:
                                mat_pos_x = tiles[k].position_x
                                mat_pos_y = tiles[k].position_y
                                tiles[k].start_pos_x = tile_print_position[(
                                    mat_pos_x, mat_pos_y)][0]
                                tiles[k].start_pos_y = tile_print_position[(
                                    mat_pos_x, mat_pos_y)][1]
                                break

    # 각 타일을 화면에 그리기
    for i in range(tile_count):
        tiles[i].draw_tyle()
    # 화면의 일부만 업데이트하도록 하여 성능 최적화,
    # 인자가 없으면 전체 Surface를 업데이트
    pygame.display.flip()
# 화면 전체 업데이트
pygame.display.update()
