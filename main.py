import pygame
from pygame.locals import *
import Node
import random
from collections import deque

WINDOW_W = 1000  # Window with in pixels.
ROWS = 50  # Number of rows in grid.
WAIT_T = 0  # Wait time in ms between each maze generation step.
WAIT_T_ASTAR = 0  # Wait time in ms between each Astar step.


#  Finds and returns the index for the lowest f_score in open set list.
def get_lowest_f_index(open_set):
    index = 0
    for i in range(len(open_set)):
        if open_set[i].get_f() < open_set[index].get_f():
            index = i
    return index


# Calculates and returns h-score with manhattan distance.
def h_score(node1: Node, node2: Node):
    r1 = node1.get_row_col()[0]
    c1 = node1.get_row_col()[1]
    r2 = node2.get_row_col()[0]
    c2 = node2.get_row_col()[1]

    return abs(r1 - r2) + abs(c1 - c2)


# Creates grid with size row * row.
def create_grid(rows):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node.Node(i, j, rows, WINDOW_W)
            grid[i].append(node)

    return grid


# Draws each Node in grid on the screen.
def draw_grid(grid, screen):
    for row in grid:
        for node in row:
            node.draw(screen)


# Removes walls between two Nodes.
def remove_walls(node1: Node, node2: Node):
    rowDiff = node1.get_row_col()[0] - node2.get_row_col()[0]
    colDiff = node1.get_row_col()[1] - node2.get_row_col()[1]

    if colDiff == 1:
        node1.get_walls()[3] = 0
        node2.get_walls()[1] = 0

    if colDiff == -1:
        node2.get_walls()[3] = 0
        node1.get_walls()[1] = 0

    if rowDiff == 1:
        node1.get_walls()[0] = 0
        node2.get_walls()[2] = 0

    if rowDiff == -1:
        node2.get_walls()[0] = 0
        node1.get_walls()[2] = 0


# Goes through came_from dictionary and returns the shortest path.
def retrace_path(came_from, current):
    total_path = [current, came_from[current]]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)

    return total_path


def main():
    # Initialize screen and creates grid.
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_W))
    pygame.display.set_caption('A*')
    stack = deque()
    grid = create_grid(ROWS)
    current = grid[0][0]
    current.set_visited(True)
    mazeNotDone = True

    # Event loop for creating maze.
    while mazeNotDone:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        draw_grid(grid, screen)
        pygame.display.flip()
        pygame.time.wait(WAIT_T)

        current.set_colour((0, 50, 0))

        n_list = current.check_neighbours(grid)  # Get list of current nodes neighbours.
        if len(n_list) > 0:  # If neighbour exists, pick a random one and remove walls between current node and a random neighbour.
            nextNode = random.choice(n_list)
            stack.append(current)
            remove_walls(current, nextNode)
            current = nextNode
            current.set_visited(True)

        elif len(stack) > 0:  # If there are no neighbours backtrack until there are possible neighbours.
            current.set_colour((0, 100, 0))
            current = stack.pop()

        current.set_colour((0, 100, 0))

        if len(stack) == 0:  # When the stack is empty the maze is done, continue to A*.
            mazeNotDone = False

    # Maze done, now start using A* to find shortest path from top left corner to bottom right corner.

    # Initialize lists.
    came_from = {}
    open_set = []
    closed_set = []
    start = current
    end = grid[ROWS - 1][ROWS - 1]

    # sets start nodes g and h score and adds it to the open set.
    start.set_g(0)
    start.set_h(h_score(start, end))
    open_set.append(start)

    while len(open_set) > 0:

        # Picks the lowest f score Node from the open set.
        lowest_f_index = get_lowest_f_index(open_set)
        current = open_set[lowest_f_index]

        if open_set[lowest_f_index] == end:  # If end node in open set, algorithm is done and path can be retraced.
            print("Done!")

            path = retrace_path(came_from, current)
            for p in path:  # Draws the path.
                p.set_colour((200, 50, 100))

                for event in pygame.event.get():
                    if event.type == QUIT:
                        return

                draw_grid(grid, screen)
                pygame.display.flip()
                pygame.time.wait(WAIT_T)

            break

        # Remove current node from open set and add it to closed set
        open_set.remove(current)
        closed_set.append(current)
        current.set_colour((100, 50, 150))

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        draw_grid(grid, screen)
        pygame.display.flip()
        pygame.time.wait(WAIT_T_ASTAR)

        neighbours = current.get_Astar_neighbours(grid)

        for n in neighbours:  # Updates scores for each neighbour Node
            tentative_gScore = current.get_g() + 1
            if tentative_gScore < n.get_g():  # If a better route was found update the scores.
                came_from[n] = current
                n.set_g(tentative_gScore)
                n.set_h(h_score(n, end))
                if open_set.count(n) == 0:  # If Node is not in open set, add it.
                    open_set.append(n)

    # Just to keep drawing screen after algorithms are done.
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        draw_grid(grid, screen)
        pygame.display.flip()


if __name__ == '__main__': main()
