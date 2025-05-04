import logging
from datetime import datetime

from flask_sqlalchemy.session import Session

from enums import EvolutionWay, HistoryMouvment
from forms import GivePokemonForm, ExchangePokemonForm, LeavePensionForm
from models import PokemonOwned, Inventory, Object, PokemonSpecies, History, PokemonSpeciesAttacks, \
    PokemonOwnedAttacks
from utils.strings import DATE_FORMAT


def can_evol(pokemon: PokemonOwned, character_id: int, session: Session) -> bool:
    """
    Détermine si un Pokémon peut évoluer
    :param pokemon: le Pokémon
    :param character_id: l'id du personnage
    :param session: le session BDD
    :return: True s'il peut évoluer
    """
    species = pokemon.species

    if not species.evolution_id:
        return False

    if pokemon.egg:
        return False

    evolution_way = EvolutionWay.get_from_value(species.evolution_way)

    evolution_way_name = evolution_way.value[1]

    if evolution_way == EvolutionWay.EXCHANGE:
        return True

    if evolution_way == EvolutionWay.LEVEL:
        return pokemon.level >= species.evolution_level

    object_inventory = session.query(Inventory).join(Object).filter(
        Inventory.character_id == character_id,
        Object.name == evolution_way_name
    ).first()

    if not object_inventory:
        logging.error(f'Object {evolution_way_name} not found for character {character_id}')
        return False

    return object_inventory.quantity >= 1


def evol_pokemon(pokemon: PokemonOwned, character_id: int, session: Session, link: str = None):
    """
    Fait évoluer un Pokémon
    :param pokemon: le Pokémon
    :param character_id: l'id du personnage
    :param session: la session BDD
    :param link: le lien du sujet d'évolution
    """
    if not can_evol(pokemon, character_id, session):
        return

    species = pokemon.species
    evolution_way = EvolutionWay.get_from_value(species.evolution_way)
    evolution_way_name = evolution_way.value[1]

    pokemon.species_id = species.evolution_id

    learn_auto_attacks(pokemon, session)

    if evolution_way in {EvolutionWay.EXCHANGE, EvolutionWay.LEVEL}:
        session.commit()
        return

    object_inventory = session.query(Inventory).join(Object).filter(
        Inventory.character_id == character_id,
        Object.name == evolution_way_name
    ).first()
    object_inventory.quantity -= 1

    history = History(
        character_id=character_id,
        movement=HistoryMouvment.OUT.value,
        movement_date=datetime.now().strftime(DATE_FORMAT),
        objects=f'1 {object_inventory.object.name}',
        link=link,
        link_title=f'Evolution {pokemon.name}',
    )
    session.add(history)

    session.commit()


def give_pokemon(character_id: int, form: GivePokemonForm, session: Session):
    """
    Donne un Pokémon
    :param character_id: l'id du personnage
    :param form: le formulaire de don
    :param session: la session BDD
    """
    pokemon = session.query(PokemonOwned).filter(
        PokemonOwned.character_id == character_id,
        PokemonOwned.id == form.pokemon_id.data
    ).first()

    if not pokemon:
        return

    session.delete(pokemon)

    history = History(
        character_id=character_id,
        movement=HistoryMouvment.OUT.value,
        movement_date=datetime.now().strftime(DATE_FORMAT),
        objects=f'{pokemon.species.species}',
        link=form.history_link.data,
        link_title=f'{form.history_name.data} ({form.new_owner.data})',
    )
    session.add(history)

    session.commit()


def exchange_pokemon(character_id: int, form: ExchangePokemonForm, session: Session):
    """
    Echange des Pokémon
    :param character_id: l'id du personnage
    :param form: le formulaire d'échange
    :param session: le session BDD
    """
    pokemon = session.query(PokemonOwned).filter(
        PokemonOwned.character_id == character_id,
        PokemonOwned.id.in_(form.pokemon_ids.data)
    ).all()

    if len(pokemon) != len(form.pokemon_ids.data):
        return

    for pkmn in pokemon:
        session.delete(pkmn)

    new_pokemons = []

    for pkmn in form.new_pokemon:
        new_pokemons.append(
            PokemonOwned(
                character_id=character_id,
                name=pkmn.form.name.data,
                species_id=pkmn.form.species_id.data,
                sex=pkmn.form.sex.data,
                level=pkmn.form.level.data,
                shiny=pkmn.form.shiny.data,
                hp_up=pkmn.form.hp_up.data,
                zinc=pkmn.form.zinc.data,
                calcium=pkmn.form.calcium.data,
                carbos=pkmn.form.carbos.data,
                iron=pkmn.form.iron.data,
                protein=pkmn.form.protein.data,
                nature=pkmn.form.nature.data,
                sprite_credits=pkmn.form.sprite_credits.data if pkmn.form.sprite_credits.data else None,
                category_id=pkmn.form.category_id.data,
                egg=pkmn.form.egg.data,
                obtention_link=form.history_link.data,
                obtention_name=form.history_name.data,
                background=pkmn.form.background.data,
                banner_credit=pkmn.form.banner_credit.data,
            )
        )

    session.add_all(new_pokemons)

    new_species = session.query(PokemonSpecies).filter(
        PokemonSpecies.id.in_([new_pkmn.species_id for new_pkmn in new_pokemons]),
    ).all()

    history = History(
        character_id=character_id,
        movement=HistoryMouvment.EXCHANGE.value,
        movement_date=datetime.now().strftime(DATE_FORMAT),
        objects_out_exchange=f'{' + '.join([pkmn.species.species for pkmn in pokemon])}',
        objects_in_exchange=f'{' + '.join([species.species for species in new_species])}',
        link=form.history_link.data,
        link_title=f'{form.history_name.data} ({form.new_owner.data})',
    )
    session.add(history)

    session.commit()

    for new_pokemon in new_pokemons:
        session.refresh(new_pokemon)
        learn_auto_attacks(new_pokemon, session)


