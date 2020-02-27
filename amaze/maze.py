# LEAP 0: (A)maze
# CPTR-405-A: Organization of Programming Languages
# filename: maze.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/26/2020
# Note: The random library is included in the Python Standard Library (https://docs.python.org/3.3/library/random.html)
import random
import os

class Maze:
    """ Top-level parent for Maze variants. """
    def __init__(self):
        self.description = "Top-level Maze Variant" # this should be replaced by any children of Maze

    def elaborate(self):
        print(f"{self.description}")

class Fork(Maze):
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.fork)
        self.depth = kwargs['depth']
        if self.depth < GameObject.recursion_limit:
            self.left = kwargs['left'](left = GameObject.build_maze(), 
                                    right = GameObject.build_maze(), 
                                    forward = GameObject.build_maze(),
                                    depth = self.depth + 1)

            self.right = kwargs['right'](left = GameObject.build_maze(), 
                                        right = GameObject.build_maze(), 
                                        forward = GameObject.build_maze(),
                                        depth = self.depth + 1)
        else:
            self.left = GameObject.get_endpoint()()
            self.right = GameObject.get_endpoint()()

    def move_forward(self):
        print("Unable to move forward. There is only a path to the left and right.")
        return self

    def move_left(self):
        return self.left

    def move_right(self):
        return self.right

    def __str__(self):
        return "Fork"

    def __repr__(self):
        return f"Fork({repr(self.left)}, {repr(self.right)})"

class DeadEnd(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)

    def move_forward(self):
        print("You've reached a dead-end. Game Over.")
        exit(0)

    def __str__(self):
        return "DeadEnd"

    def __repr__(self):
        return f"DeadEnd()"

class Room(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)
        self.depth = kwargs['depth']
        if self.depth < GameObject.recursion_limit:
            self.forward = kwargs['forward'](left = GameObject.build_maze(), 
                                            right = GameObject.build_maze(), 
                                            forward = GameObject.build_maze(),
                                            depth = self.depth + 1)
        else:
            self.forward = GameObject.get_endpoint()()
    
    def move_forward(self):
        return self.forward

    def __str__(self):
        return "Room"

    def __repr__(self):
        return f"Room({repr(self.forward)})"

class Enemy(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)
        self.depth = kwargs['depth']
        if self.depth < GameObject.recursion_limit:
            self.forward = kwargs['forward'](left = GameObject.build_maze(), 
                                            right = GameObject.build_maze(), 
                                            forward = GameObject.build_maze(),
                                            depth = self.depth + 1)
        else:
            self.forward = GameObject.get_endpoint()()

    def move_forward(self):
        print("Normally, you'd have to kill an enemy here.")
        return self.forward

    def __str__(self):
        return "Enemy"

    def __repr__(self):
        return f"Enemy({repr(self.forward)})"


class Exit(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)

    def move_forward(self):
        print("You made it out!")
        exit(0)
    
    def __str__(self):
        return "Exit"

    def __repr__(self):
        return f"Exit()"

class GameObject:
    # Static attributes
    maze_variants = [
        Fork, Fork, Fork, Fork, Fork, Fork,
        Room, Room, Room, Room, Room,
        Enemy, Enemy,
        DeadEnd,
        Exit
    ]

    recursion_limit = 10

    files = ["fork.txt"]

    for f in files:
        try:
            with open(f"./amaze/room_descriptions/{f}", "r") as f_desc:
                fork = [(i).replace("\n", "") for i in f_desc.readlines() if (i != '' and i != '\n')]
        except Exception:
            print(f"Unable to open {f}. Was it removed?")
            exit(0)

    def __init__(self):
        self.maze = Fork(left = GameObject.build_maze(), 
                         right = GameObject.build_maze(),
                         forward = GameObject.build_maze(),
                         depth = 0)

        self.commands = {
            "LOOK": self.elaborate,
            "FORWARD": self.move_forward,
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
        }


    # Define commands here instead of linking directly to Maze class to allow custom handling
    # of the results.
    def elaborate(self):
        self.maze.elaborate()

    def move_forward(self):
        self.maze = self.maze.move_forward()

    def move_left(self):
        self.maze = self.maze.move_left()

    def move_right(self):
        self.maze = self.maze.move_left()

    def prompt(self):
        user_input = input("> ").upper()
        if user_input in self.commands:
            self.commands[user_input]()
        else:
            print("You've entered an invalid command. Type 'help' to see what commands are available.")

    @staticmethod
    def set_recursion_limit(new_limit):
        GameObject.recursion_limit = new_limit

    @staticmethod
    def get_endpoint():
        return random.choice([DeadEnd, Exit])

    @staticmethod
    def build_maze():
        return random.choice(GameObject.maze_variants)


# Define the global GameObject
mazeGame = GameObject()
# print(repr(mazeGame.maze))
while True:
    mazeGame.prompt()