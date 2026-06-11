import unittest
import gooeypie as gp

class TestTable(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')
        self.tbl = gp.Table(["Col1", "Col2"])
        self.app.add(self.tbl, 1, 1)

    def test_add_row(self):
        self.tbl.add_row(["A", "B"])
        self.assertEqual(len(self.tbl.data), 1)
        self.assertEqual(self.tbl.data[0], ["A", "B"])

    def test_add_row_at(self):
        self.tbl.add_row(["A", "B"])
        self.tbl.add_row_at(0, ["C", "D"])
        self.assertEqual(len(self.tbl.data), 2)
        self.assertEqual(self.tbl.data[0], ["C", "D"])

    def test_remove_row(self):
        self.tbl.add_row(["A", "B"])
        removed = self.tbl.remove_row(0)
        self.assertEqual(removed, ["A", "B"])
        self.assertEqual(len(self.tbl.data), 0)

    def test_clear(self):
        self.tbl.add_row(["A", "B"])
        self.tbl.add_row(["C", "D"])
        self.tbl.clear()
        self.assertEqual(len(self.tbl.data), 0)

    def test_data_setter(self):
        new_data = [["a", "b"], ["c", "d"]]
        self.tbl.data = new_data
        self.assertEqual(self.tbl.data, new_data)

    def test_invalid_data_setter(self):
        with self.assertRaises(ValueError):
            # Wrong number of columns
            self.tbl.data = [["1"]]

    def test_selection_single(self):
        self.tbl.data = [["A", "B"], ["C", "D"]]
        self.tbl.select_row(1)
        self.assertEqual(self.tbl.selected_row, 1)
        self.assertEqual(self.tbl.selected, ["C", "D"])

    def test_selection_multiple(self):
        tbl_multi = gp.Table(["Col1", "Col2"], multiple_selection=True)
        self.app.add(tbl_multi, 2, 1)
        tbl_multi.data = [["A", "B"], ["C", "D"], ["E", "F"]]
        
        tbl_multi.select_all()
        self.assertEqual(len(tbl_multi.selected), 3)
        self.assertEqual(tbl_multi.selected, [["A", "B"], ["C", "D"], ["E", "F"]])

    def test_remove_selected(self):
        self.tbl.data = [["A", "B"], ["C", "D"]]
        self.tbl.select_row(0)
        removed = self.tbl.remove_selected()
        self.assertEqual(removed, ["A", "B"])
        self.assertEqual(len(self.tbl.data), 1)

if __name__ == '__main__':
    unittest.main()
