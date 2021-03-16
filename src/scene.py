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
        temp = {"next"      :self.next_scene,
                "answer1"   :self.answer1,
                "answer2"   :self.answer2,
                "answer3"   :self.answer3,
                "answer4"   :self.answer4}
        self.buttons = {}
        if scene_info.get("button_params"):
            self.buttons = {key:Button(text_info[key],
                                       scene_info["font_params"]["buttons"],
                                       scene_info["button_params"][key], temp[key])
                            for key in scene_info.get("button_params").keys()}

    def update(self, delta):
        for name in self.buttons.keys():
            self.buttons[name].update(delta)

    def render(self, target):
        target.fill(self.bg_colour)
        self.question_rect.center = (target.get_rect().centerx, self.question_rect.height)
        target.blit(self.question_surf, self.question_rect)
        for name in self.buttons.keys():
            self.buttons[name].render(target)

    def next_scene(self):
        from engine.game_env import Game
        Game.instance.request_next_scene()

    def answer1(self):
        pass

    def answer2(self):
        pass

    def answer3(self):
        pass

    def answer4(self):
        pass

    def answer(self, num):
        pass
