import unittest
from unittest.mock import Mock
from games_price_digger.src.iterators.simple_iterator import SimpleIterator
from games_price_digger.src.lists import GameBoxList

game_box1 = Mock()
game_box2 = Mock()
game_box3 = Mock()


class GameBoxListTests(unittest.TestCase):

    def test_make_iterator(self):
        """test description"""
        box_list = GameBoxList([game_box1, game_box2, game_box3])
        iterator = box_list.make_iterator()
        self.assertTrue(isinstance(iterator, SimpleIterator))


if __name__ == '__main__':
    unittest.main()
