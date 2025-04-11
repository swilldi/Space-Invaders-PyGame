import pygame as pg


class MusicSounds:
    def __init__(self):
        self.music_now = ""

        self.sound_fire = pg.mixer.Sound("sound_file/Fire.wav")
        self.sound_fire.set_volume(0.1)


        # self.destoy_ship = pg.mixer.Sound("sound_file/")
        # self.lose_music = pg.mixer.Sound("sound_file/")
        self.menu_background = pg.mixer.Sound("/Users/dmitry/Desktop/GAME/GAME/GAME/sound_file/menu_background.mp3")
        self.menu_background.set_volume(0.3)


        self.main_background = pg.mixer.Sound('sound_file/Background music.mp3')
        self.main_background.set_volume(0.3)


    def play_main_music(self):
        if self.music_now == "main_bg":
            pass
        else:
            pg.mixer.pause()
            self.main_background.play(-1)
            self.music_now = "main_bg"

    def play_menu_music(self):
        if self.music_now == "menu_bg":
            pass
        else:
            pg.mixer.pause()
            self.menu_background.play(-1)
            self.music_now = "menu_bg"

    def play_sound_fire(self):
        self.sound_fire.play()

    # def destroy_alien_ship(self):
        # self.destroy_ship.play()
    #
    # def game_over_music(self):
        # self.lose_music.play()

