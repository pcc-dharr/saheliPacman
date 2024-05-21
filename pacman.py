#creating pacman entity

import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        # Initialize Pacman entity
        Entity.__init__(self, node)
        self.name = PACMAN
        self.directions = {STOP: Vector2(), UP: Vector2(0, -1), DOWN: Vector2(0, 1), LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0)}
        self.direction = LEFT  # Initial direction
        self.speed = 100 * TILEWIDTH / 16  # Speed of Pacman
        self.radius = 10  # Radius of Pacman's collider
        self.color = YELLOW  # Color of Pacman
        self.setBetweenNodes(LEFT)  # Set Pacman between nodes initially
        self.node = node  # Current node of Pacman
        self.target = node  # Target node of Pacman
        self.collideRadius = 5  # Collider radius for collision checks
        self.alive = True  # Pacman's alive status
        self.sprites = PacmanSprites(self)  # Pacman's sprites
        self.reset()  # Reset Pacman's initial state

    def setPosition(self):
        # Set Pacman's position to its current node's position
        self.position = self.node.position.copy()

    def reset(self):
        # Reset Pacman's state to initial settings
        Entity.reset(self)  # Call parent class reset method
        self.direction = LEFT  # Reset direction to LEFT
        self.setBetweenNodes(LEFT)  # Set Pacman between nodes
        self.alive = True  # Set Pacman's alive status to True
        self.image = self.sprites.getStartImage()  # Get Pacman's starting image
        self.sprites.reset()  # Reset Pacman's sprites

    def die(self):
        # Set Pacman's alive status to False and stop its movement
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        # Update Pacman's position and behavior based on input and game state
        self.sprites.update(dt)  # Update Pacman's sprites
        self.position += self.directions[self.direction] * self.speed * dt  # Move Pacman
        direction = self.getValidKey()  # Get valid input direction
        if self.overshotTarget():  # Check if Pacman has overshot its target node
            # Update Pacman's current node and target node based on direction
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)  # Get new target node
            if self.target is not self.node:  # If Pacman has a new target
                self.direction = direction  # Update Pacman's direction
            else:
                self.target = self.getNewTarget(self.direction)  # Get new target in current direction
            if self.target is self.node:  # If Pacman's target is its current node
                self.direction = STOP  # Stop Pacman's movement
            self.setPosition()  # Set Pacman's position to its current node
        else:
            if self.oppositeDirection(direction):  # If Pacman tries to move in opposite direction
                self.reverseDirection()  # Reverse Pacman's direction

    def validDirection(self, direction):
        # Check if a direction is valid for Pacman to move
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        # Get a new target node for Pacman based on direction
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def getValidKey(self):
        # Get valid directional input key
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def overshotTarget(self):
        # Check if Pacman has overshot its target node
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        # Reverse Pacman's direction and swap current and target nodes
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        # Check if the given direction is opposite to Pacman's current direction
        if direction is not STOP:  # If the direction is not STOP
            if direction == self.direction * -1:  # If the direction is opposite to the current direction
                return True  # Return True, indicating the direction is opposite
        return False  # Return False if the direction is STOP or not opposite to the current direction

    def eatPellets(self, pelletList):
        # Check if Pacman collides with any pellets in the given list
        for pellet in pelletList:  # Iterate through the pellet list
            if self.collideCheck(pellet):  # Check collision with each pellet
                return pellet  # Return the pellet if collision occurs
        return None  # Return None if no collision with pellets

    def collideGhost(self, ghost):
        # Check if Pacman collides with a ghost
        return self.collideCheck(ghost)  # Delegate collision check to collideCheck method for the ghost entity

    def collideCheck(self, other):
        # Check if Pacman collides with the given entity (pellet or ghost)
        d = self.position - other.position  # Calculate the vector between Pacman and the other entity
        dSquared = d.magnitudeSquared()  # Calculate the squared distance
        rSquared = (self.collideRadius + other.collideRadius)**2  # Calculate the squared sum of radii
        if dSquared <= rSquared:  # If the squared distance is less than or equal to the squared sum of radii
            return True  # Collision occurred, return True
        return False  # No collision, return False
