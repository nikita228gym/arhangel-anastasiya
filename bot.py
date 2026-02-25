"""Боты с простым ИИ: patrol / chase / attack."""

from __future__ import annotations

import random

import pygame

from constants import BOT_ATTACK_DISTANCE, BOT_CHASE_DISTANCE, BOT_PATROL_WAIT
from player import Fighter


class Bot(Fighter):
    """ИИ-бот, умеющий патрулировать и атаковать врага."""

    def __init__(self, position: pygame.Vector2, team: str, weapon_name: str) -> None:
        super().__init__(position, team, weapon_name)
        self.state = "patrol"
        self.current_target: Fighter | None = None
        self.patrol_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        if self.patrol_direction.length_squared() == 0:
            self.patrol_direction = pygame.Vector2(1, 0)
        self.patrol_timer = random.uniform(0.2, 1.5)

    def choose_enemy(self, candidates: list[Fighter], walls: list[pygame.Rect]) -> Fighter | None:
        visible = [c for c in candidates if c.team != self.team and c.alive and self.can_see(c, walls)]
        if not visible:
            return None
        visible.sort(key=lambda e: self.position.distance_to(e.position))
        return visible[0]

    def update_ai(self, dt: float, walls: list[pygame.Rect], all_entities: list[Fighter]) -> pygame.Vector2:
        """Возвращает направление движения; стрельба выполняется отдельно."""
        if not self.alive:
            return pygame.Vector2()

        enemy = self.choose_enemy(all_entities, walls)
        if enemy:
            self.current_target = enemy
            distance = self.position.distance_to(enemy.position)
            if distance <= BOT_ATTACK_DISTANCE:
                self.state = "attack"
            elif distance <= BOT_CHASE_DISTANCE:
                self.state = "chase"
            else:
                self.state = "patrol"
        elif self.current_target and self.current_target.alive:
            self.state = "chase"
        else:
            self.current_target = None
            self.state = "patrol"

        if self.state == "attack" and self.current_target:
            to_enemy = self.current_target.position - self.position
            self.angle = to_enemy.as_polar()[1] * (3.14159265 / 180)
            return pygame.Vector2()

        if self.state == "chase" and self.current_target and self.current_target.alive:
            to_enemy = self.current_target.position - self.position
            self.angle = to_enemy.as_polar()[1] * (3.14159265 / 180)
            if to_enemy.length_squared() > 0:
                return to_enemy.normalize()
            return pygame.Vector2()

        # patrol
        self.patrol_timer -= dt
        if self.patrol_timer <= 0:
            self.patrol_timer = BOT_PATROL_WAIT + random.uniform(0, 1.0)
            self.patrol_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            if self.patrol_direction.length_squared() == 0:
                self.patrol_direction = pygame.Vector2(1, 0)
        self.angle = self.patrol_direction.as_polar()[1] * (3.14159265 / 180)
        return self.patrol_direction

    def try_attack(self) -> pygame.Vector2 | None:
        """Возвращает направление выстрела, если бот должен атаковать."""
        if self.state != "attack" or not self.current_target or not self.current_target.alive:
            return None
        direction = self.current_target.position - self.position
        if direction.length_squared() <= 0:
            return None
        return direction.normalize()
