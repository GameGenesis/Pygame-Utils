import math

import pygame
from pygame.math import Vector2

from pygame_utils import ButtonManager, Button, CheckBox, EventManager, Label, Square, Circle, Color

class CollisonMath:
    @staticmethod
    def distance_from_points(point_1, point_2):
        '''
        This function calculates the distance between two points given by a set of tuples (x1,y1) and (x2,y2)

        Parameters
        ----------
        point1 : float
            The first point to compare
        point2 : float
            The second point to compare

        Returns
        float
            The distance between the two points
        '''
        distance = math.sqrt(((point_2[0]-point_1[0])**2)+((point_2[1]-point_1[1])**2))

        return distance

velocity = [400, 400]
current_velocity = velocity
score = 0

def increment_score(value=1):
    global score
    score += value

def toggle_velocity(event):
    global velocity, current_velocity
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_velocity = [0, 0] if current_velocity != [0, 0] else velocity

def main():
    #-----------------------------Setup------------------------------------------------------#
    """ Set up the game and run the main game loop """
    pygame.init()      # Prepare the pygame module for use
    surface_size = (480, 720)   # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  #Force frame rate to be slower


    # Create surface of (width, height), and its window.
    pygame.display.set_caption("Game")
    main_surface = pygame.display.set_mode(surface_size)

    #-----------------------------Program Variable Initialization----------------------------#
    # Set up some data to describe a small circle and its color
    t_last = 0

    circle = Circle(Vector2(20, 20), Color.RED, 20)
    score_text = Label(font_size=60, text=score, position=(surface_size[0] - 50, 50), anchor="topright")

    def toggle_color(on):
        circle.color = Color.BLUE if on else Color.RED

    button = Button(position=Vector2(50, 50), label=Label("Button", Color.BLACK, font_size=40), on_click=increment_score, disabled=False)
    check_box = CheckBox(position=Vector2(50, surface_size[1] - 200), on_click=toggle_color)
    button_manager = ButtonManager()

    event_manager = EventManager([toggle_velocity, button_manager.handle_button_events])

    #-----------------------------Main Game Loop---------------------------------------------#
    while True:

        event_manager.handle_events()

        #-----------------------------Game Logic---------------------------------------------#
        # Update your game objects and data structures here...


        #-----------------------------Drawing Everything-------------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        main_surface.fill((0, 200, 255))

        # Current frame ticks in ms
        t = pygame.time.get_ticks()
        # DeltaTime in seconds.
        delta_time = (t - t_last) / 1000.0

        # Moving 200 pixels per second in the positive x direction
        circle.move(circle.pos.x + current_velocity[0] * delta_time, circle.pos.y + current_velocity[1] * delta_time)

        if current_velocity != [0, 0]:
            if circle.pos.x + circle.radius/2 >= main_surface.get_width() or circle.pos.x - circle.radius/2 <= 0:
                current_velocity[0] *= -1
            if circle.pos.y + circle.radius/2 >= main_surface.get_height() or circle.pos.y - circle.radius/2 <= 0:
                current_velocity[1] *= -1

        # Draw a circle on the surface
        circle.draw(main_surface)
        score_text.set_text(score)
        score_text.draw(main_surface)
        button.draw(main_surface)
        check_box.draw(main_surface)

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60) #Force frame rate to be slower

        # Storing the last frame ticks
        t_last = t


    pygame.quit()     # Once we leave the loop, close the window.

main()