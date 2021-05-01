import random as rng
import itertools as it
import os
from pynput.keyboard import Listener, Key

# SINGLETON


class SnakeCollisionError(Exception):
    pass


class Snake():
    def __init__(self):
        self.last_move_direction = 'left'
        rows = []
        for _ in range(10):
            row = ['.'] * 10
            rows.append(row)
        self.rows = rows
        self.snake = [(5, 5), (5, 4), (5, 3), (5, 2)]
        self.food_cords = (3, 3)
        self.last_move_direction = 'left'
        self.all_board_cords = set(it.product(range(10), range(10)))

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

    def move_snake(self, key):
        if not self.is_next_turn_valid(key):
            return
        self.last_move_direction = key.name
        snake_head = self.snake[-1]
        next_vector = self.get_next_vector(key)
        next_snake_head = (
            next_vector[0] + snake_head[0], next_vector[1] + snake_head[1])
        if next_snake_head == self.food_cords:
            # if len( Snake.snake) == 99:  to do : win condition
            self.food_cords = rng.choice(list(self.get_empty_board_cords()))
        else:
            self.snake.pop(0)
        if self.check_wall_collision(next_snake_head):
            raise SnakeCollisionError
        if self.check_self_collision(next_snake_head):
            raise SnakeCollisionError
        self.snake.append(next_snake_head)

    def is_next_turn_valid(self, key):
        key_to_opposite_direction = {
            Key.up: 'down',
            Key.down: 'up',
            Key.left: 'right',
            Key.right: 'left',
        }
        return self.last_move_direction != key_to_opposite_direction[key]

    def check_wall_collision(self, cords):
        if cords[0] < 0 or cords[0] > 9:
            return True
        if cords[1] < 0 or cords[1] > 9:
            return True
        return False

    def check_self_collision(self, cords):
        return cords in self.snake

    def get_next_vector(self, key):
        key_dict = {
            Key.up: (-1, 0),
            Key.down: (1, 0),
            Key.left: (0, -1),
            Key.right: (0, 1),
        }
        return key_dict[key]

    def print_board(self):
        self.empty_grid()
        self.put_snake_in_rows()
        self.draw_food()
        for row in self.rows:
            print(*row)


def on_press(key):
    try:
        os.system('cls')
        if key == Key.esc:
            return False
        snake.move_snake(key)
        snake.print_board()

    except IndexError:
        print('You loose!')
        return False
    except SnakeCollisionError:
        print('You colided with something! You loose.')
        return False


if __name__ == "__main__":
    snake = Snake()
    snake.print_board()
    with Listener(on_press=on_press) as listener:
        listener.join()
