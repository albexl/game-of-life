import time

import pygame
from pygame.locals import *

WIDTH = 700
HEIGHT = 700


def get_alive(matrix):
    count = sum(sum(row) for row in matrix)
    return count


def is_valid(x, y, n):
    return min(x, y) >= 0 and max(x, y) < n


def handle(event):
    if event.type == QUIT:
        pygame.quit()
        quit()


def draw(matrix, n):

    black_color = (0, 0, 0)
    grey_color = (105, 105, 105)
    white_color = (255, 255, 255)
    game_display.fill(white_color)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                rect = pygame.Rect(j * (HEIGHT // n), i *
                                   (HEIGHT // n), HEIGHT // n, HEIGHT // n)
                pygame.draw.rect(game_display, black_color, rect)

    for i in range(n + 1):
        pygame.draw.line(game_display, grey_color,
                         (i * (HEIGHT // n), 0), (i * (HEIGHT // n), WIDTH), width=1)

    for i in range(n + 1):
        pygame.draw.line(game_display, grey_color,
                         (0, i * (WIDTH // n)), (HEIGHT, i * (WIDTH // n)), width=1)

    pygame.display.update()


def setup(matrix, n):
    print("Place initial disposition of alive cells")

    draw(matrix, n)

    initial_setup = True
    while initial_setup:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_RETURN:
                initial_setup = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                i = pos[1] // (HEIGHT // n)
                j = pos[0] // (HEIGHT // n)
                matrix[i][j] = 1
                draw(matrix, n)


if __name__ == '__main__':

    n = int(input('Enter dimension of the system: '))

    matrix = [[0] * n for _ in range(n)]

    dx = [1, 1, -1, -1, 0, 0, 1, -1]
    dy = [1, -1, 1, -1, 1, -1, 0, 0]

    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.flip()

    setup(matrix, n)

    while get_alive(matrix) > 0:

        for event in pygame.event.get():
            handle(event)
        draw(matrix, n)

        transition = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                alive = 0
                for k in range(8):
                    nx = i + dx[k]
                    ny = j + dy[k]
                    if is_valid(nx, ny, n):
                        alive += matrix[nx][ny]
                if matrix[i][j] == 1 and alive in [2, 3]:
                    transition[i][j] = 1
                if matrix[i][j] == 0 and alive == 3:
                    transition[i][j] = 1

        for i in range(n):
            for j in range(n):
                matrix[i][j] = transition[i][j]

        time.sleep(0.2)

    for event in pygame.event.get():
        handle(event)
    draw(matrix, n)
    time.sleep(1)
