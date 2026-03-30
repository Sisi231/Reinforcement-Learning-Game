"""
Snake Eater Environment
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random


class SnakeGameEnv:
    def __init__(self, frame_size_x=150, frame_size_y=150, growing_body=True):
        # Initializes the environment with default values
        self.frame_size_x = frame_size_x
        self.frame_size_y = frame_size_y
        self.growing_body = growing_body
        self.reset()

    def reset(self):
        self.snake_pos = [50, 50]
        self.snake_body = [[50, 50], [60, 50], [70, 50]]
        self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                         random.randrange(1, (self.frame_size_y // 10)) * 10]
        self.food_spawn = True
        self.direction = 'LEFT'
        self.score = 0
        self.game_over = False
        return self.get_state()

    def step(self, action):
        # Implements the logic to change the snake's direction based on action
        # Update the snake's head position based on the direction
        # Check for collision with food, walls, or self
        # Update the score and reset food as necessary
        # Determine if the game is over
        prev_snake = self.snake_pos
        #prev_food = self.food_pos
        self.update_snake_position(action)
        reward = self.calculate_reward(prev_snake)
        self.update_food_position()
        state = self.get_state()
        self.game_over = self.check_game_over()
        return state, reward, self.game_over

    def get_state(self):
        # Your code here
        # Here, you will calculate the state based on your actual state calculation logic
        food_west = 0 if self.snake_pos[0] - self.food_pos[0] >= 0 else 1
        food_east = 0 if self.snake_pos[0] - self.food_pos[0] <= 0 else 1
        food_north = 0 if self.snake_pos[1] - self.food_pos[1] <= 0 else 1
        food_south = 0 if self.snake_pos[1] - self.food_pos[1] >= 0 else 1
        actions = self.allowed_actions()
        safe_left = 1 if 2 in actions else 0
        safe_right = 1 if 3 in actions else 0
        safe_up = 1 if 0 in actions else 0
        safe_down = 1 if 1 in actions else 0
        if 3 <= len(self.snake_body) <= 7:
            size = 0
        elif 8 <= len(self.snake_body) <= 12:
            size = 1
        elif 13 <= len(self.snake_body) <= 17:
            size = 2
        elif 18 <= len(self.snake_body) <= 22:
            size = 3
        elif 23 <= len(self.snake_body) <= float('inf'):
            size = 4
        state = [food_west, food_east, food_south, food_north, safe_up, safe_down, safe_right, safe_left, size]
        return state

    def get_body(self):
        return self.snake_body

    def get_food(self):
        return self.food_pos

    def allowed_actions(self):
        directions = {2: (-10, 0), 3: (10, 0), 0: (0, -10), 1: (0, 10)}
        safe_directions = []
        for direction, (dx, dy) in directions.items():
            x, y = self.snake_pos
            x += dx
            y += dy
            if x < 0 or x > self.frame_size_x - 10 or y < 0 or y > self.frame_size_y - 10 or (x, y) in self.snake_body:
                continue
            else:
                safe_directions.append(direction)
        opposite_actions = {"UP": 1, "DOWN": 0, "LEFT": 3, "RIGHT": 2}
        if opposite_actions.get(self.direction) in safe_directions:
            safe_directions.remove(opposite_actions.get(self.direction))
        return safe_directions

    def calculate_reward(self, prev_snake):
        # Your code here
        # Calculate and return the reward. Remember that you can provide positive or negative reward.
        if self.check_game_over():
            return -4
        elif self.food_pos == self.snake_pos:
            return 7  # apple was eaten
        elif (abs(prev_snake[0] - self.food_pos[0]) > abs(self.snake_pos[0] - self.food_pos[0])
              or abs(prev_snake[1] - self.food_pos[1]) > abs(self.snake_pos[1] - self.food_pos[1])):
            return 0.1
        else:
            return -0.1

    def check_game_over(self):
        # Return True if the game is over, else False
        if self.snake_pos[0] < 0 or self.snake_pos[0] > self.frame_size_x - 10:
            return True
        if self.snake_pos[1] < 0 or self.snake_pos[1] > self.frame_size_y - 10:
            return True
        for block in self.snake_body[1:]:
            if self.snake_pos[0] == block[0] and self.snake_pos[1] == block[1]:
                return True
        return False

    def update_snake_position(self, action):
        # Updates the snake's position based on the action
        # Map action to direction
        change_to = ''
        direction = self.direction
        if action == 0:
            change_to = 'UP'
        elif action == 1:
            change_to = 'DOWN'
        elif action == 2:
            change_to = 'LEFT'
        elif action == 3:
            change_to = 'RIGHT'

        # Move the snake
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            self.snake_pos[1] -= 10
        elif direction == 'DOWN':
            self.snake_pos[1] += 10
        elif direction == 'LEFT':
            self.snake_pos[0] -= 10
        elif direction == 'RIGHT':
            self.snake_pos[0] += 10

        self.direction = direction

        self.snake_body.insert(0, list(self.snake_pos))

        if self.snake_pos[0] == self.food_pos[0] and self.snake_pos[1] == self.food_pos[1]:
            self.score += 10
            self.food_spawn = False
            # If the snake is not growing
            if not self.growing_body:
                self.snake_body.pop()
        else:
            self.snake_body.pop()

    def update_food_position(self):
        if not self.food_spawn:
            self.food_pos = [random.randrange(1, (self.frame_size_x // 10)) * 10,
                             random.randrange(1, (self.frame_size_x // 10)) * 10]
        self.food_spawn = True
