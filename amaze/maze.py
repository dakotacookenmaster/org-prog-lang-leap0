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

debug = False # make True to run tests

class Maze:
    """ Top-level parent for Maze variants. """
    def __init__(self):
        self.description = "Top-level Maze Variant" # this should be replaced by any children of Maze

    def elaborate(self):
        '''
        elaborate() --> void \n
        Prints out the description of the current room. \n
        '''
        print(f"{self.description}")

    def __str__(self):
        '''
        str(Maze) --> String \n
        Returns a string reprentation of the object.
        '''
        return "Maze"

    def __repr__(self):
        '''
        repr(Maze) --> String \n
        Returns a string representing the object's definition.
        '''
        return "Maze()"

class Fork(Maze):
    """ Fork variant of the Maze class. Spawns a left and right Maze """
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
        '''
        move_forward() --> Maze \n
        Moves the player forward. If unable, will display a message.
        '''
        print("Unable to move forward. There is only a path to the left and right.")
        return self

    def fight(self):
        '''
        fight() --> void \n
        Starts a fight.
        '''
        print("Only the spork people fight at forks.")

    def move_left(self):
        '''
        move_left --> Maze \n
        Moves the player left.
        '''
        return self.left

    def move_right(self):
        '''
        move_right() --> Maze \n
        Moves the player right.
        '''
        return self.right

    def __str__(self):
        '''
        str(Fork) --> String \n
        Returns a string reprentation of the object.
        '''
        return "Fork"

    def __repr__(self):
        '''
        repr(Fork) --> String \n
        Returns a string representing the object's definition.
        '''
        return f"Fork({repr(self.left)}, {repr(self.right)})"

class DeadEnd(Maze):
    """ DeadEnd variant of the Maze class. Endpoint which results in a Game Over. """
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['deadend'])

    def move_left(self):
        '''
        move_left() --> void \n
        Points to move_forward().
        '''
        self.move_forward()

    def move_right(self):
        '''
        move_right() --> void \n
        Points to move_forward().
        '''
        self.move_forward()

    def fight(self):
        '''
        fight() --> void \n
        Displays a message.
        '''
        print("There's nothing to fight here.")

    def move_forward(self):
        '''
        move_forward() --> void \n
        Displays message and exits.
        '''
        print("You've reached a dead-end. Game Over.")
        exit(0)

    def __str__(self):
        '''
        str(DeadEnd) --> String \n
        Returns a string reprentation of the object.
        '''
        return "DeadEnd"

    def __repr__(self):
        '''
        repr(DeadEnd) --> String \n
        Returns a string representing the object's definition.
        '''
        return f"DeadEnd()"

class Room(Maze):
    """ Room variant of the Maze class. Spawns a forward maze. """
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
        '''
        fight() --> void \n
        Displays message.
        '''
        print("You smack your head against the wall. Things start to spin. You decide it's best to stop.")
    
    def move_forward(self):
        '''
        move_forward() --> Maze \n
        Moves the player forward.
        '''
        return self.forward

    def move_left(self):
        '''
        move_left() --> Maze \n
        Points to move_forward().
        '''
        print("You are unable to move to the left. A wall blocks your path.")
        return self

    def move_right(self):
        '''
        move_right() --> Maze \n
        Points to move_forward().
        '''
        print("You are unable to move to the right. A wall blocks your path.")
        return self

    def __str__(self):
        '''
        str(Room) --> String \n
        Returns a string reprentation of the object.
        '''
        return "Room"

    def __repr__(self):
        '''
        repr(Room) --> String \n
        Returns a string representing the object's definition.
        '''
        return f"Room({repr(self.forward)})"

class Enemy(Maze):
    """ Enemy variant of the Maze class. Spawns a enemy that must be fought, and a forward Maze. """
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
        '''
        move_forward() --> Maze \n
        If the enemy is dead, moves the player forward. \n
        If not, displays a message.
        '''
        if self.enemy_dead:
            return self.forward
        else:
            print("The danger is still in your path! You must fight to move forward!")
            return self

    def fight(self):
        '''
        fight() --> void \n
        Starts a fight with the enemy. \n
        If successful, lets player move forward. \n
        If unsuccessful, exits.
        '''
        fate = random.choice([True, True, True, True, False, False])
        if fate:
            print("By some stroke of luck, you are still alive! The enemy has been defeated, and you can move onwards.")
            self.description = "The danger has passed. You may now move forward."
            self.enemy_dead = True
        else:
            print("Your journey is now over. Rest in peace.")
            exit(0)
    
    def move_left(self):
        '''
        move_left() --> Maze \n
        Displays a message.
        '''
        print("You are unable to move to the left. A wall blocks your path.")
        return self

    def move_right(self):
        '''
        move_right() --> Maze \n
        Displays a message.
        '''
        print("You are unable to move to the right. A wall blocks your path.")
        return self

    def __str__(self):
        '''
        str(Enemy) --> String \n
        Returns a string reprentation of the object.
        '''
        return "Enemy"

    def __repr__(self):
        '''
        repr(Enemy) --> String \n
        Returns a string representing the object's definition.
        '''
        return f"Enemy({repr(self.forward)})"


