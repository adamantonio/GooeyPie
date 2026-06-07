import gooeypie as gp
from datetime import date

app = gp.GooeyPieApp("Date Picker Styles")
app.theme = "dark"

# Header
code_header = gp.Label("Code")
code_header.style.font_size = 16
code_header.style.font_weight = "bold"
result_header = gp.Label("Result")
result_header.style.font_size = 16
result_header.style.font_weight = "bold"

app.add(code_header, 1, 1)
app.add(result_header, 2, 1)

# Helper for code labels
_next_row = 2
def add_row(app, code_text, widget, align_code="left", align_widget="center"):
    global _next_row
    l = gp.Label(code_text)
    l.style.font_name = "Consolas", "monospace"
    l.style.justify = "left"
    app.add(l, 1, _next_row, align_horizontal=align_code)
    app.add(widget, 2, _next_row, align_horizontal=align_widget)
    _next_row += 1

# Default
dp_default = gp.DatePicker()
dp_default.style.date_border_width = 2
add_row(app, 'my_datepicker = gp.DatePicker()', dp_default)

# Disabled
dp_disabled = gp.DatePicker()
dp_disabled.disabled = True
add_row(app, 'my_datepicker.disabled = True', dp_disabled)

# Disabled with date
dp_disabled_filled = gp.DatePicker()
dp_disabled_filled.disabled = True
dp_disabled_filled.date = date.today()
add_row(app, 'my_datepicker.disabled = True\nmy_datepicker.date = date.today()', dp_disabled_filled)

# Disabled with custom disabled color
dp_disabled_custom = gp.DatePicker()
dp_disabled_custom.disabled = True
dp_disabled_custom.date = date.today()
dp_disabled_custom.style.text_disabled_color = "IndianRed"
add_row(app, 'my_datepicker.disabled = True\nmy_datepicker.date = date.today()\nmy_datepicker.style.text_disabled_color = "IndianRed"', dp_disabled_custom)

# Custom Colors & Borders
dp_custom = gp.DatePicker()
dp_custom.style.text_color = "SteelBlue"
dp_custom.style.date_bg_color = "LightYellow"
dp_custom.style.date_border_color = "IndianRed"
dp_custom.style.date_border_width = 3
add_row(app, 'my_datepicker.style.text_color = "SteelBlue"\nmy_datepicker.style.date_bg_color = "LightYellow"\nmy_datepicker.style.date_border_color = "IndianRed"\nmy_datepicker.style.date_border_width = 3', dp_custom)

# Custom Open Button Colors
dp_open_btn = gp.DatePicker()
dp_open_btn.style.open_button_bg_color = "SeaGreen"
dp_open_btn.style.open_button_icon_color = "black"
dp_open_btn.style.open_button_hover_color = "yellow"
add_row(app, 'my_datepicker.style.open_button_bg_color = "SeaGreen"\nmy_datepicker.style.open_button_icon_color = "black"\nmy_datepicker.style.open_button_hover_color = "yellow"', dp_open_btn)

# Custom Calendar Month & Day Styling
dp_calendar = gp.DatePicker()
dp_calendar.style.text_color = "DarkOrchid"
dp_calendar.style.month_font_name = "Georgia"
dp_calendar.style.month_font_size = 14
dp_calendar.style.month_font_weight = "bold"
dp_calendar.style.month_text_color = "DarkOrchid"
dp_calendar.style.day_font_name = "Arial"
dp_calendar.style.day_font_size = 10
dp_calendar.style.day_text_color = "MediumSeaGreen"
dp_calendar.style.day_hover_color = "lightgreen"
dp_calendar.style.month_button_bg_color = "turquoise"
dp_calendar.style.month_button_text_color = "black"
dp_calendar.style.month_button_hover_color = "pink"
add_row(app, 'my_datepicker.style.month_font_name = "Georgia"\nmy_datepicker.style.month_text_color = "DarkOrchid"\nmy_datepicker.style.day_text_color = "MediumSeaGreen"\nmy_datepicker.style.day_hover_color = "lightgreen"\nmy_datepicker.style.month_button_bg_color = "turquoise"\nmy_datepicker.style.month_button_hover_color = "pink"', dp_calendar)

# Custom Date Font Styling
dp_date_font = gp.DatePicker()
dp_date_font.width = 200
dp_date_font.date = date.today()
dp_date_font.style.date_font_name = "Cambria"
dp_date_font.style.date_font_size = 28
dp_date_font.style.date_font_weight = "bold"
add_row(app, 'my_datepicker.style.date_font_name = "Cambria"\nmy_datepicker.style.date_font_size = 28\nmy_datepicker.style.date_font_style = "italic"\nmy_datepicker.style.date_font_weight = "bold"', dp_date_font)

# Configure columns
app.set_column_weights(1, 1)


# Secret theme switch
def switch(e):
    app.theme = 'light'

code_header.on_click(switch)

app.run()
