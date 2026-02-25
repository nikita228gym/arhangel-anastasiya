"""Утилиты для математики, коллизий и обзора."""

from __future__ import annotations

import math
from typing import Iterable

import pygame


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Ограничивает число диапазоном."""
    return max(min_value, min(value, max_value))


def normalize_angle(angle_rad: float) -> float:
    """Нормализует угол в диапазоне [-pi, pi]."""
    while angle_rad > math.pi:
        angle_rad -= 2 * math.pi
    while angle_rad < -math.pi:
        angle_rad += 2 * math.pi
    return angle_rad


def angle_to_target(origin: pygame.Vector2, target: pygame.Vector2) -> float:
    """Возвращает угол направления от origin к target в радианах."""
    delta = target - origin
    return math.atan2(delta.y, delta.x)


def point_in_fov(
    origin: pygame.Vector2,
    facing_angle: float,
    target: pygame.Vector2,
    fov_angle_deg: float,
    max_distance: float,
) -> bool:
    """Проверяет, находится ли цель внутри угла обзора и дистанции."""
    delta = target - origin
    distance = delta.length()
    if distance > max_distance or distance <= 1e-5:
        return False

    target_angle = math.atan2(delta.y, delta.x)
    diff = abs(normalize_angle(target_angle - facing_angle))
    return diff <= math.radians(fov_angle_deg / 2)


def line_of_sight(
    origin: pygame.Vector2,
    target: pygame.Vector2,
    walls: Iterable[pygame.Rect],
    step: float,
) -> bool:
    """Проверяет видимость лучом между двумя точками с учётом стен."""
    direction = target - origin
    distance = direction.length()
    if distance <= 1e-6:
        return True

    direction = direction.normalize()
    traveled = 0.0
    point = pygame.Vector2(origin)

    while traveled < distance:
        for wall in walls:
            if wall.collidepoint(point.x, point.y):
                return False
        point += direction * step
        traveled += step

    return True


def circle_rect_collision(center: pygame.Vector2, radius: float, rect: pygame.Rect) -> bool:
    """Проверяет столкновение окружности и прямоугольника."""
    nearest_x = clamp(center.x, rect.left, rect.right)
    nearest_y = clamp(center.y, rect.top, rect.bottom)
    dx = center.x - nearest_x
    dy = center.y - nearest_y
    return dx * dx + dy * dy <= radius * radius
