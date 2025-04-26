import os
import re
from collections import defaultdict
from datetime import datetime
from math import floor

import chevron
from sqlalchemy import false, asc, func
from sqlalchemy.orm import joinedload
from wtforms.fields.core import Field
from wtforms.fields.list import FieldList

from models import Mental, Physical, Inventory, Object, Money, Ct, CsHistory, FluteHistory, History, \
    Social, SocialPokemon, SocialSubject, JourneyChapter, JustificatifLink, Goals, PokemonOwned, PokemonCategory, \
    PokemonOwnedAttacks, PokemonSpeciesAttacks, PokemonAttacks, NdmPosts, NdmMonths, NdmSubjects, NdmRewards
from enums import Object as ObjectEnum, JourneyStatus, GoalCategory, TypePokemon

from models import MpCharacter
from utils.strings import convert_int_to_prefixed_string, slugify, DATE_FORMAT


def generate_tcard_part(character_id: int, tcard_part: str):
    """
    Génère les parties des tcard
    :param character_id: l'id du personnage
    :param tcard_part: la partie à générer
    """
    character = MpCharacter.query.filter(MpCharacter.id == character_id).first()

    if not character:
        return

    character_name = character.firstname.lower()

    if character.id in MpCharacter.get_one_tcard_ids() and tcard_part != 'ndm':
        tcard_part = 't-card'

    with open(f'templates/tcard/{character_name}/{tcard_part}.html', 'r', encoding='utf-8') as f:
        file = f.read()

    data = vars(character)
    data['pokemon'] = defaultdict(list)

    if tcard_part in {'informations', 't-card'}:
        get_character_data(character_id, data)

    if tcard_part in {'inventaire', 't-card'}:
        get_inventory_data(character, character_id, data)

    if tcard_part in {'connaissances', 't-card'}:
        get_social_data(character_id, data)

    if tcard_part in {'ressources', 't-card'}:
        get_ressources_data(character, data)

    if tcard_part in {'parcours', 't-card'}:
        get_journeys_data(character_id, data)

    if tcard_part in {'objectifs', 't-card'}:
        get_goals_data(character_id, data)

    if tcard_part in {'pokemon', 't-card'}:
        get_pokemon_data(character_id, data, False)

    if tcard_part in {'stockage', 't-card'}:
        get_pokemon_data(character_id, data, True)

    if tcard_part in {'ndm'}:
        get_ndm_data(character_id, data)

    text = chevron.render(file, data)
    filename = os.path.join('..', character_name, tcard_part + '.html')

    with open(filename, 'w', encoding="utf-8") as file:
        file.write(text)


