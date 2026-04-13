import unittest
import gooeypie as gp

class TestListbox(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')
        self.lb = gp.Listbox(["Item 1", "Item 2", "Item 3"])
        self.app.add(self.lb, 1, 1)

    def test_add_item_at_index_normal(self):
        self.lb.add_item_at_index("New Item", 1)
        self.assertTupleEqual(self.lb.items, ("Item 1", "New Item", "Item 2", "Item 3"))

    def test_add_item_at_index_out_of_bounds_positive(self):
        self.lb.add_item_at_index("New Item", 10)
        self.assertTupleEqual(self.lb.items, ("Item 1", "Item 2", "Item 3", "New Item"))

    def test_add_item_at_index_out_of_bounds_negative(self):
        self.lb.add_item_at_index("New Item", -1)
        self.assertTupleEqual(self.lb.items, ("Item 1", "Item 2", "Item 3", "New Item"))

    def test_remove_selected_first_item(self):
        # Select the first item (index 0)
        self.lb.selected_index = 0
        self.assertEqual(self.lb.selected_index, 0)
        self.assertEqual(self.lb.selected, "Item 1")

        # Remove the selected item
        removed = self.lb.remove_selected()
        
        # Verify it was removed correctly (bug regression test)
        self.assertEqual(removed, "Item 1")
        self.assertTupleEqual(self.lb.items, ("Item 2", "Item 3"))

    def test_remove_selected_last_item(self):
        self.lb.selected_index = 2
        removed = self.lb.remove_selected()
        self.assertEqual(removed, "Item 3")
        self.assertTupleEqual(self.lb.items, ("Item 1", "Item 2"))

    def test_remove_selected_none(self):
        removed = self.lb.remove_selected()
        self.assertIsNone(removed)
        self.assertTupleEqual(self.lb.items, ("Item 1", "Item 2", "Item 3"))

    def test_programmatic_selection_generates_one_event(self):
        # Programmatic selection changes should generate EXACTLY ONE `.change` event flawlessly.
        lb_mutli = gp.Listbox(["Alpha", "Beta", "Gamma"])
        lb_mutli.multiple_selection = True
        self.app.add(lb_mutli, 2, 1)

        event_count = 0
        def count_event(e):
            nonlocal event_count
            event_count += 1
            
        lb_mutli.on_change(count_event)
        
        lb_mutli.selected = ["Alpha", "Gamma"]
        self.assertEqual(event_count, 1)
        self.assertEqual(lb_mutli.selected, ["Alpha", "Gamma"])
        
        lb_mutli.select_none()
        self.assertEqual(event_count, 2)
        self.assertEqual(lb_mutli.selected, [])

        lb_mutli.select_all()
        self.assertEqual(event_count, 3)
        self.assertEqual(lb_mutli.selected, ["Alpha", "Beta", "Gamma"])
        
        lb_mutli.selected_index = 1
        self.assertEqual(event_count, 4)

if __name__ == '__main__':
    unittest.main()
