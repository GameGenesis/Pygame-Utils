import pygame
from pygame.math import Vector2
from json_save import JsonSave

from pygame_utils import Alignment, Button, Canvas, CheckBox, EventManager, InputBox, Label, Panel, Square, Circle, Color

velocity = [400, 400]
current_velocity = velocity
score = JsonSave.load("save_data.json", "Score", 0)

def set_score(value):
    global score
    score = int(value)

def increment_score(value=1):
    global score
    score += value

def toggle_velocity(event):
    global velocity, current_velocity
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        current_velocity = [0, 0] if current_velocity != [0, 0] else velocity

def main():
    pygame.init()
    surface_size = (480, 720)

    clock = pygame.time.Clock()

    pygame.display.set_caption("Game")
    main_surface = pygame.display.set_mode(surface_size)

    t_last = 0

    circle = Circle(Vector2(20, 20), 20, Color.RED)

    def toggle_color(on):
        circle.color = Color.BLUE if on else Color.RED

    # panel = Panel()
    score_text = Label(font_size=60, text=score, position=(surface_size[0] - 25, 35), anchor=Alignment.TOP_RIGHT)
    button = Button(position=Vector2(25, 25), label=Label("Button", Color.BLACK, font_size=40), on_click=increment_score, disabled=False, label_alignment=Alignment.CENTER)
    check_box = CheckBox(position=Vector2(25, surface_size[1] - 75), on_value_change=toggle_color)
    input_box = InputBox(position=Vector2(surface_size[0] - 200, surface_size[1] - 75), on_submit=set_score)
    # event_manager = EventManager(toggle_velocity, on_quit=lambda: JsonSave.save("save_data.json", "Score", score))


    while True:
        EventManager.INSTANCE.handle_events()

        # Current frame ticks in ms
        t = pygame.time.get_ticks()
        # DeltaTime in seconds
        delta_time = (t - t_last) / 1000.0

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
        score_text.set_text(score)
        Canvas.INSTANCE.draw()

        pygame.display.flip()

        clock.tick(60)

        # Storing the last frame ticks
        t_last = t

main()