import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes a Ghost object.

        Args:
            node (Node): The starting node for the ghost.
            pacman (Entity): The Pac-Man entity the ghost interacts with.
            blinky (Ghost): The Blinky ghost instance for certain behaviors.
        """
        Entity.__init__(self, node)
        self.name = GHOST  # Assigning the entity name
        self.points = 200  # Points awarded for catching this ghost
        self.goal = Vector2()  # Initial goal position for the ghost
        self.pacman = pacman  # Reference to the Pac-Man entity
        self.mode = ModeController(self)  # Mode controller for different ghost behaviors
        self.blinky = blinky  # Reference to the Blinky ghost
        self.homeNode = node  # The node where the ghost starts

    def update(self, dt):
        """
        Updates the ghost's state.

        Args:
            dt (float): Time elapsed since the last update.
        """
        self.sprites.update(dt)  # Update ghost sprites/animations
        self.mode.update(dt)  # Update ghost mode (scatter, chase, etc.)
        if self.mode.current is SCATTER:
            self.scatter()  # Execute scatter behavior
        elif self.mode.current is CHASE:
            self.chase()  # Execute chase behavior
        Entity.update(self, dt)  # Update ghost movement based on mode

    def reset(self):
        """
        Resets the ghost's state to default values.
        """
        Entity.reset(self)  # Reset inherited attributes from the base class
        self.points = 200  # Reset points awarded for catching the ghost
        self.directionMethod = self.goalDirection  # Reset the direction method to goalDirection
    
    def scatter(self):
        """
        Sets the ghost's goal position to empty, representing a scattered state.
        """
        self.goal = Vector2()  # Set the goal position to an empty vector
    
    def chase(self):
        """
        Sets the ghost's goal position to the position of the Pac-Man entity.
        """
        self.goal = self.pacman.position  # Set the goal position to the Pac-Man's position
    
    def startFreight(self):
        """
        Starts the freight mode for the ghost, changing its behavior and speed.
        """
        self.mode.setFreightMode()  # Set the ghost mode to freight mode
        if self.mode.current == FREIGHT:
            self.setSpeed(50)  # Reduce speed during freight mode
            self.directionMethod = self.randomDirection  # Change direction method to randomDirection
    
    def normalMode(self):
        """
        Sets the ghost back to normal mode with default speed and behavior.
        """
        self.setSpeed(100)  # Set the ghost speed back to normal
        self.directionMethod = self.goalDirection  # Change direction method to goalDirection
        self.homeNode.denyAccess(DOWN, self)  # Deny access in the downward direction at the home node
    
    def spawn(self):
        """
        Sets the ghost's goal position to its spawn node's position.
        """
        self.goal = self.spawnNode.position  # Set the goal position to the spawn node's position
    
    def setSpawnNode(self, node):
        """
        Sets the spawn node for the ghost.
    
        Args:
            node (Node): The node where the ghost spawns.
        """
        self.spawnNode = node  # Set the spawn node for the ghost
    
    def startSpawn(self):
        """
        Starts the spawn mode for the ghost, changing its behavior and speed.
        """
        self.mode.setSpawnMode()  # Set the ghost mode to spawn mode
        if self.mode.current == SPAWN:
            self.setSpeed(150)  # Increase speed during spawn mode
            self.directionMethod = self.goalDirection  # Change direction method to goalDirection
            self.spawn()  # Move the ghost to its spawn position

class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes the Blinky ghost.

        Args:
            node (Node): The starting node for Blinky.
            pacman (Entity): The Pac-Man entity for Blinky to interact with.
            blinky (Ghost): Reference to another Blinky ghost.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY  # Name of the ghost
        self.color = RED  # Color of the ghost
        self.sprites = GhostSprites(self)  # Sprite animations for the ghost

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes the Pinky ghost.

        Args:
            node (Node): The starting node for Pinky.
            pacman (Entity): The Pac-Man entity for Pinky to interact with.
            blinky (Ghost): Reference to another Blinky ghost.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY  # Name of the ghost
        self.color = PINK  # Color of the ghost
        self.sprites = GhostSprites(self)  # Sprite animations for the ghost

    def scatter(self):
        """
        Sets Pinky's goal position for scatter behavior.
        """
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)  # Set goal for scatter behavior

    def chase(self):
        """
        Sets Pinky's goal position for chase behavior.
        """
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
        # Set goal for chase behavior



class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes the Inky ghost.

        Args:
            node (Node): The starting node for Inky.
            pacman (Entity): The Pac-Man entity for Inky to interact with.
            blinky (Ghost): Reference to a Blinky ghost.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY  # Name of the ghost
        self.color = TEAL  # Color of the ghost
        self.sprites = GhostSprites(self)  # Sprite animations for the ghost

    def scatter(self):
        """
        Sets Inky's goal position for scatter behavior.
        """
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)  # Set goal for scatter behavior

    def chase(self):
        """
        Sets Inky's goal position for chase behavior.
        """
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2  # Set goal for chase behavior based on Pac-Man and Blinky positions


class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        """
        Initializes the Clyde ghost.

        Args:
            node (Node): The starting node for Clyde.
            pacman (Entity): The Pac-Man entity for Clyde to interact with.
            blinky (Ghost): Reference to a Blinky ghost.
        """
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE  # Name of the ghost
        self.color = ORANGE  # Color of the ghost
        self.sprites = GhostSprites(self)  # Sprite animations for the ghost

    def scatter(self):
        """
        Sets Clyde's goal position for scatter behavior.
        """
        self.goal = Vector2(0, TILEHEIGHT*NROWS)  # Set goal for scatter behavior

    def chase(self):
        """
        Sets Clyde's goal position for chase behavior.
        """
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()  # Chase behavior changes to scatter if close to Pac-Man
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4
            # Set goal for chase behavior based on Pac-Man position and direction



class GhostGroup(object):
    def __init__(self, node, pacman):
        """
        Initializes a group of ghosts.

        Args:
            node (Node): The starting node for the ghosts.
            pacman (Entity): The Pac-Man entity for the ghosts to interact with.
        """
        # Initialize each type of ghost and store them in a list
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        """
        Allows iteration over the ghost group.
        """
        return iter(self.ghosts)

    def update(self, dt):
        """
        Updates all ghosts in the group.

        Args:
            dt (float): Time elapsed since the last update.
        """
        # Update each ghost in the group
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        """
        Initiates freight mode for all ghosts in the group.
        """
        # Start freight mode for each ghost and reset their points
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        """
        Sets the spawn node for all ghosts in the group.

        Args:
            node (Node): The spawn node for the ghosts.
        """
        # Set the spawn node for each ghost
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        """
        Updates the points for all ghosts in the group.
        """
        # Double the points for each ghost
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        """
        Resets the points for all ghosts in the group.
        """
        # Reset points to their default value
        for ghost in self:
            ghost.points = 200

    def reset(self):
        """
        Resets all ghosts in the group.
        """
        # Reset each ghost
        for ghost in self:
            ghost.reset()

    def hide(self):
        """
        Hides all ghosts in the group.
        """
        # Hide each ghost
        for ghost in self:
            ghost.visible = False

    def show(self):
        """
        Shows all ghosts in the group.
        """
        # Show each ghost
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        """
        Renders all ghosts in the group.

        Args:
            screen: The pygame screen to render the ghosts on.
        """
        # Render each ghost on the screen
        for ghost in self:
            ghost.render(screen)
