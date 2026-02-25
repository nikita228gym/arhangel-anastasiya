"""Игровая сцена: спавн, логика раунда, ИИ, рендер."""

from __future__ import annotations

import math
import random

import pygame

from bot import Bot
from bullet import Bullet
from constants import COLOR_BG, COLOR_FOV, COLOR_TEXT, FOV_ANGLE, FPS, TEAM_BLUE, TEAM_RED
from map_loader import GameMap, load_map
from player import Fighter, Player
from ui import draw_text_center
from utils import line_of_sight, point_in_fov


class GameSession:
    """Управляет матчем на выбранной карте."""

    def __init__(self, screen: pygame.Surface, map_name: str, player_team: str, weapon_name: str) -> None:
        self.screen = screen
        self.map: GameMap = load_map(map_name)
        self.player_team = player_team
        self.weapon_name = weapon_name

        self.font = pygame.font.SysFont("arial", 24)
        self.big_font = pygame.font.SysFont("arial", 44)

        self.player: Player
        self.blue_team: list[Fighter] = []
        self.red_team: list[Fighter] = []
        self.bullets: list[Bullet] = []
        self.round_result_text = ""
        self.round_over = False

        self._spawn_teams()

    def _spawn_teams(self) -> None:
        """Создаёт игрока и ботов для обеих команд."""
        blue_spawns, red_spawns = self.map.find_spawn_points()
        random.shuffle(blue_spawns)
        random.shuffle(red_spawns)

        if self.player_team == TEAM_BLUE:
            self.player = Player(blue_spawns.pop(), TEAM_BLUE, self.weapon_name)
            self.blue_team = [self.player]
            self.red_team = [Bot(red_spawns.pop(), TEAM_RED, "Автомат") for _ in range(4)]
            self.blue_team.extend(Bot(blue_spawns.pop(), TEAM_BLUE, "Пистолет") for _ in range(3))
        else:
            self.player = Player(red_spawns.pop(), TEAM_RED, self.weapon_name)
            self.red_team = [self.player]
            self.blue_team = [Bot(blue_spawns.pop(), TEAM_BLUE, "Автомат") for _ in range(4)]
            self.red_team.extend(Bot(red_spawns.pop(), TEAM_RED, "Пистолет") for _ in range(3))

    def all_entities(self) -> list[Fighter]:
        return self.blue_team + self.red_team

    def _update_player(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        movement = self.player.handle_input(keys)
        self.player.move_with_collision(movement, self.map.walls, dt)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        camera_offset = self.get_camera_offset()
        world_mouse = pygame.Vector2(mouse_x, mouse_y) + camera_offset
        aim_vec = world_mouse - self.player.position
        if aim_vec.length_squared() > 0:
            self.player.angle = math.atan2(aim_vec.y, aim_vec.x)

        if pygame.mouse.get_pressed()[0]:
            bullet = self.player.try_shoot(aim_vec)
            if bullet:
                self.bullets.append(bullet)

    def _update_bots(self, dt: float) -> None:
        entities = self.all_entities()
        for entity in entities:
            if not isinstance(entity, Bot) or not entity.alive:
                continue
            move_dir = entity.update_ai(dt, self.map.walls, entities)
            entity.move_with_collision(move_dir, self.map.walls, dt)

            attack_dir = entity.try_attack()
            if attack_dir is not None:
                # Дополнительная проверка прямой видимости перед выстрелом
                if entity.current_target and line_of_sight(
                    entity.position,
                    entity.current_target.position,
                    self.map.walls,
                    10,
                ):
                    bullet = entity.try_shoot(attack_dir)
                    if bullet:
                        self.bullets.append(bullet)

    def _update_bullets(self, dt: float) -> None:
        entities = self.all_entities()
        for bullet in self.bullets:
            bullet.update(dt, self.map.walls, entities)
        self.bullets = [b for b in self.bullets if b.alive]

    def _check_round_end(self) -> None:
        blue_alive = any(e.alive for e in self.blue_team)
        red_alive = any(e.alive for e in self.red_team)

        if blue_alive and red_alive:
            return

        self.round_over = True
        if blue_alive:
            self.round_result_text = "Раунд завершён: победили Синие"
        elif red_alive:
            self.round_result_text = "Раунд завершён: победили Красные"
        else:
            self.round_result_text = "Раунд завершён: ничья"

    def get_camera_offset(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.player.position.x - self.screen.get_width() / 2,
            self.player.position.y - self.screen.get_height() / 2,
        )

    def _draw_fov_overlay(self, camera_offset: pygame.Vector2) -> None:
        """Рисует затемнение и сектор видимости игрока."""
        darkness = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        darkness.fill((0, 0, 0, 190))

        vision = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        origin = self.player.position - camera_offset
        points = [origin]
        half = math.radians(FOV_ANGLE / 2)

        for i in range(64):
            t = i / 63
            ray_angle = self.player.angle - half + (2 * half * t)
            direction = pygame.Vector2(math.cos(ray_angle), math.sin(ray_angle))
            ray_end = self._cast_ray(self.player.position, direction)
            points.append(ray_end - camera_offset)

        pygame.draw.polygon(vision, COLOR_FOV, points)

        # Вырезаем видимую область из затемнения
        darkness.blit(vision, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(darkness, (0, 0))

    def _cast_ray(self, origin: pygame.Vector2, direction: pygame.Vector2) -> pygame.Vector2:
        """Кастует луч, пока не встретит стену или предел дистанции."""
        step = 8
        max_dist = 430
        pos = pygame.Vector2(origin)
        for _ in range(max_dist // step):
            pos += direction * step
            if any(wall.collidepoint(pos.x, pos.y) for wall in self.map.walls):
                return pos
        return pos

    def _entity_visible_for_player(self, entity: Fighter) -> bool:
        if entity is self.player or not entity.alive:
            return False
        if not point_in_fov(self.player.position, self.player.angle, entity.position, 90, 420):
            return False
        return line_of_sight(self.player.position, entity.position, self.map.walls, 10)

    def _draw_world(self) -> None:
        camera_offset = self.get_camera_offset()
        self.screen.fill(COLOR_BG)
        self.map.draw(self.screen, camera_offset)

        for bullet in self.bullets:
            bullet.draw(self.screen, camera_offset)

        # Игрок видит только врагов в поле зрения; союзники рисуются всегда для удобства
        for entity in self.all_entities():
            if entity is self.player:
                entity.draw(self.screen, camera_offset)
            elif entity.team == self.player.team:
                entity.draw(self.screen, camera_offset)
            elif self._entity_visible_for_player(entity):
                entity.draw(self.screen, camera_offset)

        self._draw_fov_overlay(camera_offset)
        self._draw_hud()

    def _draw_hud(self) -> None:
        blue_alive = sum(1 for e in self.blue_team if e.alive)
        red_alive = sum(1 for e in self.red_team if e.alive)

        hud = f"Синие: {blue_alive}   Красные: {red_alive}   HP: {self.player.hp}   Оружие: {self.player.weapon.name}"
        text_surf = self.font.render(hud, True, COLOR_TEXT)
        self.screen.blit(text_surf, (20, 20))

        if self.round_over:
            draw_text_center(self.screen, self.big_font, self.round_result_text, 120)
            draw_text_center(self.screen, self.font, "Нажмите ESC для выхода в меню", 165)

    def run(self) -> str:
        """Запускает игровой цикл раунда."""
        clock = pygame.time.Clock()

        while True:
            dt = clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "menu"

            if not self.round_over and self.player.alive:
                self.player.update_cooldown(dt)
                self._update_player(dt)

            for entity in self.all_entities():
                entity.update_cooldown(dt)

            if not self.round_over:
                self._update_bots(dt)
                self._update_bullets(dt)
                self._check_round_end()

            self._draw_world()
            pygame.display.flip()