class Exit(Maze):
    """ Exit variant of the Maze class. Endpoint which results in winning the game. """
    def __init__(self, **kwargs):
        self.description = random.choice(GameObject.descriptions['exit'])

    def move_forward(self):
        '''
        move_forward() --> void \n
        Displays message and exits the maze.
        '''
        print("You made it out!")
        exit(0)

    def move_left(self):
        '''
        move_left() --> void \n
        Points to move_forward().
        '''
        self.move_forward()

    def move_right(self):
        '''
        move_right() --> void \n
        Points to move_forward().
        '''
        self.move_forward()

    def fight(self):
        '''
        fight() --> void \n
        Displays message.
        '''
        print("There is nothing to fight here...except yourself. You give yourself a good face whacking and move on.")
    
    def __str__(self):
        '''
        str(Exit) --> String \n
        Returns a string reprentation of the object.
        '''
        return "Exit"

    def __repr__(self):
        '''
        repr(Exit) --> String \n
        Returns a string representing the object's definition.
        '''
        return f"Exit()"

class GameObject:
    """ Handles User/IO and the recursive generation of Maze objects. """
    # Static attributes
    maze_variants = [
        Fork, Fork, Fork, Fork, Fork, Fork,
        Room, Room, Room, Room, Room,
        Enemy, Enemy, Enemy, Enemy
    ]

    maze_endpoints = [DeadEnd, Exit]

    descriptions = {
        'fork': [],
        'exit': [],
        'deadend': [],
        'enemy': [],
        'room': [],
    }
    recursion_limit = 20

    for f in descriptions:
        try:
            with open(f"{f}.txt", "r") as f_desc:
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
        '''
        fight() --> void \n
        Calls corresponding Maze function.
        '''
        self.maze.fight()

    def elaborate(self):
        '''
        elaborate() --> void \n
        Calls corresponding Maze function.
        '''
        self.maze.elaborate()

    def move_forward(self):
        '''
        move_forward() --> void \n
        Reassigns current Maze to the Forward Maze.
        '''
        self.maze = self.maze.move_forward()

    def move_left(self):
        '''
        move_left() --> void \n
        Reassigns current Maze to the Left Maze.
        '''
        self.maze = self.maze.move_left()

    def move_right(self):
        '''
        move_right() --> void \n
        Reassigns current Maze to the Right Maze.
        '''
        self.maze = self.maze.move_left()

    def prompt(self):
        '''
        prompt() --> void \n
        Takes input from the user and matches to the current command list. \n
        If the Command is vaild, it executes. \n
        Otherwise, it displays an error message.
        '''
        user_input = input("> ").upper()
        if user_input in self.commands:
            self.commands[user_input]()
        else:
            print("You've entered an invalid command. Type 'help' to see what commands are available.")

    def help(self):
        '''
        help() --> void \n
        Displays information on all the valid commands.
        '''
        print("'help' --> brings up this help context.")
        print("'look' --> prints information about the room you're currently in.")
        print("'fight' --> engages in hand-to-hand combat with potential assailants.")
        print("'forward' --> allows the user to move forward if possible.")
        print("'left' --> allows the user to move to the left if possible.")
        print("'right' --> allows the user to move to the right if possible.")

    @staticmethod
    def set_recursion_limit(new_limit):
        '''
        set_recursion_limit(new_limit) --> void \n
        Sets the recursion limit.
        '''
        GameObject.recursion_limit = new_limit

    @staticmethod
    def get_endpoint():
        '''
        get_endpoint() --> Maze \n
        Returns either a DeadEnd or Exit Maze.

        '''
        return random.choice(GameObject.maze_endpoints)

    @staticmethod
    def get_maze():
        '''
        get_maze() --> Maze \n
        Returns one of: Room, Enemy, or Fork Maze.
        '''
        return random.choice(GameObject.maze_variants)

    def __str__(self):
        '''
        str(GameObject) --> String \n
        Returns a string reprentation of the object.
        '''
        return "GameObject"

    def __repr__(self):
        '''
        repr(GameObject) --> String \n
        Returns a string representing the object's definition.
        '''
        return "GameObject()"


