from datetime import date, datetime

from flask import render_template, redirect, url_for, flash, request
from wtforms.validators import NumberRange

from database import app, db
from enums import Object as ObjectType, HistoryMouvment, Assortment, GoalCategory, EvolutionWay
from forms import MoneyForm, CsHistoryForm, FluteHistoryForm, SocialForm, \
    JourneyChapterForm, JourneyForm, InventoryForm, ObjectForm, CtForm, JustificatifLinkForm, AssortmentForm, \
    CtReservationListForm, GoalsListForm, GoalsForm, InventoryExchangeForm, PokemonSpeciesForm, \
    PokemonAttacksForm, PokemonAttackForm, PokemonSpeciesAttacksForm, PokemonSpeciesAttackForm, PokemonCategoryForm, \
    PokemonOwnedForm, PokemonXpForm, PokemonEvolutionForm, GivePokemonForm, ExchangePokemonForm, \
    ExchangePokemonNewForm, LearnAttacksForm, LearnAttackForm, ToPensionForm, LeavePensionForm, PokemonStatsForm
from models import CsHistory, Ct, Money, FluteHistory, Social, Object, \
    History, JustificatifLink, SocialPokemon, SocialSubject, JourneyChapter, Journey, Goals, PokemonSpecies, \
    PokemonAttacks, PokemonSpeciesAttacks, PokemonCategory, PokemonOwned, PokemonOwnedAttacks
from utils.generator import modify_cs_flute_data, generate_tcard_part, generate_physique_or_mental
from utils.levels import level_up_pokemon, get_xp_per_level
from utils.lists import change_order

from forms import InformationsForm, MentalForm, PhysicalForm
from models import MpCharacter, Mental, Physical, Inventory
from utils.pokemon import evol_pokemon, can_evol, give_pokemon as give_pkmn, exchange_pokemon as exchange_pkmn, \
    get_non_evol_attack, learn_auto_attacks, leave_pension
from utils.strings import DATE_FORMAT


@app.route("/")
def home():
    """
    Page d'accueil
    :return: le template
    """
    return render_template(
        'home.html',
        characters=MpCharacter.query.all()
    )


@app.route("/informations/<int:character_id>", methods=('GET', 'POST'))
def informations(character_id: int):
    """
    Affichage des informations d'un personnage
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'informations.html',
            character=character,
            form=form,
            mental_form=mental_form,
            physical_form=physical_form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    mentals = Mental.query.filter(Mental.character_id == character_id).all()
    physicals = Physical.query.filter(Physical.character_id == character_id).all()

    form = InformationsForm(formdata=request.form, obj=character)
    mental_form = MentalForm(formdata=request.form, descriptions_mental=mentals)
    physical_form = PhysicalForm(formdata=request.form, descriptions_physical=physicals)

    if request.method == 'POST':
        if mental_form.add_description_mental.data:
            mental_form.descriptions_mental.append_entry(None)
            return _render()
        if physical_form.add_description_physical.data:
            physical_form.descriptions_physical.append_entry(None)
            return _render()

        form.sex.data = character.sex
        form.region.data = character.region

        if form.validate() and mental_form.validate() and physical_form.validate():
            form.populate_obj(character)

            Mental.query.filter(Mental.character_id == character_id).delete()
            Physical.query.filter(Physical.character_id == character_id).delete()

            mentals = generate_physique_or_mental(mental_form.descriptions_mental, character_id, Mental)
            physicals = generate_physique_or_mental(physical_form.descriptions_physical, character_id, Physical)

            db.session.bulk_save_objects(mentals)
            db.session.bulk_save_objects(physicals)
            db.session.commit()

            generate_tcard_part(character.id, 'informations')
            flash(f'{character.firstname} modifié avec succès', 'success')
            return redirect(url_for('home'))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/new", methods=('GET', 'POST'))
def add_character():
    """
    Le formulaire d'ajout d'un personnage
    :return: le template
    """
    def _render():
        return render_template(
            'informations.html',
            form=form,
            mental_form=mental_form,
            physical_form=physical_form
        )

    form = InformationsForm(formdata=request.form)
    mental_form = MentalForm(formdata=request.form)
    physical_form = PhysicalForm(formdata=request.form)

    if request.method == 'POST':
        if mental_form.add_description_mental.data:
            mental_form.descriptions_mental.append_entry(None)
            return _render()

        if physical_form.add_description_physical.data:
            physical_form.descriptions_physical.append_entry(None)
            return _render()

        if form.validate() and physical_form.validate() and mental_form.validate():
            today = datetime.now().strftime(DATE_FORMAT)
            mp_character = MpCharacter()
            form.populate_obj(mp_character)
            db.session.add(mp_character)
            db.session.commit()
            db.session.refresh(mp_character)

            character_id = mp_character.id

            mentals = generate_physique_or_mental(mental_form.descriptions_mental, character_id, Mental)
            physicals = generate_physique_or_mental(physical_form.descriptions_physical, character_id, Physical)

            db.session.bulk_save_objects(mentals)
            db.session.bulk_save_objects(physicals)
            db.session.commit()

            inventory = [
                Inventory(character_id=character_id, object_id=1, quantity=10),
                Inventory(character_id=character_id, object_id=2, quantity=0),
                Inventory(character_id=character_id, object_id=3, quantity=0),
                Inventory(character_id=character_id, object_id=4, quantity=0),
                Inventory(character_id=character_id, object_id=5, quantity=0),
                Inventory(character_id=character_id, object_id=6, quantity=0),
                Inventory(character_id=character_id, object_id=7, quantity=0),
                Inventory(character_id=character_id, object_id=8, quantity=0),
                Inventory(character_id=character_id, object_id=9, quantity=0),
                Inventory(character_id=character_id, object_id=10, quantity=0),
                Inventory(character_id=character_id, object_id=11, quantity=0),
                Inventory(character_id=character_id, object_id=12, quantity=2),
                Inventory(character_id=character_id, object_id=13, quantity=0),
                Inventory(character_id=character_id, object_id=14, quantity=0),
                Inventory(character_id=character_id, object_id=15, quantity=0),
                Inventory(character_id=character_id, object_id=16, quantity=0),
                Inventory(character_id=character_id, object_id=17, quantity=0),
                Inventory(character_id=character_id, object_id=18, quantity=0),
                Inventory(character_id=character_id, object_id=19, quantity=0),
                Inventory(character_id=character_id, object_id=20, quantity=0),
                Inventory(character_id=character_id, object_id=21, quantity=0),
                Inventory(character_id=character_id, object_id=22, quantity=0),
                Inventory(character_id=character_id, object_id=23, quantity=0),
                Inventory(character_id=character_id, object_id=24, quantity=0),
                Inventory(character_id=character_id, object_id=25, quantity=0),
                Inventory(character_id=character_id, object_id=26, quantity=0),
                Inventory(character_id=character_id, object_id=27, quantity=0),
                Inventory(character_id=character_id, object_id=28, quantity=0),
                Inventory(character_id=character_id, object_id=29, quantity=0),
                Inventory(character_id=character_id, object_id=30, quantity=0),
                Inventory(character_id=character_id, object_id=31, quantity=0),
                Inventory(character_id=character_id, object_id=32, quantity=0),
                Inventory(character_id=character_id, object_id=33, quantity=0),
                Inventory(character_id=character_id, object_id=34, quantity=0),
                Inventory(character_id=character_id, object_id=35, quantity=0),
                Inventory(character_id=character_id, object_id=36, quantity=0),
                Inventory(character_id=character_id, object_id=55, quantity=0),
                Inventory(character_id=character_id, object_id=56, quantity=0),
                Inventory(character_id=character_id, object_id=57, quantity=0),
                Inventory(character_id=character_id, object_id=58, quantity=0),
                Inventory(character_id=character_id, object_id=59, quantity=0),
                Inventory(character_id=character_id, object_id=60, quantity=0),
                Inventory(character_id=character_id, object_id=61, quantity=0),
                Inventory(character_id=character_id, object_id=62, quantity=0),
                Inventory(character_id=character_id, object_id=63, quantity=0),
                Inventory(character_id=character_id, object_id=64, quantity=0),
                Inventory(character_id=character_id, object_id=65, quantity=0),
                Inventory(character_id=character_id, object_id=66, quantity=0),
                Inventory(character_id=character_id, object_id=67, quantity=0),
                Inventory(character_id=character_id, object_id=68, quantity=0),
                Inventory(character_id=character_id, object_id=69, quantity=0),
                Inventory(character_id=character_id, object_id=70, quantity=0),
                Inventory(character_id=character_id, object_id=71, quantity=0),
                Inventory(character_id=character_id, object_id=72, quantity=0),
                Inventory(character_id=character_id, object_id=73, quantity=0),
                Inventory(character_id=character_id, object_id=74, quantity=0),
                Inventory(character_id=character_id, object_id=75, quantity=0),
                Inventory(character_id=character_id, object_id=76, quantity=0),
                Inventory(character_id=character_id, object_id=77, quantity=0),
                Inventory(character_id=character_id, object_id=78, quantity=0),
                Inventory(character_id=character_id, object_id=79, quantity=0),
                Inventory(character_id=character_id, object_id=80, quantity=0),
                Inventory(character_id=character_id, object_id=81, quantity=0),
                Inventory(character_id=character_id, object_id=82, quantity=0),
                Inventory(character_id=character_id, object_id=83, quantity=0),
                Inventory(character_id=character_id, object_id=84, quantity=0),
                Inventory(character_id=character_id, object_id=85, quantity=0),
                Inventory(character_id=character_id, object_id=86, quantity=0),
                Inventory(character_id=character_id, object_id=87, quantity=0),
                Inventory(character_id=character_id, object_id=88, quantity=0),
                Inventory(character_id=character_id, object_id=89, quantity=0),
                Inventory(character_id=character_id, object_id=90, quantity=0),
                Inventory(character_id=character_id, object_id=91, quantity=0),
                Inventory(character_id=character_id, object_id=92, quantity=0),
                Inventory(character_id=character_id, object_id=93, quantity=0),
                Inventory(character_id=character_id, object_id=94, quantity=0),
                Inventory(character_id=character_id, object_id=95, quantity=0),
                Inventory(character_id=character_id, object_id=96, quantity=0),
                Inventory(character_id=character_id, object_id=97, quantity=0),
                Inventory(character_id=character_id, object_id=98, quantity=0),
                Inventory(character_id=character_id, object_id=99, quantity=0),
                Inventory(character_id=character_id, object_id=100, quantity=0),
                Inventory(character_id=character_id, object_id=101, quantity=0),
                Inventory(character_id=character_id, object_id=102, quantity=0),
                Inventory(character_id=character_id, object_id=103, quantity=0),
                Inventory(character_id=character_id, object_id=104, quantity=0),
                Inventory(character_id=character_id, object_id=105, quantity=0)
            ]
            money = Money(
                character_id=character_id,
                amount=3000,
                statement_date=today
            )
            history = History(
                character_id=character_id,
                movement=HistoryMouvment.IN.value,
                movement_date=today,
                objects='10 Poké Balls ; 2 Potions',
                link=form.presentation.data,
                link_title='Validation personnage',
            )

            cs_histories = [
                CsHistory(character_id=character_id, object_id=100, frequency="1x / semaine"),
                CsHistory(character_id=character_id, object_id=97, frequency="1x / 3 mois"),
                CsHistory(character_id=character_id, object_id=99, frequency="1x / mois"),
                CsHistory(character_id=character_id, object_id=96, frequency="1x / mois"),
                CsHistory(character_id=character_id, object_id=98, frequency="1x / mois"),
                CsHistory(character_id=character_id, object_id=101, frequency="1x / semaine"),
            ]

            flute_histories = [
                FluteHistory(character_id=character_id, object_id=91, frequency="1x / mois"),
                FluteHistory(character_id=character_id, object_id=92, frequency="1x / mois"),
            ]

            db.session.add(money)
            db.session.add_all(inventory)
            db.session.add(history)
            db.session.add_all(cs_histories)
            db.session.add_all(flute_histories)
            db.session.commit()

            flash('Personnage ajouté avec succès', 'success')
            return redirect(url_for('home'))

    return _render()


@app.route("/inventory/<int:character_id>", methods=('GET', 'POST'))
def inventory(character_id: int):
    """
    La page d'accueil de l'inventaire
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'inventory.html',
            character=character,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    return _render()


