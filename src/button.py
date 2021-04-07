from pygame import Color, Rect, Surface
import pygame.mouse as pm
from src.text_generator import TextGenerator

class Button():
    STATES = ("NONE","OUT","HOVER","DOWN","UP")
    def __init__(self, button_text, text_info, button_info, func):
        self.colours = {Button.STATES[1]:button_info["out"],
                        Button.STATES[2]:button_info["hover"],
                        Button.STATES[3]:button_info["down"],
                        Button.STATES[4]:button_info["up"]}
        self.rect = Rect(button_info["rect"])
        self.surf = Surface(self.rect.size)
        self.text_surf = TextGenerator.generate_text(button_text, text_info, None)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = (self.rect.width/2, self.rect.height/2)
        self.on_click = func
        self.current_state = Button.STATES[1]
        self.previous_state = Button.STATES[1]
        self.active = True

    def update(self, delta):
        if self.active:
            self.current_state = self.check_states()
            if self.previous_state == Button.STATES[3] and\
               self.current_state == Button.STATES[2]:
                self.on_click()
            self.previous_state = self.current_state

    def render(self,target):
        self.surf.fill(self.colours[self.current_state])
        self.surf.blit(self.text_surf, self.text_rect)
        target.blit(self.surf, self.rect)

    def check_states(self):
        mouse_pos = pm.get_pos()
        mouse_buttons = pm.get_pressed()

        if not self.rect.collidepoint(mouse_pos):
            return Button.STATES[1]
        else:
            if not mouse_buttons[0]:
                return Button.STATES[2]
            else:
                return Button.STATES[3]

    def deactivate(self):
        self.active = False
        self.current_state = Button.STATES[4]

    def set_correct(self):
        self.current_state = Button.STATES[1]
