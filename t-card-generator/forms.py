from wtforms import Form, StringField, SelectField, RadioField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateField
from wtforms.fields.form import FormField
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SubmitField, URLField, BooleanField, HiddenField
from wtforms.validators import Length, DataRequired, NumberRange, InputRequired, Optional

from enums import Status, Region, Sex, JourneyStatus, TypePokemon


class InformationsForm(Form):
    """
    Formulaire des informations du personnage
    """
    firstname = StringField('Prénom', [DataRequired(), Length(max=20)])
    lastname = StringField('Nom', [DataRequired(), Length(max=20)])
    original_char_name = StringField('Perso d\'origine', [DataRequired(), Length(max=50)])
    original_game = StringField('Jeu d\'origine', [DataRequired(), Length(max=50)])
    age = IntegerField('Âge', [DataRequired(), NumberRange(min=0, max=99)])
    status = SelectField('Statut', choices=Status.to_tuple(), validators=[DataRequired()])
    sex = RadioField('Sexe', choices=Sex.to_tuple(), validators=[DataRequired()])
    region = SelectField('Région', choices=Region.to_tuple(), validators=[DataRequired()])
    starter = StringField('Starter', [DataRequired(), Length(max=100)])
    id_number = StringField('ID Dresseur', [DataRequired(), Length(min=4, max=4)])
    presentation = URLField('Lien présentation')


class DescriptionForm(Form):
    """
    Formulaire pour la description
    """
    description = StringField('')


class MentalForm(Form):
    """
    Formulaire pour les caractéristiques mental
    """
    descriptions_mental = FieldList(FormField(DescriptionForm), min_entries=1)
    add_description_mental = SubmitField("+")


class PhysicalForm(Form):
    """
    Formulaire pour les caractéristiques physiques
    """
    descriptions_physical = FieldList(FormField(DescriptionForm), min_entries=1)
    add_description_physical = SubmitField("+")


class MoneyForm(Form):
    """
    Formulaire pour l'argent
    """
    amount = IntegerField('Argent', [DataRequired(), NumberRange(min=0)])
    statement_date = DateField('Date', [DataRequired()])


class HistoryData(Form):
    """
    Formulaire pour l'historique
    """
    object = StringField()
    id = IntegerField()
    last_used = DateField('Date', [Optional()])
    link = StringField('Lien', [Length(max=255)])


class CsHistoryForm(Form):
    """
    Formulaire pour l'utilisation des CS
    """
    cs_history = FieldList(FormField(HistoryData), min_entries=6, max_entries=6)


class FluteHistoryForm(Form):
    """
    Formulaire pour l'utilisation des flûtes
    """
    flute_history = FieldList(FormField(HistoryData), min_entries=2, max_entries=2)


class SocialSubjectForm(Form):
    """
    Formulaire pour les sujets en commun avec les relations
    """
    id = IntegerField()
    link = URLField('URL', [Length(max=255)])


class SocialPokemonForm(Form):
    """
    Formulaire pour les Pokémon des relations
    """
    id = IntegerField()
    pokemon = StringField('Espèces', [Length(max=25)])
    pokemon_name = StringField('Nom', [Length(max=25)])


class SocialForm(Form):
    """
    Formulaire pour les relations
    """
    full_name = StringField('Nom', [Length(max=50), DataRequired()])
    bond = StringField('Lien', [Length(max=50), DataRequired()])
    description = StringField('Description', [DataRequired()])
    pj = RadioField('PJ ?', choices=[(0, 'Non'), (1, 'Oui')], validators=[DataRequired()])
    hexa_text = StringField('Couleur', [Length(max=25)])
    subjects = FieldList(FormField(SocialSubjectForm), min_entries=1)
    add_subject = SubmitField("+")
    pokemon = FieldList(FormField(SocialPokemonForm), min_entries=1)
    add_pokemon = SubmitField("+")


class JourneyChapterForm(Form):
    """
    Formulaire pour les aventures
    """
    name = StringField('Nom', [Length(max=25), DataRequired()])
    after = SelectField('Positionné après', coerce=int, validators=[InputRequired()])


