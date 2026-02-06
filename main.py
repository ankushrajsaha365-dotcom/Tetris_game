import pygame
import random

pygame.init()

# Screen settings
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Tetris")

clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0],
     [1, 1, 1]],     # J
    [[0, 0, 1],
     [1, 1, 1]],     # L
    [[1, 1],
     [1, 1]],        # O
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[0, 1, 0],
     [1, 1, 1]],     # T
    [[1, 1, 0],
     [0, 1, 1]]      # Z
]


class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0


grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
current_piece = Piece()


def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (40, 40, 40),
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def valid_move(piece, dx, dy, new_shape=None):
    shape = new_shape if new_shape else piece.shape

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece.x + x + dx
                ny = piece.y + y + dy

                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False
                if ny >= 0 and grid[ny][nx]:
                    return False
    return True


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def lock_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color


def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell is None for cell in row)]
    cleared = ROWS - len(new_grid)

    for _ in range(cleared):
        new_grid.insert(0, [None for _ in range(COLS)])

    grid = new_grid


fall_time = 0
fall_speed = 500

running = True
while running:
    dt = clock.tick(60)
    fall_time += dt

    screen.fill(BLACK)

    if fall_time > fall_speed:
        if valid_move(current_piece, 0, 1):
            current_piece.y += 1
        else:
            lock_piece(current_piece)
            clear_lines()
            current_piece = Piece()
        fall_time = 0

    # Controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if valid_move(current_piece, -1, 0):
                    current_piece.x -= 1

            if event.key == pygame.K_RIGHT:
                if valid_move(current_piece, 1, 0):
                    current_piece.x += 1

            if event.key == pygame.K_DOWN:
                if valid_move(current_piece, 0, 1):
                    current_piece.y += 1

            if event.key == pygame.K_UP:
                rotated = rotate(current_piece.shape)
                if valid_move(current_piece, 0, 0, rotated):
                    current_piece.shape = rotated

    # Draw current piece
    for y, row in enumerate(current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    current_piece.color,
                    ((current_piece.x + x) * BLOCK_SIZE,
                     (current_piece.y + y) * BLOCK_SIZE,
                     BLOCK_SIZE,
                     BLOCK_SIZE)
                )

    draw_grid()
    pygame.display.update()

pygame.quit()
