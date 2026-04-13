import unittest
import gooeypie as gp

class TestLabel(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')
        self.lbl = gp.Label("Test Label")

    def test_default_disabled_color(self):
        # Verify default initialized disabled colour is correctly passed
        self.assertEqual(self.lbl._constructor_kwargs.get('text_color_disabled'), ('gray74', 'gray60'))

    def test_text_disabled_color_style(self):
        # Verify the style property maps correctly to the _constructor_kwargs / _ctk_object
        self.lbl.style.text_disabled_color = "red"
        # Since it uses _set_property('text_color_disabled', value), check pending properties
        self.assertEqual(self.lbl._pending_properties.get('text_color_disabled'), "red")
        
        # Verify disabled sets state to disabled
        self.lbl.disabled = True
        self.assertEqual(self.lbl.disabled, True)
        self.assertEqual(self.lbl._constructor_kwargs.get('state'), 'disabled')

        self.lbl.disabled = False
        self.assertEqual(self.lbl.disabled, False)
        self.assertEqual(self.lbl._constructor_kwargs.get('state'), 'normal')

if __name__ == '__main__':
    unittest.main()
