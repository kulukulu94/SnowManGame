import pygame
from pygame.locals import *

# Initializes pygame's modules
pygame.init()

class Keyboard():
    """
    Returns True if the key IS pressed, it means
    the press-check occurs every frame
    """
    def key_pressed(self, key):
        key = self.to_pattern(key)
        keys = pygame.key.get_pressed()
        if keys[key]:
            return True

        return False
    
    """Shows the int code of the key"""
    def show_key_pressed(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                print(event.key)
                
    def to_pattern(self, key):
        key = key.lower()
        if key == "left":
            return pygame.K_LEFT
        elif key == "right":
            return pygame.K_RIGHT
        elif key == "up":
            return pygame.K_UP
        elif key == "down":
            return pygame.K_DOWN
        elif key == "enter" or key== "return":
            return pygame.K_RETURN
        elif key == "escape" or key == "esc":
            return pygame.K_ESCAPE
        elif key == "space":
            return pygame.K_SPACE
        elif key == "left_control":
            return pygame.K_LCTRL
        elif key == "left_shift":
            return pygame.K_LSHIFT
        elif "a" <= key <= "z":
            return getattr(pygame, "K_" + key.lower())
        elif "0" <= key <= "9":
            return getattr(pygame, "K_" + key)
        return key
