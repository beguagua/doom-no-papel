"""Renderer frontal reduzido do PaperDOOM-1."""
from .engine import PaperDoom, VECTORS

# Colunas r=-2..+2 quando olhando E.
BASE = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1))


def rotate(vector, facing):
    x, y = vector
    if facing == "E":
        return x, y
    if facing == "S":
        return -y, x
    if facing == "W":
        return -x, -y
    return y, -x  # N


def render(game: PaperDoom) -> str:
    s = game.state
    symbols = []
    for base in BASE:
        vx, vy = rotate(base, s.facing)
        found = "."
        for distance in range(1, 6):
            x = s.x + vx * distance
            y = s.y + vy * distance
            if not game._is_floor(x, y):
                found = {1: "████", 2: "▓▓▓", 3: "▒▒"}.get(distance, "░")
                break
            if s.actor.alive and (x, y) == (s.actor.x, s.actor.y):
                found = "G"
                break
        symbols.append(found)
    return (
        f"t={s.tick} pos=({s.x},{s.y}) facing={s.facing} phase={s.phase}\n"
        f"alvo  r=-2:{symbols[0]} r=-1:{symbols[1]} r=0:{symbols[2]} "
        f"r=+1:{symbols[3]} r=+2:{symbols[4]}\n"
        f"HUD   HP {s.hp} | PISTOLA | MUNIÇÃO {s.ammo} | G={s.actor.hp}"
    )
