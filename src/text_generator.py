import pygame.font
from pygame.font import Font

class TextGenerator():
    @staticmethod
    def generate_text(msg, fontparams, bgcolour):
        fontpath = pygame.font.match_font(fontparams["name"], True)
        font = Font(fontpath, fontparams["size"])
        return font.render(msg, True, fontparams["colour"], bgcolour)
