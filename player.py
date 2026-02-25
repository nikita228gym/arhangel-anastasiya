"""Класс игрока и общая логика бойца."""

from __future__ import annotations

import math

import pygame

from bullet import Bullet
from constants import (
    COLOR_BLUE,
    COLOR_HP_BG,
    COLOR_HP_FG,
    COLOR_RED,
    FOV_ANGLE,
    FOV_RANGE,
    PLAYER_HP,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    RAY_STEP,
)
from utils import circle_rect_collision, line_of_sight, point_in_fov
from weapon import Weapon, WeaponFactory


class Fighter:
    """Базовый боец, от которого наследуются игрок и бот."""

    def __init__(self, position: pygame.Vector2, team: str, weapon_name: str) -> None:
        self.position = pygame.Vector2(position)
        self.team = team
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.hp = PLAYER_HP
        self.max_hp = PLAYER_HP
        self.alive = True
        self.angle = 0.0
        self.weapon: Weapon = WeaponFactory.create(weapon_name)
        self.cooldown_timer = 0.0

    def update_cooldown(self, dt: float) -> None:
        self.cooldown_timer = max(0.0, self.cooldown_timer - dt)

    def take_damage(self, damage: int) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def move_with_collision(self, movement: pygame.Vector2, walls: list[pygame.Rect], dt: float) -> None:
        if movement.length_squared() <= 0:
            return

        direction = movement.normalize()
        delta = direction * self.speed * dt

        # Двигаем по X
        next_x = pygame.Vector2(self.position.x + delta.x, self.position.y)
        if not any(circle_rect_collision(next_x, self.radius, wall) for wall in walls):
            self.position.x = next_x.x

        # Двигаем по Y
        next_y = pygame.Vector2(self.position.x, self.position.y + delta.y)
        if not any(circle_rect_collision(next_y, self.radius, wall) for wall in walls):
            self.position.y = next_y.y

    def can_see(self, target: "Fighter", walls: list[pygame.Rect]) -> bool:
        """Проверяет видимость цели с учётом FOV и стен."""
        if not target.alive:
            return False
        if not point_in_fov(self.position, self.angle, target.position, FOV_ANGLE, FOV_RANGE):
            return False
        return line_of_sight(self.position, target.position, walls, RAY_STEP)

    def try_shoot(self, direction: pygame.Vector2) -> Bullet | None:
        """Пытается выстрелить, если перезарядка готова."""
        if self.cooldown_timer > 0 or not self.alive:
            return None
        if direction.length_squared() <= 0:
            return None

        self.cooldown_timer = self.weapon.cooldown
        return Bullet(
            position=self.position + direction.normalize() * (self.radius + 2),
            direction=direction,
            speed=self.weapon.bullet_speed,
            damage=self.weapon.damage,
            team=self.team,
            max_distance=self.weapon.range_distance,
        )

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        """Отрисовывает бойца и полоску здоровья."""
        if not self.alive:
            return

        color = COLOR_BLUE if self.team == "blue" else COLOR_RED
        draw_pos = self.position - camera_offset
        pygame.draw.circle(surface, color, (int(draw_pos.x), int(draw_pos.y)), self.radius)

        # Линия направления взгляда
        look_x = draw_pos.x + math.cos(self.angle) * (self.radius + 14)
        look_y = draw_pos.y + math.sin(self.angle) * (self.radius + 14)
        pygame.draw.line(surface, (245, 245, 245), draw_pos, (look_x, look_y), 2)

        # HP
        bar_w = self.radius * 2
        bar_h = 6
        hp_ratio = self.hp / self.max_hp
        bg_rect = pygame.Rect(draw_pos.x - self.radius, draw_pos.y - self.radius - 14, bar_w, bar_h)
        fg_rect = pygame.Rect(bg_rect.x, bg_rect.y, bar_w * hp_ratio, bar_h)
        pygame.draw.rect(surface, COLOR_HP_BG, bg_rect)
        pygame.draw.rect(surface, COLOR_HP_FG, fg_rect)


class Player(Fighter):
    """Игрок, управляемый клавиатурой и мышью."""

    def handle_input(self, keys: pygame.key.ScancodeWrapper) -> pygame.Vector2:
        movement = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            movement.y -= 1
        if keys[pygame.K_s]:
            movement.y += 1
        if keys[pygame.K_a]:
            movement.x -= 1
        if keys[pygame.K_d]:
            movement.x += 1
        return movement
