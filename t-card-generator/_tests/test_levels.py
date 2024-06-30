import unittest

from models import PokemonOwned
from utils.levels import get_xp_per_level, level_up_pokemon


class TestLevels(unittest.TestCase):

    def test_get_xp_per_level(self):
        self.assertEqual(1, get_xp_per_level(5))
        self.assertEqual(1, get_xp_per_level(10))
        self.assertEqual(1, get_xp_per_level(19))
        self.assertEqual(2, get_xp_per_level(20))
        self.assertEqual(2, get_xp_per_level(25))
        self.assertEqual(2, get_xp_per_level(29))
        self.assertEqual(3, get_xp_per_level(30))
        self.assertEqual(3, get_xp_per_level(31))
        self.assertEqual(3, get_xp_per_level(39))
        self.assertEqual(4, get_xp_per_level(40))
        self.assertEqual(4, get_xp_per_level(50))
        self.assertEqual(4, get_xp_per_level(59))
        self.assertEqual(5, get_xp_per_level(60))
        self.assertEqual(5, get_xp_per_level(64))
        self.assertEqual(5, get_xp_per_level(79))
        self.assertEqual(6, get_xp_per_level(80))
        self.assertEqual(6, get_xp_per_level(85))
        self.assertEqual(6, get_xp_per_level(89))
        self.assertEqual(7, get_xp_per_level(90))
        self.assertEqual(7, get_xp_per_level(95))
        self.assertEqual(7, get_xp_per_level(99))
        self.assertEqual(0, get_xp_per_level(100))
        self.assertEqual(0, get_xp_per_level(4))
        self.assertEqual(0, get_xp_per_level(101))

    def test_level_up_pokemon(self):
        pokemon = PokemonOwned(
            level=5,
            exp_point=0,
            exp_point_per_level=1
        )
        level_up_pokemon(pokemon, 1, 0)
        self.assertEqual(6, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 10, 0)
        self.assertEqual(16, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 4, 0)
        self.assertEqual(20, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        pokemon.exp_point = 1

        level_up_pokemon(pokemon, 14, 0)
        self.assertEqual(34, pokemon.level)
        self.assertEqual(1, pokemon.exp_point)
        self.assertEqual(3, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 66, 0)
        self.assertEqual(100, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(0, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 1, 0)
        self.assertEqual(100, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(0, pokemon.exp_point_per_level)

    def test_one_point_up_pokemon(self):
        pokemon = PokemonOwned(
            level=5,
            exp_point=0,
            exp_point_per_level=1
        )
        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(6, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(7, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(8, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(9, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(10, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        pokemon.level = 19

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(20, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(20, pokemon.level)
        self.assertEqual(1, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(21, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        pokemon.level = 29

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(29, pokemon.level)
        self.assertEqual(1, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 1)
        self.assertEqual(30, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(3, pokemon.exp_point_per_level)

    def test_more_points_up_pokemon(self):
        pokemon = PokemonOwned(
            level=5,
            exp_point=0,
            exp_point_per_level=1
        )
        level_up_pokemon(pokemon, 0, 2)
        self.assertEqual(7, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 2)
        self.assertEqual(9, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 3)
        self.assertEqual(12, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 4)
        self.assertEqual(16, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 5)
        self.assertEqual(20, pokemon.level)
        self.assertEqual(1, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 3)
        self.assertEqual(22, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(2, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 16)
        self.assertEqual(30, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(3, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 2)
        self.assertEqual(30, pokemon.level)
        self.assertEqual(2, pokemon.exp_point)
        self.assertEqual(3, pokemon.exp_point_per_level)

        level_up_pokemon(pokemon, 0, 2)
        self.assertEqual(31, pokemon.level)
        self.assertEqual(1, pokemon.exp_point)
        self.assertEqual(3, pokemon.exp_point_per_level)

    def test_level_up_pokemon_fail(self):
        pokemon = PokemonOwned(
            level=5,
            exp_point=0,
            exp_point_per_level=1
        )
        level_up_pokemon(pokemon, 1, 1)
        self.assertEqual(5, pokemon.level)
        self.assertEqual(0, pokemon.exp_point)
        self.assertEqual(1, pokemon.exp_point_per_level)


if __name__ == '__main__':
    unittest.main()