def get_pokemon_data(character_id: int, data: dict[str, any], is_stockage: bool):
    """
    Récupère les informations des Pokémon
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    :param is_stockage: si on veut les Pokémon du stockage
    """
    def _get_icon_filename(search_term: str, category: str) -> str | None:
        """
        Récupère le nom de l'image d'un Pokémon
        :param search_term: le nom à rechercher (espèce ou nom du Pokémon)
        :param category: la catégorie de recherche
        :return: le chemin de l'image ou None si non trouvée
        """
        for image in os.listdir(f'../images/pokemon/{category}'):
            match = re.match(f'^{search_term}(\\..+)', image)
            if match:
                return f'../images/pokemon/{category}/{search_term}{match.group(1)}'
        return None

    def _set_image_filename(pokemon: dict[str, any], category: str):
        """
        Rajoute les informations sur les images des Pokémon
        :param pokemon: le dictionnaire des informations du Pokémon
        :param category: la catégorie de l'image à rechercher (sprite, full, icon)
        """
        pokemon[category] = None

        if category != 'full' and pokemon['egg']:
            pokemon[category] = f'../images/pokemon/{category}/egg.png'
        else:
            search = slugify(pokemon['name'])
            pokemon[category] = _get_icon_filename(search, category)

            if not pokemon[category]:
                search = slugify(pokemon['species'].species)
                pokemon[category] = _get_icon_filename(search, category)

            if not pokemon[category]:
                pokemon[category] = f'../images/pokemon/{category}/default.png'

    def _set_attacks(pokemon: dict[str, any]):
        """
        Rajoute les informations sur les attaques du Pokémon
        :param pokemon: le dictionnaire des informations du Pokémon
        """
        pokemon['attacks'] = {
            'level': [],
            'cs': [],
            'ct': [],
            'gm': [],
            'cm': [],
            'specials_attacks_name': ''
        }

        attack_names = {
            'cs': [],
            'ct': [],
            'cm': [],
            'gm': []
        }

        pokemon_attacks = (
            PokemonOwnedAttacks
            .query
            .join(PokemonSpeciesAttacks)
            .filter(PokemonOwnedAttacks.pokemon_owned_id == pokemon['id'])
            .order_by(asc(PokemonSpeciesAttacks.level))
            .all()
        )

        for owned_attack in pokemon_attacks:
            species_attack = PokemonSpeciesAttacks.query.filter(
                PokemonSpeciesAttacks.id == owned_attack.species_attack_id
            ).first()
            attack_detail = PokemonAttacks.query.filter(PokemonAttacks.id == species_attack.attack_id).first()

            type = slugify(TypePokemon.get_from_value(attack_detail.type_id).value[1])
            attack_detail.type_full = f'../images/types/{type}_full.png'
            attack_detail.type_icon = f'../images/types/{type}.png'

            title = []
            if attack_detail.useless:
                title.append('Inutile')
            if attack_detail.informations:
                title.append(attack_detail.informations)
            if attack_detail.burn_percentage:
                title.append(f'Brulure {attack_detail.burn_percentage}%')
            if attack_detail.freeze_percentage:
                title.append(f'Gel {attack_detail.freeze_percentage}%')
            if attack_detail.paralyse_percentage:
                title.append(f'Paralisie {attack_detail.paralyse_percentage}%')
            if attack_detail.scare_percentage:
                title.append(f'Frayeur {attack_detail.scare_percentage}%')
            if attack_detail.poison_percentage:
                title.append(f'Poison {attack_detail.poison_percentage}%')
            if attack_detail.sleep_percentage:
                title.append(f'Endormissement {attack_detail.sleep_percentage}%')
            if attack_detail.boost:
                title.append(attack_detail.boost)
            if attack_detail.critique_attack:
                title.append('Chance de critique')

            attack_detail.title = ' / '.join(title)

            owned_attack.species_detail = vars(species_attack)
            owned_attack.global_detail = vars(attack_detail)

            species_detail = owned_attack.species_detail
            attack_type = next((key for key in ['ct', 'cs', 'gm', 'cm'] if species_detail[key]), 'level')

            pokemon['attacks'][attack_type].append(owned_attack)

            if attack_type != 'level':
                attack_names[attack_type].append(owned_attack.global_detail['name'])

        for attack_type, names in attack_names.items():
            if names:
                pokemon['attacks']['specials_attacks_name'] += f" / {attack_type.upper()} {' + '.join(names)}"

    def _set_types(pokemon: dict[str, any]):
        """
        Ajoute les informamation sur les types du Pokémon
        :param pokemon: le dictionnaire des informations du Pokémon
        """
        type_1 = slugify(TypePokemon.get_from_value(pokemon['species'].type_1_id).value[1])
        type_2 = TypePokemon.get_from_value(pokemon['species'].type_2_id)

        pokemon['types_full'] = [f"../images/types/{type_1}_full.png"]
        pokemon['types_icon'] = [f"../images/types/{type_1}.png"]
        if type_2:
            type_2_value = slugify(type_2.value[1])
            pokemon['types_full'].append(f"../images/types/{type_2_value}_full.png")
            pokemon['types_icon'].append(f"../images/types/{type_2_value}.png")

    def _set_total_stats(pokemon: dict[str, any]):
        """
        Ajoute les informations sur les stats du Pokémon
        :param pokemon: le dictionnaire des informations du Pokémon
        """
        pokemon["sum_hp"] = pokemon['species'].pv + pokemon['pv'] + pokemon['hp_up']
        pokemon["sum_atk"] = pokemon['species'].atk + pokemon['atk'] + pokemon['protein']
        pokemon["sum_def"] = pokemon['species'].defense + pokemon['defense'] + pokemon['iron']
        pokemon["sum_atk_spe"] = pokemon['species'].atk_special + pokemon['atk_special'] + pokemon['calcium']
        pokemon["sum_def_spe"] = pokemon['species'].defense_special + pokemon['def_special'] + pokemon['zinc']
        pokemon["sum_speed"] = pokemon['species'].speed + pokemon['speed'] + pokemon['carbos']

        pokemon["point_per_level"] = 9 if pokemon['shiny'] else 8
        pokemon["level_point"] = pokemon["level"] - 5
        pokemon["point_to_spend"] = pokemon["point_per_level"] * pokemon["level_point"]

        boosts_used = []
        if pokemon['hp_up']:
            boosts_used.append(f'{pokemon['hp_up']} PV Plus')
        if pokemon['protein']:
            boosts_used.append(f'{pokemon['protein']} Protéine')
        if pokemon['iron']:
            boosts_used.append(f'{pokemon['iron']} Fer')
        if pokemon['calcium']:
            boosts_used.append(f'{pokemon['calcium']} Calcium')
        if pokemon['zinc']:
            boosts_used.append(f'{pokemon['zinc']} Zinc')
        if pokemon['carbos']:
            boosts_used.append(f'{pokemon['carbos']} Carbone')

        pokemon["boosts_used"] = " + ".join(boosts_used) if boosts_used else "Aucun"
        pokemon["boosts_total"] = (
                pokemon['hp_up']
                + pokemon['protein']
                + pokemon['iron']
                + pokemon['calcium']
                + pokemon['zinc']
                + pokemon['carbos']
        )

    pokemon = (
        PokemonOwned
        .query
        .join(PokemonCategory)
        .options(joinedload(PokemonOwned.species))
        .filter(PokemonOwned.character_id == character_id)
    )

    if is_stockage:
        pokemon = pokemon.filter(PokemonCategory.name == 'Stockage')

    pokemon = pokemon.all()

    for poke in pokemon:
        data['pokemon'][slugify(poke.category.name)].append(vars(poke))

    for _, pokemon in data['pokemon'].items():
        for poke in pokemon:
            poke['sex'] = "♂" if poke['sex'] == 'M' else '♀'
            _set_image_filename(poke, 'icon')
            _set_image_filename(poke, 'full')
            _set_image_filename(poke, 'sprite')
            _set_types(poke)
            _set_attacks(poke)
            _set_total_stats(poke)

    if character_id == 2:
        data['all_pokemon'] = [{
            "category": pokemon[0]['category'].name,
            "pokemon": pokemon
        } for _, pokemon in data['pokemon'].items()]


