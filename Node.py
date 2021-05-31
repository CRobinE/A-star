import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)


# Node class for maze
class Node:

    def __init__(self, row, col, total_rows, window_width, colour=GRAY):
        self.g = float("inf")  # Node g-score.
        self.h = float("inf")  # Node h_score.
        self.row = row
        self.col = col
        self.colour = colour
        self.total_rows = total_rows
        self.width = (window_width // total_rows)
        self.x = self.width * col
        self.y = self.width * row
        self.walls = [1, 1, 1, 1]  # Node walls, 1 is for closed [top, right, bottom, left].
        self.visited = False
        # Pixel x and y position for each corner of Node, used to draw walls.
        self.corners = [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.width),
                        (self.x, self.y + self.width), (self.x, self.y)]
        self.neighbours = []  # List of neighbours when drawing maze.
        self.A_star_neighbours = []  # List of neighbours when doing A* calculations.

    def set_g(self, g):
        self.g = g

    def get_g(self):
        return self.g

    def set_h(self, h):
        self.h = h

    def get_f(self):
        return self.h + self.g

    def set_visited(self, value: bool):
        self.visited = value

    def get_visited(self):
        return self.visited

    def get_walls(self):
        return self.walls

    def get_row_col(self):
        return self.row, self.col

    def get_pos(self):
        return self.x, self.y

    def check_neighbours(self, grid):  # Updates neighbours for Node.
        self.neighbours = []

        if self.row > 0 and not grid[self.row - 1][self.col].get_visited():  # UP
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].get_visited():  # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].get_visited():  # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].get_visited():  # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])

        return self.neighbours

    def get_Astar_neighbours(self, grid):  # Updates A* neighbours for Node.

        if self.row > 0 and self.walls[0] == 0:  # UP
            self.A_star_neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and self.walls[1] == 0:  # RIGHT
            self.A_star_neighbours.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and self.walls[2] == 0:  # DOWN
            self.A_star_neighbours.append(grid[self.row + 1][self.col])

        if self.col > 0 and self.walls[3] == 0:  # LEFT
            self.A_star_neighbours.append(grid[self.row][self.col - 1])

        return self.A_star_neighbours

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour

    def get_neighbours(self):
        return self.neighbours

    def draw(self, window):  # Draws the node on the screen.
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))
        for count, wall in enumerate(self.walls):
            if wall == 1:
                pygame.draw.line(window, WHITE, self.corners[count], self.corners[count + 1], 1)
