from enum import Enum
from typing import List


class CustomEnum(Enum):
    """
    Classe de custom enum
    """
    @classmethod
    def to_tuple(cls) -> List[tuple[str, str]]:
        """
        Converti l'enum en liste de tuple avec la 2e valeur en clé et valeur
        :return: un tuple de l'enum
        """
        return [(member.value[1], member.value[1]) for _, member in cls.__members__.items()]

    @classmethod
    def to_tuple_str(cls) -> List[tuple[str, str]]:
        """
        Converti l'enum en liste de tuple avec la 1re valeur (string) en clé et la 2e en valeur
        :return: un tuple de l'enum
        """
        return [(member.value[0], member.value[1]) for _, member in cls.__members__.items()]

    @classmethod
    def to_tuple_int(cls) -> List[tuple[int, str]]:
        """
        Converti l'enum en liste de tuple avec la 1re valeur (integer) en clé et la 2e en valeur
        :return: un tuple de l'enum
        """
        return [(member.value[0], member.value[1]) for _, member in cls.__members__.items()]

    @classmethod
    def to_tuple_int_with_empty(cls):
        """
        Converti l'enum en liste de tuple avec 0 et valeur vide puis la 1re valeur (integer) en clé et la 2e en valeur
        :return: un tuple de l'enum
        """
        return [(0, '')] + cls.to_tuple_int()

    @classmethod
    def get_from_value(cls, value: any) -> Enum | None:
        """
        Récupère le membre de l'enum d'après une des valeurs
        :return: l'enum ou None si non trouvé
        """
        for name, member in cls.__members__.items():
            if value in member.value:
                return member
        return None

    def get_id(self) -> int:
        """
        Récupère l'id du membre de l'enum, sa valeur si qu'une valeur
        :return: l'id du membre de l'enum
        """
        return self.value[0] if isinstance(self.value, tuple) else self.value


class Status(CustomEnum):
    """
    Enum des status possibles
    """
    DRESSEUR = 1, 'Dresseur'
    COORDINATEUR = 2, 'Coordinateur'
    RANGER = 3, 'Ranger'
    SBIRE = 4, 'Sbire'


class Region(CustomEnum):
    """
    Enum des régions
    """
    KANTO = 1, 'Kantô'
    JOHTO = 2, 'Johto'
    HOENN = 3, 'Hoenn'
    SINNOH = 4, 'Sinnoh'
    UNYS = 5, 'Unys'
    KALOS = 6, 'Kalos'
    ALOLA = 7, "Alola"
    GALAR = 8, "Galar"
    PALDEA = 9, "Paldea"


class Sex(CustomEnum):
    """
    Enum des sexes
    """
    FEMININ = 1, "Féminin"
    MASCULIN = 2, "Masculin"


class Object(CustomEnum):
    """
    Enum des types d'objets
    """
    BALLS = 'balls'
    HEAL = 'heal'
    EVOL = 'evol'
    CT = 'ct'
    BERRY = 'berry'
    OTHER = 'other'
    RARE = 'rare'


class JourneyStatus(CustomEnum):
    """
    Enum des status des sujets RP
    """
    UPCOMING = 1, 'À venir', 'fa-play-circle'
    ONGOING = 2, 'En cours', 'fa-circle-minus'
    ABANDONNED = 3, 'Abandonné', 'fa-circle-xmark'
    FINISHED = 4, 'Fini', 'fa-circle-check'


class HistoryMouvment(CustomEnum):
    """
    Enum des mouvements possibles dans l'historique
    """
    IN = 'in'
    OUT = 'out'
    EXCHANGE = 'exchange'


class Assortment(CustomEnum):
    """
    Enum des assortiments
    """
    HEALING = [(2, 12), (2, 13), (2, 14), (2, 15), (2, 25)], 'Soin'
    ANTI_STATUS = [(5, 22), (5, 23), (5, 20), (5, 21), (5, 24)], 'Anti-status'
    SURVIVAL = [(2, 15), (2, 26), (2, 27), (2, 25)], 'Survie'
    FRESHNESS = [(2, 18), (2, 16), (2, 17)], 'Fraîcheur'
    BERRIES = [(3, 56), (3, 57), (3, 58), (3, 59), (3, 60), (3, 62)], 'Baies'
    CAPTURE = [(3, 1), (3, 2), (3, 3)], 'Capture'
    SPECIAL_CAPTURE = [(1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10)], 'Capture spécial'
    EVOLVE = [(1, 29), (1, 30), (1, 31), (1, 32), (1, 33), (1, 34), (1, 35)], 'Evolution'
    VITAMINS = [(1, 78), (1, 80), (1, 81), (1, 82), (1, 83), (1, 79)], 'Vitamines'
    ETHOLOGICAL = [(1, 72), (1, 73), (1, 74), (3, 75)], 'Ethologique'