def __get_non_evol_attacks(pokemon: PokemonOwned, only_level: bool, session: Session) -> list[PokemonSpeciesAttacks]:
    """
    Récupère les attaques non apprises par l'évolution
    :param pokemon: le Pokémon
    :param only_level: si on veut juste les attaques perdues par l'apprentissage par niveau
    :param session: la session BDD
    :return: la liste des attaques non apprises par l'évolution
    """
    species = pokemon.species

    if not species.evolution_id:
        return []

    actual_attacks = (
        session.query(PokemonSpeciesAttacks).filter(PokemonSpeciesAttacks.species_id == pokemon.species_id)
    )
    if only_level:
        actual_attacks = actual_attacks.filter(PokemonSpeciesAttacks.level > pokemon.level)
    else:
        actual_attacks = actual_attacks.filter(
            (PokemonSpeciesAttacks.level > pokemon.level)
            | PokemonSpeciesAttacks.cm
            | PokemonSpeciesAttacks.ct
            | PokemonSpeciesAttacks.cs
            | PokemonSpeciesAttacks.gm
        )

    actual_attacks = actual_attacks.all()

    evolution_attacks = (
        session
        .query(PokemonSpeciesAttacks)
        .filter(PokemonSpeciesAttacks.species_id == species.evolution_id)
    )

    if only_level:
        evolution_attacks = evolution_attacks.filter(PokemonSpeciesAttacks.level != None)

    evolution_attacks = evolution_attacks.all()

    actual_attack_ids = set(attack.attack_id for attack in actual_attacks)
    evol_attack_ids = set(attack.attack_id for attack in evolution_attacks)

    disappear_ids = actual_attack_ids - evol_attack_ids

    return [attack for attack in actual_attacks if attack.attack_id in disappear_ids]


def get_non_evol_attacks(pokemon: PokemonOwned, session: Session) -> list[PokemonSpeciesAttacks]:
    """
    Récupère les attaques non apprises par l'évolution
    :param pokemon: le Pokémon
    :param session: la session BDD
    :return: la liste des attaques non apprises par l'évolution
    """
    return __get_non_evol_attacks(pokemon, False, session)


def get_non_evol_attack_by_level(pokemon: PokemonOwned, session: Session) -> list[PokemonSpeciesAttacks]:
    """
    Récupère les attaques non apprises par l'évolution
    :param pokemon: le Pokémon
    :param session: la session BDD
    :return: la liste des attaques non apprises par l'évolution
    """
    return __get_non_evol_attacks(pokemon, True, session)


def learn_auto_attacks(pokemon: PokemonOwned, session: Session):
    """
    Apprend les attaques par niveau
    :param pokemon: Le Pokémon
    :param session: la session BDD
    """
    # Récupération des attaques déjà apprises
    learned_attacks = PokemonOwnedAttacks.get_attacks(pokemon.id, session)

    # Récupération des attaques qu'il peut apprendre
    new_attacks = (
        session
        .query(PokemonSpeciesAttacks)
        .filter(PokemonSpeciesAttacks.species_id == pokemon.species_id)
        .filter(PokemonSpeciesAttacks.level <= pokemon.level)
        .all()
    )

    new_attacks_to_save = []

    for new_attack in new_attacks:

        attack = next(
            (learned for learned in learned_attacks if learned.attack.attack.id == new_attack.attack.id),
            None
        )

        if not attack:
            new_attacks_to_save.append(PokemonOwnedAttacks(
                pokemon_owned_id=pokemon.id,
                species_attack_id=new_attack.id,
            ))

    session.add_all(new_attacks_to_save)
    session.commit()


def leave_pension(pokemon: PokemonOwned, form: LeavePensionForm, session: Session):
    """
    Retire un Pokémon de pension
    :param pokemon: le Pokémon
    :param form: le formulaire de départ de pension
    :param session: la session BDD
    """
    from utils.levels import get_xp_per_level

    pokemon.pension = None
    pokemon.level = form.new_level.data
    pokemon.exp_point = form.new_xp.data
    pokemon.exp_point_per_level = get_xp_per_level(form.new_level.data)

    session.add(pokemon)
    session.commit()

    learn_auto_attacks(pokemon, session)