def get_ressources_data(character: MpCharacter, data: dict[str, any]):
    """
    Récupère les liens des ressources (avatars, signatures, ...)
    :param character: le personnage
    :param data: le dictionnaire des informations
    """
    def _get_images(path: str, data: dict[str, any], folder_name: str = 'moi'):
        """
        Ajoute les liens des images
        :param path: le lien vers le dossier image
        :param data: le dictionnaire des informations
        :param folder_name: le nom du dossier à parcourir
        """
        folder_name = folder_name if folder_name in {'moi', 'ici'} else folder_name.title()
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                data[folder_name].append(file_path)
            elif os.path.isdir(file_path):
                _get_images(file_path, data, file)

    folders = [('autre', 'ici'), ('avatar', 'moi'), ('signature', 'moi'), ('stamp', 'ici')]
    tmp = dict()

    for folder in folders:
        cat_name = folder[0]
        url = os.path.join('..\\', 'images', character.firstname.lower(), cat_name)
        tmp[cat_name] = defaultdict(list)
        _get_images(url, tmp[cat_name], folder[1])
        data[cat_name] = []

    for category, values in tmp.items():
        for name, image in values.items():
            data[category].append({
                'name': name,
                'image': image
            })

    regex = re.compile(r'\..\\images\\(?:luna|lime)\\stamp\\(\d+)\.png')
    data["stamp"][0]['image'] = sorted(data["stamp"][0]['image'], key=lambda x: int(regex.search(x).group(1)))


