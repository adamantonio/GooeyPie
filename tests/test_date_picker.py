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

    def test_styles(self):
        self.dp.style.month_font_name = "Times New Roman"
        self.assertEqual(self.dp.style.month_font_name, "Times New Roman")

        self.dp.style.day_text_color = "red"
        self.assertEqual(self.dp.style.day_text_color, "red")

        self.dp.style.month_button_bg_color = "black"
        self.assertEqual(self.dp.style.month_button_bg_color, "black")

if __name__ == '__main__':
    unittest.main()
