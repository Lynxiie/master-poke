import unittest
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from forms import NewDexForm, DexExperiencesForm
from models import PokemonOwned, Dex, DexExperience
from utils.dex import create_new_dex, give_dex_experience


class TestDex(unittest.TestCase):

    def test_dex_1(self):
        new_dex_form = NewDexForm(dex_name="Dex de Toto")

        start_date = datetime(2025, 1, 25)
        create_new_dex(new_dex_form, 1, self.session, start_date)

        dex_db = self.session.query(Dex).filter(Dex.character_id == 1).all()
        self.assertEqual(1, len(dex_db))

        dex = dex_db[0]
        self.assertEqual(1, dex.id)
        self.assertEqual("Dex de Toto", dex.name)
        self.assertEqual("janvier 2025", dex.start_date)
        self.assertEqual("décembre 2025", dex.end_date)

        self.assertEqual(12, len(dex.experiences_gave))
        self.assertEqual("janvier 2025", dex.experiences_gave[0].month)
        self.assertEqual("février 2025", dex.experiences_gave[1].month)
        self.assertEqual("mars 2025", dex.experiences_gave[2].month)
        self.assertEqual("avril 2025", dex.experiences_gave[3].month)
        self.assertEqual("mai 2025", dex.experiences_gave[4].month)
        self.assertEqual("juin 2025", dex.experiences_gave[5].month)
        self.assertEqual("juillet 2025", dex.experiences_gave[6].month)
        self.assertEqual("août 2025", dex.experiences_gave[7].month)
        self.assertEqual("septembre 2025", dex.experiences_gave[8].month)
        self.assertEqual("octobre 2025", dex.experiences_gave[9].month)
        self.assertEqual("novembre 2025", dex.experiences_gave[10].month)
        self.assertEqual("décembre 2025", dex.experiences_gave[11].month)

        pokemon_names, base_lvl, end_lvl = set(), set(), set()
        for experience in dex.experiences_gave:
            pokemon_names.add(experience.pokemon_name)
            base_lvl.add(experience.base_lvl)
            end_lvl.add(experience.end_lvl)

        self.assertEqual(1, len(pokemon_names))
        self.assertIsNone(list(pokemon_names)[0])
        self.assertEqual(1, len(base_lvl))
        self.assertIsNone(list(base_lvl)[0])
        self.assertEqual(1, len(end_lvl))
        self.assertIsNone(list(end_lvl)[0])

    def test_dex_2(self):
        new_dex_form = NewDexForm(dex_name="Dex de Toto")

        start_date = datetime(2025, 6, 25)
        create_new_dex(new_dex_form, 1, self.session, start_date)

        dex_db = self.session.query(Dex).filter(Dex.character_id == 1).all()
        self.assertEqual(1, len(dex_db))

        dex = dex_db[0]
        self.assertEqual(1, dex.id)
        self.assertEqual("Dex de Toto", dex.name)
        self.assertEqual("juin 2025", dex.start_date)
        self.assertEqual("mai 2026", dex.end_date)

        self.assertEqual(12, len(dex.experiences_gave))
        self.assertEqual("juin 2025", dex.experiences_gave[0].month)
        self.assertEqual("juillet 2025", dex.experiences_gave[1].month)
        self.assertEqual("août 2025", dex.experiences_gave[2].month)
        self.assertEqual("septembre 2025", dex.experiences_gave[3].month)
        self.assertEqual("octobre 2025", dex.experiences_gave[4].month)
        self.assertEqual("novembre 2025", dex.experiences_gave[5].month)
        self.assertEqual("décembre 2025", dex.experiences_gave[6].month)
        self.assertEqual("janvier 2026", dex.experiences_gave[7].month)
        self.assertEqual("février 2026", dex.experiences_gave[8].month)
        self.assertEqual("mars 2026", dex.experiences_gave[9].month)
        self.assertEqual("avril 2026", dex.experiences_gave[10].month)
        self.assertEqual("mai 2026", dex.experiences_gave[11].month)

        pokemon_names, base_lvl, end_lvl = set(), set(), set()
        for experience in dex.experiences_gave:
            pokemon_names.add(experience.pokemon_name)
            base_lvl.add(experience.base_lvl)
            end_lvl.add(experience.end_lvl)

        self.assertEqual(1, len(pokemon_names))
        self.assertIsNone(list(pokemon_names)[0])
        self.assertEqual(1, len(base_lvl))
        self.assertIsNone(list(base_lvl)[0])
        self.assertEqual(1, len(end_lvl))
        self.assertIsNone(list(end_lvl)[0])


    def test_give_dex_experience(self):
        new_dex_form = NewDexForm(dex_name="Dex de Toto")
        start_date = datetime(2025, 1, 25)
        create_new_dex(new_dex_form, 1, self.session, start_date)

        form = DexExperiencesForm()
        form.experiences.append_entry(
            {
                'experience_id': 1,
                'experience_dex_id': 1,
                'month': 'janvier 2025',
                'pokemon_name': None,
                'pokemon_name_display': 'POKEMON 1',
                'give': True,
            }
        )
        form.experiences.append_entry(
            {
                'experience_id': 2,
                'experience_dex_id': 1,
                'month': 'février 2025',
                'pokemon_name': '0',
                'give': False,
            }
        )
        form.experiences.append_entry(
            {
                'experience_id': 3,
                'experience_dex_id': 1,
                'month': 'mars 2025',
                'pokemon_name': 'POKEMON 2',
                'give': False,
            }
        )
        form.experiences.append_entry(
            {
                'experience_id': 4,
                'experience_dex_id': 1,
                'month': 'avril 2025',
                'pokemon_name': None,
                'pokemon_name_display': None,
                'give': False,
            }
        )

        give_dex_experience(form, self.session)

        dex_experiences = self.session.query(DexExperience).filter(DexExperience.dex_id == 1).all()
        self.assertEqual(12, len(dex_experiences))

        experience = dex_experiences[0]
        self.assertEqual(1, experience.id)
        self.assertEqual(1, experience.dex_id)
        self.assertEqual('janvier 2025', experience.month)
        self.assertEqual('POKEMON 1', experience.pokemon_name)
        self.assertEqual('ESPECE 1', experience.pokemon_species)
        self.assertEqual(15, experience.base_lvl)
        self.assertEqual(17, experience.end_lvl)
        self.assertTrue(experience.give)

        experience = dex_experiences[1]
        self.assertEqual(2, experience.id)
        self.assertEqual(1, experience.dex_id)
        self.assertEqual('février 2025', experience.month)
        self.assertIsNone(experience.pokemon_name)
        self.assertIsNone(experience.pokemon_species)
        self.assertIsNone(experience.base_lvl)
        self.assertIsNone(experience.end_lvl)
        self.assertFalse(experience.give)

        experience = dex_experiences[2]
        self.assertEqual(3, experience.id)
        self.assertEqual(1, experience.dex_id)
        self.assertEqual('mars 2025', experience.month)
        self.assertEqual('POKEMON 2', experience.pokemon_name)
        self.assertEqual('ESPECE 2', experience.pokemon_species)
        self.assertEqual(11, experience.base_lvl)
        self.assertEqual(13, experience.end_lvl)
        self.assertFalse(experience.give)

        experience = dex_experiences[3]
        self.assertEqual(4, experience.id)
        self.assertEqual(1, experience.dex_id)
        self.assertEqual('avril 2025', experience.month)
        self.assertEqual('Rien', experience.pokemon_name)
        self.assertIsNone(experience.pokemon_species)
        self.assertIsNone(experience.base_lvl)
        self.assertIsNone(experience.end_lvl)
        self.assertTrue(experience.give)

        pokemon_list = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        self.assertEqual(2, len(pokemon_list))
        self.assertEqual('POKEMON 1', pokemon_list[0].name)
        self.assertEqual(17, pokemon_list[0].level)

        self.assertEqual('POKEMON 2', pokemon_list[1].name)
        self.assertEqual(11, pokemon_list[1].level)


    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/dex.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def setUp(cls):
        cls.session.execute(text("DELETE FROM dex"))
        cls.session.execute(text("DELETE FROM dex_experience"))
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