def get_social_data(character_id: int, data: dict[str, any]):
    """
    Récupère les informations pour la partie relation
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    socials_pnj = Social.query.filter(
        Social.character_id == character_id, Social.pj == 0
    ).join(SocialPokemon, isouter=True).join(SocialSubject, isouter=True).all()

    socials_pj = Social.query.filter(
        Social.character_id == character_id, Social.pj == 1
    ).join(SocialPokemon, isouter=True).join(SocialSubject, isouter=True).all()

    data['socials_pnj'] = convert_social_for_ihm(socials_pnj)
    data['socials_pj'] = convert_social_for_ihm(socials_pj)


def get_inventory_data(character: MpCharacter, character_id: int, data: dict[str, any]):
    """
    Ajoute les informations sur l'inventaire
    :param character: le personnage
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    balls = (Inventory.query.filter(Inventory.character_id == character_id)
             .join(Object).filter(Object.category == ObjectEnum.BALLS.value).all())
    heals = (Inventory.query.filter(Inventory.character_id == character_id)
             .join(Object).filter(Object.category == ObjectEnum.HEAL.value).all())
    evols = (Inventory.query.filter(Inventory.character_id == character_id)
             .join(Object).filter(Object.category == ObjectEnum.EVOL.value).all())
    others = (Inventory.query.filter(Inventory.character_id == character_id)
              .join(Object).filter(Object.category == ObjectEnum.OTHER.value).all())
    berries = (Inventory.query.filter(Inventory.character_id == character_id)
               .join(Object).filter(Object.category == ObjectEnum.BERRY.value).all())
    rares = (Inventory.query.filter(Inventory.character_id == character_id)
             .join(Object).filter(Object.category == ObjectEnum.RARE.value).all())
    money = Money.query.filter(Money.character_id == character_id).first()
    cts = Ct.query.filter(Ct.character_id == character_id).join(Object).all()
    cs_history = CsHistory.query.filter(CsHistory.character_id == character_id).join(Object).all()
    flute_history = FluteHistory.query.filter(FluteHistory.character_id == character_id).join(Object).all()
    histories = History.query.filter(History.character_id == character_id).all()

    def _get_date(objet: History):
        """
        Récupère la date de transaction
        :param objet: l'objet history
        :return: la date au format jour/mois/année
        """
        return datetime.strptime(objet.movement_date, DATE_FORMAT)

    histories = sorted(histories, key=lambda history: (-_get_date(history).timestamp(), -history.id))

    for ct in cts:
        ct.quantity_string = convert_int_to_prefixed_string(int(ct.quantity))
        ct.type = slugify(ct.object.name)

    if character.firstname == 'Luna':
        for history in histories:
            history.icon = '►' if history.movement == 'in' else '◄' if history.movement == 'out' else '◄►'
    elif character.firstname == 'Lime':
        grouped_history = defaultdict(list)

        for history in histories:
            history.icon = (
                'fa-arrow-right-long ' if history.movement == 'in'
                else 'fa-arrow-left-long' if history.movement == 'out'
                else 'fa-arrow-right-arrow-left'
            )

            grouped_history[history.movement_date].append(history)

        histories = [
            {'date': date, 'history': items}
            for date, items in grouped_history.items()
        ]

    data['ballsCat'] = convert_object_for_ihm(balls, character_id)
    data['healsCat'] = convert_object_for_ihm(heals, character_id)
    data['evolCat'] = convert_object_for_ihm(evols, character_id)
    data['raresCat'] = convert_object_for_ihm(rares, character_id)
    data['money'] = money
    data['ct'] = cts
    data['csHistory'] = cs_history
    data['fluteHistory'] = flute_history
    data['histories'] = histories
    data['otherCat'] = convert_object_for_ihm(others, character_id)
    data['berriesCat'] = convert_object_for_ihm(berries, character_id)