class JourneyForm(Form):
    """
    Formulaire pour les aventures
    """
    name = StringField('Nom', [Length(max=100), DataRequired()])
    link = URLField('Lien', validators=[Length(max=255)])
    after = SelectField('Positionné après', coerce=int, validators=[InputRequired()])
    status = SelectField('Statut', choices=JourneyStatus.to_tuple(), validators=[InputRequired()])
    feat = StringField('Feat', [Length(max=100), DataRequired()], default="Solo")


class ObjectForm(Form):
    """
    Formulaire pour la gestion des objets
    """
    object_id = StringField()
    object_name = StringField('Nom de l\'object')
    delta = IntegerField('Delta', [DataRequired(), NumberRange(min=0)])


class CtForm(Form):
    """
    Formulaire pour la gestion des CT
    """
    ct_type = StringField('Type CT')
    object_name = StringField('Nom CT', [DataRequired(), Length(max=50)])
    delta = IntegerField('Delta', [DataRequired(), NumberRange(min=0)])
    reserved = StringField('Réservé à', [Length(max=100)])


class AssortmentForm(Form):
    """
    Formulaire pour les assortiments
    """
    assortment_name = StringField('Nom')
    quantity = IntegerField('Quantité', [DataRequired()])


class CtReservationForm(Form):
    """
    Formulaire pour la réservation des CT
    """
    id = IntegerField()
    name = StringField('CT')
    reserved = StringField('Réservé à', [Length(max=100)])


class CtReservationListForm(Form):
    """
    Formulaire pour la réservation des CT (liste)
    """
    ct_reservations = FieldList(FormField(CtReservationForm))


class InventoryForm(Form):
    """
    Formulaire pour l'inventaire
    """
    objects = FieldList(FormField(ObjectForm))
    add_object = SubmitField("+")
    ct_list = FieldList(FormField(CtForm))
    add_ct = SubmitField("+")
    new_ct_list = FieldList(FormField(CtForm))
    add_new_ct = SubmitField("+")
    assortment_list = FieldList(FormField(AssortmentForm))
    add_assortment = SubmitField("+")
    movement = RadioField('Ajout', choices=[('in', 'Oui'), ('out', 'Non')], validators=[DataRequired()])
    movement_date = DateField('Date', [DataRequired()])
    link = URLField('Lien', [Length(max=255), DataRequired()])
    link_name = StringField('Nom lien', [Length(max=100), DataRequired()])


class InventoryExchangeForm(Form):
    """
    Formulaire pour les échanges
    """
    objects_in = FieldList(FormField(ObjectForm))
    add_object_in = SubmitField("+")
    ct_in = FieldList(FormField(CtForm))
    add_ct_in = SubmitField("+")
    new_ct_in = FieldList(FormField(CtForm))
    add_new_ct_in = SubmitField("+")
    objects_out = FieldList(FormField(ObjectForm))
    add_object_out = SubmitField("+")
    ct_out = FieldList(FormField(CtForm))
    add_ct_out = SubmitField("+")
    exchange_date = DateField('Date', [DataRequired()])
    link = URLField('Lien', [Length(max=255), DataRequired()])
    link_name = StringField('Nom lien', [Length(max=100), DataRequired()])


class LinksForm(Form):
    """
    Formulaire pour les liens des justificatifs
    """
    id = IntegerField()
    object_name = StringField('Objet')
    link = URLField('Lien')
    link_title = StringField('Nom')
    removed_link = URLField('Utilisation')


class JustificatifLinkForm(Form):
    """
    Formulaire pour les justificatifs
    """
    justificatif_links = FieldList(FormField(LinksForm))


class GoalsForm(Form):
    """
    Formulaire pour les buts
    """
    id = IntegerField()
    description = StringField('Nom', validators=[Length(max=100)])
    category = IntegerField()
    done = BooleanField('Fini')


class GoalsListForm(Form):
    """
    Formulaire pour la liste des buts
    """
    globals_goals = FieldList(FormField(GoalsForm))
    add_globals = SubmitField("+")
    pokemon_goals = FieldList(FormField(GoalsForm))
    add_pokemon = SubmitField("+")


