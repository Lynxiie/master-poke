import logging

from flask_sqlalchemy.session import Session

from models import PokemonOwned
from utils.pokemon import learn_auto_attacks

XP_PER_LEVEL = {
    "5-19": 1,
    "20-29": 2,
    "30-39": 3,
    "40-59": 4,
    "60-79": 5,
    "80-89": 6,
    "90-99": 7
}


def get_xp_per_level(level: int) -> int:
    """
    Calcule le nom d'expérience par niveau
    :param level: le niveau
    :return: le nombre d'expérience pour monter au niveau suivant
    """
    for levels, points in XP_PER_LEVEL.items():
        inferior, superior = map(int, levels.split('-'))
        if inferior <= level <= superior:
            return points

    return 0


def level_up_pokemon(pokemon: PokemonOwned, level: int, point: int, session: Session = None):
    """
    Level up un Pokémon
    :param pokemon: le Pokémon
    :param level: Le nombre de niveau gagner - Incompatible avec point
    :param point: Le nombre de point d'expérience gagné - Incompatible avec level
    :param session: le session de la base de donnée
    """
    if level and point:
        logging.error("Cannot add level and point to Pokemon")
        return

    if level:
        level_up_pokemon_level(pokemon, level)
    else:
        level_up_pokemon_point(pokemon, point)

    pokemon.exp_point = pokemon.exp_point if pokemon.level < 100 else 0

    if session:
        learn_auto_attacks(pokemon, session)


def level_up_pokemon_level(pokemon: PokemonOwned, level: int):
    """
    Fait gagner des niveaux à un Pokémon
    :param pokemon: le Pokémon
    :param level: le nombre de niveau gagné
    """
    pokemon.level += level
    pokemon.exp_point_per_level = get_xp_per_level(pokemon.level)

    if pokemon.level > 100:
        pokemon.level = 100


def level_up_pokemon_point(pokemon: PokemonOwned, point: int):
    """
    Fait gagner des points d'expérience à un Pokémon
    :param pokemon: le Pokémon
    :param point: le nombre de point d'expérience gagné
    """
    if point + pokemon.exp_point < pokemon.exp_point_per_level:
        pokemon.exp_point = point + pokemon.exp_point
        return

    if point + pokemon.exp_point == pokemon.exp_point_per_level:
        pokemon.exp_point = 0
        level_up_pokemon_level(pokemon, 1)
        return

    used_point = pokemon.exp_point_per_level - pokemon.exp_point
    pokemon.exp_point = 0
    level_up_pokemon_level(pokemon, 1)
    level_up_pokemon_point(pokemon, point - used_point)
