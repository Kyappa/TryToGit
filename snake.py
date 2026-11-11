"""Классическая игра «Змейка» на pygame.

Управление: стрелки — движение, ESC — выход.
"""

import random
import sys

import pygame

# Настройки игры
CELL_SIZE = 20          # размер клетки в пикселях
GRID_WIDTH = 30         # клеток по горизонтали
GRID_HEIGHT = 22        # клеток по вертикали
FPS = 8                 # скорость змейки (кадров в секунду)

# Цвета
BLACK = (15, 15, 15)
GREEN = (46, 204, 113)
RED = (231, 76, 60)

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)


def random_free_cell(occupied):
    """Возвращает случайную клетку, не занятую другими объектами."""
    empty_points = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in occupied
    ]
    return random.choice(empty_points)


def draw_cell(surface, cell, color):
    """Рисует один квадрат сетки."""
    rect = pygame.Rect(cell[0] * CELL_SIZE, cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect.inflate(-2, -2))


def game_over_screen(screen, score):
    """Показывает финальный счёт и ждёт выхода игрока."""
    font = pygame.font.SysFont("arial", 36)
    text = font.render(f"Игра окончена! Счёт: {score}", True, GREEN)
    text_rect = text.get_rect(center=screen.get_size() // 2)
    screen.fill(BLACK)
    screen.blit(text, text_rect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


def run_game(screen, clock):
    """Основной игровой цикл одной партии."""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = RIGHT
    food = random_free_cell(set(snake))
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                new_direction = {
                    pygame.K_UP: UP,
                    pygame.K_DOWN: DOWN,
                    pygame.K_LEFT: LEFT,
                    pygame.K_RIGHT: RIGHT,
                }.get(event.key)
                # Запрещаем разворот на 180 градусов
                if new_direction and (new_direction != (-direction[0], -direction[1])):
                    direction = new_direction
                if event.key == pygame.K_ESCAPE:
                    return None

        head = (snake[-1][0] + direction[0], snake[-1][1] + direction[1])
        hit_wall = not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT)
        hit_self = head in snake[:-1]  # хвост сдвинется, если еда не съедена

        if head == food:
            score += 1
            food = random_free_cell(set(snake) | {head})
            snake.append(head)
        else:
            snake.pop(0)
            if hit_wall or hit_self:
                return score
            snake.append(head)

        screen.fill(BLACK)
        for cell in snake:
            draw_cell(screen, cell, GREEN)
        draw_cell(screen, food, RED)
        pygame.display.set_caption(f"Змейка — счёт: {score}")
        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    size = (GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    while True:
        score = run_game(screen, clock)
        if score is None:  # игрок вышел сам
            break
        game_over_screen(screen, score)

    pygame.quit()


if __name__ == "__main__":
    main()
