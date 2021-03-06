import os
import sys
import pygame
from pygame.math import Vector2

sys.path.append(os.getcwd())

from utils.json_save import JsonSave
from utils.ui import Alignment, Button, Canvas, CheckBox, EventManager, InputBox, Label, Panel, Color, UiImage
from utils.shape import Circle
from utils.window import Window
import utils.logger as logging

FPS = 60
WINDOW_SIZE = (480, 720)

VELOCITY = [400, 400]
current_velocity = VELOCITY

SAVE_FILE = os.path.abspath(os.path.join("examples", "save_data.json"))
score = JsonSave.load(SAVE_FILE, "Score", 0)

def quit_game():
    logging.logger.error("Quit game!", stack_info=True, stacklevel=1)
    pygame.quit()
    sys.exit()

def set_score(value):
    global score
    score = int(value)

def increment_score(value=1):
    global score
    score += value
    logging.logger.debug(f"Score: {score}")

def toggle_velocity(event):
    global VELOCITY, current_velocity
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_velocity = [0, 0] if current_velocity != [0, 0] else VELOCITY
        logging.logger.warning("Velocity has been updated")

def main():
    logging.init_logger()
    window = Window(WINDOW_SIZE)

    circle = Circle(Vector2(20, 20), 20, Color.RED)

    def toggle_ui(event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            panel.visible = not panel.visible

    def toggle_color(on):
        circle.color = Color.BLUE if on else Color.RED

    panel = Panel()
    fps_text = Label(position=Vector2(WINDOW_SIZE[0]-25, 20), color=Color.BLACK, anchor=Alignment.MID_RIGHT)
    score_text = Label(font_size=60, text=score, position=Vector2(WINDOW_SIZE[0] - 25, 40), anchor=Alignment.TOP_RIGHT)
    check_box = CheckBox(position=Vector2(25, WINDOW_SIZE[1] - 75), on_value_change=toggle_color)
    input_box = InputBox(position=Vector2(WINDOW_SIZE[0] - 200, WINDOW_SIZE[1] - 75), on_submit=set_score)
    quit_button = Button(position=Vector2(25, 25), label=Label("Quit", Color.BLACK, font_size=40), on_click=quit_game, disabled=False, label_alignment=Alignment.CENTER)
    present_button = Button(image=UiImage(file_name=os.path.abspath("examples\\images\\Present_64px.png")), size=Vector2(150, 150), position=Vector2(WINDOW_SIZE[0]/2 - 75, WINDOW_SIZE[1]/2 - 75), on_click=increment_score, parent=panel)

    for ge in Canvas.graphic_elements:
        if not isinstance(ge, Panel):
            ge.parent = panel

    EventManager.set_events([toggle_velocity, toggle_ui], on_quit=lambda: JsonSave.save(SAVE_FILE, "Score", score))

    while True:
        delta_time = window.get_delta_time(window.clock.tick(FPS))

        for event in EventManager.handle_events():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("Restart")

        # Moving 200 pixels per second in the positive x direction
        circle.move(circle.position.x + current_velocity[0] * delta_time, circle.position.y + current_velocity[1] * delta_time)

        if current_velocity != [0, 0]:
            if circle.position.x + circle.radius/2 >= window.surface.get_width() or circle.position.x - circle.radius/2 <= 0:
                current_velocity[0] *= -1
            if circle.position.y + circle.radius/2 >= window.surface.get_height() or circle.position.y - circle.radius/2 <= 0:
                current_velocity[1] *= -1

        window.surface.fill((0, 200, 255))
        circle.draw(window.surface)

        # UI Elements
        fps_text.set_text(f"FPS: {int(window.clock.get_fps())}")
        score_text.set_text(score)
        Canvas.draw()

        pygame.display.update()

        # Storing the last frame ticks
main()