from random import choice
from itertools import product
from os import system
from time import sleep
from pynput.keyboard import Listener, Key


KEY_TO_DIRECTION = {
    Key.up : 'up',
    Key.down : 'down',
    Key.left : 'left',
    Key.right : 'right'
}

class SnakeCollisionError(Exception):
    pass

class SnakeEndCondition(Exception):
    pass

class Snake():
    def __init__(self):
        rows = []
        for _ in range(10):
            row = ['.'] * 10
            rows.append(row)
        self.rows = rows
        self.snake = [(5, 5), (5, 4), (5, 3), (5, 2)]
        self.food_cords = (3, 3)
        self.direction = 'left'
        self.last_direction = 'left'
        self.all_board_cords = set(product(range(10), range(10)))

    def set_direction(self, direction):
            self.direction = direction

    def draw_food(self):
        x, y = self.food_cords
        self.rows[x][y] = 'o'

    def get_empty_board_cords(self):
        snake_cords = set(self.snake)
        return self.all_board_cords.difference(snake_cords)

    def empty_grid(self):
        for row in self.rows:
            for n in range(len(row)):
                row[n] = '.'

    def put_snake_in_rows(self):
        for x, y in self.snake:
            self.rows[x][y] = 'x'

    def move_snake(self):
        if not self.is_next_turn_valid():
            self.direction = self.last_direction
            
        snake_head = self.snake[-1]
        next_vector = self.get_next_vector()
        next_snake_head = (
            next_vector[0] + snake_head[0], next_vector[1] + snake_head[1])
        if next_snake_head == self.food_cords:
            if len(self.snake) == 99:
                raise SnakeEndCondition
            self.food_cords = choice(list(self.get_empty_board_cords()))
        else:
            self.snake.pop(0)
        if self.check_wall_collision(next_snake_head):
            raise SnakeCollisionError
        if self.check_self_collision(next_snake_head):
            raise SnakeCollisionError
        self.snake.append(next_snake_head)
        self.last_direction = self.direction

    def is_next_turn_valid(self):
        opposite_direction = {
            'up': 'down',
            'down': 'up',
            'left': 'right',
            'right': 'left',
        }
        return self.last_direction != opposite_direction[self.direction]

    def check_wall_collision(self, cords):
        if cords[0] < 0 or cords[0] > 9:
            return True
        if cords[1] < 0 or cords[1] > 9:
            return True
        return False

    def check_self_collision(self, cords):
        return cords in self.snake

    def get_next_vector(self):
        key_dict = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1),
        }
        return key_dict[self.direction]

    def print_board(self):
        self.empty_grid()
        self.put_snake_in_rows()
        self.draw_food()
        for row in self.rows:
            print(*row)


def on_press_for_snake(snake):
    def on_press(key):
        if key == Key.esc:
            return False
        pressed_direction = KEY_TO_DIRECTION.get(key)
        if pressed_direction is not None:
            snake.set_direction(pressed_direction)
    return on_press


if __name__ == "__main__":
    snake = Snake()
    with Listener(on_press=on_press_for_snake(snake)) as listener:
        try:
            while True:
                snake.print_board()
                sleep(0.5)
                system('cls')
                snake.move_snake()
        except SnakeEndCondition:
            print('You win!')
        except IndexError:
            print('You loose!')
        except SnakeCollisionError:
            print('You colided with something! You loose.')
