import numpy as np
import string

with open('input.txt', 'r') as f:
    maze = [list(x[:-1]) for x in f]

maze = np.array(maze)

class MazeRunner(object):
    def __init__(self, maze) -> None:
        self.maze = maze
        self.pos = np.array((0, list(maze[0, :]).index('|')))
        self.down = np.array((1, 0))
        self.up = np.array((-1, 0))
        self.left = np.array((0, 1))
        self.right = np.array((0, -1))
        self.direction = self.down
        self.steps = 0

        self.letter_seq = []

    @property
    def position(self):
        return (self.pos[0], self.pos[1])

    @property
    def directions(self):
        directions = [
            tuple(self.up), tuple(self.down),
            tuple(self.left), tuple(self.right)
        ]

        curr_dir = tuple(self.direction)

        if curr_dir == directions[1]:
            del directions[0]
        elif curr_dir == directions[0]:
            del directions[1]
        elif curr_dir == directions[3]:
            del directions[2]
        else:
            del directions[3]

        return [np.array(x) for x in directions]

    def run_maze(self):
        while True:
            print(self.maze[self.position])
            if self.maze[self.position] in string.ascii_letters:
                self.letter_seq.append(self.maze[self.position])
            elif self.maze[self.position] == ' ' or any(x < 0 for x in self.position):
                break
        
            elif self.maze[self.position] == '+':
                search_dir = self.directions
                print('Searching in', *search_dir)

                for direction in search_dir:
                    try:
                        offset = self.pos + direction
                        offset = (offset[0], offset[1])
                        if self.maze[offset] != " ":
                            print('Current position is', self.position)
                            print(f'Maze at offset {offset} is:', self.maze[offset])
                            print('Current direction is ', self.direction)
                            print('Switching to', direction)
                            self.direction = direction
                            break
                        print('Space found.')
                    except IndexError:
                        continue

            self.pos += self.direction
            self.steps += 1

        print(''.join(self.letter_seq))
        print(self.steps, 'steps')

runner = MazeRunner(maze)
runner.run_maze()