class PokemonSpeciesForm(Form):
    """
    Formulaire pour les espèces de Pokémon
    """
    species = StringField('Espèce', validators=[DataRequired()])
    type_1_id = SelectField('Type 1', choices=TypePokemon.to_tuple_int(), validators=[InputRequired()])
    type_2_id = SelectField('Type 2', choices=TypePokemon.to_tuple_int_with_empty(), validators=[Optional()])
    evolution_id = SelectField('Evolution', coerce=int, validators=[InputRequired()])
    evolution_way = SelectField('Moyen d\'évolution', coerce=int)
    evolution_level = IntegerField('Niveau d\'évolution', validators=[Optional(), NumberRange(min=0)])
    pv = IntegerField('PV', validators=[InputRequired(), NumberRange(min=0)])
    atk = IntegerField('Attaque', validators=[InputRequired(), NumberRange(min=0)])
    atk_special = IntegerField('Attaque Spéciale', validators=[InputRequired(), NumberRange(min=0)])
    defense = IntegerField('Défense', validators=[InputRequired(), NumberRange(min=0)])
    defense_special = IntegerField('Défense Spéciale', validators=[InputRequired(), NumberRange(min=0)])
    speed = IntegerField('Vitesse', validators=[InputRequired(), NumberRange(min=0)])


class PokemonAttackForm(Form):
    """
    Formulaire pour les attaques
    """
    name = StringField('Nom', validators=[DataRequired()])
    type_id = SelectField('Type', coerce=int, choices=TypePokemon.to_tuple_int(), validators=[InputRequired()])
    informations = StringField('Informations')
    power = IntegerField('Puissance', validators=[Optional(), NumberRange(min=0)])
    precision = IntegerField('Précision', validators=[Optional(), NumberRange(min=0)])
    useless = BooleanField('Inutile en combat')
    burn_percentage = IntegerField('Chance de brûler', validators=[Optional(), NumberRange(min=0)])
    freeze_percentage = IntegerField('Chance de geler', validators=[Optional(), NumberRange(min=0)])
    paralyse_percentage = IntegerField('Chance de paralyser', validators=[Optional(), NumberRange(min=0)])
    scare_percentage = IntegerField('Chance d\'effrayer', validators=[Optional(), NumberRange(min=0)])
    poison_percentage = IntegerField('Chance d\'empoissonner', validators=[Optional(), NumberRange(min=0)])
    sleep_percentage = IntegerField('Chance d\'endormir', validators=[Optional(), NumberRange(min=0)])
    boost = StringField('Boost')
    critique_attack = BooleanField('Chance augmentée de critique')


class PokemonAttacksForm(Form):
    """
    Formulaire pour gérer les attaques
    """
    attacks = FieldList(FormField(PokemonAttackForm))
    add_attack = SubmitField("+")


class PokemonSpeciesAttackForm(Form):
    """
    Formulaire pour lier les attaques aux espèces
    """
    attack_id = IntegerField(validators=[InputRequired()])
    learned = BooleanField('')
    attack_name = StringField('', validators=[InputRequired()], render_kw={'readonly': True})
    level = IntegerField('Niveau', validators=[Optional(), NumberRange(min=0)])
    ct = BooleanField('CT')
    cs = BooleanField('CS')
    gm = BooleanField('GM')
    cm = BooleanField('CM')


class PokemonSpeciesAttacksForm(Form):
    """
    Formulaire pour lier les attaques aux espèces (liste)
    """
    species_id = SelectField('Pokémon', coerce=int, validators=[InputRequired()])
    attacks = FieldList(FormField(PokemonSpeciesAttackForm))


