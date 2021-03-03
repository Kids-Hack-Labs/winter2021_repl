#Note: As this module is imported into quiz.py, all paths become
#      relative to where quiz.py is
import pygame
from pygame.locals import *
from pygame.time import Clock
from engine.scene_manager import SceneManager
from src.scene import Scene

global FPS

class Game():
    class __Game():
        def __init__(self, config_info):
            global FPS
            FPS = config_info["FPS"]

            self.is_start = False
            self.is_run = False
            self.delta = 0
            self.time_since_started = 0
            self.clock = Clock()

            pygame.init()
            self.screen = pygame.display.set_mode((config_info["WIDTH"],
                                                   config_info["HEIGHT"]))
            pygame.display.set_caption(config_info["CAPTION"])
            self.time_since_started = pygame.time.get_ticks()

            SceneManager()
            self.scene = None
            self.is_run = True

        def start(self):
            temp = SceneManager.instance.request_scene_data(0, "TITLE")
            self.scene = Scene(temp[0], temp[1])
            self.is_start = pygame.get_init() and self.scene != None

        def process_events(self):
            for evt in pygame.event.get():
                if evt.type == QUIT:
                    self.quit()
                    
        def update(self, delta):
            self.scene.update(delta)

        def render(self, target):
            self.scene.render(target)
            pygame.display.flip()

        def run(self):
            if self.is_start:
                return
            self.start()
            while self.is_run:
                self.process_events()
                self.update(self.delta)
                self.render(self.screen)
                self.delta = self.clock.tick(FPS)
                self.time_since_started = pygame.time.get_ticks()
            pygame.quit()

        def quit(self):
            self.is_run = False

    #Singleton:
    instance = None
    def __init__(self, cfg_info):
        if not Game.instance:
            Game.instance = Game.__Game(cfg_info)

    def __getattr__(self, name):
        return getattr(self.instance, name)
