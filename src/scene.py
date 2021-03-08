from pygame import Color, Rect, Surface
from src.text_generator import TextGenerator
from src.button import Button

class Scene():
    def __init__(self, text_info, scene_info):
        self.bg_colour = scene_info["background"]
        self.question_surf = TextGenerator.generate_text(text_info["question"],
                                                         scene_info["font_params"]["question"],
                                                         self.bg_colour)
        self.question_rect = self.question_surf.get_rect()
        self.buttons = {}

    def update(self, delta):
        pass
    
    def render(self, target):
        target.fill(self.bg_colour)
        self.question_rect.center = (target.get_rect().centerx, self.question_rect.height)
        target.blit(self.question_surf, self.question_rect)

    def next_scene(self):
        pass
    
    def answer1(self):
        pass

    def answer2(self):
        pass

    def answer3(self):
        pass

    def answer4(self):
        pass
