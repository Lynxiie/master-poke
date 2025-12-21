from flask_sqlalchemy.session import Session
from sqlalchemy import Integer, String, ForeignKey, Boolean, asc
from sqlalchemy.orm import relationship, Mapped

from database import db
from utils.lists import sort_by_previous_value


class MpCharacter(db.Model):
    """Modèle d'un personnage"""
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(String, nullable=False)
    lastname = db.Column(String, nullable=False)
    original_char_name = db.Column(String, nullable=False)
    original_game = db.Column(String, nullable=False)
    age = db.Column(Integer, nullable=False)
    status = db.Column(String, nullable=False)
    sex = db.Column(String, nullable=False)
    region = db.Column(String, nullable=False)
    starter = db.Column(String, nullable=False)
    id_number = db.Column(String, nullable=False)
    mental = relationship('Mental')
    physical = relationship('Physical')

    @staticmethod
    def get_one_tcard_ids() -> set[int]:
        """
        Retourne les id des personnages avec une tcard d'un seul fichier
        :return: un set d'id
        """
        return {2}

    def get_full_name(self) -> str:
        return f'{self.firstname} {self.lastname}'


class Mental(db.Model):
    """Modèle des caractéristiques mentals"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    description = db.Column(String, nullable=False)


class Physical(db.Model):
    """Modèle des caractéristiques physiques"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    description = db.Column(String, nullable=False)


class Object(db.Model):
    """Modèle d'un objet"""
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    category = db.Column(String, nullable=False)

    @staticmethod
    def get_objects_id_with_justificatif() -> set[int]:
        """
        Récupère les id des objets avec justificatifs
        :return: set d'id
        """
        return {103, 109}

    @staticmethod
    def get_objects_id_no_exchangeable() -> set[int]:
        """
        Récupère les id des objets non échangeables
        :return: set d'id
        """
        return {76, 105}


class Inventory(db.Model):
    """Modèle de l'inventaire"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    object_id = db.Column(Integer, ForeignKey(Object.id))
    object = relationship(Object, backref="object")
    quantity = db.Column(Integer, nullable=False)


class Money(db.Model):
    """Modèle de l'argent"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    amount = db.Column(Integer, nullable=False)
    statement_date = db.Column(String, nullable=False)


class Ct(db.Model):
    """Modèle d'une CT"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    object_id = db.Column(Integer, ForeignKey(Object.id))
    object = relationship(Object, backref="object_ct")
    name = db.Column(String, nullable=False)
    quantity = db.Column(Integer, nullable=False)
    reserved = db.Column(String)


class CsHistory(db.Model):
    """Modèle d'un historique de CS"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    object_id = db.Column(Integer, ForeignKey(Object.id))
    object = relationship(Object, backref="object_cs")
    last_used = db.Column(String)
    link = db.Column(String)
    frequency = db.Column(String, nullable=False)


class FluteHistory(db.Model):
    """Modèle d'un historique de flûte"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    object_id = db.Column(Integer, ForeignKey(Object.id))
    object = relationship(Object, backref="object_flute")
    last_used = db.Column(String)
    link = db.Column(String)
    frequency = db.Column(String, nullable=False)


class History(db.Model):
    """Modèle de l'historique"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    movement = db.Column(String, nullable=False)
    movement_date = db.Column(String, nullable=False)
    objects = db.Column(String)
    objects_in_exchange = db.Column(String)
    objects_out_exchange = db.Column(String)
    link = db.Column(String, nullable=False)
    link_title = db.Column(String, nullable=False)
    rank_history = db.Column(Boolean, nullable=False, default=False)


class JustificatifLink(db.Model):
    """Modèle des liens justificatifs"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    object_id = db.Column(Integer, ForeignKey(Object.id))
    object = relationship(Object, backref="justificatif_link_object")
    link = db.Column(String, nullable=False)
    link_title = db.Column(String, nullable=False)
    rank_link = db.Column(Boolean, nullable=False, default=False)


class Social(db.Model):
    """Modèle des relations"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    full_name = db.Column(String, nullable=False)
    bond = db.Column(String, nullable=False)
    description = db.Column(String, nullable=False)
    pj = db.Column(Integer, nullable=False)
    hexa_text = db.Column(String)

    pokemon: Mapped[list["SocialPokemon"]] = relationship(backref="social_pokemon")
    subjects: Mapped[list["SocialSubject"]] = relationship(backref="social_subjects")


