"""Оружие и фабрика доступных вариантов."""

from __future__ import annotations

from dataclasses import dataclass

from constants import WEAPON_PISTOL, WEAPON_RIFLE


@dataclass
class Weapon:
    """Описание параметров оружия."""

    name: str
    damage: int
    bullet_speed: float
    cooldown: float
    range_distance: float


class WeaponFactory:
    """Выдаёт объекты оружия по имени."""

    @staticmethod
    def create(weapon_name: str) -> Weapon:
        if weapon_name == WEAPON_PISTOL:
            return Weapon(
                name=WEAPON_PISTOL,
                damage=24,
                bullet_speed=620,
                cooldown=0.35,
                range_distance=520,
            )
        if weapon_name == WEAPON_RIFLE:
            return Weapon(
                name=WEAPON_RIFLE,
                damage=14,
                bullet_speed=700,
                cooldown=0.1,
                range_distance=620,
            )
        raise ValueError(f"Неизвестное оружие: {weapon_name}")
