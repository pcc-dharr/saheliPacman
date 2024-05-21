#animates for all characters

from constants import *

class Animator(object):
    def __init__(self, frames=None, speed=20, loop=True):
        """
        Initializes the Animator object.

        Args:
            frames (list): A list of frames for the animation. Defaults to an empty list.
            speed (int): The speed of the animation (frames per second). Defaults to 20.
            loop (bool): Whether the animation should loop. Defaults to True.
        """
        self.frames = frames if frames is not None else []  # Initialize frames to an empty list if none provided
        self.current_frame = 0  # Index of the current frame being displayed
        self.speed = speed  # Speed of the animation in frames per second
        self.loop = loop  # Flag to indicate if the animation should loop
        self.dt = 0  # Time accumulator for frame switching
        self.finished = False  # Flag to indicate if the animation has finished

    def reset(self):
        """
        Resets the animation to the beginning.
        """
        self.current_frame = 0  # Reset the current frame to the first frame
        self.finished = False  # Mark the animation as not finished

    def update(self, dt):
        """
        Updates the current frame of the animation based on the elapsed time.

        Args:
            dt (float): The time elapsed since the last update call.

        Returns:
            The current frame of the animation.
        """
        if not self.finished:
            self.nextFrame(dt)  # Advance to the next frame if the animation is not finished
        if self.current_frame == len(self.frames):  # Check if the current frame is the last frame
            if self.loop:
                self.current_frame = 0  # Loop back to the first frame if looping is enabled
            else:
                self.finished = True  # Mark the animation as finished
                self.current_frame = max(0, len(self.frames) - 1)  # Stay at the last frame if not looping

        return self.frames[self.current_frame]  # Return the current frame

    def nextFrame(self, dt):
        """
        Advances to the next frame based on the elapsed time.

        Args:
            dt (float): The time elapsed since the last frame switch.
        """
        self.dt += dt  # Accumulate the elapsed time
        if self.dt >= (1 / float(self.speed)):  # Check if enough time has passed to switch frames
            self.current_frame += 1  # Advance to the next frame
            self.dt = 0  # Reset the time accumulator
