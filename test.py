import pygame
from pygame.math import Vector2
from utils.json_save import JsonSave

from utils.pygame_utils import Alignment, Button, Canvas, CheckBox, EventManager, InputBox, Label, Panel, Square, Circle, Color, UiImage

FPS = 60
WINDOW_SIZE = (480, 720)

VELOCITY = [400, 400]
current_velocity = VELOCITY

score = JsonSave.load("save_data.json", "Score", 0)

def set_score(value):
    global score
    score = int(value)

def increment_score(value=1):
    global score
    score += value

def toggle_velocity(event):
    global VELOCITY, current_velocity
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_velocity = [0, 0] if current_velocity != [0, 0] else VELOCITY

def main():
    pygame.init()

    clock = pygame.time.Clock()

    pygame.display.set_caption("Game")
    main_surface = pygame.display.set_mode(WINDOW_SIZE)

    circle = Circle(Vector2(20, 20), 20, Color.RED)

    def toggle_color(on):
        circle.color = Color.BLUE if on else Color.RED

    panel = Panel()
    fps_text = Label(position=Vector2(WINDOW_SIZE[0]-25, 20), color=Color.BLACK, anchor=Alignment.MID_RIGHT)
    score_text = Label(font_size=60, text=score, position=Vector2(WINDOW_SIZE[0] - 25, 40), anchor=Alignment.TOP_RIGHT)
    button = Button(position=Vector2(25, 25), label=Label("Button", Color.BLACK, font_size=40), on_click=increment_score, disabled=False, label_alignment=Alignment.CENTER)
    check_box = CheckBox(position=Vector2(25, WINDOW_SIZE[1] - 75), on_value_change=toggle_color)
    input_box = InputBox(position=Vector2(WINDOW_SIZE[0] - 200, WINDOW_SIZE[1] - 75), on_submit=set_score)
    button2 = Button(image=UiImage(file_name="images/Present_64px.png"), size=Vector2(150, 150), position=Vector2(WINDOW_SIZE[0]/2 - 75, WINDOW_SIZE[1]/2 - 75), on_click=increment_score)
    EventManager.set_events(toggle_velocity, on_quit=lambda: JsonSave.save("save_data.json", "Score", score))

    while True:
        delta_time = float(clock.tick(FPS)) / 1000.0
        EventManager.handle_events()

        # Moving 200 pixels per second in the positive x direction
        circle.move(circle.position.x + current_velocity[0] * delta_time, circle.position.y + current_velocity[1] * delta_time)

        if current_velocity != [0, 0]:
            if circle.position.x + circle.radius/2 >= main_surface.get_width() or circle.position.x - circle.radius/2 <= 0:
                current_velocity[0] *= -1
            if circle.position.y + circle.radius/2 >= main_surface.get_height() or circle.position.y - circle.radius/2 <= 0:
                current_velocity[1] *= -1

        main_surface.fill((0, 200, 255))
        circle.draw(main_surface)

        # UI Elements
        fps_text.set_text(f"FPS: {int(clock.get_fps())}")
        score_text.set_text(score)
        Canvas.draw()

        pygame.display.update()

        # Storing the last frame ticks
main()