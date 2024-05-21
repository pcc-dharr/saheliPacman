#determines the general actions of each charcter

import pygame
from pygame.locals import *
from vector import Vector2  
from constants import *  # Importing constants
from random import randint  # Importing random integer function

class Entity(object):
    def __init__(self, node):
        """
        Initializes the Entity object with the given start node.

        Args:
            node (Node): The starting node for the entity.
        """
        self.name = None
        # Directions mapped to vector movements
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1), 
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP  # Initial direction is STOP
        self.setSpeed(100)  # Set initial speed
        self.radius = 10  # Radius for rendering the entity
        self.collideRadius = 5  # Radius for collision detection
        self.color = WHITE  # Default color
        self.visible = True  # Entity visibility
        self.disablePortal = False  # Portal usage flag
        self.goal = None  # Goal position
        self.directionMethod = self.goalDirection  # Method to determine direction
        self.setStartNode(node)  # Set start node and initial position
        self.image = None  # Entity image

    def setStartNode(self, node):
        """
        Sets the start node for the entity and initializes position and target.

        Args:
            node (Node): The node to set as the start node.
        """
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def reset(self):
        """
        Resets the entity to its start node and initial state.
        """
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def setBetweenNodes(self, direction):
        """
        Sets the entity's position to be between two nodes in a given direction.

        Args:
            direction (int): The direction to move between nodes.
        """
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def setPosition(self):
        """
        Sets the entity's position to the current node's position.
        """
        self.position = self.node.position.copy()

    def update(self, dt):
        """
        Updates the entity's position and direction based on elapsed time.

        Args:
            dt (float): The time delta since the last update.
        """
        self.position += self.directions[self.direction] * self.speed * dt
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal and self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            self.setPosition()

    def validDirection(self, direction):
        """
        Checks if a given direction is valid from the current node.

        Args:
            direction (int): The direction to check.

        Returns:
            bool: True if the direction is valid, False otherwise.
        """
        if direction is not STOP:
            if self.name in self.node.access[direction] and self.node.neighbors[direction] is not None:
                return True
        return False

    def validDirections(self):
        """
        Returns a list of valid directions the entity can move to from the current node.

        Returns:
            list: A list of valid direction constants.
        """
        directions = [key for key in [UP, DOWN, LEFT, RIGHT] if self.validDirection(key) and key != self.direction * -1]
        if not directions:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        """
        Chooses a random direction from the list of valid directions.

        Args:
            directions (list): The list of valid directions.

        Returns:
            int: A randomly chosen direction.
        """
        return directions[randint(0, len(directions) - 1)]

    def getNewTarget(self, direction):
        """
        Gets the new target node in the specified direction.

        Args:
            direction (int): The direction to move to.

        Returns:
            Node: The new target node.
        """
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        """
        Checks if the entity has overshot its target node.

        Returns:
            bool: True if the entity has overshot the target, False otherwise.
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        """
        Reverses the entity's direction.
        """
        self.direction *= -1
        self.node, self.target = self.target, self.node

    def oppositeDirection(self, direction):
        """
        Checks if a given direction is the opposite of the current direction.

        Args:
            direction (int): The direction to check.

        Returns:
            bool: True if the direction is opposite, False otherwise.
        """
        return direction == self.direction * -1

    def setSpeed(self, speed):
        """
        Sets the entity's speed.

        Args:
            speed (int): The speed to set.
        """
        self.speed = speed * TILEWIDTH / 16

    def goalDirection(self, directions):
        """
        Determines the direction that brings the entity closest to its goal.

        Args:
            directions (list): A list of valid directions.

        Returns:
            int: The direction that minimizes the distance to the goal.
        """
        distances = [((self.node.position + self.directions[direction] * TILEWIDTH) - self.goal).magnitudeSquared() for direction in directions]
        return directions[distances.index(min(distances))]

    def render(self, screen):
        """
        Renders the entity on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the entity on.
        """
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
