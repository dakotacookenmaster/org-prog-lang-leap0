# LEAP 0: (A)maze
# CPTR-405-A: Organization of Programming Languages
# filename: maze.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/26/2020
# Note: The random library is included in the Python Standard Library (https://docs.python.org/3.3/library/random.html)
import random

class Maze:
    """ Top-level parent for Maze variants. """
    def __init__(self):
        self.description = "Top-level Maze Variant" # this should be replaced by any children of Maze

    def elaborate(self):
        print(f"{self.description}")

class Fork(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)
        self.left = kwargs['left'](left = GameObject.build_maze(), 
                                   right = GameObject.build_maze(), 
                                   forward = GameObject.build_maze())

        self.right = kwargs['right'](left = GameObject.build_maze(), 
                                     right = GameObject.build_maze(), 
                                     forward = GameObject.build_maze())

    def move_forward(self):
        print("Unable to move forward. There is only a path to the left and right.")
        return self

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
        self.forward = kwargs['forward'](left = GameObject.build_maze(), 
                                         right = GameObject.build_maze(), 
                                         forward = GameObject.build_maze())
    
    def move_forward(self):
        return self.forward

    def __str__(self):
        return "Room"

    def __repr__(self):
        return f"Room({repr(self.forward)})"

class Enemy(Maze):
    def __init__(self, **kwargs):
        self.description = str(self)
        self.forward = kwargs['forward'](left = GameObject.build_maze(), 
                                         right = GameObject.build_maze(), 
                                         forward = GameObject.build_maze())

    def move_forward(self):
        print("Normall, you'd have to kill an enemy here.")
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
    def __init__(self):
        self.maze = Room(left = GameObject.build_maze(), 
                         right = GameObject.build_maze(),
                         forward = GameObject.build_maze())

        self.commands = {
            "LOOK": self.elaborate,
            "FORWARD": self.move_forward
        }

    # Define commands here instead of linking directly to Maze class to allow custom handling
    # of the results.
    def elaborate(self):
        self.maze.elaborate()

    def move_forward(self):
        self.maze = self.maze.move_forward()

    def prompt(self):
        user_input = input("> ").upper()
        if user_input in self.commands:
            self.commands[user_input]()
        else:
            print("You've entered an invalid command. Type 'help' to see what commands are available.")
    
    @staticmethod
    def build_maze():
        maze_variants = [
            Room, Room,
            Fork, Fork,
            DeadEnd,
            Enemy,
            Exit
        ]
        return random.choice(maze_variants)

# Define the global GameObject
mazeGame = GameObject()

while True:
    mazeGame.prompt()