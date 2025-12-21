from datetime import datetime

from slugify import slugify as slug

DATE_FORMAT = '%d/%m/%y'


def convert_int_to_prefixed_string(to_convert: int, max_lenght: int = 2) -> str:
    """
    Converti un int en string préfixée par "0"
    :param to_convert: le nombre à convertir
    :param max_lenght: la taille maximal voulue - Ne rogne pas le nombre de base s'il est plus grand que la taille
        max désirée
    :return: une string du nombre converti
    """
    to_convert = str(to_convert)
    number_len = len(to_convert)

    if number_len > max_lenght:
        max_lenght = number_len

    return to_convert.zfill(max_lenght)


def slugify(string: str) -> str:
    """
    Slugify une string
    :param string: une string à slugifier
    :return: la string slugifiée
    """
    return slug(string, replacements=[['-', '_']])


def convert_month_db_to_datetime(month_db: str) -> datetime:
    mois_fr = {
        "janvier": 1,
        "février": 2,
        "mars": 3,
        "avril": 4,
        "mai": 5,
        "juin": 6,
        "juillet": 7,
        "août": 8,
        "septembre": 9,
        "octobre": 10,
        "novembre": 11,
        "décembre": 12
    }
    month, year = month_db.split()
    return datetime(int(year.strip()), mois_fr[month.strip()], 1)
