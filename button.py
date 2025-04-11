from typing import Any

import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.width, self.height = 200, 50

        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        if msg.lower() == "play":
            self.button_color = ('#0376BB')
            self.text_color = (255, 255, 255)
            self.font = pygame.font.SysFont(None, 48)

            self.rect[1] += 100

        elif msg.lower() == "replay":
            self.button_color = ('#0376BB')
            self.text_color = (255, 255, 255)
            self.font = pygame.font.SysFont(None, 48)

            self.rect[0] -= 200
            self.rect[1] += 100

        elif msg.lower() == "exit game":
            self.button_color = ('#0376BB')
            self.text_color = (255, 255, 255)
            self.font = pygame.font.SysFont(None, 48)

            self.rect[0] += 200
            self.rect[1] += 100



        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)



