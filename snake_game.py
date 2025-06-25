import os
import random
import time
import threading
from collections import deque
import sys

# For Windows-specific keyboard input
try:
    import msvcrt
except ImportError:
    msvcrt = None

class SnakeGame:
    def __init__(self, width=40, height=20):
        self.width = width
        self.height = height
        self.snake = deque([(width//2, height//2)])
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.running = True
        self.last_key = None
        
    def generate_food(self):
        """Generate food at random position not occupied by snake"""
        while True:
            food = (random.randint(1, self.width-2), random.randint(1, self.height-2))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """Move snake in current direction"""
        head_x, head_y = self.snake[0]
        
        # Calculate new head position based on direction
        if self.direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif self.direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif self.direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
        
        # Check for collisions with walls
        if (new_head[0] <= 0 or new_head[0] >= self.width-1 or 
            new_head[1] <= 0 or new_head[1] >= self.height-1):
            self.game_over = True
            return
        
        # Check for collision with self
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food is eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def change_direction(self, new_direction):
        """Change snake direction (prevent 180-degree turns)"""
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction
    
    def draw_game(self):
        """Draw the game board"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create game board
        board = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if x == 0 or x == self.width-1 or y == 0 or y == self.height-1:
                    row.append('#')  # Wall
                elif (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        row.append('O')  # Snake head
                    else:
                        row.append('o')  # Snake body
                elif (x, y) == self.food:
                    row.append('*')  # Food
                else:
                    row.append(' ')  # Empty space
            board.append(''.join(row))
        
        # Print the board
        for row in board:
            print(row)
        
        # Print score and controls
        print(f"\nScore: {self.score}")
        print("Controls: W/A/S/D to move, Q to quit")
        print("Direction: ↑(W) ↓(S) ←(A) →(D)")
        
        if self.game_over:
            print("\n*** GAME OVER ***")
            print("Press R to restart or Q to quit")
    
    def get_key_input(self):
        """Get keyboard input in a non-blocking way"""
        if msvcrt and msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            return key
        return None
    
    def handle_input(self):
        """Handle keyboard input"""
        key = self.get_key_input()
        if key:
            if key == 'w':
                self.change_direction('UP')
            elif key == 's':
                self.change_direction('DOWN')
            elif key == 'a':
                self.change_direction('LEFT')
            elif key == 'd':
                self.change_direction('RIGHT')
            elif key == 'q':
                return 'quit'
            elif key == 'r' and self.game_over:
                return 'restart'
        return 'continue'
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = deque([(self.width//2, self.height//2)])
        self.direction = 'RIGHT'
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
    
    def run(self):
        """Main game loop"""
        print("Welcome to Snake Game!")
        print("Controls: W/A/S/D to move, Q to quit")
        print("Press any key to start...")
        
        # Wait for initial key press
        while not self.get_key_input():
            time.sleep(0.1)
        
        while self.running:
            self.draw_game()
            
            # Handle input
            action = self.handle_input()
            if action == 'quit':
                self.running = False
                break
            elif action == 'restart':
                self.reset_game()
                continue
            
            # Move snake if game is not over
            if not self.game_over:
                self.move_snake()
            
            # Game speed
            time.sleep(0.2)
        
        print("\nThanks for playing Snake!")

def main():
    """Main function to start the game"""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure you're running this in a terminal that supports the required features.")

if __name__ == "__main__":
    main()

