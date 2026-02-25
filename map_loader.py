"""Загрузка тайловых карт и работа с геометрией мира."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from constants import COLOR_GRID, COLOR_WALL, TILE_SIZE


MAP_DATA = {
    "map1": [
        "11111111111111111111",
        "10000000000100000001",
        "10111111100101111101",
        "10000000100100000101",
        "10111100111101110101",
        "10100000100001000101",
        "10101111101111010101",
        "10100000000001010101",
        "10101111111101010101",
        "10100010000001000101",
        "10111010111101111101",
        "10000010000100000001",
        "11111111111111111111",
    ],
    "map2": [
        "11111111111111111111",
        "10000000010000000001",
        "10111111010111111101",
        "10100001010100000101",
        "10101101010101110101",
        "10101001000101000101",
        "10101011111101011101",
        "10101000000101010001",
        "10101111110101010101",
        "10100000010100010101",
        "10111111010111110101",
        "10000000010000000001",
        "11111111111111111111",
    ],
}


@dataclass
class GameMap:
    """Описание карты: тайлы и список стен."""

    name: str
    tiles: list[str]

    def __post_init__(self) -> None:
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)
        self.walls = self._build_walls()

    def _build_walls(self) -> list[pygame.Rect]:
        walls: list[pygame.Rect] = []
        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                if cell == "1":
                    walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return walls

    def draw(self, surface: pygame.Surface, camera_offset: pygame.Vector2) -> None:
        """Отрисовывает сетку и стены карты."""
        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                rect = pygame.Rect(
                    x * TILE_SIZE - camera_offset.x,
                    y * TILE_SIZE - camera_offset.y,
                    TILE_SIZE,
                    TILE_SIZE,
                )
                pygame.draw.rect(surface, COLOR_GRID, rect, 1)
                if cell == "1":
                    pygame.draw.rect(surface, COLOR_WALL, rect)

    def find_spawn_points(self) -> tuple[list[pygame.Vector2], list[pygame.Vector2]]:
        """Возвращает две группы стартовых точек для команд."""
        blue_spawns: list[pygame.Vector2] = []
        red_spawns: list[pygame.Vector2] = []

        for y, row in enumerate(self.tiles):
            for x, cell in enumerate(row):
                if cell != "0":
                    continue
                pos = pygame.Vector2(
                    x * TILE_SIZE + TILE_SIZE / 2,
                    y * TILE_SIZE + TILE_SIZE / 2,
                )
                if x < self.width // 2:
                    blue_spawns.append(pos)
                else:
                    red_spawns.append(pos)

        return blue_spawns, red_spawns


def load_map(name: str) -> GameMap:
    """Загружает карту по имени."""
    if name not in MAP_DATA:
        raise ValueError(f"Карта '{name}' не найдена")
    return GameMap(name=name, tiles=MAP_DATA[name])
