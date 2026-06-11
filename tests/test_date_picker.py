import unittest
import datetime as dt
from datetime import datetime
import gooeypie as gp

class TestDatePicker(unittest.TestCase):
    def setUp(self):
        self.app = gp.GooeyPieApp('test')
        self.dp = gp.DatePicker()

    def test_initialization(self):
        self.assertIsNone(self.dp.date)
        self.assertEqual(self.dp.date_str, "")

    def test_date_property(self):
        test_date = dt.date(2023, 5, 10)
        self.dp.date = test_date
        self.assertEqual(self.dp.date, test_date)
        self.assertEqual(self.dp.date_str, test_date.strftime(self.dp.format))

    def test_date_str_property(self):
        self.dp.format = "%Y-%m-%d"
        self.dp.date_str = "2023-06-15"
        self.assertEqual(self.dp.date, dt.date(2023, 6, 15))

    def test_date_str_property_invalid_format(self):
        self.dp.format = "%Y-%m-%d"
        with self.assertRaises(ValueError) as ctx:
            self.dp.date_str = "invalid_format"
        self.assertIn("does not match the required format '%Y-%m-%d'", str(ctx.exception))
        
        with self.assertRaises(ValueError):
            self.dp.date_str = "12/25/2026"

    def test_set_today(self):
        self.dp.set_today()
        self.assertEqual(self.dp.date, datetime.now().date())

    def test_add_subtract_days(self):
        self.dp.date = dt.date(2023, 5, 10)
        self.dp.add_days(5)
        self.assertEqual(self.dp.date, dt.date(2023, 5, 15))
        self.dp.subtract_days(10)
        self.assertEqual(self.dp.date, dt.date(2023, 5, 5))

    def test_add_subtract_months(self):
        self.dp.date = dt.date(2023, 5, 15)
        self.dp.add_months(2)
        self.assertEqual(self.dp.date, dt.date(2023, 7, 15))
        self.dp.subtract_months(8)
        self.assertEqual(self.dp.date, dt.date(2022, 11, 15))

    def test_add_subtract_years(self):
        self.dp.date = dt.date(2023, 5, 15)
        self.dp.add_years(2)
        self.assertEqual(self.dp.date, dt.date(2025, 5, 15))
        self.dp.subtract_years(5)
        self.assertEqual(self.dp.date, dt.date(2020, 5, 15))

    def test_clear(self):
        self.dp.date = dt.date(2023, 5, 15)
        self.dp.clear()
        self.assertIsNone(self.dp.date)
        self.assertEqual(self.dp.date_str, "")

    def test_allow_manual_input(self):
        self.assertTrue(self.dp.allow_manual_input)
        self.dp.allow_manual_input = False
        self.assertFalse(self.dp.allow_manual_input)

    def test_disabled_state(self):
        self.assertFalse(self.dp.disabled)
        self.dp.disabled = True
        self.assertTrue(self.dp.disabled)

        self.app.add(self.dp, 1, 1)
        self.assertEqual(self.dp._ctk_object.date_entry.cget('state'), 'disabled')
        self.assertEqual(self.dp._ctk_object.calendar_button.cget('state'), 'disabled')
        self.assertEqual(self.dp._ctk_object.date_entry.cget('text_color'), self.dp._ctk_object._default_disabled_color)

        self.dp.disabled = False
        self.assertFalse(self.dp.disabled)
        self.assertEqual(self.dp._ctk_object.date_entry.cget('state'), 'normal')
        self.assertEqual(self.dp._ctk_object.calendar_button.cget('state'), 'normal')
        self.assertEqual(self.dp._ctk_object.date_entry.cget('text_color'), self.dp._ctk_object._original_text_color)

    def test_styles(self):
        self.dp.style.month_font_name = "Times New Roman"
        self.assertEqual(self.dp.style.month_font_name, "Times New Roman")

        self.dp.style.day_text_color = "red"
        self.assertEqual(self.dp.style.day_text_color, "red")

        self.dp.style.month_button_bg_color = "black"
        self.assertEqual(self.dp.style.month_button_bg_color, "black")

        self.dp.style.month_button_hover_color = "green"
        self.assertEqual(self.dp.style.month_button_hover_color, "green")

        self.dp.style.open_button_hover_color = "blue"
        self.assertEqual(self.dp.style.open_button_hover_color, "blue")

        self.dp.style.open_button_icon_color = "yellow"
        self.assertEqual(self.dp.style.open_button_icon_color, "yellow")

        self.dp.style.day_hover_color = "purple"
        self.assertEqual(self.dp.style.day_hover_color, "purple")

        self.dp.style.text_disabled_color = "pink"
        self.assertEqual(self.dp.style.text_disabled_color, "pink")

    def test_date_font_styles(self):
        self.dp.style.date_font_name = "Arial"
        self.dp.style.date_font_size = 14
        self.dp.style.date_font_style = "italic"
        self.dp.style.date_font_weight = "bold"

        self.assertEqual(self.dp.style.date_font_name, "Arial")
        self.assertEqual(self.dp.style.date_font_size, 14)
        self.assertEqual(self.dp.style.date_font_style, "italic")
        self.assertEqual(self.dp.style.date_font_weight, "bold")

        self.app.add(self.dp, 1, 1)

        # Now verify actual tk font configurations
        font = self.dp._ctk_object.date_entry.cget("font")
        if hasattr(font, 'cget'):
            self.assertEqual(font.cget("family"), "Arial")
            self.assertEqual(font.cget("size"), 14)
            self.assertEqual(font.cget("slant"), "italic")
            self.assertEqual(font.cget("weight"), "bold")
        else:
            # Tkinter tuple
            self.assertEqual(font[0], "Arial")
            self.assertEqual(font[1], 14)
            self.assertIn("bold", font)
            self.assertIn("italic", font)

        # Check updates after instantiation
        self.dp.style.date_font_size = 16
        font = self.dp._ctk_object.date_entry.cget("font")
        if hasattr(font, 'cget'):
            self.assertEqual(font.cget("size"), 16)
        else:
            self.assertEqual(font[1], 16)

    def test_width(self):
        dp = gp.DatePicker(width=250)
        self.assertEqual(dp.width, 250)

        self.app.add(dp, 1, 1)
        self.assertEqual(dp._ctk_object.cget('width'), 250)
        self.assertEqual(dp._ctk_object.date_entry.cget('width'), 210)

        # Test dynamic updates
        dp.width = 350
        self.assertEqual(dp.width, 350)
        self.assertEqual(dp._ctk_object.cget('width'), 350)
        self.assertEqual(dp._ctk_object.date_entry.cget('width'), 310)

    def test_min_max_dates(self):
        today = dt.date.today()
        future_28_days = today + dt.timedelta(days=28)

        # Setter/getter tests
        self.dp.minimum_date = today
        self.dp.maximum_date = future_28_days
        self.assertEqual(self.dp.minimum_date, today)
        self.assertEqual(self.dp.maximum_date, future_28_days)

        # Validate range limits exception
        with self.assertRaises(ValueError) as ctx:
            self.dp.maximum_date = today - dt.timedelta(days=1)
        self.assertIn("cannot be earlier than", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            self.dp.minimum_date = future_28_days + dt.timedelta(days=1)
        self.assertIn("cannot be later than", str(ctx.exception))

        # Check date property validation
        with self.assertRaises(ValueError):
            self.dp.date = today - dt.timedelta(days=1)

        with self.assertRaises(ValueError):
            self.dp.date = future_28_days + dt.timedelta(days=1)

        # Check acceptable date sets correctly
        self.dp.date = today + dt.timedelta(days=5)
        self.assertEqual(self.dp.date, today + dt.timedelta(days=5))

    def test_open_calendar_defaults_to_entry_date(self):
        self.app.add(self.dp, 1, 1)
        past_date = dt.date(2020, 5, 15)
        self.dp.date = past_date

        self.dp.open()

        self.assertEqual(self.dp._ctk_object.current_year, 2020)
        self.assertEqual(self.dp._ctk_object.current_month, 5)

    def test_event_bindings(self):
        focus_gained_called = False
        focus_lost_called = False
        key_press_called = False
        click_called = False

        def on_focus_gained(e):
            nonlocal focus_gained_called
            focus_gained_called = True

        def on_focus_lost(e):
            nonlocal focus_lost_called
            focus_lost_called = True

        def on_key_press(e):
            nonlocal key_press_called
            key_press_called = True

        def on_click(e):
            nonlocal click_called
            click_called = True

        self.dp.on_focus_gained(on_focus_gained)
        self.dp.on_focus_lost(on_focus_lost)
        self.dp.on_key_press(on_key_press)
        self.dp.on_click(on_click)

        self.app.add(self.dp, 1, 1)
        self.app._ctk_object.update()

        # Trigger events on the internal widgets and assert they execute our handlers
        self.dp._ctk_object.date_entry._entry.event_generate("<FocusIn>")
        self.app._ctk_object.update()
        self.assertTrue(focus_gained_called)

        self.dp._ctk_object.date_entry._entry.event_generate("<FocusOut>")
        self.app._ctk_object.update()
        self.assertTrue(focus_lost_called)

        self.dp._ctk_object.date_entry._entry.focus_set()
        self.dp._ctk_object.date_entry._entry.event_generate("<KeyPress>", keysym="a")
        self.app._ctk_object.update()
        self.assertTrue(key_press_called)

        self.dp._ctk_object.date_entry._entry.event_generate("<ButtonRelease-1>")
        self.app._ctk_object.update()
        self.assertTrue(click_called)




if __name__ == '__main__':
    unittest.main()

