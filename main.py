"""Точка входа в игру."""

from __future__ import annotations

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game import GameSession
from menu import MenuManager


def main() -> None:
    """Инициализирует pygame и управляет циклами меню/матча."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    menu = MenuManager(screen)

    running = True
    while running:
        action = menu.run_main_menu()
        if action == "quit":
            break

        map_name = menu.run_map_select()
        if map_name is None:
            break

        team = menu.run_team_select()
        if team is None:
            break

        weapon_name = menu.run_weapon_select()
        if weapon_name is None:
            break

        session = GameSession(screen, map_name, team, weapon_name)
        result = session.run()
        if result == "quit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
