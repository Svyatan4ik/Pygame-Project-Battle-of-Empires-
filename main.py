import pygame
import os
import sys

FPS = 60
pygame.init()
clock = pygame.time.Clock()
size = 850, 700
screen_size = (1280,  720)
screen = pygame.display.set_mode(size)
CONST_CELLS = [(0, 4), (0, 5), (0, 6), (1, 6), (1, 5), (1, 4), (16, 4),
               (16, 4), (16, 5), (16, 5), (16, 6), (16, 6), (15, 6), (15, 6),
               (15, 5), (15, 5), (15, 4), (15, 4)]
CONST_FLAG = [(8, 5), (8, 5), (8, 5)]

POLE = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['#_B', '#_B', '$_B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '$_R', '#_R', '#_R'],
        ['B', 'B', '!_B', '%_B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '%_R', '!_R', 'R', 'R'],
        ['B', 'B', '&_B', '@@_B', '@@_B', '.', '.', '.', '.', '.', '.', '.', '@@_R', '@@_R', '&_R', 'R', 'R'],
        ['B', 'B', '!_B', '%_B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '%_R', '!_R', 'R', 'R'],
        ['#_B', '#_B', '$_B', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '$_R', '#_R', '#_R'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


unit_images = {
    'crusader_red': load_image('crusader_red.png'),
    'crusader_blue': load_image('crusader_blue.png'),
    'crusader_red_ranen': load_image('crusader_red_ranen.png'),
    'crusader_blue_ranen': load_image('crusader_blue_ranen.png'),
    'catapult_red': load_image('catapult_red.png'),
    'catapult_blue': load_image('catapult_blue.png'),
    'guard_red': load_image('guard_red.png'),
    'guard_blue': load_image('guard_blue.png'),
    'monk_red': load_image('monk_red.png'),
    'monk_blue': load_image('monk_blue.png'),
    'marksman_red': load_image('marksman_red.png'),
    'marksman_blue': load_image('marksman_blue.png'),
    'swordsman_red': load_image('swordsman_red.png'),
    'swordsman_blue': load_image('swordsman_blue.png'),
    'castle_red': load_image('castle_red.png'),
    'castle_blue': load_image('castle_blue.png'),
}

tile_width = tile_height = 50


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        # self.rect = None

    def get_event(self, event):
        pass


sprite_group = SpriteGroup()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        colors = [pygame.Color("black"), pygame.Color("blue"), pygame.Color("red"), pygame.Color("yellow")]
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, colors[self.board[y][x]], (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, pygame.Color("white"), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 4

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height or (cell_x, cell_y) in CONST_CELLS:
            return cell_x, cell_y
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["БИТВА ИМПЕРИЙ", "",
                  "",
                  "Цель игры: захватить замок другого игрока.", "По центру карты находится флаг"
                    " который даёт 1 ход при захвате", " В игре есть 5 классов юнитов: Мечник,"
                                                                  " Рыцарь,",
                                                                  " Страж, Лучник"
                                                                  " Осадный юнит"]

    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def draw(tiletype, x, y):
    screen.blit(unit_images[tiletype], (x * 50, y * 50 + 50))


def generate_level(POLE):
    for y in range(len(POLE)):
        for x in range(len(POLE[y])):
            if POLE[y][x] == '@@_R':
                draw('crusader_red', x, y)
            elif POLE[y][x] == '@@_B':
                draw('crusader_blue', x, y)
            if POLE[y][x] == '@_R':
                draw('crusader_red_ranen', x, y)
            elif POLE[y][x] == '@_B':
                draw('crusader_blue_ranen', x, y)
            elif POLE[y][x] == '!_R':
                draw('guard_red', x, y)
            elif POLE[y][x] == '!_B':
                draw('guard_blue', x, y)
            elif POLE[y][x] == '#_R':
                draw('catapult_red', x, y)
            elif POLE[y][x] == '#_B':
                draw('catapult_blue', x, y)
            elif POLE[y][x] == '$_R':
                draw('marksman_red', x, y)
            elif POLE[y][x] == '$_B':
                draw('marksman_blue', x, y)
            elif POLE[y][x] == '&_R':
                draw('monk_red', x, y)
            elif POLE[y][x] == '&_B':
                draw('monk_blue', x, y)
            elif POLE[y][x] == '%_R':
                draw('swordsman_red', x, y)
            elif POLE[y][x] == '%_B':
                draw('swordsman_blue', x, y)
            elif POLE[y][x] == 'R':
                draw('castle_red', x, y)
            elif POLE[y][x] == 'B':
                draw('castle_blue', x, y)


turn = 'red'
red_moves = 0
blue_moves = 0
flag = 0
castle_red = 6
castle_blue = 6
units_killed_red = 0
units_killed_blue = 0


def is_end():
    global POLE
    castles_red = 0
    castles_blue = 0
    units_blue = 0
    units_red = 0
    for y in POLE:
        for x in y:
            if 'B' in x:
                units_blue += 1
            if 'R' in x:
                units_red += 1
            if x == 'B':
                castles_blue += 1
            if x == 'R':
                castles_red += 1
    if castles_red == 0 or units_red - castles_red == 0:
        return 'Победа синей команды'
    if castles_blue == 0 or units_blue - castles_blue == 0:
        return 'Победа красной команды'
    else:
        return None



def move(pos_start, pos_final):
    global POLE, turn, red_moves, blue_moves, units_killed_red, units_killed_blue
    print(pos_start, pos_final)
    raznica_y = pos_final[0] - pos_start[0]
    raznica_x = pos_final[1] - pos_start[1]
    mraznica_x = abs(raznica_x)
    mraznica_y = abs(raznica_y)
    unit = POLE[pos_start[1]][pos_start[0]]
    unit_final = POLE[pos_final[1]][pos_final[0]]
    if "B" in unit and "B" in unit_final:
        return None
    if "R" in unit and "R" in unit_final:
        return None
    if red_moves >= 3:
        red_moves = 0
        turn = 'blue'
    if blue_moves >= 3:
        blue_moves = 0
        turn = 'red'
    if unit == 'R' or unit == 'B':
        return None
    if pos_final == (8, 5) and turn == 'red' and flag != 'red':
        red_moves -= 1
    if pos_final == (8, 5) and turn == 'blue' and flag != ' blue':
        blue_moves -= 1
    if turn == 'red' and 'B' in unit:
        return None
    if turn == 'blue' and 'R' in unit:
        return None
    if pos_start == pos_final:
        return None
    if mraznica_x > 2 or mraznica_y > 2:
        print((raznica_x, raznica_y), (mraznica_x, mraznica_y))
        if raznica_x < 0:
            raznica_x = -2
        if raznica_y < 0:
            raznica_y = -2
        if raznica_y > 2:
            raznica_y = 2
        if raznica_x > 2:
            raznica_x = 2
        new_final_pos = (pos_start[1] + raznica_x, pos_start[0] + raznica_y)
        if "R" in POLE[new_final_pos[0]][new_final_pos[1]] and 'R' in unit:
            return None
        if "B" in POLE[new_final_pos[0]][new_final_pos[1]] and 'B' in unit:
            return None
        if "@@" in unit_final:
            if turn == 'red':
                POLE[pos_final[1]][pos_final[0]] = '@_B'
                red_moves += 1
                return None
            if turn == 'blue':
                POLE[pos_final[1]][pos_final[0]] = '@_R'
                blue_moves += 1
                return None
        POLE[new_final_pos[0]][new_final_pos[1]] = unit
        POLE[pos_start[1]][pos_start[0]] = '.'
        if turn == 'red':
            red_moves += 1
        if turn == 'blue':
            blue_moves += 1
    else:
        if "@@" in unit_final:
            if turn == 'red':
                POLE[pos_final[1]][pos_final[0]] = '@_B'
                red_moves += 1
                return None
            if turn == 'blue':
                POLE[pos_final[1]][pos_final[0]] = '@_R'
                blue_moves += 1
                return None
        POLE[pos_final[1]][pos_final[0]] = unit
        POLE[pos_start[1]][pos_start[0]] = '.'
        if turn == 'red':
            red_moves += 1
            if unit_final != '.':
                units_killed_red += 1
        if turn == 'blue':
            blue_moves += 1
            if unit_final != '.':
                units_killed_blue += 1


board = Board(17, 11)
for i in CONST_CELLS:
    board.on_click(i)
for i in CONST_FLAG:
    board.on_click(i)
board.set_view(0, 50, 50)
start_screen()
running = True
clicks = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clicks == 1:
                startc = board.get_cell(event.pos)
                clicks += 1
                if POLE[startc[1]][startc[0]] == '.':
                    clicks = 1
                continue
            elif clicks == 2:
                finalc = board.get_cell(event.pos)
                clicks = 1
                move(startc, finalc)
                break
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    if turn == 'red':
        turn_text = font.render(f"Ходит красный", True, (255, 0, 0))
    else:
        turn_text = font.render(f"Ходит синий", True, (0, 0, 255))
    screen.blit(turn_text, (10, 10))
    board.render()
    generate_level(POLE)
    win = is_end()
    if win is not None:
        win_text1 = font.render(f"{win}", True, (255, 255, 255))
        win_text2 = font.render(f"Уничтожено синих юнитов: {units_killed_red}", True, (255, 255, 255))
        win_text3 = font.render(f"Уничтожено красных юнитов: {units_killed_blue}", True, (255, 255, 255))
        screen.blit(win_text1, (0, 600))
        screen.blit(win_text2, (0, 636))
        screen.blit(win_text3, (0, 672))
    pygame.display.set_caption('Битва Империй')
    pygame.display.flip()
pygame.quit()
