import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from enums import HistoryMouvment
from models import PokemonOwned, Inventory, History
from utils.pokemon import can_evol, evol_pokemon


class TestPokemonEvol(unittest.TestCase):

    def test_can_evol(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 1).one()
        self.assertEqual("ESPECE 1", pokemon.name)
        self.assertEqual("Sans Evol", pokemon.species.species)
        self.assertFalse(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 2).one()
        self.assertEqual("EVOL LVL 60", pokemon.species.species)
        self.assertFalse(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 3).one()
        self.assertEqual("EVOL LVL 60", pokemon.species.species)
        self.assertTrue(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 4).one()
        self.assertEqual("PIERRE FOUDRE", pokemon.species.species)
        self.assertFalse(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 5).one()
        self.assertEqual("LVL 40", pokemon.species.species)
        self.assertTrue(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 6).one()
        self.assertEqual("EXCHANGE", pokemon.species.species)
        self.assertTrue(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 7).one()
        self.assertEqual("PIERRE FEU", pokemon.species.species)
        self.assertTrue(can_evol(pokemon, 1, self.session))

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 8).one()
        self.assertEqual("EVOL LVL 60", pokemon.species.species)
        self.assertFalse(can_evol(pokemon, 1, self.session))

    def test_evol_pokemon(self):
        # Evolution par niveau
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 3).one()
        self.assertEqual("ESPECE 2.2", pokemon.name)
        self.assertEqual("EVOL LVL 60", pokemon.species.species)

        evol_pokemon(pokemon, 1, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 3).one()
        self.assertEqual("ESPECE 2.2", pokemon.name)
        self.assertEqual("Sans Evol", pokemon.species.species)

        stones = self.session.query(Inventory).filter(Inventory.character_id == 1).all()
        self.assertEqual(2, len(stones))
        self.assertEqual('Pierre Feu', stones[0].object.name)
        self.assertEqual(1, stones[0].quantity)
        self.assertEqual('Pierre Foudre', stones[1].object.name)
        self.assertEqual(0, stones[1].quantity)

        history = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(0, len(history))

        # Evolution par échange
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 6).one()
        self.assertEqual("ESPECE 5", pokemon.name)
        self.assertEqual("EXCHANGE", pokemon.species.species)

        evol_pokemon(pokemon, 1, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 6).one()
        self.assertEqual("ESPECE 5", pokemon.name)
        self.assertEqual("LVL 40", pokemon.species.species)

        stones = self.session.query(Inventory).filter(Inventory.character_id == 1).all()
        self.assertEqual(2, len(stones))
        self.assertEqual('Pierre Feu', stones[0].object.name)
        self.assertEqual(1, stones[0].quantity)
        self.assertEqual('Pierre Foudre', stones[1].object.name)
        self.assertEqual(0, stones[1].quantity)

        history = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(0, len(history))

        # Evolution par pierre
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 7).one()
        self.assertEqual("ESPECE 6", pokemon.name)
        self.assertEqual("PIERRE FEU", pokemon.species.species)

        evol_pokemon(pokemon, 1, self.session, "http://0.0.0.1")

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 7).one()
        self.assertEqual("ESPECE 6", pokemon.name)
        self.assertEqual("EXCHANGE", pokemon.species.species)

        stones = self.session.query(Inventory).filter(Inventory.character_id == 1).all()
        self.assertEqual(2, len(stones))
        self.assertEqual('Pierre Feu', stones[0].object.name)
        self.assertEqual(0, stones[0].quantity)
        self.assertEqual('Pierre Foudre', stones[1].object.name)
        self.assertEqual(0, stones[1].quantity)

        history = self.session.query(History).filter(History.character_id == 1).one()
        self.assertEqual(HistoryMouvment.OUT.value, history.movement)
        self.assertIn('Pierre Feu', history.objects)
        self.assertEqual('Evolution ESPECE 6', history.link_title)

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/insert_evol_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
