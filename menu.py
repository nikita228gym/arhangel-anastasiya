"""Экраны меню: главное, выбор карты, стороны и оружия."""

from __future__ import annotations

import pygame

from constants import COLOR_BG, MAP_NAMES, TEAM_BLUE, TEAM_RED, WEAPON_PISTOL, WEAPON_RIFLE
from ui import Button, draw_text_center


class MenuManager:
    """Управляет переходами между экранами подготовки матча."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font_title = pygame.font.SysFont("arial", 52)
        self.font_button = pygame.font.SysFont("arial", 30)

    def run_main_menu(self) -> str:
        """Главное меню: старт или выход."""
        start_btn = Button(pygame.Rect(500, 300, 280, 60), "Начать игру", self.font_button)
        quit_btn = Button(pygame.Rect(500, 390, 280, 60), "Выход", self.font_button)
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if start_btn.is_clicked(event):
                    return "start"
                if quit_btn.is_clicked(event):
                    return "quit"

            self.screen.fill(COLOR_BG)
            draw_text_center(self.screen, self.font_title, "Тактический шутер", 170)
            start_btn.draw(self.screen, mouse_pos)
            quit_btn.draw(self.screen, mouse_pos)
            pygame.display.flip()
            clock.tick(60)

    def run_map_select(self) -> str | None:
        """Экран выбора карты."""
        buttons = [
            Button(pygame.Rect(500, 280, 280, 58), "map1", self.font_button),
            Button(pygame.Rect(500, 355, 280, 58), "map2", self.font_button),
        ]
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                for idx, btn in enumerate(buttons):
                    if btn.is_clicked(event):
                        return MAP_NAMES[idx]

            self.screen.fill(COLOR_BG)
            draw_text_center(self.screen, self.font_title, "Выбор карты", 170)
            for btn in buttons:
                btn.draw(self.screen, mouse_pos)
            pygame.display.flip()
            clock.tick(60)

    def run_team_select(self) -> str | None:
        """Экран выбора стороны."""
        blue_btn = Button(pygame.Rect(500, 280, 280, 58), "Команда Синих", self.font_button)
        red_btn = Button(pygame.Rect(500, 355, 280, 58), "Команда Красных", self.font_button)
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if blue_btn.is_clicked(event):
                    return TEAM_BLUE
                if red_btn.is_clicked(event):
                    return TEAM_RED

            self.screen.fill(COLOR_BG)
            draw_text_center(self.screen, self.font_title, "Выбор стороны", 170)
            blue_btn.draw(self.screen, mouse_pos)
            red_btn.draw(self.screen, mouse_pos)
            pygame.display.flip()
            clock.tick(60)

    def run_weapon_select(self) -> str | None:
        """Экран закупки оружия."""
        pistol_btn = Button(pygame.Rect(500, 280, 280, 58), WEAPON_PISTOL, self.font_button)
        rifle_btn = Button(pygame.Rect(500, 355, 280, 58), WEAPON_RIFLE, self.font_button)
        clock = pygame.time.Clock()

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if pistol_btn.is_clicked(event):
                    return WEAPON_PISTOL
                if rifle_btn.is_clicked(event):
                    return WEAPON_RIFLE

            self.screen.fill(COLOR_BG)
            draw_text_center(self.screen, self.font_title, "Закупка", 170)
            draw_text_center(self.screen, self.font_button, "Выберите оружие на раунд", 225)
            pistol_btn.draw(self.screen, mouse_pos)
            rifle_btn.draw(self.screen, mouse_pos)
            pygame.display.flip()
            clock.tick(60)
