import unittest

from enums import Region, Object, JourneyStatus, Status, Sex, EvolutionWay


class TestEnum(unittest.TestCase):

    def test_to_tupple(self):
        region_tuple = Region.to_tuple()

        self.assertEqual(region_tuple[0][0], 'Kantô')
        self.assertEqual(region_tuple[0][1], 'Kantô')
        self.assertEqual(region_tuple[1][0], 'Johto')
        self.assertEqual(region_tuple[2][0], 'Hoenn')
        self.assertEqual(region_tuple[3][0], 'Sinnoh')
        self.assertEqual(region_tuple[4][0], 'Unys')
        self.assertEqual(region_tuple[5][0], 'Kalos')
        self.assertEqual(region_tuple[6][0], 'Alola')
        self.assertEqual(region_tuple[7][0], 'Galar')
        self.assertEqual(region_tuple[8][0], 'Paldea')

    def test_get_from_value(self):
        object_test = Object.get_from_value('balls')
        self.assertEqual(object_test, Object.BALLS)

        journey_test = JourneyStatus.get_from_value('À venir')
        self.assertEqual(journey_test, JourneyStatus.UPCOMING)

        journey_test = JourneyStatus.get_from_value('Rien')
        self.assertEqual(journey_test, None)

        journey_test = JourneyStatus.get_from_value('finished')
        self.assertEqual(journey_test, None)

        status_test = Status.get_from_value(1)
        self.assertEqual(status_test, Status.DRESSEUR)

    def test_get_id(self):
        self.assertEqual(1, Sex.FEMININ.get_id())
        self.assertEqual(6, Region.KALOS.get_id())
        self.assertEqual(4, Status.SBIRE.get_id())
        self.assertEqual(6, EvolutionWay.WATER_STONE.get_id())
        self.assertEqual('balls', Object.BALLS.get_id())


if __name__ == '__main__':
    unittest.main()
