import unittest

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database import Base
from forms import ExchangePokemonForm, ExchangePokemonNewForm, LeavePensionForm
from models import PokemonOwned, PokemonOwnedAttacks
from utils.levels import level_up_pokemon
from utils.pokemon import evol_pokemon, learn_auto_attacks, exchange_pokemon, leave_pension


class TestLearnAttack(unittest.TestCase):

    def test_learn_auto_xp_base(self):
        id = 1
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == id).one()
        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(0, len(attacks))

        level_up_pokemon(pokemon, 0, 1, self.session)
        self.assertEqual(16, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(2, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)

        level_up_pokemon(pokemon, 0, 2, self.session)
        self.assertEqual(18, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(2, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)

        level_up_pokemon(pokemon, 0, 1, self.session)
        self.assertEqual(19, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(3, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual("ATTAQUE 4", attacks[2].attack.attack.name)

        level_up_pokemon(pokemon, 0, 1, self.session)
        self.assertEqual(20, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(3, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual("ATTAQUE 4", attacks[2].attack.attack.name)

        level_up_pokemon(pokemon, 3, 0, self.session)
        self.assertEqual(23, pokemon.level)
        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(4, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual("ATTAQUE 4", attacks[2].attack.attack.name)
        self.assertEqual("ATTAQUE 5", attacks[3].attack.attack.name)

    def test_learn_auto_xp_evolved(self):
        id = 2
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == id).one()
        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(0, len(attacks))

        level_up_pokemon(pokemon, 0, 3, self.session)
        self.assertEqual(14, pokemon.level)
        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(0, len(attacks))

        level_up_pokemon(pokemon, 10, 0, self.session)
        self.assertEqual(24, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(id, self.session)
        self.assertEqual(1, len(attacks))
        self.assertEqual("ATTAQUE 4", attacks[0].attack.attack.name)

    def test_learn_auto_new_pokemon_base(self):
        pokemon_owned = PokemonOwned(
            id=3,
            character_id=1,
            name="POKE 1",
            species_id=1,
            sex='F',
            level=15,
            shiny=False,
            pv=0,
            atk=0,
            atk_special=0,
            defense=0,
            def_special=0,
            speed=0,
            exp_point=0,
            exp_point_per_level=1,
            hp_up=0,
            zinc=0,
            calcium=0,
            carbos=0,
            iron=0,
            protein=0,
            obtention_link='http://localhost:5000',
            obtention_name='Test',
            nature='Test',
            sprite_credits=None,
            category_id=1,
            pension=None,
            egg=False,
            background="a"
        )

        self.session.add(pokemon_owned)
        self.session.commit()
        learn_auto_attacks(pokemon_owned, self.session)

        attacks = PokemonOwnedAttacks.get_attacks(3, self.session)

        self.assertEqual(2, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)

    def test_learn_auto_new_pokemon_evolved(self):
        pokemon_owned = PokemonOwned(
            character_id=1,
            name="POKE 1",
            species_id=2,
            sex='F',
            level=20,
            shiny=False,
            pv=0,
            atk=0,
            atk_special=0,
            defense=0,
            def_special=0,
            speed=0,
            exp_point=0,
            exp_point_per_level=1,
            hp_up=0,
            zinc=0,
            calcium=0,
            carbos=0,
            iron=0,
            protein=0,
            obtention_link='http://localhost:5000',
            obtention_name='Test',
            nature='Test',
            sprite_credits=None,
            category_id=1,
            pension=None,
            egg=False,
            background="a"
        )
        self.session.add(pokemon_owned)
        self.session.commit()

        learn_auto_attacks(pokemon_owned, self.session)

        attacks = PokemonOwnedAttacks.get_attacks(3, self.session)

        self.assertEqual(1, len(attacks))
        self.assertEqual('ATTAQUE 4', attacks[0].attack.attack.name)

    def test_learn_auto_new_pokemon_egg(self):
        pokemon_owned = PokemonOwned(
            character_id=1,
            name="POKE 1",
            species_id=1,
            sex='F',
            level=15,
            shiny=False,
            pv=0,
            atk=0,
            atk_special=0,
            defense=0,
            def_special=0,
            speed=0,
            exp_point=0,
            exp_point_per_level=1,
            hp_up=0,
            zinc=0,
            calcium=0,
            carbos=0,
            iron=0,
            protein=0,
            obtention_link='http://localhost:5000',
            obtention_name='Test',
            nature='Test',
            sprite_credits=None,
            category_id=1,
            pension=None,
            egg=True,
            background="a"
        )
        self.session.add(pokemon_owned)
        self.session.commit()

        learn_auto_attacks(pokemon_owned, self.session)

        attacks = PokemonOwnedAttacks.get_attacks(3, self.session)

        self.assertEqual(2, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)

    def test_learn_auto_exchange(self):
        pokemon_1 = ExchangePokemonNewForm()
        pokemon_1.name = "Machin"
        pokemon_1.species_id = 1
        pokemon_1.sex = 'F'
        pokemon_1.level = 35
        pokemon_1.category_id = 1
        pokemon_1.nature = 'Nature'
        pokemon_1.shiny = False
        pokemon_1.sprite_credits = None
        pokemon_1.banner_credit = None

        form = ExchangePokemonForm(
            pokemon_ids=[1],
            new_owner='Titi',
            history_link='https://localhost:8080',
            history_name='TEST'
        )
        form.new_pokemon.append_entry(pokemon_1)

        exchange_pokemon(1, form, self.session)

        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 3).one()
        self.assertEqual("Machin", pokemon.name)

        attacks = PokemonOwnedAttacks.get_attacks(3, self.session)
        self.assertEqual(4, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)

    def test_learn_auto_evolution(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 1).one()
        level_up_pokemon(pokemon, 0, 5, self.session)
        self.assertEqual(20, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)

        self.assertEqual(3, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)

        level_up_pokemon(pokemon, 15, 0, self.session)
        self.assertEqual(35, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)
        self.assertEqual(4, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)

        evol_pokemon(pokemon, 1, self.session, None)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)

        self.assertEqual(5, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)
        self.assertEqual('ATTAQUE 3', attacks[4].attack.attack.name)

    def test_learn_auto_evolution_2(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 1).one()
        self.assertEqual(15, pokemon.level)
        level_up_pokemon(pokemon, 32, 0, self.session)
        self.assertEqual(47, pokemon.level)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)
        self.assertEqual(4, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)

        evol_pokemon(pokemon, 1, self.session, None)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)

        self.assertEqual(6, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)
        self.assertEqual('ATTAQUE 3', attacks[4].attack.attack.name)
        self.assertEqual('ATTAQUE 6', attacks[5].attack.attack.name)

    def test_learn_auto_pension(self):
        pokemon = self.session.query(PokemonOwned).filter(PokemonOwned.id == 1).one()
        form = LeavePensionForm(new_level=45, new_xp=3)

        leave_pension(pokemon, form, self.session)

        attacks = PokemonOwnedAttacks.get_attacks(1, self.session)

        self.assertEqual(4, len(attacks))
        self.assertEqual('ATTAQUE 2', attacks[0].attack.attack.name)
        self.assertEqual('ATTAQUE 1', attacks[1].attack.attack.name)
        self.assertEqual('ATTAQUE 4', attacks[2].attack.attack.name)
        self.assertEqual('ATTAQUE 5', attacks[3].attack.attack.name)

    def test_learn_ct(self):
        pass

    def test_learn_cs(self):
        pass

    def test_learn_cm(self):
        pass

    def test_learn_gm(self):
        pass

    def test_learn_all(self):
        pass

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        cls.Session = sessionmaker(bind=cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.session = cls.Session()

        with open('sql/insert_learn_attack_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def setUp(cls):
        cls.session.execute(text("DELETE FROM pokemon_species"))
        cls.session.execute(text("DELETE FROM pokemon_owned"))
        cls.session.execute(text("DELETE FROM pokemon_attacks"))
        cls.session.execute(text("DELETE FROM pokemon_species_attacks"))
        cls.session.execute(text("DELETE FROM pokemon_owned_attacks"))

        with open('sql/insert_learn_attack_data.sql', 'r') as data_file:
            pokemon_data = data_file.read().split(';')

            for command in pokemon_data:
                cls.session.execute(text(command))

            cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()


if __name__ == '__main__':
    unittest.main()
