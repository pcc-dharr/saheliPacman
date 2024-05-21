#creates fruit object

import pygame
from entity import Entity  
from constants import *  # Importing constants
from sprites import FruitSprites  # Importing FruitSprites class

class Fruit(Entity):
    def __init__(self, node, level=0):
        """
        Initializes the Fruit object with the given node and optional level.

        Args:
            node (Node): The node where the fruit is placed.
            level (int, optional): The level of the game. Defaults to 0.
        """
        Entity.__init__(self, node)  # Initialize the base class (Entity)
        self.name = FRUIT  # Set the name to FRUIT (constant from constants.py)
        self.color = GREEN  # Set the color of the fruit
        self.lifespan = 5  # Lifespan of the fruit in seconds
        self.timer = 0  # Timer to track lifespan
        self.destroy = False  # Flag to indicate if the fruit should be destroyed
        self.points = 100 + level * 20  # Points awarded for collecting the fruit (scaled with level)
        self.setBetweenNodes(RIGHT)  # Start the fruit moving towards the right
        self.sprites = FruitSprites(self, level)  # Create fruit sprites for animation

    def update(self, dt):
        """
        Updates the state of the fruit over time.

        Args:
            dt (float): The time elapsed since the last update.
        """
        self.timer += dt  # Increment the timer by the elapsed time
        if self.timer >= self.lifespan:
            self.destroy = True  # Set the destroy flag if the fruit's lifespan is over
