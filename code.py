import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(grid, start, end):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                continue
            if grid[node_position[0]][node_position[1]] != 0:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)


def main():

    grid = np.random.choice([0, 1], (40, 40))
    grid[::2, ::2] = 0
    grid[1::2, 1::2] = 0

    print("The grid is 40 x 40\n")
    start_x = input("Please enter start x-coordinate\n")
    start_y = input("Please enter start y-coordinate\n")
    end_x = input("Please enter end x-coordinate\n")
    end_y = input("Please enter end y-coordinate\n")
    start = (int(start_x), int(start_y))
    end = (int(end_x), int(end_y))

    path = astar(grid, start, end)
    print(path)

    for i in range(len(path)):
        grid[path[i][0]][path[i][1]] = 2

    grid[path[0][0]][path[0][1]] = 3
    grid[path[len(path) - 1][0]][path[len(path) - 1][1]] = 4

    cmap = colors.ListedColormap(['white', 'red', 'blue', 'yellow', 'green'])
    plt.figure(figsize=(6, 6))
    plt.pcolor(grid[::-1], cmap=cmap, edgecolors='k', linewidths=3)
    plt.show()


if __name__ == '__main__':
    main()