def get_character_data(character_id: int, data: dict[str, any]):
    """
    Ajoute les informations du personnage
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    mentals = Mental.query.filter(Mental.character_id == character_id).all()
    physicals = Physical.query.filter(Physical.character_id == character_id).all()

    data['mental'] = [mental.description for mental in mentals]
    data['physical'] = [physical.description for physical in physicals]


def get_journeys_data(character_id: int, data: dict[str, any]):
    """
    Ajoute les données sur le parcours
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    chapters = JourneyChapter.get_ordered_chapter(character_id=character_id, with_journeys=True)

    for chapter in chapters:
        for journey in chapter.journeys:
            status = JourneyStatus.get_from_value(journey.status)
            journey.status_class = status.name.lower()
            journey.icon = status.value[2]

    data['chapters'] = [vars(chapter) for chapter in chapters]


def get_goals_data(character_id: int, data: dict[str, any]):
    """
    Ajoute les informations sur les objectifs
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    goals = Goals.query.filter(Goals.character_id == character_id, Goals.category == GoalCategory.GLOBAL.value).all()
    pokemon = Goals.query.filter(
        Goals.character_id == character_id,
        Goals.category == GoalCategory.POKEMON.value,
        Goals.done == false()
    ).all()

    data['globale_goals'] = [vars(goal) for goal in goals]
    data['pokemon_goals'] = [vars(poke) for poke in pokemon]


def get_ndm_data(character_id: int, data: dict[str, any]):
    """
    Ajoute les informations sur les NDM
    :param character_id: l'id du personnage
    :param data: le dictionnaire des informations
    """
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().strftime('%Y')

    actual_month = (
        NdmMonths
        .query
        .filter(NdmMonths.month == current_month, NdmMonths.year == current_year)
        .first()
    )

    ndms = NdmPosts.query.filter(NdmPosts.character_id == character_id).all()
    small_month_id = min([ndm.id for ndm in ndms]) if ndms else 1

    months = NdmMonths.query.filter(NdmMonths.id >= small_month_id, NdmMonths.id != actual_month.id).all()

    grouped = defaultdict(list)
    for month in months:
        grouped[month.year].append({
            "month": month_convert(month.month),
            "month_slug": f"{month.month}{month.year}"
        })

    archives = [{"year": year, "months": mois} for year, mois in grouped.items()]
    data['archives'] = archives

    ndm_current_month = (
        NdmPosts
        .query
        .join(NdmSubjects, NdmPosts.subject_id == NdmSubjects.id)
        .filter(
            NdmPosts.month_id == actual_month.id,
            NdmPosts.character_id == character_id
        )
        .with_entities(
            NdmSubjects.name.label("subject_name"),
            NdmSubjects.info.label("subject_info"),
            NdmSubjects.url.label("subject_link"),
            func.count(NdmPosts.id).label("total_posts"),
            func.sum(NdmPosts.words).label("total_words")
        )
        .group_by(NdmPosts.subject_id)
        .order_by(NdmPosts.subject_id.asc())
        .all()
    )

    subjects = []
    for ndm in ndm_current_month:
        subjects.append({
            "name": ndm.subject_name,
            "info": ndm.subject_info,
            "url": ndm.subject_link,
            "total_words": ndm.total_words,
            "total_posts": ndm.total_posts,
        })

    global_total_words = sum([subject["total_words"] for subject in subjects])
    global_total_posts = sum([subject["total_posts"] for subject in subjects])

    current_month_data = {
        'name': f"{month_convert(actual_month.month)} {actual_month.year}",
        'subjects': subjects,
        'total_words': global_total_words,
        'total_posts': global_total_posts,
        'avg_words': floor(global_total_words / global_total_posts) if global_total_posts else 0,
    }
    data['current_month'] = current_month_data

    past_month = []
    for p_month in months:
        m = (
            NdmPosts
            .query
            .join(NdmSubjects, NdmPosts.subject_id == NdmSubjects.id)
            .filter(
                NdmPosts.month_id == p_month.id,
                NdmPosts.character_id == character_id
            )
            .with_entities(
                NdmSubjects.name.label("subject_name"),
                NdmSubjects.info.label("subject_info"),
                NdmSubjects.url.label("subject_link"),
                func.count(NdmPosts.id).label("total_posts"),
                func.sum(NdmPosts.words).label("total_words")
            )
            .group_by(NdmPosts.subject_id)
            .order_by(NdmPosts.subject_id.asc())
            .all()
        )

        subjects = []
        for ndm in m:
            subjects.append({
                "name": ndm.subject_name,
                "info": ndm.subject_info,
                "url": ndm.subject_link,
                "total_words": ndm.total_words,
                "total_posts": ndm.total_posts,
            })

        global_total_words = sum([subject["total_words"] for subject in subjects])
        global_total_posts = sum([subject["total_posts"] for subject in subjects])

        reward = NdmRewards.query.filter(NdmRewards.month_id == p_month.id).first()

        past_month_data = {
            'name': f"{month_convert(p_month.month)} {p_month.year}",
            'slug': f"{p_month.month}{p_month.year}",
            'subjects': subjects,
            'total_words': global_total_words,
            'total_posts': global_total_posts,
            'avg_words': floor(global_total_words / global_total_posts) if global_total_posts else 0,
            'level_winned': f"{reward.level_winned} ({reward.level_winned_justif})" if reward else '/',
            'distribution': reward.distribution if reward else '/',
        }
        past_month.append(past_month_data)

    data['past_month'] = past_month


def generate_physique_or_mental(
        field: Field, character_id: int, clazz: type[Mental] | type[Physical]
) -> list[Mental | Physical]:
    """
    Génère les informations sur le physique ou la psychologie
    :param field: les champs du formulaire
    :param character_id: l'id du personnage
    :param clazz: la classe Physical or Mental
    :return: Une liste d'objet Physical or Mental
    """
    output = []
    for description in field.data:
        if description['description']:
            output.append(clazz(
                id=None,
                character_id=character_id,
                description=description['description']
            ))
    return output


def modify_cs_flute_data(field: FieldList, histories: list[CsHistory | FluteHistory]):
    """
    Modifie les utilisations des CS / Flûtes
    :param field: les champs du formulaire de modification
    :param histories: les utilisations en base de données
    """
    for history_form in field:
        for history in histories:
            if history.object.id == history_form.object.data.id and history_form.last_used.data:
                history.last_used = history_form.last_used.data.strftime(DATE_FORMAT)
                history.link = history_form.link.data
                break


def convert_object_for_ihm(items: list[Inventory], character_id: int) -> list[Inventory]:
    """
    Modifie la liste des objets pour affichage dans le template mustache
    :param items: les items
    :param character_id: l'id du personnage
    :return: la liste des objets
    """
    for item in items:
        if item.object_id in Object.get_objects_id_with_justificatif():
            item.links = JustificatifLink.query.filter(
                JustificatifLink.object_id == item.object_id,
                JustificatifLink.character_id == character_id
            ).all()
        item.quantity_string = convert_int_to_prefixed_string(int(item.quantity))
        item.slug_name = slugify(item.object.name)

    return items


def convert_social_for_ihm(items: list[Social]) -> list[Social]:
    """
    Modifie la liste des relations pour affichage dans le template mustache
    :param items: les items
    :return: la liste des relations
    """
    for item in items:
        item.slug_full_name = slugify(item.full_name)
        for pokemon in item.pokemon:
            pokemon.slug_pokemon = slugify(pokemon.pokemon)

    return items


def month_convert(month: str) -> str:
    months = {
        'janvier': 'Janvier',
        'fevrier': 'Février',
        'mars': 'Mars',
        'avril': 'Avril',
        'mai': 'Mai',
        'juin': 'Juin',
        'juillet': 'Juillet',
        'aout': 'Août',
        'septembre': 'Septembre',
        'octobre': 'Octobre',
        'novembre': 'Novembre',
        'decembre': 'Décembre',
    }

    return months.get(month)
