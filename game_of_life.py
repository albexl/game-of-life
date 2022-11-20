"""An implementation of the Game of Life."""


import sys
import time

import pygame
from pygame.locals import K_RETURN, KEYDOWN, QUIT

WIDTH = 700
HEIGHT = 700


def get_alive(matrix):
    count = sum(sum(row) for row in matrix)
    return count


def is_valid(x_cord, y_cord, size):
    return min(x_cord, y_cord) >= 0 and max(x_cord, y_cord) < size


def handle(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()


def draw(matrix, size):

    black_color = (0, 0, 0)
    grey_color = (105, 105, 105)
    white_color = (255, 255, 255)
    game_display.fill(white_color)

    for row in range(size):
        for col in range(size):
            if matrix[row][col] == 1:
                rect = pygame.Rect(col * (HEIGHT // size), row *
                                   (HEIGHT // size), HEIGHT // size, HEIGHT // size)
                pygame.draw.rect(game_display, black_color, rect)

    for row in range(size + 1):
        pygame.draw.line(game_display, grey_color,
                         (row * (HEIGHT // size), 0), (row * (HEIGHT // size), WIDTH), width=1)

    for col in range(size + 1):
        pygame.draw.line(game_display, grey_color,
                         (0, col * (WIDTH // size)), (HEIGHT, col * (WIDTH // size)), width=1)

    pygame.display.update()


def setup(matrix, size):
    print("Place initial disposition of alive cells")

    draw(matrix, size)

    initial_setup = True
    while initial_setup:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                initial_setup = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                i = pos[1] // (HEIGHT // size)
                j = pos[0] // (HEIGHT // size)
                matrix[i][j] = 1
                draw(matrix, size)


if __name__ == '__main__':

    size = int(input('Enter dimension of the system: '))

    matrix = [[0] * size for _ in range(size)]

    dx = [1, 1, -1, -1, 0, 0, 1, -1]
    dy = [1, -1, 1, -1, 1, -1, 0, 0]

    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.flip()

    setup(matrix, size)

    while get_alive(matrix) > 0:

        for event in pygame.event.get():
            handle(event)
        draw(matrix, size)

        transition = [[0] * size for _ in range(size)]
        for row in range(size):
            for col in range(size):
                alive = 0
                for k in range(8):
                    nx = row + dx[k]
                    ny = col + dy[k]
                    if is_valid(nx, ny, size):
                        alive += matrix[nx][ny]
                if matrix[row][col] == 1 and alive in [2, 3]:
                    transition[row][col] = 1
                if matrix[row][col] == 0 and alive == 3:
                    transition[row][col] = 1

        for row in range(size):
            for col in range(size):
                matrix[row][col] = transition[row][col]

        time.sleep(0.2)

    for event in pygame.event.get():
        handle(event)
    draw(matrix, size)
    time.sleep(1)