class PokemonOwnedForm(Form):
    """
    Formulaire pour les Pokémon possédés
    """
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    species_id = SelectField('Espèce', coerce=int, validators=[DataRequired()])
    sex = SelectField('Sexe', choices=[('M', 'Mâle'), ('F', 'Femelle')], validators=[DataRequired()])
    level = IntegerField('Level', validators=[DataRequired(), NumberRange(min=5, max=100)])
    shiny = BooleanField('Shiny')
    pv = IntegerField('HP', validators=[NumberRange(min=0)], default=0)
    atk = IntegerField('ATK', validators=[NumberRange(min=0)], default=0)
    atk_special = IntegerField('ATK Spé', validators=[NumberRange(min=0)], default=0)
    defense = IntegerField('DEF', validators=[NumberRange(min=0)], default=0)
    def_special = IntegerField('DEF Spé', validators=[NumberRange(min=0)], default=0)
    speed = IntegerField('Vitesse', validators=[NumberRange(min=0)], default=0)
    exp_point = IntegerField('Points XP', validators=[NumberRange(min=0)], default=0)
    hp_up = IntegerField('PV Plus', validators=[NumberRange(min=0)], default=0)
    zinc = IntegerField('Zinc', validators=[NumberRange(min=0)], default=0)
    calcium = IntegerField('Calcium', validators=[NumberRange(min=0)], default=0)
    carbos = IntegerField('Carbone', validators=[NumberRange(min=0)], default=0)
    iron = IntegerField('Fer', validators=[NumberRange(min=0)], default=0)
    protein = IntegerField('Proteine', validators=[NumberRange(min=0)], default=0)
    obtention_link = StringField('Lien d\'obtention', validators=[DataRequired(), Length(max=255)])
    obtention_name = StringField('Nom du lien', validators=[DataRequired(), Length(max=255)])
    nature = StringField('Nature', validators=[DataRequired(), Length(max=20)])
    sprite_credits = StringField('Sprite Credits', validators=[Length(max=255)])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    egg = BooleanField('Oeuf')
    background = SelectField('Sprite background', validators=[DataRequired()])
    banner_credit = StringField('Crédit bannière')


class PokemonOwnedEditForm(Form):
    """
    Formulaire d'édition d'un Pokémon
    """
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    sex = SelectField('Sexe', choices=[('M', 'Mâle'), ('F', 'Femelle')], validators=[DataRequired()])
    shiny = BooleanField('Shiny')
    obtention_link = StringField('Lien d\'obtention', validators=[DataRequired(), Length(max=255)])
    obtention_name = StringField('Nom du lien', validators=[DataRequired(), Length(max=255)])
    nature = StringField('Nature', validators=[DataRequired(), Length(max=20)])
    sprite_credits = StringField('Sprite Credits', validators=[Length(max=255)])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    banner_credit = StringField('Crédit bannière')


class PokemonCategoryForm(Form):
    """
    Formulaire pour les catégories de Pokémon
    """
    name = StringField('Nom', validators=[DataRequired(), Length(max=255)])


class PokemonXpForm(Form):
    """
    Formulaire pour les gain d'exp
    """
    level = IntegerField('Niveau', validators=[NumberRange(min=0), Optional()])
    point = IntegerField('Point d\'expérience', validators=[NumberRange(min=0), Optional()])


class PokemonEvolutionForm(Form):
    """
    Formulaire pour l'évolution
    """
    link = StringField('Lien', [Length(max=255)])


class GivePokemonForm(Form):
    """
    Formulaire pour le don de Pokémon
    """
    pokemon_id = SelectField('Pokémon', coerce=int, validators=[DataRequired()])
    new_owner = StringField('A qui ?', validators=[DataRequired(), Length(max=50)])
    history_link = StringField('Lien', validators=[DataRequired(), Length(max=255)])
    history_name = StringField('Titre historique', validators=[DataRequired(), Length(max=255)])


class ExchangePokemonNewForm(Form):
    """
    Formulaire pour le Pokémon lors d'un échange
    """
    name = StringField('Nom', validators=[DataRequired(), Length(max=100)])
    species_id = SelectField('Espèce', coerce=int, validators=[DataRequired()])
    sex = SelectField('Sexe', choices=[('M', 'Mâle'), ('F', 'Femelle')], validators=[DataRequired()])
    level = IntegerField('Level', validators=[DataRequired(), NumberRange(min=5)])
    shiny = BooleanField('Shiny', default=False)
    hp_up = IntegerField('PV Plus', validators=[NumberRange(min=0)], default=0)
    zinc = IntegerField('Zinc', validators=[NumberRange(min=0)], default=0)
    calcium = IntegerField('Calcium', validators=[NumberRange(min=0)], default=0)
    carbos = IntegerField('Carbone', validators=[NumberRange(min=0)], default=0)
    iron = IntegerField('Fer', validators=[NumberRange(min=0)], default=0)
    protein = IntegerField('Proteine', validators=[NumberRange(min=0)], default=0)
    nature = StringField('Nature', validators=[DataRequired(), Length(max=20)])
    sprite_credits = StringField('Sprite Credits', validators=[Length(max=255)])
    category_id = SelectField('Catégorie', coerce=int, validators=[DataRequired()])
    egg = BooleanField('Oeuf')
    background = SelectField('Sprite background', validators=[DataRequired()])
    banner_credit = StringField('Crédit bannière')


