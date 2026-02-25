"""Компоненты UI: кнопки и простые помощники."""

from __future__ import annotations

import pygame

from constants import COLOR_BUTTON, COLOR_BUTTON_HOVER, COLOR_TEXT


class Button:
    """Кликабельная кнопка с текстом."""

    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font) -> None:
        self.rect = rect
        self.text = text
        self.font = font

    def draw(self, surface: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        hovered = self.rect.collidepoint(mouse_pos)
        color = COLOR_BUTTON_HOVER if hovered else COLOR_BUTTON
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (180, 180, 210), self.rect, width=2, border_radius=8)

        text_surf = self.font.render(self.text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text_center(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    y: int,
    color: tuple[int, int, int] = COLOR_TEXT,
) -> None:
    """Рисует текст по центру экрана на заданной высоте."""
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surf, text_rect)