if debug:
    ##############################################
    ############## GameObject Tests ##############
    ##############################################

    # Static Function Tests
    assert GameObject.get_maze() in GameObject.maze_variants, f"get_maze() failed to produce valid maze variant in {GameObject}."
    assert GameObject.get_endpoint() in GameObject.maze_endpoints, f"get_endpoint() failed to produce a valid endpoint in {GameObject}." 
    recursion_limit = GameObject.recursion_limit
    GameObject.set_recursion_limit(20)
    assert GameObject.recursion_limit == 20, f"set_recursion_limit() failed in {GameObject}."

    # GameObject Movement Tests
    # Move Left
    myGame = GameObject()
    old_maze = myGame.maze
    myGame.move_left()
    new_maze = myGame.maze
    assert old_maze is not new_maze, f"move_left() failed in {myGame}."
    del myGame

    # Move Right
    myGame = GameObject()
    old_maze = myGame.maze
    myGame.move_left()
    new_maze = myGame.maze
    assert old_maze is not new_maze, f"move_right() failed in {myGame}."

    # Move Forward
    myGame.maze = Room(forward=DeadEnd(), depth=GameObject.recursion_limit)
    old_maze = myGame.maze
    myGame.move_forward()
    new_maze = myGame.maze
    assert old_maze is not new_maze, f"move_forward() failed in {myGame}."

    # Elaborate
    assert myGame.descriptions is not None, f"Descriptions are undefined in {myGame}."
    assert myGame.maze.description is not None,  f"Maze description is undefined in {myGame}."
    del myGame

    ######################################################
    ################# Generic Maze Tests #################
    ######################################################
    myMaze = Maze()
    assert myMaze.description is not None, "Maze description was left uninitialized."
    del myMaze

    ######################################################
    ################# Maze Variant Tests #################
    ######################################################
    myFork = Fork(depth=GameObject.recursion_limit)
    myRoom = Room(depth=GameObject.recursion_limit)
    myEnemy = Enemy(depth=GameObject.recursion_limit)
    myDeadEnd = DeadEnd()
    myExit = Exit()
    fullMaze = Fork(depth=GameObject.recursion_limit)
    myRoom.forward = DeadEnd()
    fullMaze.left = myRoom
    myEnemy.forward = Exit()
    fullMaze.right = myEnemy

    assert myFork is not None, f"Fork initialization failed."
    assert myFork is myFork.move_forward(), f"move_forward() erroneously allowed forward movement in {myFork}."
    assert myFork is not myFork.move_right(), f"move_right() failed in {myFork}."
    assert myFork is not myFork.move_left(), f"move_left() failed in {myFork}."
    assert myFork.description is not None, f"Fork description left uninitialized in {myFork}."
    assert myRoom is not None, f"Room initialization failed."
    assert myRoom is myRoom.move_left(), f"move_left() erroneously allowed leftward movement in {myRoom}."
    assert myRoom is myRoom.move_right(), f"move_right() erroneously allowed forward movement in {myRoom}."
    assert myRoom is not myRoom.move_forward(), f"move_forward() failed in {myRoom}."
    assert myRoom.description is not None, f"Room description left uninitialized in {myRoom}."
    assert myEnemy is not None, f"Enemy initialization failed."
    assert myEnemy is myEnemy.move_left(), f"move_left() erroneously allowed leftward movement in {myEnemy}."
    assert myEnemy is myEnemy.move_right(), f"move_right() erroneously allowed forward movement in {myEnemy}."
    assert myEnemy is myEnemy.move_forward(), f"move_forward() erroneously allowed forward movement without defeating enemy in {myEnemy}."
    myEnemy.enemy_dead = True
    assert myEnemy is not myEnemy.move_forward(), f"move_forward() failed in {myEnemy}."
    assert myEnemy.description is not None, f"Fork description left uninitialized in {myEnemy}."
    assert myDeadEnd is not None, f"DeadEnd initialization failed."
    assert myExit is not None, f"Exit initialization failed."
    assert str(fullMaze) == "Fork", f"str() failed in {fullMaze}."
    assert repr(fullMaze) == "Fork(Room(DeadEnd()), Enemy(Exit()))", f"repr() failed in {fullMaze}."

# Define the global GameObject
mazeGame = GameObject()
print()
print("Welcome to the maze of mystery! Inside, you may live, die, or escape. The journey is the destination!")
print("Type 'help' to learn what commands you can use.")
print()
while True:
    mazeGame.prompt()