class SocialPokemon(db.Model):
    """Modèle des Pokémon qui appartiennent aux relations"""
    id = db.Column(Integer, primary_key=True)
    social_id = db.Column(Integer, ForeignKey(Social.id))
    pokemon = db.Column(String, nullable=False)
    pokemon_name = db.Column(String, nullable=False)


class SocialSubject(db.Model):
    """Modèle des sujets en commun avec les relations"""
    id = db.Column(Integer, primary_key=True)
    social_id = db.Column(Integer, ForeignKey(Social.id))
    link = db.Column(String, nullable=False)


class JourneyChapter(db.Model):
    """Modèle des chapitres du parcours du personnage"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    name = db.Column(String, nullable=False)
    after = db.Column(Integer, nullable=False)

    journeys: Mapped[list["Journey"]] = relationship(backref="journeys")

    @classmethod
    def get_ordered_chapter(cls, character_id: int, with_journeys: bool = False) -> list['JourneyChapter']:
        """
        Récupère les chapitres ordonnés
        :param character_id: l'id du personnage
        :param with_journeys: si on veut les aventures en plus des chapitres
        :return: une liste de chapitres
        """
        chapters = cls.query.filter(JourneyChapter.character_id == character_id)

        if with_journeys:
            chapters = chapters.join(Journey, full=True)

        chapters = chapters.all()

        if chapters:
            chapters = sort_by_previous_value(chapters)
            if with_journeys:
                for chapter in chapters:
                    if chapter.journeys:
                        chapter.journeys = sort_by_previous_value(chapter.journeys)

        return chapters


class Journey(db.Model):
    """Modèle d'une aventure"""
    id = db.Column(Integer, primary_key=True)
    journey_chapter_id = db.Column(Integer, ForeignKey(JourneyChapter.id))
    name = db.Column(String, nullable=False)
    link = db.Column(String, nullable=False)
    after = db.Column(Integer, nullable=False)
    status = db.Column(String, nullable=False)
    feat = db.Column(String)

    @classmethod
    def get_ordered_journey(cls, chapter_id: int) -> list['Journey']:
        """
        Récupère les aventures ordonnées
        :param chapter_id: l'id du chapitre auquel les aventures sont rattachés
        :return: la liste des aventures
        """
        journeys = cls.query.filter(Journey.journey_chapter_id == chapter_id).all()

        if journeys:
            journeys = sort_by_previous_value(journeys)

        return journeys


class MissionsChapter(db.Model):
    """Modèle des missions du personnage"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    name = db.Column(String, nullable=False)
    after = db.Column(Integer, nullable=False)

    missions: Mapped[list["Missions"]] = relationship(backref="missions")

    @classmethod
    def get_ordered_chapter(cls, character_id: int, with_missions: bool = False) -> list['MissionsChapter']:
        """
        Récupère les missions ordonnées
        :param character_id: l'id du personnage
        :param with_missions: si on veut les aventures en plus des missions
        :return: une liste de missions
        """
        chapters = cls.query.filter(MissionsChapter.character_id == character_id)

        if with_missions:
            chapters = chapters.join(Missions, full=True)

        chapters = chapters.all()

        if chapters:
            chapters = sort_by_previous_value(chapters)
            if with_missions:
                for chapter in chapters:
                    if chapter.missions:
                        chapter.missions = sort_by_previous_value(chapter.missions)

        return chapters


class Missions(db.Model):
    """Modèle d'une mission"""
    id = db.Column(Integer, primary_key=True)
    missions_chapter_id = db.Column(Integer, ForeignKey(MissionsChapter.id))
    name = db.Column(String, nullable=False)
    link = db.Column(String, nullable=False)
    after = db.Column(Integer, nullable=False)
    status = db.Column(String, nullable=False)
    feat = db.Column(String)

    @classmethod
    def get_ordered_missions(cls, chapter_id: int) -> list['Missions']:
        """
        Récupère les aventures ordonnées
        :param chapter_id: l'id du chapitre auquel les aventures sont rattachés
        :return: la liste des aventures
        """
        missions = cls.query.filter(Missions.missions_chapter_id == chapter_id).all()

        if missions:
            missions = sort_by_previous_value(missions)

        return missions


