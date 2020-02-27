# LEAP 0: (A)maze
# CPTR-405-A: Organization of Programming Languages
# filename: maze.py
# Programmed by:
#   Dakota Cookenmaster
#   Michael Yoon
# Last edit: 02/26/2020
# Note: The random library is included in the Python Standard Library (https://docs.python.org/3.3/library/random.html)
# We realize that we are supposed to include what is *absolutely* necessary, and we would argue that it is. I have no way to access
# the hardware for microtime (unless I include the time library), and writing a random function would simply copy what already exists.
# We simply include this one module from the standard library to make some random choices about which maze section will spawn next.
import random

class Maze:
    """ Top-level parent for Maze variants. """
    def __init__(self):
        self.description = "Top-level Maze Variant" # this should be replaced by any children of Maze

    def elaborate(self):
        print(f"{self.description}")

class Fork(Maze):
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['fork'])
        self.depth = kwargs['depth']
        if self.depth < GameObject.recursion_limit:
            self.left = kwargs['left'](left = GameObject.get_maze(), 
                                    right = GameObject.get_maze(), 
                                    forward = GameObject.get_maze(),
                                    depth = self.depth + 1)

            self.right = kwargs['right'](left = GameObject.get_maze(), 
                                        right = GameObject.get_maze(), 
                                        forward = GameObject.get_maze(),
                                        depth = self.depth + 1)
        else:
            self.left = GameObject.get_endpoint()()
            self.right = GameObject.get_endpoint()()

    def move_forward(self):
        print("Unable to move forward. There is only a path to the left and right.")
        return self

    def fight(self):
        print("Only the spork people fight at forks.")

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
        self.description = random.choice(GameObject.descriptions['deadend'])

    def move_left(self):
        self.move_forward()

    def move_right(self):
        self.move_forward()

    def fight(self):
        print("There's nothing to fight here.")

    def move_forward(self):
        print("You've reached a dead-end. Game Over.")
        exit(0)

    def __str__(self):
        return "DeadEnd"

    def __repr__(self):
        return f"DeadEnd()"

class Room(Maze):
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['room'])
        self.depth = kwargs['depth']
        if self.depth < GameObject.recursion_limit:
            self.forward = kwargs['forward'](left = GameObject.get_maze(), 
                                            right = GameObject.get_maze(), 
                                            forward = GameObject.get_maze(),
                                            depth = self.depth + 1)
        else:
            self.forward = GameObject.get_endpoint()()

    def fight(self):
        print("You smack your head against the wall. Things start to spin. You decide it's best to stop.")
    
    def move_forward(self):
        return self.forward

    def move_left(self):
        print("You are unable to move to the left. A wall blocks your path.")
        return self

    def move_right(self):
        print("You are unable to move to the right. A wall blocks your path.")
        return self

    def __str__(self):
        return "Room"

    def __repr__(self):
        return f"Room({repr(self.forward)})"

class Enemy(Maze):
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['enemy'])
        self.depth = kwargs['depth']
        self.enemy_dead = False
        if self.depth < GameObject.recursion_limit:
            self.forward = kwargs['forward'](left = GameObject.get_maze(), 
                                            right = GameObject.get_maze(), 
                                            forward = GameObject.get_maze(),
                                            depth = self.depth + 1)
        else:
            self.forward = GameObject.get_endpoint()()

    def move_forward(self):
        if self.enemy_dead:
            return self.forward
        else:
            print("The danger is still in your path! You might fight to move forward!")
            return self

    def fight(self):
        fate = random.choice([True, True, True, True, True, False])
        if fate:
            print("By some stroke of luck, you are still alive! The enemy has been defeated, and you can move onwards.")
            self.description = "The danger has passed. You may now move forward."
            self.enemy_dead = True
        else:
            print("Your journey is now over. Rest in peace.")
            exit(0)
    
    def move_left(self):
        print("You are unable to move to the left. A wall blocks your path.")
        return self

    def move_right(self):
        print("You are unable to move to the right. A wall blocks your path.")
        return self

    def __str__(self):
        return "Enemy"

    def __repr__(self):
        return f"Enemy({repr(self.forward)})"


class Exit(Maze):
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['exit'])

    def move_forward(self):
        print("You made it out!")
        exit(0)

    def move_left(self):
        self.move_forward()

    def move_right(self):
        self.move_forward()

    def fight(self):
        print("There is nothing to fight here...except yourself. You give yourself a good face whacking and move on.")
    
    def __str__(self):
        return "Exit"

    def __repr__(self):
        return f"Exit()"

class GameObject:
    # Static attributes
    maze_variants = [
        Fork, Fork, Fork, Fork, Fork, Fork,
        Room, Room, Room, Room, Room,
        Enemy, Enemy, Enemy, Enemy
    ]

    descriptions = {
        'fork': [],
        'exit': [],
        'deadend': [],
        'enemy': [],
        'exit': [],
        'room': [],
    }
    recursion_limit = 20

    for f in descriptions:
        try:
            with open(f"./amaze/room_descriptions/{f}.txt", "r") as f_desc:
                descriptions[f] = [(i).replace("\n", "") for i in f_desc.readlines() if (i != '' and i != '\n')]
        except Exception:
            print(f"Unable to open {f}. Was it removed?")
            exit(0)

    def __init__(self):
        self.maze = Fork(left = GameObject.get_maze(), 
                         right = GameObject.get_maze(),
                         forward = GameObject.get_maze(),
                         depth = 0)

        self.commands = {
            "LOOK": self.elaborate,
            "FORWARD": self.move_forward,
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
            "FIGHT": self.fight,
            "HELP": self.help,
        }

    # def map(self, maze = False, tab_level = 1):
    #     if not maze:
    #         maze = self.maze
    #     if str(maze) == "Fork":
    #         print(" " * tab_level, end="")
    #         print(f"{self.map(maze.left, tab_level + 1)} <== {self.maze} ==> {self.map(maze.right, tab_level + 1)}")
    #     elif str(maze) == "Room":
    #         print(" " * tab_level, end="")
    #         print("||")
    #         print(" " * tab_level, end="")
    #         print(f"{self.map(maze.forward, tab_level + 1)}")

    ###########################################################################################
    # Define commands here instead of linking directly to Maze class to allow custom handling #
    # of the results.                                                                         #
    ###########################################################################################
    
    def fight(self):
        self.maze.fight()

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

    def help(self):
        print("'help' --> brings up this help context.")
        print("'look' --> prints information about the room you're currently in.")
        print("'fight' --> engages in hand-to-hand combat with potential assailants.")
        print("'forward' --> allows the user to move forward if possible.")
        print("'left' --> allows the user to move to the left if possible.")
        print("'right' --> allows the user to move to the right if possible.")

    @staticmethod
    def set_recursion_limit(new_limit):
        GameObject.recursion_limit = new_limit

    @staticmethod
    def get_endpoint():
        return random.choice([DeadEnd, Exit])

    @staticmethod
    def get_maze():
        return random.choice(GameObject.maze_variants)


# Define the global GameObject
mazeGame = GameObject()
print()
print("Welcome to the maze of mystery! Inside, you may live, die, or escape. The journey is the destination!")
print("Type 'help' to learn what commands you can use.")
print()
while True:
    mazeGame.prompt()