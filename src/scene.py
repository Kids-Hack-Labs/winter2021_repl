from pygame import Color, Rect, Surface

class Scene():
    def __init__(self, questions, scene_info):
        self.bg_colour = scene_info["background"]

    def update(self, delta):
        pass

    def render(self, target):
        target.fill(self.bg_colour)
