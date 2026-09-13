"""Núcleo do demake PaperDOOM-1.

Este módulo é um validador do protocolo de papel. Não lê WADs e não é um
port do motor DOOM.
"""
from dataclasses import dataclass
from typing import Dict, List, Tuple

DIRS = ("N", "E", "S", "W")
VECTORS = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
DAMAGE = {1: 5, 2: 10, 3: 15}


@dataclass
class Actor:
    ident: int = 1
    kind: str = "SENTINEL"
    x: int = 4
    y: int = 3
    hp: int = 20
    alive: bool = True
    cooldown: int = 0


@dataclass
class State:
    tick: int = 0
    phase: str = "PLAY"
    x: int = 1
    y: int = 3
    facing: str = "E"
    hp: int = 100
    ammo: int = 3
    rng_index: int = 0
    actor: Actor = None

    def __post_init__(self):
        if self.actor is None:
            self.actor = Actor()


class PaperDoom:
    """Simulador de uma sala mínima com F, T e A."""

    WIDTH = 7
    HEIGHT = 5
    TAPE = (2, 1, 3)

    def __init__(self):
        self.state = State()

    @staticmethod
    def _is_floor(x: int, y: int) -> bool:
        return 1 <= x <= 5 and 1 <= y <= 3

    @staticmethod
    def _direction_after_turn(facing: str) -> str:
        return DIRS[(DIRS.index(facing) + 1) % len(DIRS)]

    def checksum(self) -> int:
        s = self.state
        direction = DIRS.index(s.facing)
        living = 1 if s.actor.alive else 0
        return (
            s.tick + 3 * s.x + 5 * s.y + 7 * direction + 11 * s.hp
            + 13 * s.ammo + 19 * living + 23 * s.rng_index
        ) % 97

    def _actor_was_adjacent_at_start(self, before: Tuple[int, int]) -> bool:
        ax, ay = self.state.actor.x, self.state.actor.y
        px, py = before
        return abs(ax - px) + abs(ay - py) == 1

    def _attack(self) -> str:
        s = self.state
        if s.ammo <= 0:
            return "REJECTED_NO_AMMO"
        s.ammo -= 1
        dx, dy = VECTORS[s.facing]
        for distance in range(1, 6):
            x = s.x + dx * distance
            y = s.y + dy * distance
            if not self._is_floor(x, y):
                return "SHOT_BLOCKED"
            if s.actor.alive and (s.actor.x, s.actor.y) == (x, y):
                value = self.TAPE[s.rng_index % len(self.TAPE)]
                s.rng_index += 1
                s.actor.hp = max(0, s.actor.hp - DAMAGE[value])
                if s.actor.hp == 0:
                    s.actor.alive = False
                    return f"HIT_G_{DAMAGE[value]}_DEAD"
                return f"HIT_G_{DAMAGE[value]}"
        return "SHOT_MISSED"

    def _player_action(self, action: str) -> str:
        s = self.state
        if action == "T":
            s.facing = self._direction_after_turn(s.facing)
            return f"TURN_{s.facing}"
        if action == "F":
            dx, dy = VECTORS[s.facing]
            nx, ny = s.x + dx, s.y + dy
            occupied = s.actor.alive and (s.actor.x, s.actor.y) == (nx, ny)
            if not self._is_floor(nx, ny) or occupied:
                return "MOVE_BLOCKED"
            s.x, s.y = nx, ny
            return f"MOVE_{nx}_{ny}"
        if action == "A":
            return self._attack()
        return "REJECTED_INVALID"

    def _actor_phase(self, player_before: Tuple[int, int]) -> str:
        s = self.state
        if not s.actor.alive:
            return "G_DEAD_NO_ACTION"
        if s.actor.cooldown > 0:
            s.actor.cooldown -= 1
        if self._actor_was_adjacent_at_start(player_before) and s.actor.cooldown == 0:
            s.hp = max(0, s.hp - 5)
            s.actor.cooldown = 2
            return "G_ATTACK_5"
        return "G_IDLE"

    def step(self, action: str) -> Dict[str, object]:
        """Aplicar um tick e retornar uma linha de log serializável."""
        action = action.upper()
        s = self.state
        before = (s.x, s.y)
        if s.phase != "PLAY":
            player_event = "REJECTED_TERMINAL"
            actor_event = "NO_ACTION_TERMINAL"
        else:
            player_event = self._player_action(action)
            actor_event = self._actor_phase(before)
            if s.hp <= 0:
                s.phase = "LOST"
            elif not s.actor.alive:
                s.phase = "WON"
        tick_before = s.tick
        s.tick += 1
        return {
            "tick": tick_before,
            "action": action,
            "player_event": player_event,
            "actor_event": actor_event,
            "x": s.x,
            "y": s.y,
            "facing": s.facing,
            "hp": s.hp,
            "ammo": s.ammo,
            "g_hp": s.actor.hp,
            "g_alive": s.actor.alive,
            "g_cooldown": s.actor.cooldown,
            "rng_index": s.rng_index,
            "phase": s.phase,
            "checksum": self.checksum(),
        }

    def run(self, actions: List[str]) -> List[Dict[str, object]]:
        return [self.step(action) for action in actions]


def golden_trace() -> List[Dict[str, object]]:
    return PaperDoom().run(["F", "F", "A", "A", "A"])
