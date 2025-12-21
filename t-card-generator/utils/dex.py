from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm.session import Session

from forms import NewDexForm, DexExperiencesForm
from models import PokemonOwned, Dex, DexExperience
from utils.levels import level_up_pokemon


def create_new_dex(form: NewDexForm, character_id: int, session: Session, start_date: datetime = None):
    """
    Ajoute de nouveaux cookies
    :param form: le formulaire d'ajout de cookies
    :param character_id: l'id du personnage
    :param session: la session BDD
    :param start_date: datetime de début du dex
    """
    if not start_date:
        start_date = datetime.now()

    end_date = start_date + relativedelta(months=11)

    dex = Dex(
        character_id=character_id,
        name=form.dex_name.data,
        start_date=f'{start_date.strftime("%B")} {start_date.year}',
        end_date=f'{end_date.strftime("%B")} {end_date.year}'
    )

    session.add(dex)
    session.flush()
    session.refresh(dex)

    new_experiences = []
    for experience_number in range(12):
        month = start_date + relativedelta(months=experience_number)
        new_experiences.append(DexExperience(
            dex_id=dex.id,
            month = f'{month.strftime("%B")} {month.year}'
        ))

    session.add_all(new_experiences)
    session.commit()


def give_dex_experience(dex_exp: DexExperiencesForm, session: Session):
    """
    Donne l'expérience d'un dex
    :param dex_exp: le formulaire d'ajout d'expérience
    :param session: la session BDD
    """
    pokemon_name = set(exp.pokemon_name.data for exp in dex_exp.experiences)
    pokemon_name_display = set(exp.pokemon_name_display.data for exp in dex_exp.experiences)
    pokemon_names = pokemon_name_display.union(pokemon_name)
    dex_exp_id = set(exp.experience_id.data for exp in dex_exp.experiences)

    all_pokemon = session.query(PokemonOwned).filter(PokemonOwned.name.in_(pokemon_names)).all()
    all_pokemon = {pokemon.name: pokemon for pokemon in all_pokemon}

    experiences = session.query(DexExperience).filter(DexExperience.id.in_(dex_exp_id)).all()
    experiences = {experience.id: experience for experience in experiences}

    for dex_xp in dex_exp.experiences:
        pokemon_name = dex_xp.pokemon_name.data
        pokemon_name_display = dex_xp.pokemon_name_display.data
        experience = experiences[int(dex_xp.experience_id.data)]

        # Nom vaut 0 = un select mais pas de Pokémon choisi = on passe
        if pokemon_name == '0':
            continue

        # Pas de nom = pas de select = ancien mois
        if not pokemon_name:
            # Pas de nom + pas d'experience à donner = oubli pour ce mois-ci
            if not pokemon_name_display and not dex_xp.give.data:
                experience.pokemon_name = 'Rien'
                experience.base_lvl = None
                experience.end_lvl = None
                experience.give = True
                session.flush()

            # Experience à donner + nom = on donne les niveaux
            if pokemon_name_display and dex_xp.give.data:
                pokemon = all_pokemon[pokemon_name_display]
                experience.pokemon_name = pokemon.name
                experience.pokemon_species = pokemon.species.species
                experience.base_lvl = pokemon.level
                level_up_pokemon(pokemon, 2, 0, session)
                experience.end_lvl = pokemon.level
                experience.give = True
                session.flush()

        # Nom = select = on enregistre les données, mais on ne donne pas les niveaux
        else:
            experience = experiences[int(dex_xp.experience_id.data)]
            pokemon = all_pokemon[pokemon_name]

            experience.pokemon_name = pokemon.name
            experience.pokemon_species = pokemon.species.species
            experience.base_lvl = pokemon.level
            experience.end_lvl = pokemon.level + 2
            experience.give = False

            session.flush()

    session.commit()
