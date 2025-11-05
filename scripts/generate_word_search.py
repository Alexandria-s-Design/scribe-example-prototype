#!/usr/bin/env python3
"""Generate word search grid for educational worksheets"""

import random
from typing import List, Tuple

class WordSearchGenerator:
    def __init__(self, size: int = 15):
        self.size = size
        self.grid = [['' for _ in range(size)] for _ in range(size)]
        self.placed_words = []

    def generate(self, words: List[str]) -> Tuple[List[List[str]], List[dict]]:
        """
        Generate word search grid with given words.
        Returns: (grid, word_positions)
        """
        # Convert all words to uppercase
        words = [word.upper() for word in words]

        # Sort by length (longest first for better placement)
        words.sort(key=len, reverse=True)

        # Place each word
        for word in words:
            placed = False
            attempts = 0
            max_attempts = 100

            while not placed and attempts < max_attempts:
                # Random direction: 0=horizontal, 1=vertical, 2=diagonal
                direction = random.choice([0, 1, 2])

                if direction == 0:  # Horizontal
                    placed = self._place_horizontal(word)
                elif direction == 1:  # Vertical
                    placed = self._place_vertical(word)
                else:  # Diagonal
                    placed = self._place_diagonal(word)

                attempts += 1

        # Fill empty spaces with random letters
        self._fill_empty_spaces()

        return self.grid, self.placed_words

    def _place_horizontal(self, word: str) -> bool:
        """Try to place word horizontally"""
        if len(word) > self.size:
            return False

        # Random starting position
        row = random.randint(0, self.size - 1)
        col = random.randint(0, self.size - len(word))

        # Check if space is available
        for i, letter in enumerate(word):
            if self.grid[row][col + i] != '' and self.grid[row][col + i] != letter:
                return False

        # Place the word
        for i, letter in enumerate(word):
            self.grid[row][col + i] = letter

        self.placed_words.append({
            'word': word,
            'start': (row, col),
            'end': (row, col + len(word) - 1),
            'direction': 'horizontal'
        })
        return True

    def _place_vertical(self, word: str) -> bool:
        """Try to place word vertically"""
        if len(word) > self.size:
            return False

        # Random starting position
        row = random.randint(0, self.size - len(word))
        col = random.randint(0, self.size - 1)

        # Check if space is available
        for i, letter in enumerate(word):
            if self.grid[row + i][col] != '' and self.grid[row + i][col] != letter:
                return False

        # Place the word
        for i, letter in enumerate(word):
            self.grid[row + i][col] = letter

        self.placed_words.append({
            'word': word,
            'start': (row, col),
            'end': (row + len(word) - 1, col),
            'direction': 'vertical'
        })
        return True

    def _place_diagonal(self, word: str) -> bool:
        """Try to place word diagonally"""
        if len(word) > self.size:
            return False

        # Random starting position
        row = random.randint(0, self.size - len(word))
        col = random.randint(0, self.size - len(word))

        # Check if space is available
        for i, letter in enumerate(word):
            if self.grid[row + i][col + i] != '' and self.grid[row + i][col + i] != letter:
                return False

        # Place the word
        for i, letter in enumerate(word):
            self.grid[row + i][col + i] = letter

        self.placed_words.append({
            'word': word,
            'start': (row, col),
            'end': (row + len(word) - 1, col + len(word) - 1),
            'direction': 'diagonal'
        })
        return True

    def _fill_empty_spaces(self):
        """Fill empty spaces with random letters"""
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '':
                    self.grid[i][j] = random.choice(letters)

    def print_grid(self):
        """Print the grid (for debugging)"""
        for row in self.grid:
            print(' '.join(row))

if __name__ == '__main__':
    # Test with cell biology words
    words = [
        'NUCLEUS', 'MITOCHONDRIA', 'CHLOROPLAST', 'MEMBRANE',
        'CYTOPLASM', 'RIBOSOME', 'VACUOLE', 'ORGANELLE',
        'CELLWALL', 'DIFFUSION'
    ]

    generator = WordSearchGenerator(size=15)
    grid, placed = generator.generate(words)

    print("Word Search Grid:")
    generator.print_grid()
    print(f"\nPlaced {len(placed)} words")
    for word_info in placed:
        print(f"  {word_info['word']}: {word_info['direction']}")
