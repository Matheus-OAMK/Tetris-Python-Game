import pygame
import random

pygame.init()

# **** Blocks ****
#   [0][1][2]
#   [3][4][5]
#   [6][7][8]
blocks = [
    [[1, 4, 7], [3, 4, 5]],  # straight
    [[1, 3, 4, 5, 7]],  # cross
    [[0, 1, 4, 5], [1, 3, 4, 6]],  # two on two variant 1
    [[1, 2, 3, 4], [0, 3, 4, 7]],  # two on two variant 2
    [[0, 1, 3, 6], [0, 1, 2, 5], [2, 5, 7, 8], [3, 6, 7, 8]],  # L shape variant 1
    [[1, 2, 5, 8], [5, 6, 7, 8], [0, 3, 6, 7], [0, 1, 2, 3]],  # L shape variant 2
    [[4, 6, 7, 8], [0, 3, 4, 6], [0, 1, 2, 4], [2, 4, 5, 8]],  # one on three
]
# Colours
colours = [
    (255, 0, 0),  # Red
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (128, 0, 128),  # Purple
    (0, 247, 255),  # cyan
    (0, 128, 0),  # Green
]


# Font
font = pygame.font.SysFont("Arial", 25, True, False)
font2 = pygame.font.SysFont("Arial", 50, True, False)

# Score
score = 0

# Check if game is over
game_finished = False

# Variable to keep track if arrow down is pressed
is_down_pressed = False


class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(blocks) - 1)
        self.rotation = 0
        self.colour = colours[random.randint(0, len(colours) - 1)]

    def shape(self):
        return blocks[self.type][self.rotation]


# **** Helper functions ****
# Function to create a block
def draw_block():
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                pygame.draw.rect(
                    screen,
                    (block.colour),
                    [
                        (x + block.x) * grid_size + x_gap + 1,
                        (y + block.y) * grid_size + y_gap + 1,
                        grid_size - 2,
                        grid_size - 2,
                    ],
                )


# Funcion to rotate block
def rotate_block():
    last_rotation = block.rotation
    block.rotation = (block.rotation + 1) % len(blocks[block.type])
    can_rotate = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 0):
                    can_rotate = False
    if not can_rotate:
        block.rotation = last_rotation
    


# Function to render some text
def render_text(text, font, x, y, color=(255, 255, 255)):
    text_surface = font.render(
        text, True, color
    )  # the second parameter is anti aliasing
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Function to draw grid
def draw_grid(rows, cols, grid_size, x_gap, y_gap):
    for y in range(rows):  # rows
        for x in range(cols):  # cols
            pygame.draw.rect(
                screen,
                (100, 100, 100),
                [x * grid_size + x_gap, y * grid_size + y_gap, grid_size, grid_size],
                1,
            )
            if game_board[x][y] != (0, 0, 0):
                pygame.draw.rect(
                    screen,
                    (game_board[x][y]),
                    [
                        x * grid_size + x_gap + 1,
                        y * grid_size + y_gap + 1,
                        grid_size - 1,
                        grid_size - 1,
                    ],
                )


# Check for collision with other blocks or sides
def collides(nx, ny):
    collision = False
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if y + block.y + ny < 0 or y + block.y + ny > rows - 1:
                    collision = True
                    break
                if x + block.x + nx < 0 or x + block.x + nx > cols - 1:
                    collision = True
                    break
                if game_board[x + block.x + nx][y + block.y + ny] != (0, 0, 0):
                    collision = True
                    break
    return collision


# Function to drop the block
def drop_block():
    can_drop = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 1):
                    can_drop = False
    if can_drop:   
        block.y += 1
    else:
        for y in range(3):
            for x in range(3):
                if y * 3 + x in block.shape():
                    game_board[x + block.x][y + block.y] = block.colour
    return can_drop


# Function to move blocks from side to side
def side_move(dx):
    can_move = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(dx, 0):
                    can_move = False
    if can_move:
        block.x += dx
    else:
        drop_block()

def down_move():
    can_move = True
    for y in range(3):
        for x in range(3):
            if y * 3 + x in block.shape():
                if collides(0, 1):
                    can_move = False
    if can_move:
        block.y += 1
    else:
        drop_block()


# Function to find completed lines
def find_lines():
    lines = 0
    for y in range(rows):
        empty = 0
        for x in range(cols):
            if game_board[x][y] == (0, 0, 0):
                empty += 1
        if empty == 0:
            lines += 1
            for y2 in range(y, 1, -1):
                for x2 in range(cols):
                    game_board[x2][y2] = game_board[x2][y2 - 1]
    return lines


# Initialize the game screen
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Tetris")
game_over = False


grid_size = 30
rows = screen.get_height() // grid_size
cols = screen.get_width() // grid_size
x_gap = (screen.get_width() - (cols * grid_size)) // 2
y_gap = (screen.get_height() - (rows * grid_size)) // 2

clock = pygame.time.Clock()


# Creating first block in the middle
block = Block((cols - 1) // 2, 0)

# Initialize game board
game_board = []
for i in range(cols):
    new_col = []
    for j in range(rows):
        new_col.append((0, 0, 0))
    game_board.append(new_col)

fps = 6
while not game_over:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rotate_block()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]:
        down_move()
        fps = 15  # Increase frame rate when the key is held
    else:
        fps = 10  # Reset frame rate when the key is released

    if keys[pygame.K_LEFT]:
        side_move(-1)
        is_sideways_moving = True
    if keys[pygame.K_RIGHT]:
        side_move(1)
        is_sideways_moving = True
        


    screen.fill((0, 0, 0))  # paint screen black
    draw_grid(rows, cols, grid_size, x_gap, y_gap)
    if block is not None:
        draw_block()
        if event.type != pygame.KEYDOWN:
            if not drop_block() and not game_finished:
                score += find_lines()
                block = Block(random.randint(5, cols - 5), 0)
                if collides(0, 0):
                    game_finished = True

    render_text(f"Score: {score}", font, 45, 15)
    if game_finished:
        render_text(
            "Game Over", font2, screen.get_width() // 2, screen.get_height() // 2
        )
    pygame.display.update()
pygame.quit()
