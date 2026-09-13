"""Linha de comando para validar um traço PaperDOOM-1."""
import argparse

from .engine import PaperDoom
from .renderer import render


def main():
    parser = argparse.ArgumentParser(description="Validador do PaperDOOM-1")
    parser.add_argument("--trace", nargs="+", default=["F", "F", "A", "A", "A"])
    args = parser.parse_args()
    game = PaperDoom()
    print(f"initial checksum={game.checksum()}")
    for row in game.run(args.trace):
        print(
            "t={tick} action={action} player={player_event} actor={actor_event} "
            "state=({x},{y},{facing}) hp={hp} ammo={ammo} g={g_hp}/{g_alive} "
            "rng={rng_index} phase={phase} chk={checksum}".format(**row)
        )
    print(render(game))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
