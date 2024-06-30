import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from forms import LeavePensionForm
from models import PokemonOwned
from utils.pokemon import leave_pension


class TestPension(unittest.TestCase):

    def test_to_pension(self):
        pass

    def test_leave_pension(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 2).one()
        form = LeavePensionForm(new_level=45, new_xp=3)

        leave_pension(pokemon, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 2).one()
        self.assertEqual('A RETIRER DE PENSION', pokemon.name)
        self.assertIsNone(pokemon.pension)
        self.assertEqual(45, pokemon.level)
        self.assertEqual(3, pokemon.exp_point)
        self.assertEqual(4, pokemon.exp_point_per_level)

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/pension_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def setUp(cls):
        cls.session.execute(text("DELETE FROM pokemon_owned"))
        cls.session.execute(text("DELETE FROM history"))
        cls.session.execute(text("DELETE FROM pokemon_species"))
        cls.session.execute(text("DELETE FROM pokemon_category"))

        with open('sql/pension_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
