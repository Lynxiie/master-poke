import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from enums import HistoryMouvment
from forms import GivePokemonForm
from models import PokemonOwned, History

from utils.pokemon import give_pokemon


class TestGivePokemon(unittest.TestCase):

    def test_give(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(6, len(pokemon))
        self.assertEqual([1, 4, 5, 6, 7, 8], ids)

        pokemon_gived = pokemon[3]

        form = GivePokemonForm(
            pokemon_id=6,
            new_owner='Toto',
            history_link='https://localhost:8080',
            history_name='Don'
        )

        give_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(5, len(pokemon))
        self.assertEqual([1, 4, 5, 7, 8], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(1, len(histories))

        history = histories[0]
        self.assertEqual(HistoryMouvment.OUT.value, history.movement)
        self.assertEqual(pokemon_gived.species.species, history.objects)
        self.assertEqual('Don (Toto)', history.link_title)

    def test_give_no_pokemon(self):
        pokemon = self.session.query(PokemonOwned).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(8, len(pokemon))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], ids)

        form = GivePokemonForm(
            pokemon_id=2,
            new_owner='Toto',
            history_link='https://localhost:8080',
            history_name='Don'
        )

        give_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(8, len(pokemon))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(0, len(histories))

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/insert_give_data.sql', 'r') as data_file:
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

        with open('sql/insert_give_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
