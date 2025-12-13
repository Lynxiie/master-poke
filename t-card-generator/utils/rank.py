from sqlalchemy.orm.session import Session

from forms import NewCookiesForm, UsedCookiesListForm
from models import CookiesUsed, CookiesMonths, PokemonOwned


def new_cookies(form: NewCookiesForm, character_id: int, session: Session):
    """
    Ajoute de nouveaux cookies
    :param form: le formulaire d'ajout de cookies
    :param character_id: l'id du personnage
    :param session: la session BDD
    """
    cookies_win = int(form.win_cookies.data)

    cookies_month = CookiesMonths(
        character_id=character_id,
        month=form.month.data,
        win_cookies=cookies_win
    )

    session.add(cookies_month)
    session.flush()
    session.refresh(cookies_month)

    new_cookies = []
    for cookie_number in range(cookies_win):
        new_cookies.append(CookiesUsed(
            cookies_months_id=cookies_month.id
        ))

    session.add_all(new_cookies)
    session.commit()


def give_cookies(used_cookies_form: UsedCookiesListForm, session: Session):
    """
    Utilise des cookies
    :param used_cookies_form: le formulaire d'utilisation des cookies
    :param session: la session BDD
    """
    pokemon_id = set(cookies_forms.pokemon_id.data for cookies_forms in used_cookies_form.cookies_forms)
    used_cookies_id = set(cookies_forms.used_cookies_id.data for cookies_forms in used_cookies_form.cookies_forms)

    all_pokemon = session.query(PokemonOwned).filter(PokemonOwned.id.in_(pokemon_id)).all()
    all_pokemon = {pokemon.id: pokemon for pokemon in all_pokemon}

    used_cookies = session.query(CookiesUsed).filter(CookiesUsed.id.in_(used_cookies_id)).all()
    used_cookies = {cookies.id: cookies for cookies in used_cookies}

    for cookies_forms in used_cookies_form.cookies_forms:
        if not cookies_forms.pokemon_id.data:
            continue
        pokemon = all_pokemon[cookies_forms.pokemon_id.data]
        cookies = used_cookies[int(cookies_forms.used_cookies_id.data)]

        cookies.pokemon_id = pokemon.id
        cookies.before_lvl = pokemon.level
        pokemon.level += 1
        cookies.after_lvl = pokemon.level

        session.flush()

    session.commit()
