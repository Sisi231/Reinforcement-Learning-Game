"""
Snake Eater Q learning basic algorithm
Made with PyGame
Last modification in April 2024 by José Luis Perán
Machine Learning Classes - University Carlos III of Madrid
"""
import numpy as np
import random
import json
import time


class QLearning:
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.95, epsilon=0, epsilon_min=0,
                 epsilon_decay=0.999999):
        self.n_states = n_states
        self.n_actions = n_actions
        self.actions = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.load_q_table()

    def choose_action(self, state, allowed_actions):
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(allowed_actions)  # Explore
        else:
            action = np.argmax(self.q_table[self.calculate_row(state)])
        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)
        return action

    def update_q_table(self, state, action, reward, next_state):
        # Your code here
        # Update the current Q-value using the Q-learning formula
        row = self.calculate_row(state)
        action_column = action
        if reward == 7 or reward == -2:
            self.q_table[row, action_column] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * reward
        else:
            self.q_table[row, action_column] = ((1 - self.alpha) * self.getQValue(state, action) +
                                                self.alpha * (reward + self.gamma * max(
                        self.q_table[self.calculate_row(next_state)])))

    def calculate_row(self, state):
        a, b, c, d, e, f, g, h, i = state
        food_direction = {(1, 0, 0, 0): 0, (1, 0, 1, 0): 1, (1, 0, 0, 1): 2, (0, 1, 0, 0): 3, (0, 1, 1, 0): 4,
                          (0, 1, 0, 1): 5, (0, 0, 1, 0): 6, (0, 0, 0, 1): 7, (0, 0, 0, 0): 8}
        food_row = food_direction.get((a, b, c, d))
        danger_row = int(f"{e}{f}{g}{h}", 2)
        return (food_row * 16 + danger_row)*5 + i

    def getQValue(self, state, action):
        position = int(self.calculate_row(state))
        action_column = action
        return self.q_table[position, action_column]

    def save_q_table(self, filename="q_table.txt"):
        np.savetxt(filename, self.q_table)

    def load_q_table(self, filename="q_table.txt"):
        try:
            self.q_table = np.loadtxt(filename)
        except IOError:
            # If the file doesn't exist, initialize Q-table with zeros as per dimensions
            self.q_table = np.zeros((self.n_states, self.n_actions))
