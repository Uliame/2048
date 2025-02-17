import numpy as np
import random
import pygame

GRID_SIZE = 4
TILE_SIZE = 100
MARGIN = 10
WIDTH, HEIGHT = (GRID_SIZE * (TILE_SIZE + MARGIN)) + MARGIN, (GRID_SIZE * (TILE_SIZE + MARGIN)) + MARGIN
BACKGROUND_COLOR = (125, 125, 125)
TILE_COLORS = {
    0: (68, 68, 68), 2: (245, 206, 255), 4: (229, 191, 255), 8: (219, 171, 255),
    16: (198, 144, 237), 32: (176, 116, 220), 64: (145, 105, 193), 128: (46, 124, 40),
    256: (19, 144, 9), 512: (75, 213, 65), 1024: (114, 233, 105), 2048: (171, 246, 166)
}

class Game2048:
    def __init__(self):
        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.add_new_tile()
        self.add_new_tile()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2048")
        self.font = pygame.font.Font(None, 36)
    
    def add_new_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i, j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i, j] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction):
        original_board = self.board.copy()
        if direction == "left":
            self.board = self.merge(self.board)
        elif direction == "right":
            self.board = np.fliplr(self.merge(np.fliplr(self.board)))
        elif direction == "up":
            self.board = np.rot90(self.merge(np.rot90(self.board, 1)), -1)
        elif direction == "down":
            self.board = np.rot90(self.merge(np.rot90(self.board, -1)), 1)
        
        if not np.array_equal(original_board, self.board):
            self.add_new_tile()
    
    def merge(self, board):
        new_board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        for i in range(GRID_SIZE):
            row = [num for num in board[i] if num != 0]  # Remove zeros
            new_row = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j < len(row) - 1 and row[j] == row[j + 1]:
                    new_row.append(row[j] * 2)
                    skip = True
                else:
                    new_row.append(row[j])
            new_row += [0] * (GRID_SIZE - len(new_row))  # Preenche com zeros até completar a linha
            new_board[i] = new_row
        return new_board
    
    def is_game_over(self):
        temp_board = self.board.copy()
        for direction in ["left", "right", "up", "down"]:
            if not np.array_equal(temp_board, self.move_simulation(direction)):
                return False
        return True
    
    def move_simulation(self, direction):
        temp_board = self.board.copy()
        game_copy = Game2048()
        game_copy.board = temp_board
        game_copy.move(direction)
        return game_copy.board
    
    def draw_board(self):
        self.screen.fill(BACKGROUND_COLOR)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color = TILE_COLORS.get(value, (60, 58, 50))
                pygame.draw.rect(self.screen, color, 
                                 (j * (TILE_SIZE + MARGIN) + MARGIN, 
                                  i * (TILE_SIZE + MARGIN) + MARGIN, 
                                  TILE_SIZE, TILE_SIZE))
                if value != 0:
                    text_surface = self.font.render(str(value), True, (0, 0, 0))
                    text_rect = text_surface.get_rect(center=((j * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2),
                                                              (i * (TILE_SIZE + MARGIN) + MARGIN + TILE_SIZE // 2)))
                    self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw_board()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        self.move("left")
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.move("right")
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        self.move("up")
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.move("down")
        pygame.quit()

game = Game2048()
game.run()
