import pygame as pg
import sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from music_sounds import MusicSounds
from random import randint
from button import Button


class AlienInvasion:

    def __init__(self):

        pg.init()
        self.sound = MusicSounds()
        self.settings = Settings()

        self.stats = GameStats(self)

        pg.time.Clock().tick(60)

        # создание экрана
        self.screen = pg.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption('Alien Invasion')

        self.ship = Ship(self)

        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")
        self.replay_button = Button(self, "Replay")
        self.exit_button = Button(self, "Exit game")

        self.sound.play_menu_music()

    def run_game(self):
        while True:
            # self.settings.bullet_color = (randint(100, 255), randint(100, 255), randint(0, 100))
            self._check_events()
            print(self.settings.ship_limit, self.stats.game_active, self.stats.game_over)

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()

            self._update_screen()

    def _check_events(self):
        for event in pg.event.get():
            if self.stats.game_active:
                if event.type == pg.QUIT:
                    sys.exit()

                elif event.type == pg.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pg.KEYUP:
                    self._check_keyup_events(event)
            else:
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    self._check_button(mouse_pos)

    def _update_screen(self):
        if self.stats.game_active:
            # Заливка экрана фоном
            self.screen.blit(self.settings.background, (0, 0))
            # каждый цикл перерисовывается экрна
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

        elif self.stats.game_over:
            self.screen.blit(self.settings.game_over_background, (0, 0))
            self.replay_button.draw_button()
            self.exit_button.draw_button()
        elif not self.stats.game_active:
            self.screen.blit(self.settings.menu_background, (0, 0))
            self.play_button.draw_button()

        pg.display.flip()

    def _check_keyup_events(self, event):
        if event.key in self.settings.button_right:
            self.ship.moving_right = False
        elif event.key in self.settings.button_left:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        if event.key in self.settings.button_right:
            self.ship.moving_right = True
        elif event.key in self.settings.button_left:
            self.ship.moving_left = True
        elif event.key == pg.K_SPACE:
            self._fire_bullet()

    def _check_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            pg.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.sound.play_main_music()

        elif self.exit_button.rect.collidepoint(mouse_pos) and self.stats.game_over:
            sys.exit()

        elif self.replay_button.rect.collidepoint(mouse_pos) and self.stats.game_over:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_over = False
            self.stats.game_active = True

            pg.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.sound.play_main_music()

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            MusicSounds().play_sound_fire()

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        collisions = pg.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        # if collisions:
        # MusicSounds.destroy_alien_ship()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = (
            pg.sprite.groupcollide(self.bullets, self.aliens, True, True)
        )

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

            self.settings.increase_speed()

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (
                self.settings.screen_height - (3 * alien_width) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = (alien_width + 2 * alien_width * alien_number) + 111
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_alien(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            self.stats.game_over = True
            self.sound.play_menu_music()
            pg.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


# запуск игры
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