class GoalCategory(CustomEnum):
    """
    Enum des catégories d'objectifs
    """
    GLOBAL = 1
    POKEMON = 2


class TypePokemon(CustomEnum):
    """
    Types des Pokémon
    """
    STEEL = 1, 'Acier'
    FIGHTING = 2, 'Combat'
    DRAGON = 3, 'Dragon'
    WATER = 4, 'Eau'
    ELECTRIC = 5, 'Electrik'
    FAIRY = 6, 'Fée'
    FIRE = 7, 'Feu'
    ICE = 8, 'Glace'
    BUG = 9, 'Insecte'
    NORMAL = 10, 'Normal'
    GRASS = 11, 'Plante'
    POISON = 12, 'Poison'
    PSYCHIC = 13, 'Psy'
    ROCK = 14, 'Roche'
    GROUND = 15, 'Sol'
    GHOST = 16, 'Spectre'
    DARK = 17, 'Ténèbres'
    FLYING = 18, 'Vol'


class EvolutionWay(CustomEnum):
    """
    Moyens d'évolution
    """
    LEVEL = 1, 'Niveau'
    MOON_STONE = 2, 'Pierre Lune'
    THUNDER_STONE = 3, 'Pierre Foudre'
    FIRE_STONE = 4, 'Pierre Feu'
    SUN_STONE = 5, 'Pierre Soleil'
    WATER_STONE = 6, 'Pierre Eau'
    GRASS_STONE = 7, 'Pierre Plante'
    ICE_STONE = 8, 'Pierre Glace'
    EXCHANGE = 9, 'Echange'
    SERUM = 10, 'Sérum M'


class SpriteBackground(CustomEnum):
    """
    Listes des backgrounds possibles pour les sprites
    """
    BEACH_AFTERNOON = 'beach_afternoon', 'Plage (après-midi)', 1
    BEACH_MORNING = 'beach_morning', 'Plage (matin)', 1
    BEACH_NIGHT = 'beach_night', 'Plage (nuit)', 1
    WOOD_AFTERNOON = 'wood_afternoon', 'Bois (après-midi)', 2
    WOOD_MORNING = 'wood_morning', 'Bois (matin)', 2
    WOOD_NIGHT = 'wood_night', 'Bois (nuit)', 2
    LABO = 'labo', 'Labo', 1
    BRIGDE_AFTERNOON = 'brigde_afternoon', 'Pont (après-midi)', 1
    BRIGDE_DAWN = 'brigde_dusk', 'Pont (crépuscule)', 1
    BRIGDE_MOON_LIGHT = 'brigde_moon_light', 'Pont (clair de lune)', 1
    BRIGDE_MORNING = 'brigde_morning', 'Pont (matin)', 1
    BRIGDE_NIGHT = 'brigde_night', 'Pont (nuit)', 1
    PLAINS_AFTERNOON = 'plains_afternoon', 'Plaines (après-midi)', 1
    PLAINS_MORNING = 'plains_morning', 'Plaines (matin)', 1
    PLAINS_NIGHT = 'plains_night', 'Plaines (nuit)', 1
    SEA_NIGHT = 'sea_night', 'Mer (nuit)', 2
    SEA_AFTERNOON = 'sea_afternoon', 'Mer (après-midi)', 2
    SEA_MORNING = 'sea_morning', 'Mer (matin)', 2
    MOUNTAIN_FIELD = 'mountain_field', 'Montagnes', 1
    MOUNTAIN_MORNING = 'mountain_morning', 'Montagnes (matin)', 1
    MOUNTAIN_AFTERNOON = 'mountain_afternoon', 'Montagnes (après-midi)', 1
    MOUNTAIN_NIGHT = 'mountain_night', 'Montagnes (nuit)', 1
    BATTLE_MORNING = 'battle_morning', 'Battlefield (matin)', 1
    BATTLE_AFTERNOON = 'battle_afternoon', 'Battlefield (après-midi)', 1
    BATTLE_NIGHT = 'battle_night', 'Battlefield (nuit)', 1
    ROCK_BRIDGE_MORNING = 'rock_bridge_morning', 'Pont de pierre (matin)', 1
    ROCK_BRIDGE_AFTERNOON = 'rock_bridge_afternoon', 'Pont de pierre (après-midi)', 1
    ROCK_BRIDGE_NIGHT = 'rock_bridge_night', 'Pont de pierre (nuit)', 1
    WALL_MORNING = 'wall_morning', 'Mur (matin)', 1
    WALL_AFTERNOON = 'wall_afternoon', 'Mur (après-midi)', 1
    WALL_NIGHT = 'wall_night', 'Mur (nuit)', 1

    @classmethod
    def get_background(cls, character_id: int) -> List[tuple[str, str]]:
        return [
            (member.value[0], member.value[1])
            for _, member in cls.__members__.items()
            if member.value[2] == character_id
        ]
