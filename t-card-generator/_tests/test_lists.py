import unittest

from models import JourneyChapter, Object
from utils.lists import sort_by_previous_value, change_order


class TestLists(unittest.TestCase):

    def test_sort_by_previous_value(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '1')
        self.assertEqual(journey_chapters[1].name, '2')
        self.assertEqual(journey_chapters[2].name, '3')
        self.assertEqual(journey_chapters[3].name, '4')

    def test_sort_by_previous_value_no_after(self):
        objects = [
            Object(id=1, name="3", category="4"),
            Object(id=2, name="1", category="0"),
            Object(id=3, name="4", category="1"),
            Object(id=4, name="2", category="2")
        ]

        objects = sort_by_previous_value(objects)

        self.assertEqual(objects[0].name, '3')
        self.assertEqual(objects[1].name, '1')
        self.assertEqual(objects[2].name, '4')
        self.assertEqual(objects[3].name, '2')

    def test_change_order_same_rank(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        change_order(journey_chapters, journey_chapters[1], 0)
        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '1')
        self.assertEqual(journey_chapters[1].name, '2')
        self.assertEqual(journey_chapters[2].name, '3')
        self.assertEqual(journey_chapters[3].name, '4')

    def test_change_order_third_to_first(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        change_order(journey_chapters, journey_chapters[0], 0)
        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '3')
        self.assertEqual(journey_chapters[1].name, '1')
        self.assertEqual(journey_chapters[2].name, '2')
        self.assertEqual(journey_chapters[3].name, '4')

    def test_change_order_fist_to_last(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        change_order(journey_chapters, journey_chapters[1], 3)
        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '2')
        self.assertEqual(journey_chapters[1].name, '3')
        self.assertEqual(journey_chapters[2].name, '4')
        self.assertEqual(journey_chapters[3].name, '1')

    def test_change_order_last_to_fist(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        change_order(journey_chapters, journey_chapters[2], 0)
        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '4')
        self.assertEqual(journey_chapters[1].name, '1')
        self.assertEqual(journey_chapters[2].name, '2')
        self.assertEqual(journey_chapters[3].name, '3')

    def test_change_order_after_itself(self):
        journey_chapters = [
            JourneyChapter(id=1, character_id=1, name="3", after=4),
            JourneyChapter(id=2, character_id=1, name="1", after=0),
            JourneyChapter(id=3, character_id=1, name="4", after=1),
            JourneyChapter(id=4, character_id=1, name="2", after=2)
        ]

        change_order(journey_chapters, journey_chapters[2], 3)
        journey_chapters = sort_by_previous_value(journey_chapters)

        self.assertEqual(journey_chapters[0].name, '1')
        self.assertEqual(journey_chapters[1].name, '2')
        self.assertEqual(journey_chapters[2].name, '3')
        self.assertEqual(journey_chapters[3].name, '4')


if __name__ == '__main__':
    unittest.main()
