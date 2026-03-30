![Python](https://img.shields.io/badge/Language-Python-blue)
![RL](https://img.shields.io/badge/Type-Reinforcement%20Learning-green)

# Reinforcement Learning Snake Agent

This project implements a Q-learning agent to play the classic Snake game. The goal is for the agent to learn an optimal policy to maximize rewards by eating food while avoiding collisions with walls and its own body.

The project explores:

- State space design
- Reward function engineering
- Hyperparameter tuning (α, γ, ε)
- Performance across different board sizes

# Technologies Used
- Programming Language: Python
- Libraries: pygame(for game environment), sys, random, numpy, json, time

# Methodology
State Representation

The environment state is represented using:

- Safe movement directions: safe_up, safe_down, safe_left, safe_right
- Relative food position: food_north, food_south, food_east, food_west
- (Enhanced model) Snake size (discretized into bins)

This results in:

- Basic model: 144 states
- Enhanced model: 720 states
  
# Reward Function

The agent receives:

+7 → eating food

-2 / -4 → crashing (depending on model)

+0.1 → moving closer to food

-0.1 → moving away from food

# Learning Algorithm
- Q-learning (tabular)
- Actions: up, down, left, right
- Q-table updated based on:
  - Learning rate (α)
  - Discount factor (γ)
  - Exploration rate (ε)

# Experiments
Hyperparameter Tuning

Different combinations of:
- α (learning rate)
- γ (future reward importance)
- ε (exploration rate)

were tested across:
- 150×150 board
- 300×300 board
- 500×500 board

# Key Findings
- Lower ε improves performance after sufficient training
- Larger boards require:
  - More training episodes
  - Lower learning rates
- Models trained on medium boards generalize best

# Results
Best Model (Non-growing snake):
- Trained on: 300×300 board
- Average rewards:
  - 150×150 → ~2688
  - 300×300 → ~2735
  - 500×500 → ~2154

Enhanced Model (Growing snake):
- Includes snake body collision + size feature
- Average rewards:
  - 150×150 → ~45
  - 300×300 → ~63
  - 500×500 → ~62

# Project Structure
├── Phase2/
    ├──q_learning.py
    ├──q_table.txt
    ├──snake_env.py
    ├──SnakeGame.py
    ├──__pychache__
         ├──q_learning.cpython-310
         └──snake_env.cpython-310
    └──Experimentation - q-tables
         ├──q_table-150
         ├──q_table-300-best
         └──q_table-500
├── Phase3/
    ├──q_learning.py
    ├──q_table.txt
    ├──snake_env.py
    ├──SnakeGame.py
    ├──__pychache__
         ├──q_learning.cpython-310
         ├──snake_env.cpython-310
         ├──q_learning.cpython-311
         └──snake_env.cpython-311
    └──Experimentation - q-tables
         ├──q_table-150
         ├──q_table-300
         └──q_table-500-best
├── Report/
       └──Reinforcement Learning.pdf
└── README.md

# How to Run
Clone the repository

Install dependencies

Run the game with a trained agent:

python SnakeGame.py

# Key Takeaways
- Q-learning performance depends heavily on state design
- Reward shaping significantly impacts learning speed
- Exploration vs exploitation must be carefully balanced
- Larger environments require more training, but can generalize better

# Author

Silvia Andreeva
