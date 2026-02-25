"""Пули и их поведение в игровом мире."""

from __future__ import annotations

import pygame

from constants import COLOR_BULLET


class Bullet:
    """Пуля с направлением, скоростью и уроном."""

    def __init__(
        self,
        position: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float,
        damage: int,
        team: str,
        max_distance: float,
    ) -> None:
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction).normalize()
        self.speed = speed
        self.damage = damage
        self.team = team
        self.max_distance = max_distance
        self.travelled = 0.0
        self.radius = 4
        self.alive = True

    def update(self, dt: float, walls: list[pygame.Rect], entities: list) -> None:
        """Обновляет позицию и проверяет попадания/столкновения."""
        if not self.alive:
            return

        move_vec = self.direction * self.speed * dt
        next_pos = self.position + move_vec

        # Попадание в стены
        for wall in walls:
            if wall.collidepoint(next_pos.x, next_pos.y):
                self.alive = False
                return

        # Попадание в игроков/ботов
        for entity in entities:
            if not entity.alive or entity.team == self.team:
                continue
            if entity.position.distance_to(next_pos) <= entity.radius:
                entity.take_damage(self.damage)
                self.alive = False
                return

        self.position = next_pos
        self.travelled += move_vec.length()
        if self.travelled >= self.max_distance:
            self.alive = False

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        """Рисует пулю как маленький круг."""
        if not self.alive:
            return
        draw_pos = self.position - camera_offset
        pygame.draw.circle(surface, COLOR_BULLET, (int(draw_pos.x), int(draw_pos.y)), self.radius)
