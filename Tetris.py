import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(SHAPES)
        self.color = random.choice([CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE])

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False

    def new_piece(self):
        return Tetromino(GRID_WIDTH // 2 - 1, 0)

    def valid_move(self, piece, dx=0, dy=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = piece.x + x + dx, piece.y + y + dy
                    if (new_x < 0 or new_x >= GRID_WIDTH or
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and self.grid[new_y][new_x] != BLACK)):
                        return False
        return True

    def place_piece(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[piece.y + y][piece.x + x] = piece.color

    def remove_completed_rows(self):
        full_rows = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])

    def update(self):
        if not self.game_over:
            if self.valid_move(self.current_piece, dy=1):
                self.current_piece.move(0, 1)
            else:
                self.place_piece(self.current_piece)
                self.remove_completed_rows()
                self.current_piece = self.new_piece()
                if not self.valid_move(self.current_piece):
                    self.game_over = True

    def draw(self):
        screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        if self.current_piece:
            for y, row in enumerate(self.current_piece.shape):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(screen, self.current_piece.color,
                                         ((self.current_piece.x + x) * BLOCK_SIZE,
                                          (self.current_piece.y + y) * BLOCK_SIZE,
                                          BLOCK_SIZE, BLOCK_SIZE), 0)

        pygame.display.flip()

def main():
    game = TetrisGame()
    fall_time = 0
    fall_speed = 0.5  # Time in seconds between each drop

    while True:
        dt = clock.tick(60) / 1000  # Convert to seconds
        fall_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and game.valid_move(game.current_piece, dx=-1):
                    game.current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT and game.valid_move(game.current_piece, dx=1):
                    game.current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN and game.valid_move(game.current_piece, dy=1):
                    game.current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    rotated = Tetromino(game.current_piece.x, game.current_piece.y)
                    rotated.shape = list(zip(*game.current_piece.shape[::-1]))
                    if game.valid_move(rotated):
                        game.current_piece = rotated

        if fall_time >= fall_speed:
            game.update()
            fall_time = 0

        game.draw()

        if game.game_over:
            font = pygame.font.Font(None, 74)
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

if __name__ == "__main__":
    main()