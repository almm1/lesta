import colorsys
from secrets import choice
import pygame
import random


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MAP_SIZE = 5
FIELDS_NUM = 5
FIELD_SIZE = 48

triangle = "A"
circ = "O"
square = "L"
block = "X"
empty = " "

fields = ([triangle] + [circ] + [square])*FIELDS_NUM
random.shuffle(fields)


def field():
    return fields.pop()


level = [
    field()+block+field()+block+field(),
    field()+empty+field()+empty+field(),
    field()+block+field()+block+field(),
    field()+empty+field()+empty+field(),
    field()+block+field()+block+field()
]

pygame.init()
size = (MAP_SIZE*FIELD_SIZE, MAP_SIZE*FIELD_SIZE)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("lesta")

FPS = 60        # число кадров в секунду
clock = pygame.time.Clock()


def main():
    game_over = False
    screen.fill(WHITE)
    m_x = m_y = -1
    choise = []
    prev_choise = []

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (0 <= x <= 5*FIELD_SIZE) and (0 <= y <= 5*FIELD_SIZE):

                    i = y // FIELD_SIZE
                    j = x // FIELD_SIZE

                    choise.clear()
                    choise.insert(0, level[i][j])
                    choise.insert(1, (j, i))

                    if choise[0] == block:
                        continue
                    elif choise[0] == empty:
                        if prev_choise:
                            x1 = choise[1][0]
                            y1 = choise[1][1]
                            x2 = prev_choise[1][0]
                            y2 = prev_choise[1][1]
                            if (1 == abs(x1-x2) and y1 == y2) or (1 == abs(y1-y2) and x1 == x2):
                                field2 = prev_choise[0]
                                level[y1] = level[y1][:x1] + \
                                    field2+level[y1][x1+1:]
                                level[y2] = level[y2][:x2] + \
                                    empty+level[y2][x2+1:]
                                m_x = m_y = -1
                                prev_choise.clear()
                                break
                    else:
                        m_x = FIELD_SIZE * j
                        m_y = FIELD_SIZE * i

                    prev_choise.clear()
                    prev_choise.insert(0, level[i][j])
                    prev_choise.insert(1, (j, i))
        if not is_win():
            draw_map(m_x, m_y)
        else:
            win()
        pygame.display.update()
        pygame.display.flip()
        clock.tick(FPS)


def win():
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:
            draw_field(x, y, GREEN)
            x += FIELD_SIZE  # блоки платформы ставятся на ширине блоков
        y += FIELD_SIZE  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля  # каждый символ


def is_win():
    for i in range(0, 4, 2):  # вся строка
        s = level[0][i]
        for j in range(0, FIELDS_NUM):  # каждый символ
            if s == level[j][i]:
                continue
            else:
                return False
    return True


def draw_map(m_x, m_y):
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == block:
                draw_field(x, y, RED)
            elif col == circ:
                draw_field(x, y, GREEN)
            elif col == triangle:
                draw_field(x, y, BLUE)
            elif col == square:
                draw_field(x, y, BLACK)
            elif col == empty:
                draw_field(x, y, WHITE)
            x += FIELD_SIZE  # блоки платформы ставятся на ширине блоков
        y += FIELD_SIZE  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля
    if m_x >= 0 and m_y >= 0:
        pygame.draw.rect(screen, WHITE, (m_x, m_y, FIELD_SIZE, FIELD_SIZE), 5)


def draw_field(x, y, color):
    pf = pygame.Surface((FIELD_SIZE, FIELD_SIZE))
    pf.fill(color)
    screen.blit(pf, (x, y))


main()
pygame.quit()
