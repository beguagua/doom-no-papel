import unittest

from src.paperdoom.engine import PaperDoom
from src.paperdoom.renderer import render


class PaperDoomTests(unittest.TestCase):
    def test_initial_checksum(self):
        game = PaperDoom()
        self.assertEqual(game.checksum(), 19)

    def test_golden_trace(self):
        game = PaperDoom()
        rows = game.run(["F", "F", "A", "A", "A"])
        self.assertEqual([row["checksum"] for row in rows], [23, 27, 80, 91, 83])
        self.assertEqual(game.state.phase, "WON")
        self.assertFalse(game.state.actor.alive)
        self.assertEqual(game.state.actor.hp, 0)
        self.assertEqual(game.state.hp, 95)
        self.assertEqual(game.state.ammo, 0)
        self.assertEqual(game.state.rng_index, 3)

    def test_wall_blocks_forward_move(self):
        game = PaperDoom()
        game.state.facing = "N"
        game.state.y = 1
        row = game.step("F")
        self.assertEqual(row["player_event"], "MOVE_BLOCKED")
        self.assertEqual((game.state.x, game.state.y), (1, 1))

    def test_turn_is_clockwise_without_motion(self):
        game = PaperDoom()
        row = game.step("T")
        self.assertEqual(row["player_event"], "TURN_S")
        self.assertEqual((game.state.x, game.state.y), (1, 3))

    def test_shot_miss_consumes_ammo_but_not_tape(self):
        game = PaperDoom()
        game.state.facing = "N"
        row = game.step("A")
        self.assertEqual(row["player_event"], "SHOT_BLOCKED")
        self.assertEqual(game.state.ammo, 2)
        self.assertEqual(game.state.rng_index, 0)

    def test_dead_actor_does_not_attack_same_tick(self):
        game = PaperDoom()
        game.state.x = 3
        game.state.actor.hp = 5
        row = game.step("A")
        self.assertEqual(row["player_event"], "HIT_G_10_DEAD")
        self.assertEqual(row["actor_event"], "G_DEAD_NO_ACTION")
        self.assertEqual(game.state.hp, 100)
        self.assertEqual(game.state.phase, "WON")

    def test_terminal_input_is_rejected(self):
        game = PaperDoom()
        game.run(["F", "F", "A", "A", "A"])
        row = game.step("F")
        self.assertEqual(row["player_event"], "REJECTED_TERMINAL")
        self.assertEqual(row["phase"], "WON")

    def test_renderer_is_derived_from_state(self):
        game = PaperDoom()
        game.run(["F", "F"])
        frame = render(game)
        self.assertIn("r=0:G", frame)
        self.assertIn("HP 100", frame)


if __name__ == "__main__":
    unittest.main()