@app.route("/inventory/<int:character_id>/edit", methods=('GET', 'POST'))
def edit_inventory(character_id: int):
    """
    Le formulaire d'édition de l'inventaire
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'inventory_edit.html',
            character=character,
            form=form,
            inventory=inventory,
            ct_list=ct_list,
            new_ct_list=new_ct_list,
            assortment_list=assortment_list
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    inventory = Inventory.query.join(Object).filter(Inventory.character_id == character_id).all()
    ct_list = Ct.query.join(Object).filter(Ct.character_id == character_id).all()
    new_ct_list = Object.query.filter(Object.category == ObjectType.CT.name.lower()).all()
    assortment_list = Assortment.to_tuple()

    form = InventoryForm(formdata=request.form)
    if request.method == 'GET':
        form.movement_date.data = date.today()

    if request.method == 'POST':
        if form.add_object.data:
            object_id = int(request.form.get('objects'))

            object_form = ObjectForm()
            object_form.object_name = next(obj for obj in inventory if obj.id == object_id).object.name
            form.objects.append_entry(object_form)

            return _render()

        if form.add_ct.data:
            object_id = int(request.form.get('ct_list'))
            ct = next(ct for ct in ct_list if ct.id == object_id)
            ct_form = CtForm()
            ct_form.ct_type = ct.object.name
            ct_form.object_name = ct.name
            ct_form.reserved = ct.reserved
            form.ct_list.append_entry(ct_form)

            return _render()

        if form.add_new_ct.data:
            object_id = int(request.form.get('new_ct_list'))
            ct = next(ct for ct in new_ct_list if ct.id == object_id)
            ct_form = CtForm()
            ct_form.ct_type = ct.name
            ct_form.object_name = None
            ct_form.reserved = None
            form.new_ct_list.append_entry(ct_form)

            return _render()

        if form.add_assortment.data:
            assortment_form = AssortmentForm()
            assortment_form.assortment_name = request.form.get('assortments')
            assortment_form.quantity = 1
            form.assortment_list.append_entry(assortment_form)

            return _render()

        if form.validate():
            objects_list = form.objects.data + form.ct_list.data + form.new_ct_list.data
            assortments = form.assortment_list.data

            if not objects_list and not assortments:
                flash('Aucun objet ajouter ou supprimer !', 'danger')
                return _render()

            if form.movement.data == "out" and form.new_ct_list.data:
                flash('Impossible de supprimer une CT qui n\'appartient pas au personnage !', 'danger')
                return _render()

            if form.movement.data == "out" and assortments:
                flash('Impossible de supprimer un assortiment', 'danger')
                return _render()

            if objects_list:
                objects_history = (
                    f'{" ; ".join([str(obj["delta"]) + " " + obj["object_name"] for obj in objects_list])}'
                )
            else:
                objects_history = ''

            history = History(
                character_id=character_id,
                movement=form.movement.data,
                movement_date=form.movement_date.data.strftime(DATE_FORMAT),
                objects=None,
                link=form.link.data,
                link_title=form.link_name.data
            )

            justificatif_links = []
            for obj in form.objects.data:
                actual_object = next(inv for inv in inventory if obj['object_name'] == inv.object.name)

                if actual_object.object_id in Object.get_objects_id_with_justificatif():
                    if form.movement.data == "out":
                        flash('Impossible de supprimer un objet avec justification via cette IHM', 'danger')
                        return _render()

                    for _ in range(obj['delta']):
                        justificatif_links.append(JustificatifLink(
                            character_id=character_id,
                            object_id=actual_object.object_id,
                            link=form.link.data,
                            link_title=form.link_name.data
                        ))

                if form.movement.data == "in":
                    actual_object.quantity += obj['delta']
                if form.movement.data == "out":
                    if actual_object.quantity < obj['delta']:
                        flash(
                            f'Impossible d\'avoir un solde négatif de {actual_object.object.name} '
                            f'(possédé : {actual_object.quantity})',
                            'danger'
                        )
                        return _render()
                    actual_object.quantity -= obj['delta']

            for obj in form.ct_list.data:
                actual_object = next(ct for ct in ct_list if obj['ct_type'] == ct.object.name)
                actual_object.reserved = obj['reserved']
                if form.movement.data == "in":
                    actual_object.quantity += obj['delta']
                if form.movement.data == "out":
                    if actual_object.quantity < obj['delta']:
                        flash(
                            f'Impossible d\'avoir un solde négatif de {actual_object.object.name} '
                            f'(possédé : {actual_object.quantity})',
                            'danger'
                        )
                        return _render()
                    actual_object.quantity -= obj['delta']

            new_ct = []
            for obj in form.new_ct_list.data:
                if form.movement.data == "out":
                    flash('Impossible de supprimer de nouvelles CT', 'danger')
                    return _render()
                ct_type = next(ct for ct in new_ct_list if obj['ct_type'] == ct.name)
                new_ct.append(Ct(
                    character_id=character_id,
                    object_id=ct_type.id,
                    name=obj['object_name'],
                    quantity=obj['delta'],
                    reserved=obj['reserved']
                ))

            for assortment in assortments:
                if objects_history != '':
                    objects_history += ' ; '

                objects_history += (
                    f"{assortment['quantity']} Assortiment {assortment['assortment_name']}"
                    f" <span class='help'>("
                )

                for object in Assortment.get_from_value(assortment['assortment_name']).value[0]:
                    actual_object = next(inv for inv in inventory if object[1] == inv.object.id)
                    actual_object.quantity += assortment['quantity'] * object[0]

                    objects_history += f"{assortment['quantity'] * object[0]} {actual_object.object.name} ; "

                objects_history = objects_history[:-3]
                objects_history += ')</span>'

            history.objects = objects_history
            db.session.bulk_save_objects(justificatif_links)
            db.session.add(history)
            db.session.bulk_save_objects(new_ct)
            db.session.commit()

            flash(f'Inventaire de {character.firstname} modifié avec succès', 'success')
            generate_tcard_part(character.id, 'inventaire')
            return redirect(url_for('inventory', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/inventory/<int:character_id>/moneyHmAndFlute", methods=('GET', 'POST'))
def edit_money_hm_flute(character_id: int):
    """
    Formulaire d'édition de l'argent et de l'utilisation des CS / flûtes
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'money_hm_flute_edit.html',
            character=character,
            money_form=money_form,
            cs_history_form=cs_history_form,
            flute_history_form=flute_history_form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    money = Money.query.filter(Money.character_id == character_id).first()
    money.statement_date = datetime.strptime(money.statement_date, DATE_FORMAT)

    cs_history = CsHistory.query.filter(CsHistory.character_id == character_id).join(Object).all()
    flute_history = FluteHistory.query.filter(FluteHistory.character_id == character_id).join(Object).all()
    for cs in cs_history:
        if cs.last_used:
            cs.last_used = datetime.strptime(cs.last_used, DATE_FORMAT)
    for flute in flute_history:
        if flute.last_used:
            flute.last_used = datetime.strptime(flute.last_used, DATE_FORMAT)

    money_form = MoneyForm(formdata=request.form, obj=money)
    cs_history_form = CsHistoryForm(formdata=request.form, cs_history=cs_history)
    flute_history_form = FluteHistoryForm(formdata=request.form, flute_history=flute_history)

    if request.method == 'POST':
        if money_form.validate() and cs_history_form.validate() and flute_history_form.validate():

            money_form.populate_obj(money)
            money.statement_date = money.statement_date.strftime(DATE_FORMAT)
            modify_cs_flute_data(cs_history_form.cs_history, cs_history)
            modify_cs_flute_data(flute_history_form.flute_history, flute_history)

            db.session.commit()

            generate_tcard_part(character.id, 'inventaire')
            return redirect(url_for('inventory', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/inventory/<int:character_id>/passAlmia", methods=('GET', 'POST'))
def edit_pass_almia(character_id: int):
    """
    Utilisation d'un passe Almia
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pass_almia_edit.html',
            character=character,
            links=links,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    links = JustificatifLink.query.filter(JustificatifLink.character_id == character_id).all()

    if not links:
        form = JustificatifLinkForm()
        return _render()

    form = JustificatifLinkForm(formdata=request.form, justificatif_links=links)

    for justif_link in form.justificatif_links:
        for link in links:
            if justif_link.form.id.data == link.id:
                justif_link.object_name.data = link.object.name
                break

    if request.method == 'POST':
        if form.validate():
            used_id = set()
            removed_link = None
            for link in form.justificatif_links:
                if link.removed_link.data:
                    used_id.add(link.form.id.data)
                    removed_link = link.removed_link.data

            if not used_id:
                return _render()

            JustificatifLink.query.filter(JustificatifLink.id.in_(used_id)).delete()
            pass_almia = Inventory.query.filter(
                Inventory.character_id == character_id,
                Inventory.object_id.in_(Object.get_objects_id_with_justificatif())
            ).first()

            pass_almia.quantity -= len(used_id)

            history = History(
                character_id=character_id,
                movement=HistoryMouvment.OUT.value,
                movement_date=date.today().strftime(DATE_FORMAT),
                objects=f'{len(used_id)} {pass_almia.object.name}',
                link=removed_link,
                link_title='Utilisation Almia'
            )

            db.session.add(history)
            db.session.commit()

            generate_tcard_part(character.id, 'inventaire')
            return redirect(url_for('inventory', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/inventory/<int:character_id>/ctReservation", methods=('GET', 'POST'))
def edit_ct_reservation(character_id: int):
    """
    Formulaire de réservation des CT
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'ct_reservation_edit.html',
            character=character,
            form=form,
            cts=cts,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    cts = Ct.query.filter(Ct.character_id == character_id).all()

    if not cts:
        form = CtReservationListForm()
        return _render()

    form = CtReservationListForm(formdata=request.form, ct_reservations=cts)

    if request.method == 'POST':
        if form.validate():
            for ct in cts:
                for ct_reservation in form.ct_reservations:
                    if ct_reservation.form.id.data == ct.id:
                        ct.reserved = ct_reservation.reserved.data
                        break
            db.session.commit()

            generate_tcard_part(character.id, 'inventaire')
            return redirect(url_for('inventory', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/inventory/<int:character_id>/exchange", methods=('GET', 'POST'))
def object_exchange(character_id: int):
    """
    Formulaire d'échange d'objets
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'object_exchange.html',
            character=character,
            form=form,
            inventory=inventory,
            ct_list=ct_list,
            new_ct_list=new_ct_list,
            objects_list=objects_list,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    inventory = (
        Inventory
        .query
        .join(Object)
        .filter(
            Inventory.character_id == character_id,
            Inventory.quantity > 0,
            Object.id.not_in(Object.get_objects_id_no_exchangeable().union(Object.get_objects_id_with_justificatif()))
        )
        .all()
    )
    objects_list = (
        Inventory
        .query
        .join(Object)
        .filter(Inventory.character_id == character_id, Object.id.not_in(Object.get_objects_id_no_exchangeable()))
        .all()
    )
    ct_list = Ct.query.join(Object).filter(Ct.character_id == character_id, Ct.quantity > 0).all()

    new_ct_list = Object.query.filter(Object.category == ObjectType.CT.name.lower()).all()

    form = InventoryExchangeForm(formdata=request.form)

    if request.method == 'GET':
        form.exchange_date.data = date.today()

    if request.method == 'POST':
        if form.add_object_out.data:
            object_id = int(request.form.get('objects_out'))
            object_form = ObjectForm()
            object_form.object_name = next(obj for obj in inventory if obj.id == object_id).object.name
            form.objects_out.append_entry(object_form)
            return _render()

        if form.add_ct_out.data:
            object_id = int(request.form.get('ct_out'))
            ct = next(ct for ct in ct_list if ct.id == object_id)
            ct_form = CtForm()
            ct_form.ct_type = ct.object.name
            ct_form.object_name = ct.name
            form.ct_out.append_entry(ct_form)

            return _render()

        if form.add_object_in.data:
            object_id = int(request.form.get('objects_in'))
            object_form = ObjectForm()
            object_form.object_name = next(obj for obj in objects_list if obj.id == object_id).object.name
            form.objects_in.append_entry(object_form)

            return _render()

        if form.add_ct_in.data:
            object_id = int(request.form.get('ct_in'))
            ct = next(ct for ct in ct_list if ct.id == object_id)
            ct_form = CtForm()
            ct_form.ct_type = ct.object.name
            ct_form.object_name = ct.name
            ct_form.reserved = ct.reserved
            form.ct_in.append_entry(ct_form)

            return _render()

        if form.add_new_ct_in.data:
            object_id = int(request.form.get('new_ct_in'))
            ct = next(ct for ct in new_ct_list if ct.id == object_id)
            ct_form = CtForm()
            ct_form.ct_type = ct.name
            ct_form.object_name = None
            ct_form.reserved = None
            form.new_ct_in.append_entry(ct_form)

            return _render()

        if form.validate():
            objects_in = form.objects_in.data + form.ct_in.data + form.new_ct_in.data
            objects_out = form.objects_out.data + form.ct_out.data

            if not objects_in or not objects_out:
                flash('Aucun objet à échanger !', 'danger')
                return _render()

            objects_in_history = f'{" ; ".join([str(obj["delta"]) + " " + obj["object_name"] for obj in objects_in])}'
            objects_out_history = f'{" ; ".join([str(obj["delta"]) + " " + obj["object_name"] for obj in objects_out])}'

            history = History(
                character_id=character_id,
                movement=HistoryMouvment.EXCHANGE.value,
                movement_date=form.exchange_date.data.strftime(DATE_FORMAT),
                objects_in_exchange=objects_in_history,
                objects_out_exchange=objects_out_history,
                link=form.link.data,
                link_title=form.link_name.data
            )

            justificatif_links = []
            for obj in form.objects_out.data:
                actual_object = next(inv for inv in inventory if obj['object_name'] == inv.object.name)

                if actual_object.quantity < obj['delta']:
                    flash(
                        f'Impossible d\'avoir un solde négatif de {actual_object.object.name} '
                        f'(possédé : {actual_object.quantity})',
                        'danger'
                    )
                    return _render()
                actual_object.quantity -= obj['delta']

            for obj in form.ct_out.data:
                actual_object = next(ct for ct in ct_list if obj['ct_type'] == ct.object.name)
                actual_object.reserved = obj['reserved']

                if actual_object.quantity < obj['delta']:
                    flash(
                        f'Impossible d\'avoir un solde négatif de '
                        f'{actual_object.object.name} (possédé : {actual_object.quantity})',
                        'danger'
                    )
                    return _render()
                actual_object.quantity -= obj['delta']

            for obj in form.objects_in.data:
                actual_object = next(inv for inv in objects_list if obj['object_name'] == inv.object.name)

                if actual_object.object_id in Object.get_objects_id_with_justificatif():
                    for _ in range(obj['delta']):
                        justificatif_links.append(JustificatifLink(
                            character_id=character_id,
                            object_id=actual_object.object_id,
                            link=form.link.data,
                            link_title=form.link_name.data
                        ))

                actual_object.quantity += obj['delta']

            for obj in form.ct_in.data:
                actual_object = next(ct for ct in ct_list if obj['ct_type'] == ct.object.name)
                actual_object.reserved = obj['reserved']
                actual_object.quantity += obj['delta']

            new_ct = []
            for obj in form.new_ct_in.data:
                ct_type = next(ct for ct in new_ct_list if obj['ct_type'] == ct.name)
                new_ct.append(Ct(
                    character_id=character_id,
                    object_id=ct_type.id,
                    name=obj['object_name'],
                    quantity=obj['delta'],
                    reserved=obj['reserved']
                ))

            db.session.bulk_save_objects(justificatif_links)
            db.session.add(history)
            db.session.bulk_save_objects(new_ct)
            db.session.commit()

            flash(f'Inventaire de {character.firstname} modifié avec succès', 'success')
            generate_tcard_part(character.id, 'inventaire')
            return redirect(url_for('inventory', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/social/<int:character_id>", methods=('GET', 'POST'))
def social_relation(character_id: int):
    """
    Affichage des relations
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'social.html',
            character=character,
            socials=socials
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    socials = Social.query.filter(Social.character_id == character_id).all()
    return _render()


@app.route("/social/<int:character_id>/new", methods=('GET', 'POST'))
def new_social_relation(character_id: int):
    """
    Formulaire d'ajout d'une nouvelle connaissance
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'social_edit.html',
            character=character,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    form = SocialForm(formdata=request.form)

    if request.method == 'POST':
        if form.add_subject.data:
            form.subjects.append_entry(None)
            return _render()

        if form.add_pokemon.data:
            form.pokemon.append_entry(None)
            return _render()

        if form.validate():

            social = Social(
                character_id=character_id,
                full_name=form.full_name.data,
                bond=form.bond.data,
                description=form.description.data,
                pj=form.pj.data,
                hexa_text=form.hexa_text.data,
            )

            db.session.add(social)
            db.session.commit()
            db.session.refresh(social)

            pokemon = []
            subjects = []

            for pkmn in form.pokemon:
                if pkmn.data['pokemon'] != '' and pkmn.data['pokemon_name'] != '':
                    pokemon.append(SocialPokemon(social_id=social.id, **pkmn.data))

            for subject in form.subjects:
                if subject.data['id'] is None:
                    if subject.data['link'] != '':
                        subjects.append(SocialSubject(social_id=social.id, link=subject.data['link']))

            db.session.bulk_save_objects(pokemon)
            db.session.bulk_save_objects(subjects)
            db.session.commit()

            generate_tcard_part(character.id, 'connaissances')
            flash(f'{social.full_name} correctement crée', 'success')
            return redirect(url_for('social_relation', character_id=character_id))
        else:
            for error in form.errors:
                flash(f'Erreur : {error} {form.errors[error]}', 'danger')

    return _render()


@app.route("/social/<int:character_id>/edit/<int:social_id>", methods=('GET', 'POST'))
def edit_social_relation(character_id: int, social_id: int):
    """
    Edition d'une connaissance
    :param character_id: l'id du personnage
    :param social_id: id de la connaissance
    :return: le template
    """
    def _render():
        return render_template(
            'social_edit.html',
            character=character,
            form=form,
            social=social,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    social = Social.query.filter(Social.id == social_id).one_or_404()

    if character_id != social.character_id:
        flash(f'Erreur lors de la récupération de la relation {social_id}', 'danger')
        return redirect(url_for('home'))

    form = SocialForm(formdata=request.form, obj=social)

    if request.method == 'POST':
        if form.add_subject.data:
            form.subjects.append_entry(None)
            return _render()

        if form.add_pokemon.data:
            form.pokemon.append_entry(None)
            return _render()

        if form.validate():
            pokemon = []
            subjects = []

            social.bond = form.bond.data
            social.description = form.description.data
            social.pj = form.pj.data
            social.hexa_text = form.hexa_text.data

            for pkmn in form.pokemon:
                if pkmn.data['id'] is None:
                    if pkmn.data['pokemon'] != '' and pkmn.data['pokemon_name'] != '':
                        pokemon.append(SocialPokemon(social_id=social_id, **pkmn.data))
                else:
                    for social_pokemon in social.pokemon:
                        if pkmn.data['id'] == social_pokemon.id:
                            social_pokemon.pokemon = pkmn.data['pokemon']
                            social_pokemon.pokemon_name = pkmn.data['pokemon_name']

            for subject in form.subjects:
                if subject.data['id'] is None:
                    if subject.data['link'] != '':
                        subjects.append(SocialSubject(social_id=social_id, link=subject.data['link']))
                else:
                    for social_subject in social.subjects:
                        if subject.data['id'] == social_subject.id:
                            social_subject.link = subject.data['link']

            db.session.bulk_save_objects(pokemon)
            db.session.bulk_save_objects(subjects)
            db.session.commit()

            generate_tcard_part(character.id, 'connaissances')
            flash(f'{social.full_name} correctement modifié', 'success')
            return redirect(url_for('social_relation', character_id=character_id))
        else:
            for error in form.errors:
                flash(f'Erreur : {error} {form.errors[error]}', 'danger')

    return _render()


@app.route("/gallery/<int:character_id>", methods=('GET', 'POST'))
def gallery(character_id: int):
    """
    Page pour générer la gallery
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'gallery.html',
            character=character,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    if request.method == 'POST':
        generate_tcard_part(character.id, 'ressources')

    return _render()


@app.route("/pokemon/<int:character_id>", methods=['GET'])
def pokemon(character_id: int):
    """
    Affichage des Pokémon
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon.html',
            character=character,
            pokemon=pokemon,
            session=db.session
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = (
        PokemonOwned
        .query
        .join(PokemonSpecies)
        .join(PokemonCategory)
        .filter(PokemonOwned.character_id == character.id)
        .all()
    )

    for pok in pokemon:
        pok.can_evol = can_evol(pok, character_id, db.session)
        pok.no_evol_attack = get_non_evol_attack(pok, db.session)

    return _render()


@app.route("/pokemon/<int:character_id>/pokemon/<int:pokemon_id>/one_xp_point", methods=['POST'])
def pokemon_add_one_xp(character_id: int, pokemon_id: int):
    """
    Ajoute un point d'expérience à un Pokémon
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template de la liste des Pokémon
    """
    MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    level_up_pokemon(pokemon, 0, 1, db.session)
    db.session.commit()

    return redirect(url_for('pokemon', character_id=character_id))


@app.route("/pokemon/<int:character_id>/pokemon/<int:pokemon_id>/experience", methods=['GET', 'POST'])
def pokemon_add_xp(character_id: int, pokemon_id: int):
    """
    Formulaire d'ajout de plusieurs niveaux ou point d'expérience
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_xp.html',
            character=character,
            pokemon=pokemon,
            form=form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()
    form = PokemonXpForm(formdata=request.form)

    if request.method == 'POST':
        if form.validate():
            if form.level.data and form.point.data:
                flash('Impossible d\'ajouter un niveau et des points d\'expérience en même temps', 'danger')
                return redirect(url_for('pokemon', character_id=character_id))

            level = form.level.data if form.level.data else 0
            point = form.point.data if form.point.data else 0

            level_up_pokemon(pokemon, level, point, db.session)
            db.session.commit()

            flash('Expérience ajoutée avec succès', 'success')
            return redirect(url_for('pokemon', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/pokemon/<int:character_id>/new_species", methods=('GET', 'POST'))
def new_species(character_id: int):
    """
    Formulaire d'un nouvelle espèce de Pokémon
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'species_new.html',
            form=form,
            character=character,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    form = PokemonSpeciesForm(formdata=request.form)
    form.evolution_id.choices = [(0, '')] + [(species.id, species.species) for species in PokemonSpecies.query.all()]
    form.evolution_way.choices = EvolutionWay.to_tuple_int_with_empty()

    if request.method == 'POST' and form.validate():
        if form.evolution_id.data:
            if form.evolution_way.data == 0:
                flash('Une évolution doit avoir un moyen d\'évolution', 'danger')
                return _render()

            level_is_invalid = not form.evolution_level.data or int(form.evolution_level.data) <= 0
            if form.evolution_way.data == EvolutionWay.LEVEL.get_id() and level_is_invalid:
                flash('Une évolution par niveau doit avoir un niveau d\'évolution', 'danger')
                return _render()

            if form.evolution_way.data != EvolutionWay.LEVEL.get_id():
                form.evolution_level.data = None
        else:
            form.evolution_way.data = None
            form.evolution_level.data = None

        pokemon = PokemonSpecies()
        form.populate_obj(pokemon)

        try:
            db.session.add(pokemon)
            db.session.commit()
            db.session.refresh(pokemon)
            flash(f'{pokemon.species} créé avec succès', 'success')
            return redirect(url_for('pokemon', character_id=character_id))
        except Exception as exception:
            flash(f'Une erreur est arrivée lors de l\'enregistrement : {exception}', 'danger')
            return _render()

    return _render()


@app.route("/pokemon/<int:character_id>/new_attacks", methods=('GET', 'POST'))
def new_attacks(character_id: int):
    """
    Formulaire d'ajout d'attaques
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'attacks_new.html',
            form=form,
            character=character,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    form = PokemonAttacksForm(formdata=request.form)

    if request.method == 'POST':
        if form.add_attack.data:
            attack = PokemonAttackForm()
            attack.name = None
            attack.informations = None
            attack.boost = None
            attack.useless = False
            attack.critique_attack = False
            form.attacks.append_entry(attack)
            return _render()

        if form.validate():
            attacks = []
            for attack in form.attacks:
                atk = PokemonAttacks(
                    name=attack.data['name'],
                    type_id=attack.data['type_id'],
                    informations=attack.data['informations'],
                    power=attack.data['power'],
                    precision=attack.data['precision'],
                    useless=attack.data['useless'],
                    burn_percentage=attack.data['burn_percentage'],
                    freeze_percentage=attack.data['freeze_percentage'],
                    paralyse_percentage=attack.data['paralyse_percentage'],
                    scare_percentage=attack.data['scare_percentage'],
                    poison_percentage=attack.data['poison_percentage'],
                    sleep_percentage=attack.data['sleep_percentage'],
                    boost=attack.data['boost'],
                    critique_attack=attack.data['critique_attack']
                )
                attacks.append(atk)

            db.session.bulk_save_objects(attacks)
            db.session.commit()
            flash(f'{len(attacks)} attaque(s) ajoutée(s) avec succès', 'success')
            return redirect(url_for('pokemon', character_id=character_id))

    attack = PokemonAttackForm()
    attack.name = None
    attack.informations = None
    attack.boost = None
    attack.useless = False
    attack.critique_attack = False
    form.attacks.append_entry(attack)

    return _render()


@app.route("/pokemon/<int:character_id>/new", methods=('GET', 'POST'))
def new_pokemon(character_id: int):
    """
    Formulaire de nouveau Pokémon pour un personnage
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_new.html',
            character=character,
            form=form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    form = PokemonOwnedForm(formdata=request.form)
    species_options = [(species.id, species.species) for species in PokemonSpecies.query.all()]
    categories_options = [
        (category.id, category.name)
        for category
        in PokemonCategory.query.filter(PokemonCategory.character_id.in_([character_id, 0]))
        .all()
    ]
    form.species_id.choices = species_options
    form.category_id.choices = categories_options

    if request.method == 'POST' and form.validate():
        pokemon_owned = PokemonOwned(character_id=character_id)
        form.populate_obj(pokemon_owned)
        if pokemon_owned.egg:
            pokemon_owned.level = 15
        pokemon_owned.exp_point_per_level = get_xp_per_level(pokemon_owned.level)
        db.session.add(pokemon_owned)
        db.session.commit()

        db.session.refresh(pokemon_owned)

        learn_auto_attacks(pokemon_owned, db.session)

        generate_tcard_part(character.id, 'stockage')
        generate_tcard_part(character.id, 'pokemon')

        flash(f'{pokemon_owned.name} ajoutée avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/edit/<int:pokemon_id>", methods=('GET', 'POST'))
def edit_pokemon(character_id: int, pokemon_id: int):
    """
    Formulaire d'édition d'un Pokémon
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_edit.html',
            character=character,
            pokemon=pokemon,
            form=form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    form = PokemonOwnedForm(formdata=request.form, obj=pokemon)

    if request.method == 'GET':
        form.shiny.data = pokemon.shiny

    species_options = [(species.id, species.species) for species in PokemonSpecies.query.all()]
    categories_options = [
        (category.id, category.name)
        for category
        in PokemonCategory.query.filter(PokemonCategory.character_id == character_id).all()
    ]
    form.species_id.choices = species_options
    form.category_id.choices = categories_options

    if request.method == 'POST' and form.validate():
        pokemon.name = form.name.data
        pokemon.sex = form.sex.data
        pokemon.shiny = form.shiny.data
        pokemon.obtention_link = form.obtention_link.data
        pokemon.obtention_name = form.obtention_name.data
        pokemon.nature = form.nature.data
        pokemon.sprite_credits = form.sprite_credits.data
        pokemon.category_id = form.category_id.data
        pokemon.background = form.background.data
        pokemon.banner_credit = form.banner_credit.data
        db.session.commit()

        generate_tcard_part(character.id, 'stockage')
        generate_tcard_part(character.id, 'pokemon')

        flash(f'{pokemon.name} modifié avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/give", methods=('GET', 'POST'))
def give_pokemon(character_id: int):
    """
    Formulaire de don d'un Pokémon
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_give.html',
            character=character,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    form = GivePokemonForm(formdata=request.form)
    pokemon_options = [
        (pokemon.id, pokemon.name)
        for pokemon
        in PokemonOwned.query.filter(PokemonOwned.character_id == character_id).all()
    ]
    form.pokemon_id.choices = pokemon_options

    if request.method == 'POST' and form.validate():
        pokemon = PokemonOwned.query.filter(
            PokemonOwned.character_id == character_id,
            PokemonOwned.id == form.pokemon_id.data
        ).one_or_404()

        give_pkmn(character_id, form, db.session)
        db.session.commit()

        generate_tcard_part(character.id, 'inventaire')
        generate_tcard_part(character.id, 'stockage')
        generate_tcard_part(character.id, 'pokemon')

        flash(f'{pokemon.name} donné avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/exchange", methods=('GET', 'POST'))
def exchange_pokemon(character_id: int):
    """
    Formulaire d'échange de Pokémon
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_exchange.html',
            character=character,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    form = ExchangePokemonForm(formdata=request.form)
    pokemon_options = [
        (pokemon.id, pokemon.name)
        for pokemon
        in PokemonOwned.query.filter(PokemonOwned.character_id == character_id).all()
    ]
    form.pokemon_ids.choices = pokemon_options

    species = [(species.id, species.species) for species in PokemonSpecies.query.all()]
    categories = [(category.id, category.name) for category in PokemonCategory.query.all()]

    for pokemon_form in form.new_pokemon:
        pokemon_form.species_id.choices = species
        pokemon_form.category_id.choices = categories

    if request.method == 'POST':

        if form.add_new_pokemon.data:
            new_pokemon_form = ExchangePokemonNewForm()
            new_pokemon_form.name = None
            new_pokemon_form.level = 0
            new_pokemon_form.shiny = False
            new_pokemon_form.hp_up = 0
            new_pokemon_form.zinc = 0
            new_pokemon_form.calcium = 0
            new_pokemon_form.carbos = 0
            new_pokemon_form.iron = 0
            new_pokemon_form.protein = 0
            new_pokemon_form.nature = None
            new_pokemon_form.sprite_credits = None
            new_pokemon_form.banner_credit = None
            new_pokemon_form.egg = False

            form.new_pokemon.append_entry(new_pokemon_form)

            for pokemon_form in form.new_pokemon:
                pokemon_form.species_id.choices = species
                pokemon_form.category_id.choices = categories

            return _render()

        if form.validate():
            exchange_pkmn(character_id, form, db.session)
            db.session.commit()

            generate_tcard_part(character.id, 'inventaire')
            generate_tcard_part(character.id, 'stockage')
            generate_tcard_part(character.id, 'pokemon')

            flash('Echange réalisé avec succès', 'success')
            return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/pokemon_hatching/<int:pokemon_id>", methods=['POST'])
def pokemon_hatching(character_id: int, pokemon_id: int):
    """
    Fait éclore un oeuf
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template de la liste des Pokémon
    """
    MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    pokemon.egg = False
    db.session.commit()

    generate_tcard_part(character_id, 'stockage')
    generate_tcard_part(character_id, 'pokemon')

    flash(f'{pokemon.name} a éclos avec succès', 'success')
    return redirect(url_for('pokemon', character_id=character_id))


@app.route("/pokemon/<int:character_id>/evolution/<int:pokemon_id>", methods=['POST', 'GET'])
def pokemon_evolution(character_id: int, pokemon_id: int):
    """
    Fait évoluer un Pokémon
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template si évolution par pierre, la liste des Pokémon si autres méthodes d'évolution
    """
    def _render():
        return render_template(
            'pokemon_evolution.html',
            character=character,
            pokemon=pokemon,
            evolution_way=evolution_way.value[1],
            form=form
        )
    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    evolution_way = EvolutionWay.get_from_value(pokemon.species.evolution_way)

    if evolution_way in {EvolutionWay.EXCHANGE, EvolutionWay.LEVEL}:
        evol_pokemon(pokemon, character_id, db.session)

        flash(f'{pokemon.name} a évolué en {pokemon.species.species} avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    form = PokemonEvolutionForm(formdata=request.form)

    if request.method == 'POST' and form.validate():
        evol_pokemon(pokemon, character_id, db.session, form.link.data)

        generate_tcard_part(character_id, 'stockage')
        generate_tcard_part(character_id, 'pokemon')

        flash(f'{pokemon.name} a évolué en {pokemon.species.species} avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/learn_attack/<int:pokemon_id>", methods=['POST', 'GET'])
def pokemon_learn_attack(character_id: int, pokemon_id: int):
    """
    Formulaire pour apprendre des attaques à un Pokémon
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_learn_attack.html',
            character=character,
            pokemon=pokemon,
            form=form
        )
    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    form = LearnAttacksForm(formdata=request.form)

    if request.method == 'GET':
        known_attacks = PokemonOwnedAttacks.get_attacks(pokemon.id, db.session)
        known_attacks_id = {known_attack.species_attack_id for known_attack in known_attacks}

        attacks = (
            PokemonSpeciesAttacks
            .query
            .filter(PokemonSpeciesAttacks.species_id == pokemon.species_id)
            .filter(
                PokemonSpeciesAttacks.ct
                | PokemonSpeciesAttacks.cs
                | PokemonSpeciesAttacks.gm
                | PokemonSpeciesAttacks.cm
            )
            .filter(~PokemonSpeciesAttacks.id.in_(known_attacks_id))
            .all()
        )

        for attack in attacks:
            atk = LearnAttackForm()
            atk.attack_id = attack.id
            atk.learned = False

            attack_name = (
                f'{attack.attack.name} '
                f'({"CT" if attack.ct else "CS" if attack.cs else "GM" if attack.gm else "CM"})'
            )
            atk.attack_name = attack_name

            form.attacks.append_entry(atk)

        form.attacks = sorted(form.attacks, key=lambda x: x.attack_name.data)
        return _render()

    if form.validate():
        new_attacks = []

        for attack in form.attacks:
            if not attack.data['learned']:
                continue

            attack_id = attack.data['attack_id']

            new_attacks.append(PokemonOwnedAttacks(
                pokemon_owned_id=pokemon_id,
                species_attack_id=attack_id
            ))

        db.session.add_all(new_attacks)
        db.session.commit()

        generate_tcard_part(character_id, 'stockage')
        generate_tcard_part(character_id, 'pokemon')

        flash(f'{len(new_attacks)} attaque(s) apprise(s) avec succès à {pokemon.name}', 'success')

        return redirect(url_for('pokemon', character_id=character_id))

    flash(f'{form.errors}', 'danger')
    return _render()


@app.route("/pokemon/<int:character_id>/to_pension/<int:pokemon_id>", methods=['POST', 'GET'])
def pokemon_to_pension(character_id: int, pokemon_id: int):
    """
    Formulaire pour placer un Pokémon en pension
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_to_pension.html',
            character=character,
            pokemon=pokemon,
            form=form
        )
    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    form = ToPensionForm(formdata=request.form)

    if request.method == 'POST' and form.validate():
        pokemon.pension = form.pension_name.data

        db.session.add(pokemon)
        db.session.commit()

        generate_tcard_part(character_id, 'stockage')
        generate_tcard_part(character_id, 'pokemon')

        flash(f'{pokemon.name} placé dans la pension de {form.pension_name.data} avec succès', 'success')

        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/leave_pension/<int:pokemon_id>", methods=['POST', 'GET'])
def pokemon_leave_pension(character_id: int, pokemon_id: int):
    """
    Formulaire pour sortir un Pokémon de pension
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_leave_pension.html',
            character=character,
            pokemon=pokemon,
            form=form
        )
    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    form = LeavePensionForm(formdata=request.form)

    if request.method == 'POST' and form.validate():
        leave_pension(pokemon, form, db.session)

        generate_tcard_part(character_id, 'stockage')
        generate_tcard_part(character_id, 'pokemon')

        flash(f'{pokemon.name} récupéré de pension avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/edit_stats/<int:pokemon_id>", methods=('GET', 'POST'))
def pokemon_edit_stats(character_id: int, pokemon_id: int):
    """
    Formulaire d'édition de stats
    :param character_id: l'id du personnage
    :param pokemon_id: l'id du Pokémon
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_stats.html',
            character=character,
            pokemon=pokemon,
            form=form
        )

    def _update_validators_range(validators, unit_used, vita_used):
        for validator in validators:
            if isinstance(validator, NumberRange):
                validator.min = unit_used
                validator.field_flags["min"] = unit_used
                validator.max = 10 - vita_used + unit_used
                validator.field_flags["max"] = 10 - vita_used + unit_used

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    pokemon = PokemonOwned.query.filter(
        PokemonOwned.character_id == character_id, PokemonOwned.id == pokemon_id
    ).one_or_404()

    form = PokemonStatsForm(formdata=request.form)

    if request.method == 'GET':
        form.pv.data = pokemon.pv
        form.hp_up.data = pokemon.hp_up
        form.atk.data = pokemon.atk
        form.protein.data = pokemon.protein
        form.defense.data = pokemon.defense
        form.iron.data = pokemon.iron
        form.atk_spe.data = pokemon.atk_special
        form.calcium.data = pokemon.calcium
        form.defense_spe.data = pokemon.def_special
        form.zinc.data = pokemon.zinc
        form.speed.data = pokemon.speed
        form.carbos.data = pokemon.carbos

    vita_used = pokemon.hp_up + pokemon.protein + pokemon.iron + pokemon.calcium + pokemon.zinc + pokemon.carbos
    _update_validators_range(form.hp_up.validators, pokemon.hp_up, vita_used)
    _update_validators_range(form.protein.validators, pokemon.protein, vita_used)
    _update_validators_range(form.iron.validators, pokemon.iron, vita_used)
    _update_validators_range(form.calcium.validators, pokemon.calcium, vita_used)
    _update_validators_range(form.zinc.validators, pokemon.zinc, vita_used)
    _update_validators_range(form.carbos.validators, pokemon.carbos, vita_used)

    if request.method == 'POST' and form.validate():
        pokemon.pv = form.pv.data
        pokemon.atk = form.atk.data
        pokemon.atk_special = form.atk_spe.data
        pokemon.defense = form.defense.data
        pokemon.def_special = form.defense_spe.data
        pokemon.speed = form.speed.data
        pokemon.hp_up = form.hp_up.data
        pokemon.zinc = form.zinc.data
        pokemon.calcium = form.calcium.data
        pokemon.carbos = form.carbos.data
        pokemon.iron = form.iron.data
        pokemon.protein = form.protein.data

        db.session.add(pokemon)
        db.session.commit()

        generate_tcard_part(character_id, 'stockage')
        generate_tcard_part(character_id, 'pokemon')

        flash(f'Stats de {pokemon.name} modifiées avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/categories", methods=('GET', 'POST'))
def pokemon_category(character_id: int):
    """
    Gestion des catégories
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'pokemon_category.html',
            character=character,
            categories=categories,
            category_form=category_form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    categories = PokemonCategory.query.all()
    category_form = PokemonCategoryForm(formdata=request.form)

    for category in categories:
        if PokemonOwned.query.filter(PokemonOwned.category_id == category.id).first():
            category.used = True

    if request.method == 'POST' and category_form.validate():
        category = PokemonCategory(
            character_id=character_id,
            name=category_form.name.data
        )
        db.session.add(category)
        db.session.commit()

        flash(f'Catégorie de Pokémon "{category.name}" ajoutée avec succès', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/pokemon/<int:character_id>/categories/<int:category_id>", methods=['DELETE'])
def pokemon_category_delete(character_id: int, category_id: int):
    """
    Suppression d'une catégorie
    :param character_id: l'id du personnage
    :param category_id: l'id de la catégorie
    :return: template de la liste des catégories
    """
    MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    category = PokemonCategory.query.filter(PokemonCategory.id == category_id).one_or_404()

    if PokemonOwned.query.filter(PokemonOwned.category_id == category.id).first():
        flash(f'Catégorie "{category.name}" utilisée. Impossible de la supprimer', 'danger')
        return redirect(url_for('pokemon_category', character_id=character_id))

    db.session.delete(category)
    db.session.commit()
    flash(f'Catégorie "{category.name}" supprimée avec succès', 'success')
    return redirect(url_for('pokemon_category', character_id=character_id))


@app.route("/pokemon/<int:character_id>/link_species_attacks", methods=('GET', 'POST'))
def link_species_attacks(character_id: int):
    """
    Formulaire d'ajout des attaques à une espèce de Pokémon
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'link_species_attacks.html',
            character=character,
            form=form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    form = PokemonSpeciesAttacksForm(formdata=request.form)
    form.species_id.choices = [(species.id, species.species) for species in PokemonSpecies.query.all()]

    if request.method == 'GET':
        attacks = PokemonAttacks.query.all()

        for attack in attacks:
            atk = PokemonSpeciesAttackForm()
            atk.attack_id = attack.id
            atk.learned = False
            atk.attack_name = attack.name
            atk.level = None
            atk.ct = False
            atk.cs = False
            atk.gm = False
            atk.cm = False

            form.attacks.append_entry(atk)

    if request.method == 'POST' and form.validate():
        species_id = form.species_id.data

        species_attacks = []
        for attack in form.attacks:
            if not attack.data['learned']:
                continue

            if (
                    attack.data['learned']
                    and not (attack.data['level'] and attack.data['level'] > 0)
                    and not attack.data['ct']
                    and not attack.data['cs']
                    and not attack.data['gm']
                    and not attack.data['cm']
            ):
                flash(f'Attaque {attack.data["attack_name"]} sans méthode d\'apprentissage', 'danger')
                return _render()

            attack_id = attack.data['attack_id']

            if attack.data['level'] and attack.data['level'] > 0:
                species_attack = PokemonSpeciesAttacks(
                    species_id=species_id,
                    attack_id=attack_id,
                    level=attack.data['level'],
                    ct=False,
                    cs=False,
                    gm=False,
                    cm=False
                )
                species_attacks.append(species_attack)

            if attack.data['ct']:
                species_attack = PokemonSpeciesAttacks(
                    species_id=species_id,
                    attack_id=attack_id,
                    level=None,
                    ct=True,
                    cs=False,
                    gm=False,
                    cm=False
                )
                species_attacks.append(species_attack)

            if attack.data['cs']:
                species_attack = PokemonSpeciesAttacks(
                    species_id=species_id,
                    attack_id=attack_id,
                    level=None,
                    ct=False,
                    cs=True,
                    gm=False,
                    cm=False
                )
                species_attacks.append(species_attack)

            if attack.data['gm']:
                species_attack = PokemonSpeciesAttacks(
                    species_id=species_id,
                    attack_id=attack_id,
                    level=None,
                    ct=False,
                    cs=False,
                    gm=True,
                    cm=False
                )
                species_attacks.append(species_attack)

            if attack.data['cm']:
                species_attack = PokemonSpeciesAttacks(
                    species_id=species_id,
                    attack_id=attack_id,
                    level=None,
                    ct=False,
                    cs=False,
                    gm=False,
                    cm=True
                )
                species_attacks.append(species_attack)

        db.session.bulk_save_objects(species_attacks)
        db.session.commit()
        flash(f'{len(species_attacks)} attaque(s) liée(s) à un Pokémon', 'success')
        return redirect(url_for('pokemon', character_id=character_id))

    return _render()


@app.route("/goals/<int:character_id>", methods=('GET', 'POST'))
def goals(character_id: int):
    """
    Objectif d'un personnage
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'goals.html',
            character=character,
            goals=goals,
            pokemon=pokemon,
            form=form
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    goals = Goals.query.filter(Goals.character_id == character_id, Goals.category == GoalCategory.GLOBAL.value).all()
    pokemon = Goals.query.filter(Goals.character_id == character_id, Goals.category == GoalCategory.POKEMON.value).all()

    form = GoalsListForm(formdata=request.form, globals_goals=goals, pokemon_goals=pokemon)

    if request.method == 'GET':
        for goal in goals:
            for globals_goal in form.globals_goals:
                if goal.id == globals_goal.form.id.data:
                    globals_goal.done.data = goal.done

        for poke in pokemon:
            for pokemon_goal in form.pokemon_goals:
                if poke.id == pokemon_goal.form.id.data:
                    pokemon_goal.done.data = poke.done

        return _render()

    if form.add_globals.data:
        goals_form = GoalsForm()
        goals_form.description = None
        goals_form.category = GoalCategory.GLOBAL.value
        goals_form.done = False
        form.globals_goals.append_entry(goals_form)
        return _render()
    if form.add_pokemon.data:
        pokemon_form = GoalsForm()
        pokemon_form.description = None
        pokemon_form.category = GoalCategory.POKEMON.value
        pokemon_form.done = False
        form.pokemon_goals.append_entry(pokemon_form)
        return _render()

    id_to_delete = set()
    to_add = []
    for globals_goal in form.globals_goals:
        if not globals_goal.form.description.data and globals_goal.form.id.data:
            id_to_delete.add(globals_goal.form.id.data)
        elif globals_goal.form.description.data and not globals_goal.form.id.data:
            to_add.append(Goals(
                character_id=character_id,
                description=globals_goal.form.description.data,
                category=GoalCategory.GLOBAL.value,
                done=globals_goal.done.data
            ))
        else:
            for goal in goals:
                if goal.id == globals_goal.form.id.data:
                    goal.done = globals_goal.done.data
                    goal.description = globals_goal.form.description.data
                    continue

    for pokemon_goal in form.pokemon_goals:
        if not pokemon_goal.form.description.data and pokemon_goal.form.id.data:
            id_to_delete.add(pokemon_goal.form.id.data)
        elif pokemon_goal.form.description.data and not pokemon_goal.form.id.data:
            to_add.append(Goals(
                character_id=character_id,
                description=pokemon_goal.form.description.data,
                category=GoalCategory.POKEMON.value,
                done=pokemon_goal.done.data
            ))
        else:
            for poke in pokemon:
                if poke.id == pokemon_goal.form.id.data:
                    poke.done = pokemon_goal.done.data
                    poke.description = pokemon_goal.form.description.data
                    continue

    db.session.bulk_save_objects(to_add)
    db.session.commit()
    Goals.query.filter(Goals.id.in_(id_to_delete)).delete()
    db.session.commit()

    generate_tcard_part(character.id, 'objectifs')
    flash(f'Objectifs de {character.firstname} correctement modifiés', 'success')
    return redirect(url_for('home', character_id=character_id))


@app.route("/journey/<int:character_id>", methods=('GET', 'POST'))
def journey(character_id: int):
    """
    Parcours d'un personnage
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'journey.html',
            character=character,
            journey_chapters=journey_chapters
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    journey_chapters = JourneyChapter.get_ordered_chapter(character_id=character_id, with_journeys=True)

    return _render()


@app.route("/journey/<int:character_id>/newChapter", methods=('GET', 'POST'))
def new_journey_chapter(character_id: int):
    """
    Nouveau chapitre dans le parcours d'un personnage
    :param character_id: id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'journey_chapter_edit.html',
            character=character,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()

    journey_chapters = [(0, 'Début')]

    all_journey_chapters = JourneyChapter.get_ordered_chapter(character_id=character_id)
    if all_journey_chapters:
        journey_chapters += [(journey_chapter.id, journey_chapter.name) for journey_chapter in all_journey_chapters]

    form = JourneyChapterForm(formdata=request.form)
    form.after.choices = journey_chapters

    if request.method == 'POST':
        if form.validate():

            new_journey_chapter = JourneyChapter(character_id=character_id)
            form.populate_obj(new_journey_chapter)
            db.session.add(new_journey_chapter)
            db.session.commit()
            db.session.refresh(new_journey_chapter)

            chapter = next((chap for chap in all_journey_chapters if chap.after == new_journey_chapter.after), None)
            if chapter:
                chapter.after = new_journey_chapter.id
                db.session.commit()

            flash(f'Chapitre {new_journey_chapter.name} ajouté avec succès', 'success')
            return redirect(url_for('journey', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/journey/<int:character_id>/editChapter/<int:chapter_id>", methods=('GET', 'POST'))
def edit_journey_chapter(character_id: int, chapter_id: int):
    """
    Edition d'un chapitre
    :param character_id: id du personnage
    :param chapter_id: id du chapitre
    :return: le template
    """
    def _render():
        return render_template(
            'journey_chapter_edit.html',
            character=character,
            chapter=chapter,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    chapter = JourneyChapter.query.filter(JourneyChapter.id == chapter_id).one_or_404()

    if chapter.character_id != character_id:
        flash(f'Pas chapitre de parcours n°{chapter_id} avec l\'id {character_id}', 'danger')
        return redirect(url_for('home'))

    journey_chapters = [(0, 'Début')]

    all_journey_chapters = JourneyChapter.get_ordered_chapter(character_id=character_id)
    if all_journey_chapters:
        journey_chapters += [(journey_chapter.id, journey_chapter.name) for journey_chapter in all_journey_chapters]

    form = JourneyChapterForm(formdata=request.form, obj=chapter)
    form.after.choices = journey_chapters

    if request.method == 'POST':
        if form.validate():

            change_order(all_journey_chapters, chapter, form.after.data)
            chapter.name = form.name.data

            db.session.commit()

            flash(f'Chapitre {chapter.name} édité avec succès', 'success')
            return redirect(url_for('journey', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/journey/<int:character_id>/chapter/<int:chapter_id>/new", methods=('GET', 'POST'))
def new_journey(character_id: int, chapter_id: int):
    """
    Nouvelle aventure
    :param character_id: id du personnage
    :param chapter_id: id du chapitre auquel est rattaché l'aventure
    :return: le template
    """
    def _render():
        return render_template(
            'journey_edit.html',
            character=character,
            chapter=chapter,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    chapter = JourneyChapter.query.filter(JourneyChapter.id == chapter_id).one_or_404()

    if chapter.character_id != character_id:
        flash(f'Pas chapitre de parcours n°{chapter_id} avec l\'id {character_id}', 'danger')
        return redirect(url_for('home'))

    journeys = [(0, 'Début')]

    all_journeys = Journey.get_ordered_journey(chapter_id=chapter_id)
    if all_journeys:
        journeys += [(journey.id, journey.name) for journey in all_journeys]

    form = JourneyForm(formdata=request.form)
    form.after.choices = journeys

    if request.method == 'POST':
        if form.validate():

            new_journey = Journey(journey_chapter_id=chapter_id)
            form.populate_obj(new_journey)
            db.session.add(new_journey)
            db.session.commit()
            db.session.refresh(new_journey)

            journey = next((journey for journey in all_journeys if journey.after == new_journey.after), None)
            if journey:
                journey.after = new_journey.id
                db.session.commit()

            flash(f'Chapitre {chapter.name} édité avec succès', 'success')
            generate_tcard_part(character.id, 'parcours')
            return redirect(url_for('journey', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')
    return _render()


@app.route("/journey/<int:character_id>/chapter/<int:chapter_id>/edit/<int:journey_id>", methods=('GET', 'POST'))
def edit_journey(character_id: int, chapter_id: int, journey_id: int):
    """
    Edition d'une aventure
    :param character_id: id du personnage
    :param chapter_id: id du chapitre
    :param journey_id: id de l'aventure
    :return: le template
    """
    def _render():
        return render_template(
            'journey_edit.html',
            character=character,
            chapter=chapter,
            journey=journey,
            form=form,
        )

    character = MpCharacter.query.filter(MpCharacter.id == character_id).one_or_404()
    chapter = JourneyChapter.query.filter(JourneyChapter.id == chapter_id).one_or_404()
    journey = Journey.query.filter(Journey.id == journey_id).one_or_404()

    if chapter.character_id != character_id or journey.journey_chapter_id != chapter_id:
        flash(f'Pas sujet n°{journey_id} sur le chapitre {chapter_id}', 'danger')
        return redirect(url_for('home'))

    journeys = [(0, 'Début')]

    all_journeys = Journey.get_ordered_journey(chapter_id=chapter_id)
    if all_journeys:
        journeys += [(journey.id, journey.name) for journey in all_journeys]

    form = JourneyForm(formdata=request.form, obj=journey)
    form.after.choices = journeys

    if request.method == 'POST':
        if form.validate():

            change_order(all_journeys, journey, form.after.data)
            journey.name = form.name.data
            journey.link = form.link.data
            journey.status = form.status.data
            journey.feat = form.feat.data

            db.session.commit()

            flash(f'Chapitre {chapter.name} édité avec succès', 'success')
            generate_tcard_part(character.id, 'parcours')
            return redirect(url_for('journey', character_id=character_id))
        else:
            flash('Erreur dans le formulaire', 'danger')

    return _render()


@app.route("/dex/<int:character_id>", methods=('GET', 'POST'))
def dex(character_id: int):
    """
    Affichage des dex auquel le personnage est abonné (ou a été abonné)
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'home.html',
        )
    return _render()


@app.route("/job_informations/<int:character_id>", methods=('GET', 'POST'))
def job_informations(character_id: int):
    """
    Affichage des informations de rang
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'home.html',
        )
    return _render()


@app.route("/job_pokemon/<int:character_id>", methods=('GET', 'POST'))
def job_pokemon(character_id: int):
    """
    Affichage des Pokémon de rangs
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'home.html',
        )
    return _render()


@app.route("/job_missions/<int:character_id>", methods=('GET', 'POST'))
def job_missions(character_id: int):
    """
    Affichage des missions réalisées
    :param character_id: l'id du personnage
    :return: le template
    """
    def _render():
        return render_template(
            'home.html',
        )
    return _render()
