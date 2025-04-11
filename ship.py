import pygame as pg
from settings import Settings




class Ship():

    def __init__(self, ai_game):
        self.settings = Settings()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # загрузка изображения корабля и получение его прямоугольника
        self.image = pg.image.load('img/ship.png')
        self.rect = self.image.get_rect()

        # появление корабля у нижнего края
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def update(self):

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed_factor

    def blitme(self):
        # отрисовка корабля
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)






