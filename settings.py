import pygame as pg
from datetime import datetime


class Settings():

    def __init__(self):
        pg.init()
        # настройки экрана
        self.screen_width = 1200
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # настройки корабля
        # тут короче жизней на одну меньшье чем написано. Типо 0 - можно выдержать одну атаку врага вот...
        self.ship_limit = 0


        # настройки снарядов
        self.bullet_width = 5
        self.bullet_height = 50
        self.bullet_color = (255, 0, 0)
        self.bullets_allowed = 3

        # настройки прищельцев
        self.fleet_drop_speed = 15

        # темп игры
        self.speedup_scale = 1.1
        # темп роста стоимости прищельцев
        self.score_sclae = 1.5

        self.initialize_dynamic_settings()







        self.button_left = [pg.K_LEFT, pg.K_a]
        self.button_right = [pg.K_RIGHT, pg.K_d]

        self.game_over_background = pg.image.load("/Users/dmitry/Desktop/GAME/GAME/GAME/img/Game_over_gb.png")
        self.background = pg.transform.scale(self.game_over_background, (self.screen_width, self.screen_height))

        self.background = pg.image.load('img/background.jpg')
        self.background = pg.transform.scale(self.background, (self.screen_width, self.screen_height))

        self.menu_background = pg.image.load('img/menu_background.png')
        self.menu_background = pg.transform.scale(self.menu_background, (self.screen_width, self.screen_height))

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 0.75
        self.bullet_speed_factor = 1.25
        self.alien_speed_factor = 1.0

        # fleet_direction = 1 обозначает движение вправо; а -1 влево
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_sclae)
        print(self.alien_points)


