import random
import time

import pygame
from pygame.locals import *

WIDTH = 700
HEIGHT = 700


def get_alive(matrix):
    count = 0
    for row in matrix:
        count += sum(row)
    return count


def is_valid(x, y, n):
    return min(x, y) >= 0 and max(x, y) < n


def handle(event):
    if event.type == QUIT:
        pygame.quit()
        quit()


def draw(matrix, n):

    white_color = (255, 255, 255)
    black_color = (0, 0, 0)
    game_display.fill(white_color)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                rect = pygame.Rect(j * (HEIGHT // n), i *
                                   (HEIGHT // n), HEIGHT // n, HEIGHT // n)
                pygame.draw.rect(game_display, black_color, rect)

    for i in range(n + 1):
        pygame.draw.line(game_display, black_color,
                         (i * (HEIGHT // n), 0), (i * (HEIGHT // n), WIDTH), width=1)

    for i in range(n + 1):
        pygame.draw.line(game_display, black_color,
                         (0, i * (WIDTH // n)), (HEIGHT, i * (WIDTH // n)), width=1)

    pygame.display.update()


if __name__ == '__main__':

    n = int(input('Enter dimension of the system: '))

    starting_cells = min(n**2, 3 * n)
    matrix = [[0] * n for _ in range(n)]
    population = []

    for i in range(n):
        for j in range(n):
            population.append((i, j))

    random.shuffle(population)
    for i in range(starting_cells):
        matrix[population[i][0]][population[i][1]] = 1

    dx = [1, 1, -1, -1, 0, 0, 1, -1]
    dy = [1, -1, 1, -1, 1, -1, 0, 0]

    pygame.init()
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.flip()
    game_display.fill((0, 0, 0))

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

        time.sleep(0.5)

    for event in pygame.event.get():
        handle(event)
    draw(matrix, n)
    time.sleep(1)
