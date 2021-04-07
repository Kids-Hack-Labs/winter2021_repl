from pygame import Surface
from src.text_generator import TextGenerator
from src.button import Button

class Scene():
    score = 0
    def __init__(self, text_info, scene_info):
        self.bg_colour = scene_info["background"]

        self.correct_answer = text_info.get("correct", -1)
        
        self.score_surf = Surface((0,0))
        self.score_rect = self.score_surf.get_rect()
        self.score_params = None
        self.score_center = None
        if scene_info["font_params"].get("score", False):
            self.score_params = scene_info["font_params"]["score"]
            self.score_center = scene_info["score_pos"]
            self.redraw_score()

        self.timer = text_info.get("timer", 0) #note: timer is returned in ms
        self.max_time = text_info.get("timer", 0) #note: timer is returned in ms
        self.timer_surf = Surface((0,0))
        self.timer_rect = self.timer_surf.get_rect()
        self.timer_params = None
        self.timer_center = None
        if scene_info["font_params"].get("timer", False):
            self.timer_params = scene_info["font_params"]["timer"]
            self.timer_center = scene_info["timer_pos"]
            self.redraw_timer()

        self.answered = False
            
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

        if not self.answered:
            self.update_timer(delta)

    def render(self, target):
        target.fill(self.bg_colour)
        self.question_rect.center = (target.get_rect().centerx, self.question_rect.height)
        target.blit(self.question_surf, self.question_rect)
        for name in self.buttons.keys():
            self.buttons[name].render(target)
            
        target.blit(self.score_surf, self.score_rect)

        target.blit(self.timer_surf, self.timer_rect)

    def next_scene(self):
        if not self.answered:
            self.answer(0)
            return
        from engine.game_env import Game
        Game.instance.request_next_scene()

    def answer1(self):
        self.answer(1)

    def answer2(self):
        self.answer(2)

    def answer3(self):
        self.answer(3)

    def answer4(self):
        self.answer(4)

    def answer(self, num):
        self.answered = True
        if self.correct_answer == num:
            Scene.score += int(1000*self.timer/self.max_time)
            self.redraw_score() #Assumes valid self.score_params
        for button in self.buttons.keys():
            if button[0] == "a":
                self.buttons[button].deactivate()
        if self.correct_answer > 0:
            self.buttons["answer"+str(self.correct_answer)].set_correct()

    def redraw_score(self):
        self.score_surf = TextGenerator.generate_text(str(Scene.score),
                                                      self.score_params,
                                                      self.bg_colour)
        self.score_rect = self.score_surf.get_rect()
        self.score_rect.center = tuple(self.score_center)

    def redraw_timer(self):
        self.timer_surf = TextGenerator.generate_text(str(self.timer//1000),
                                                      self.timer_params,
                                                      self.bg_colour)
        self.timer_rect = self.timer_surf.get_rect()
        self.timer_rect.center = tuple(self.timer_center)

    def update_timer(self, delta):
        if self.answered:
            return
        self.timer -= delta
        if self.timer <= 0:
            self.answered = True
            self.answer(0)
            return
        self.redraw_timer()
