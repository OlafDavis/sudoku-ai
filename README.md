# Sudoku Game

A simple Sudoku game implemented in Python using Pygame. The game generates random Sudoku puzzles and allows you to solve them interactively.

## Requirements

- Python 3.7 or higher
- Pygame
- NumPy

## Installation

1. Clone this repository or download the files
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. Game Controls:
   - Click on an empty cell to select it
   - Press number keys (1-9) to enter a number
   - Press Backspace or Delete to clear a cell
   - Press Escape to quit the game

3. Rules:
   - Fill the 9x9 grid with numbers 1-9
   - Each row, column, and 3x3 box must contain all numbers from 1-9 without repetition
   - The original numbers (in blue) cannot be changed
   - Your numbers will appear in black

## Features

- Random puzzle generation
- Unique solution guarantee
- Visual grid with 3x3 box highlighting
- Original numbers highlighted in blue
- Selected cell highlighted in red
- Input validation to ensure valid moves 