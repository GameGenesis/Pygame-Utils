import os
import sys
import time

from random import randint, choice
import pygame

from ui import Canvas

class State():
    """
    Parent class to inherit from for each game state
    """
    def __init__(self, state_stack: list) -> None:
        """
        Parameters
        ----------
        state_stack : list
            A reference to a list of states

        Returns
        -------
        None
        """
        self.state_stack = state_stack
        self.prev_state = None

    def update(self, delta_time: float, events: list[pygame.event.Event]) -> None:
        """
        Unimplemented base class update method.
        This method is run every frame

        Parameters
        ----------
        delta_time : float
            Application delta time for movement
        events : list[Event]
            A list of pygame events for the current frame

        Returns
        -------
        None
        """
        pass

    def enter_state(self) -> None:
        """
        Adds this state to the state stack as the current stack

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if len(self.state_stack) > 1:
            self.prev_state = self.state_stack[-1]
        self.state_stack.append(self)

    def exit_state(self) -> None:
        """
        Removes this state from the state stack and removes all canvas objects

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        if self.state_stack:
            Canvas.update_managed_objects(list())
            self.state_stack.pop()