class Goals(db.Model):
    """Modèle des objectifs"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    description = db.Column(String, nullable=False)
    category = db.Column(Integer, nullable=False)
    done = db.Column(Boolean, nullable=False, default=False)


class PokemonSpecies(db.Model):
    """Modèle d'une espèce de Pokémon"""
    id = db.Column(Integer, primary_key=True)
    species = db.Column(String, nullable=False)
    type_1_id = db.Column(Integer, nullable=False)
    type_2_id = db.Column(Integer)
    evolution_id = db.Column(Integer, nullable=True)
    evolution_way = db.Column(Integer, nullable=True)
    evolution_level = db.Column(Integer, nullable=True)
    pv = db.Column(Integer, nullable=False)
    atk = db.Column(Integer, nullable=False)
    atk_special = db.Column(Integer, nullable=False)
    defense = db.Column(Integer, nullable=False)
    defense_special = db.Column(Integer, nullable=False)
    speed = db.Column(Integer, nullable=False)


class PokemonAttacks(db.Model):
    """Modèle d'attaque"""
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    type_id = db.Column(Integer, nullable=False)
    informations = db.Column(String)
    power = db.Column(Integer)
    precision = db.Column(Integer)
    useless = db.Column(Boolean, default=False)
    burn_percentage = db.Column(Integer)
    freeze_percentage = db.Column(Integer)
    paralyse_percentage = db.Column(Integer)
    scare_percentage = db.Column(Integer)
    poison_percentage = db.Column(Integer)
    sleep_percentage = db.Column(Integer)
    boost = db.Column(String)
    critique_attack = db.Column(Boolean, default=False)


class PokemonSpeciesAttacks(db.Model):
    """Modèle de la liaison entre les espèces et les attaques"""
    id = db.Column(Integer, primary_key=True)
    species_id = db.Column(Integer, ForeignKey(PokemonSpecies.id))
    attack_id = db.Column(Integer, ForeignKey(PokemonAttacks.id))
    level = db.Column(Integer)
    ct = db.Column(Boolean, default=False)
    cs = db.Column(Boolean, default=False)
    gm = db.Column(Boolean, default=False)
    cm = db.Column(Boolean, default=False)

    attack = relationship(PokemonAttacks, backref="attack")

    def __repr__(self):
        return f'PokemonSpeciesAttacks #{self.id} - {self.attack.name} level {self.level}'


class PokemonCategory(db.Model):
    """Modèle des catégories des Pokémon"""
    id = db.Column(Integer, primary_key=True)
    character_id = db.Column(Integer, ForeignKey(MpCharacter.id))
    name = db.Column(String)
    time_used = False


