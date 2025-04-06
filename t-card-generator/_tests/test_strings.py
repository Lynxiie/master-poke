import unittest

from utils.strings import convert_int_to_prefixed_string, slugify


class TestStrings(unittest.TestCase):

    def test_convert_int_to_prefixed_string(self):
        self.assertEqual(convert_int_to_prefixed_string(0), '00')
        self.assertEqual(convert_int_to_prefixed_string(2), '02')
        self.assertEqual(convert_int_to_prefixed_string(12), '12')
        self.assertEqual(convert_int_to_prefixed_string(120), '120')
        self.assertEqual(convert_int_to_prefixed_string(12, 3), '012')
        self.assertEqual(convert_int_to_prefixed_string(1200, 3), '1200')
        self.assertEqual(convert_int_to_prefixed_string(0, 3), '000')
        self.assertEqual(convert_int_to_prefixed_string(5, 3), '005')

    def test_slugify(self):
        self.assertEqual(slugify('toto'), 'toto')
        self.assertEqual(slugify('Anti-brûle'), 'anti_brule')
        self.assertEqual(slugify('Appat 5 étoiles'), 'appat_5_etoiles')
        self.assertEqual(slugify('Pokéflûte'), 'pokeflute')
        self.assertEqual(slugify('Pomme d\'or'), 'pomme_d_or')
        self.assertEqual(slugify('CT Ténèbres'), 'ct_tenebres')


if __name__ == '__main__':
    unittest.main()
