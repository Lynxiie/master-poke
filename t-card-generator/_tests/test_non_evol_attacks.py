import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from models import PokemonOwned
from utils.pokemon import get_non_evol_attack


class TestNoEvolAttacks(unittest.TestCase):

    def test_get_non_evol_attack(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 1).one()
        no_evol_attack = get_non_evol_attack(pokemon, self.session)
        self.assertEqual(5, len(no_evol_attack))
        self.assertEqual('ATTAQUE 4', no_evol_attack[0].attack.name)
        self.assertEqual('ATTAQUE 5', no_evol_attack[1].attack.name)
        self.assertEqual('ATTAQUE 6', no_evol_attack[2].attack.name)
        self.assertEqual('ATTAQUE 7', no_evol_attack[3].attack.name)
        self.assertEqual('ATTAQUE 8', no_evol_attack[4].attack.name)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 2).one()
        no_evol_attack = get_non_evol_attack(pokemon, self.session)
        self.assertEqual(2, len(no_evol_attack))
        self.assertEqual('ATTAQUE 2', no_evol_attack[0].attack.name)
        self.assertEqual('ATTAQUE 9', no_evol_attack[1].attack.name)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 3).one()
        no_evol_attack = get_non_evol_attack(pokemon, self.session)
        self.assertEqual(0, len(no_evol_attack))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 4).one()
        no_evol_attack = get_non_evol_attack(pokemon, self.session)
        self.assertEqual(0, len(no_evol_attack))

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/insert_no_evol_attack_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