class PokemonOwned(db.Model):
    """Modèle des Pokémon possédés"""
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, ForeignKey('mp_character.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    species_id = db.Column(db.Integer, ForeignKey('pokemon_species.id'), nullable=False)
    sex = db.Column(db.String(1), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=0)
    shiny = db.Column(db.Boolean, nullable=False, default=False)
    pv = db.Column(db.Integer, nullable=False, default=0)
    atk = db.Column(db.Integer, nullable=False, default=0)
    atk_special = db.Column(db.Integer, nullable=False, default=0)
    defense = db.Column(db.Integer, nullable=False, default=0)
    def_special = db.Column(db.Integer, nullable=False, default=0)
    speed = db.Column(db.Integer, nullable=False, default=0)
    exp_point = db.Column(db.Integer, nullable=False, default=0)
    exp_point_per_level = db.Column(db.Integer, nullable=False, default=1)
    hp_up = db.Column(db.Integer, nullable=False, default=0)
    zinc = db.Column(db.Integer, nullable=False, default=0)
    calcium = db.Column(db.Integer, nullable=False, default=0)
    carbos = db.Column(db.Integer, nullable=False, default=0)
    iron = db.Column(db.Integer, nullable=False, default=0)
    protein = db.Column(db.Integer, nullable=False, default=0)
    obtention_link = db.Column(db.String(255), nullable=False)
    obtention_name = db.Column(db.String(255), nullable=False)
    nature = db.Column(db.String(20), nullable=False)
    sprite_credits = db.Column(db.String(255), nullable=True)
    category_id = db.Column(db.Integer, ForeignKey('pokemon_category.id'), nullable=False)
    pension = db.Column(db.String)
    egg = db.Column(db.Boolean, nullable=False, default=False)
    background = db.Column(db.String(150), nullable=False)
    banner_credit = db.Column(db.String(150), nullable=True)

    category = relationship(PokemonCategory, backref="category")
    species = relationship(PokemonSpecies, backref="pokemon_species")
    attacks = relationship('PokemonOwnedAttacks', back_populates="pokemon", cascade="all, delete-orphan")

    def __repr__(self):
        return f'PokemonOwned #{self.id} - {self.name}'


class PokemonOwnedAttacks(db.Model):
    """Modèle de la liaison entre le Pokémon possédé et l'attaque apprise par l'espèce"""
    id = db.Column(db.Integer, primary_key=True)
    pokemon_owned_id = db.Column(db.Integer, ForeignKey('pokemon_owned.id'), nullable=False)
    species_attack_id = db.Column(db.Integer, ForeignKey('pokemon_species_attacks.id'), nullable=False)

    pokemon = relationship(PokemonOwned, back_populates="attacks")
    attack = relationship(PokemonSpeciesAttacks, backref="pokemon_attack")

    def __repr__(self):
        return f'PokemonOwnedAttacks #{self.id} - {self.pokemon} - {self.attack}'

    @staticmethod
    def get_attacks(pokemon_id: int, session: Session) -> list['PokemonOwnedAttacks']:
        """
        Récupère les attaques d'un Pokémon
        :param pokemon_id: l'id du Pokémon
        :param session: la session BDD
        :return: la liste des attaques
        """
        attacks = (
            session
            .query(PokemonOwnedAttacks)
            .join(PokemonSpeciesAttacks)
            .filter(PokemonOwnedAttacks.pokemon_owned_id == pokemon_id)
            .order_by(asc(PokemonSpeciesAttacks.level))
            .all()
        )

        return attacks


class NdmMonths(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    month = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    posts = db.relationship('NdmPosts', back_populates='month', cascade="all, delete-orphan")
    rewards = db.relationship('NdmRewards', back_populates='month', cascade="all, delete-orphan")


class NdmSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey('mp_character.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    info = db.Column(db.String(255), nullable=False)
    closed = db.Column(db.Boolean, default=False, nullable=False)

    posts = db.relationship('NdmPosts', back_populates='subject', cascade="all, delete-orphan")


class NdmPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey('mp_character.id'), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('ndm_months.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('ndm_subjects.id'), nullable=False)
    words = db.Column(db.Integer, nullable=False)

    month = db.relationship('NdmMonths', back_populates='posts')
    subject = db.relationship('NdmSubjects', back_populates='posts')
    character = db.relationship('MpCharacter', backref='ndm_posts')


class NdmRewards(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey('mp_character.id'), nullable=False)
    month_id = db.Column(db.Integer, db.ForeignKey('ndm_months.id'), nullable=False)
    level_winned = db.Column(db.Integer, nullable=False)
    level_winned_justif = db.Column(db.String(255), nullable=False)
    distribution = db.Column(db.String(255), nullable=False)

    month = db.relationship('NdmMonths', back_populates='rewards')
    character = db.relationship('MpCharacter', backref='ndm_rewards')


class CookiesMonths(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey('mp_character.id'), nullable=False)
    month = db.Column(db.String, nullable=False)
    win_cookies = db.Column(db.Integer, nullable=False)

    character = db.relationship('MpCharacter', backref='mp_character')
    cookies_used = db.relationship('CookiesUsed', back_populates='cookies_months')


class CookiesUsed(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cookies_months_id = db.Column(db.Integer, db.ForeignKey('cookies_months.id'), nullable=False)
    pokemon_name = db.Column(db.String, nullable=True)
    before_lvl = db.Column(db.Integer, nullable=True)
    after_lvl = db.Column(db.Integer, nullable=True)

    cookies_months = db.relationship('CookiesMonths', back_populates='cookies_used')


class Dex(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    character_id = db.Column(db.Integer, db.ForeignKey('mp_character.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.Integer, nullable=False)

    character = db.relationship('MpCharacter', backref='dex_character')
    experiences_gave = db.relationship('DexExperience')

class DexExperience(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dex_id = db.Column(db.Integer, db.ForeignKey('dex.id'), nullable=False)
    month = db.Column(db.String, nullable=False)
    pokemon_name = db.Column(db.String, nullable=True)
    pokemon_species = db.Column(db.String, nullable=True)
    base_lvl = db.Column(db.Integer, nullable=True)
    end_lvl = db.Column(db.Integer, nullable=True)
    give = db.Column(db.Boolean, nullable=False, default=False)
