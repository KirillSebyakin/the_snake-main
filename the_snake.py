from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position):
        self.position = position
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self, screen_width, screen_height):
        super().__init__((0, 0))
        self.body_color = (APPLE_COLOR)  # Красный цвет
        self.randomize_position(screen_width, screen_height)

    def randomize_position(self, screen_width, screen_height):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, (screen_width // GRID_SIZE) - 1) * GRID_SIZE,
            randint(0, (screen_height // GRID_SIZE) - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self, screen_width, screen_height, snake_positions):
        """Ресет"""
        self.randomize_position(screen_width, screen_height)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self, screen_width, screen_height):
        start_x = (screen_width // 2) - (screen_width // 2) % GRID_SIZE
        start_y = (screen_height // 2) - (screen_height // 2) % GRID_SIZE
        super().__init__((start_x, start_y))
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        move_x, move_y = self.direction
        new_head = (
            (head_x + move_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + move_y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions = [new_head] + self.positions

        if len(self.positions) > self.length:
            self.positions.pop()

    def check_collision(self):
        """Проверяет столкновение змейки с собой."""
        return self.positions[0] in self.positions[1:]

    def eat(self):
        """Увеличивает длину змейки при поедании яблока."""
        self.length += 1

    def draw(self):
        """Отрисовка змейки на игровой поверхности."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс змейки в начальное состояние."""
        start_x = (SCREEN_WIDTH // 2) - (SCREEN_WIDTH // 2) % GRID_SIZE
        start_y = (SCREEN_HEIGHT // 2) - (SCREEN_HEIGHT // 2) % GRID_SIZE
        self.positions = [(start_x, start_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация PyGame:"""
    pygame.init()

    # Тут нужно создать экземпляры классов.
    snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
    apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        # Обработка событий
        handle_keys(snake)

        # Обновление направления змеи
        snake.update_direction()

        # Движение змеи
        snake.move()

        # Проверка поедания яблока
        if snake.get_head_position() == apple.position:
            snake.eat()
            while True:
                if apple.position not in snake.position:
                    apple.randomize_position(
                        SCREEN_WIDTH, SCREEN_HEIGHT)
                    break

        # Проверка столкновения змейки с собой
        if snake.check_collision():
            snake.reset()
            apple.reset(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Отрисовка змейки и яблока
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
