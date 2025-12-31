import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from forms import NewCookiesForm, UsedCookiesListForm
from models import PokemonOwned, CookiesMonths, CookiesUsed
from utils.rank import new_cookies, give_cookies


class TestCookies(unittest.TestCase):

    def test_cookies_1(self):
        cookies = NewCookiesForm(
            month="01/25",
            win_cookies=1,
        )

        new_cookies(cookies, 1, self.session)

        cookies = self.session.query(CookiesMonths).filter(CookiesMonths.character_id == 1).all()
        self.assertEqual(1, len(cookies))
        self.assertEqual(1, cookies[0].id)
        self.assertEqual("01/25", cookies[0].month)
        self.assertEqual(1, cookies[0].win_cookies)

        used_cookies = self.session.query(CookiesUsed).filter(CookiesUsed.cookies_months_id == 1).all()
        self.assertEqual(1, len(used_cookies))
        self.assertEqual(1, used_cookies[0].cookies_months_id)
        self.assertIsNone(used_cookies[0].pokemon_name)
        self.assertIsNone(used_cookies[0].before_lvl)
        self.assertIsNone(used_cookies[0].after_lvl)

    def test_cookies_2(self):
        cookies = NewCookiesForm(
            month="02/25",
            win_cookies=5,
        )

        new_cookies(cookies, 1, self.session)

        cookies = self.session.query(CookiesMonths).filter(CookiesMonths.character_id == 1).all()
        self.assertEqual(1, len(cookies))
        self.assertEqual(1, cookies[0].id)
        self.assertEqual("02/25", cookies[0].month)
        self.assertEqual(5, cookies[0].win_cookies)

        self.assertEqual(5, len(cookies[0].cookies_used))

        for cookie in cookies[0].cookies_used:
            self.assertEqual(1, cookie.cookies_months_id)
            self.assertIsNone(cookie.pokemon_name)
            self.assertIsNone(cookie.before_lvl)
            self.assertIsNone(cookie.after_lvl)

    def test_give_cookies(self):
        cookies = NewCookiesForm(month="01/25", win_cookies=2)
        new_cookies(cookies, 1, self.session)
        cookies = NewCookiesForm(month="02/25", win_cookies=3)
        new_cookies(cookies, 1, self.session)
        cookies = NewCookiesForm(month="01/25", win_cookies=1)
        new_cookies(cookies, 2, self.session)

        form = UsedCookiesListForm()
        form.cookies_forms.append_entry({'cookies_months_id': 1, 'used_cookies_id': 1, 'pokemon_name': 'POKEMON 1'})
        form.cookies_forms.append_entry({'cookies_months_id': 2, 'used_cookies_id': 3, 'pokemon_name': 'POKEMON 1'})
        form.cookies_forms.append_entry({'cookies_months_id': 2, 'used_cookies_id': 4, 'pokemon_name': 'POKEMON 1'})
        form.cookies_forms.append_entry({'cookies_months_id': 1, 'used_cookies_id': 2, 'pokemon_name': 'POKEMON 2'})
        form.cookies_forms.append_entry({'cookies_months_id': 2, 'used_cookies_id': 5, 'pokemon_name': None})

        give_cookies(form, self.session)

        all_cookies = self.session.query(CookiesMonths).filter(CookiesMonths.character_id == 1).all()
        self.assertEqual(2, len(all_cookies))

        cookies = all_cookies[0]
        self.assertEqual(1, cookies.id)
        self.assertEqual("01/25", cookies.month)
        self.assertEqual(2, cookies.win_cookies)
        self.assertEqual(2, len(cookies.cookies_used))

        used_cookie = cookies.cookies_used[0]
        self.assertEqual(1, used_cookie.cookies_months_id)
        self.assertEqual('POKEMON 1', used_cookie.pokemon_name)
        self.assertEqual(15, used_cookie.before_lvl)
        self.assertEqual(16, used_cookie.after_lvl)

        used_cookie = cookies.cookies_used[1]
        self.assertEqual(1, used_cookie.cookies_months_id)
        self.assertEqual('POKEMON 2', used_cookie.pokemon_name)
        self.assertEqual(11, used_cookie.before_lvl)
        self.assertEqual(12, used_cookie.after_lvl)

        cookies = all_cookies[1]
        self.assertEqual(2, cookies.id)
        self.assertEqual("02/25", cookies.month)
        self.assertEqual(3, cookies.win_cookies)
        self.assertEqual(3, len(cookies.cookies_used))

        used_cookie = cookies.cookies_used[0]
        self.assertEqual(2, used_cookie.cookies_months_id)
        self.assertEqual('POKEMON 1', used_cookie.pokemon_name)
        self.assertEqual(16, used_cookie.before_lvl)
        self.assertEqual(17, used_cookie.after_lvl)

        used_cookie = cookies.cookies_used[1]
        self.assertEqual(2, used_cookie.cookies_months_id)
        self.assertEqual('POKEMON 1', used_cookie.pokemon_name)
        self.assertEqual(17, used_cookie.before_lvl)
        self.assertEqual(18, used_cookie.after_lvl)

        all_cookies = self.session.query(CookiesMonths).filter(CookiesMonths.character_id == 2).all()
        self.assertEqual(1, len(all_cookies))

        cookies = all_cookies[0]
        self.assertEqual(3, cookies.id)
        self.assertEqual("01/25", cookies.month)
        self.assertEqual(1, cookies.win_cookies)
        self.assertEqual(1, len(cookies.cookies_used))

        used_cookie = cookies.cookies_used[0]
        self.assertEqual(3, used_cookie.cookies_months_id)
        self.assertIsNone(used_cookie.pokemon_name)
        self.assertIsNone(used_cookie.before_lvl)
        self.assertIsNone(used_cookie.after_lvl)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        self.assertEqual(2, len(pokemon))
        self.assertEqual(18, pokemon[0].level)
        self.assertEqual(12, pokemon[1].level)

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/cookies.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def setUp(cls):
        cls.session.execute(text("DELETE FROM cookies_months"))
        cls.session.execute(text("DELETE FROM cookies_used"))
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
