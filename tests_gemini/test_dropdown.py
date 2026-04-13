import unittest
import gooeypie as gp

class TestDropdown(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')
        self.dd = gp.Dropdown(['Alpha', 'Beta', 'Gamma'])

    def test_initial_selected_index(self):
        # By default not explicitly selected will return -1 for matching
        self.assertEqual(self.dd.selected_index, -1)

    def test_selected_index_setter_getter(self):
        self.dd.selected_index = 1
        self.assertEqual(self.dd.selected, 'Beta')
        self.assertEqual(self.dd.selected_index, 1)

        self.dd.selected_index = 2
        self.assertEqual(self.dd.selected, 'Gamma')
        self.assertEqual(self.dd.selected_index, 2)

        self.dd.selected_index = 0
        self.assertEqual(self.dd.selected, 'Alpha')
        self.assertEqual(self.dd.selected_index, 0)

    def test_selected_index_setter_invalid_type(self):
        with self.assertRaises(TypeError):
            self.dd.selected_index = '1'
            
        with self.assertRaises(TypeError):
            self.dd.selected_index = 1.5

    def test_selected_index_setter_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.dd.selected_index = -1
            
        with self.assertRaises(IndexError):
            self.dd.selected_index = 5

    def test_selected_index_updates_with_selected(self):
        self.dd.selected = 'Beta'
        self.assertEqual(self.dd.selected_index, 1)

if __name__ == '__main__':
    unittest.main()
