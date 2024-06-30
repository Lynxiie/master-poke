import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from enums import HistoryMouvment
from forms import ExchangePokemonForm, ExchangePokemonNewForm
from models import PokemonOwned, History
from utils.pokemon import exchange_pokemon


class TestExchangePokemon(unittest.TestCase):

    def test_exchange(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(6, len(pokemon))
        self.assertEqual([1, 4, 5, 6, 7, 8], ids)

        pokemon_exchanged_1 = pokemon[0]
        pokemon_exchanged_2 = pokemon[1]
        pokemon_exchanged_3 = pokemon[5]

        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 1
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[1, 4, 8],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='Echange CEIR'
        )
        form.new_pokemon.append_entry(pokemon_1)

        exchange_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(4, len(pokemon))
        self.assertEqual([5, 6, 7, 9], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(1, len(histories))

        history = histories[0]
        self.assertEqual(HistoryMouvment.EXCHANGE.value, history.movement)
        self.assertEqual(
            f'{pokemon_exchanged_1.species.species} '
            f'+ {pokemon_exchanged_2.species.species} '
            f'+ {pokemon_exchanged_3.species.species}',
            history.objects_out_exchange
        )
        self.assertIn('Sans Evol', history.objects_in_exchange)
        self.assertEqual('Echange CEIR (Titi)', history.link_title)

    def test_exchange_multi(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(6, len(pokemon))
        self.assertEqual([1, 4, 5, 6, 7, 8], ids)

        pokemon_exchanged = pokemon[0]

        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 1
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        pokemon_2 = ExchangePokemonNewForm()
        pokemon_2.name = "Machin 2"
        pokemon_2.species_id = 2
        pokemon_2.sex = 'F'
        pokemon_2.level = 1
        pokemon_2.category_id = 1
        pokemon_2.nature = 'Nature'
        pokemon_2.shiny = False
        pokemon_2.sprite_credits = None
        pokemon_2.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[1],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='Echange CEIR'
        )

        form.new_pokemon.append_entry(pokemon_1)
        form.new_pokemon.append_entry(pokemon_2)

        exchange_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(7, len(pokemon))
        self.assertEqual([4, 5, 6, 7, 8, 9, 10], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(1, len(histories))

        history = histories[0]
        self.assertEqual(HistoryMouvment.EXCHANGE.value, history.movement)
        self.assertEqual(pokemon_exchanged.species.species, history.objects_out_exchange)
        self.assertIn('Sans Evol + ESPECE', history.objects_in_exchange)
        self.assertEqual('Echange CEIR (Titi)', history.link_title)

    def test_exchange_multi_2(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(6, len(pokemon))
        self.assertEqual([1, 4, 5, 6, 7, 8], ids)

        pokemon_exchanged_1 = pokemon[0]
        pokemon_exchanged_2 = pokemon[1]
        pokemon_exchanged_3 = pokemon[5]

        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 1
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        pokemon_2 = ExchangePokemonNewForm()
        pokemon_2.name = "Machin 2"
        pokemon_2.species_id = 2
        pokemon_2.sex = 'F'
        pokemon_2.level = 1
        pokemon_2.category_id = 1
        pokemon_2.nature = 'Nature'
        pokemon_2.shiny = False
        pokemon_2.sprite_credits = None
        pokemon_2.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[1, 4, 8],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='Echange CEIR'
        )

        form.new_pokemon.append_entry(pokemon_1)
        form.new_pokemon.append_entry(pokemon_2)

        exchange_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.character_id == 1).all()

        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(5, len(pokemon))
        self.assertEqual([5, 6, 7, 9, 10], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(1, len(histories))

        history = histories[0]
        self.assertEqual(HistoryMouvment.EXCHANGE.value, history.movement)
        self.assertEqual(
            f'{pokemon_exchanged_1.species.species} '
            f'+ {pokemon_exchanged_2.species.species} '
            f'+ {pokemon_exchanged_3.species.species}',
            history.objects_out_exchange
        )
        self.assertIn('Sans Evol + ESPECE', history.objects_in_exchange)
        self.assertEqual('Echange CEIR (Titi)', history.link_title)

    def test_exchange_no_pokemon(self):
        pokemon = self.session.query(PokemonOwned).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(8, len(pokemon))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], ids)

        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 1
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[2, 3],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='Echange CEIR'
        )
        form.new_pokemon.append_entry(pokemon_1)

        exchange_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(8, len(pokemon))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], ids)

        histories = self.session.query(History).filter(History.character_id == 1).all()
        self.assertEqual(0, len(histories))

    def test_exchange_not_all_pokemon(self):
        pokemon = self.session.query(PokemonOwned).all()
        ids = [pkmn.id for pkmn in pokemon]
        self.assertEqual(8, len(pokemon))
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8], ids)

        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 1
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[1, 2, 3],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='Echange CEIR'
        )
        form.new_pokemon.append_entry(pokemon_1)

        exchange_pokemon(1, form, self.session)

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