class ExchangePokemonForm(Form):
    """
    Formulaire pour l'échange de Pokémon
    """
    pokemon_ids = SelectMultipleField("Pokémon", coerce=int, validators=[DataRequired()])
    new_pokemon = FieldList(FormField(ExchangePokemonNewForm))
    add_new_pokemon = SubmitField("+")
    new_owner = StringField('A qui ?', validators=[DataRequired(), Length(max=50)])
    history_link = StringField('Lien', validators=[DataRequired(), Length(max=255)])
    history_name = StringField('Titre historique', validators=[DataRequired(), Length(max=255)])


class LearnAttackForm(Form):
    """
    Formulaire pour les attaques lors de l'apprentissage
    """
    attack_id = HiddenField('', validators=[InputRequired()], render_kw={'display': None})
    attack_name = StringField('', validators=[InputRequired()], render_kw={'readonly': True})
    learned = BooleanField('Apprendre ?')


class LearnAttacksForm(Form):
    """
    Formulaire pour l'apprentissage d'attaques
    """
    attacks = FieldList(FormField(LearnAttackForm))


class ToPensionForm(Form):
    """
    Formulaire pour placer un Pokémon en pension
    """
    pension_name = StringField('Nom de la pension', validators=[DataRequired(), Length(max=255)])


class LeavePensionForm(Form):
    """
    Formulaire pour retirer un Pokémon de pension
    """
    new_level = IntegerField('Nouveau niveau', validators=[DataRequired(), NumberRange(min=5, max=100)])
    new_xp = IntegerField('Nouvelle expérience', validators=[InputRequired(), NumberRange(min=0, max=7)])


class PokemonStatsForm(Form):
    """
    Formulaire pour la gestion des stats
    """
    pv = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    hp_up = IntegerField('', validators=[InputRequired(), NumberRange()])
    atk = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    protein = IntegerField('', validators=[InputRequired(), NumberRange()])
    defense = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    iron = IntegerField('', validators=[InputRequired(), NumberRange(max=10)])
    atk_spe = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    calcium = IntegerField('', validators=[InputRequired(), NumberRange(max=10)])
    defense_spe = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    zinc = IntegerField('', validators=[InputRequired(), NumberRange(max=10)])
    speed = IntegerField('', validators=[InputRequired(), NumberRange(min=0)])
    carbos = IntegerField('', validators=[InputRequired(), NumberRange(max=10)])


class SubjectForm(Form):
    """
    Formulaire pour ajouter un post à un sujet pour les ndm
    """
    subject_id = HiddenField('', validators=[DataRequired()])
    subject_name = StringField('Sujet', render_kw={'readonly': True})
    words = IntegerField('Nombre de mots', validators=[Optional(), NumberRange(min=0)])
    actual_words = StringField('Mots actuels', render_kw={'readonly': True})


class NewPostForm(Form):
    """
    Formulaire listant les sujets des ndm
    """
    subjects = FieldList(FormField(SubjectForm))


class NewNdmSubjectForm(Form):
    """
    Formulaire pour un sujet de ndm
    """
    name = StringField('Nom', validators=[DataRequired()])
    url = URLField('Lien', validators=[DataRequired()])
    info = StringField('Information', validators=[DataRequired()])


class NdmRewardForm(Form):
    """
    Formulaire pour les récompenses des NDM
    """
    level_winned = IntegerField('Niveaux gagnés', validators=[DataRequired(), NumberRange(min=0)])
    level_winned_justif = StringField('Justification', validators=[DataRequired()])
    distribution = StringField('Distribution')
    money = BooleanField('Convertir en argent')
