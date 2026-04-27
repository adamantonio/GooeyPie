import gooeypie as gp

app = gp.GooeyPieApp("Dropdown Styles")
app.theme = "light"

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

VALS = ["Option 1", "Option 2", "Option 3"]

# Default
d1 = gp.Dropdown(VALS)
d1.selected = "Option 1"
add_row(app, 'my_dropdown = gp.Dropdown(options)', d1)

# Disabled
d_disabled = gp.Dropdown(VALS)
d_disabled.disabled = True
d_disabled.selected = "Option 1"
add_row(app, 'my_dropdown.disabled = True', d_disabled)

# Disabled colour
d_disabled_colour = gp.Dropdown(VALS)
d_disabled_colour.disabled = True
d_disabled_colour.selected = "Option 1"
d_disabled_colour.style.text_disabled_color = "IndianRed"
add_row(app, 'my_dropdown.disabled = True\nstyle.text_disabled_color = "IndianRed"', d_disabled_colour)

# Width
d_width = gp.Dropdown(["Narrow", "Option 2"])
d_width.width = 100
d_width.selected = "Narrow"
add_row(app, 'my_dropdown.width = 100', d_width)

# Font
d_font = gp.Dropdown(["Serif 18", "Option 2"])
d_font.style.font_size = 18
d_font.style.font_name = "serif"
d_font.selected = "Serif 18"
add_row(app, 'my_dropdown.style.font_size = 18\nmy_dropdown.style.font_name = "serif"', d_font)

# Input Colors
d_input = gp.Dropdown(["Red Text", "Yellow BG"])
d_input.selected = "Red Text"
d_input.style.text_color = "IndianRed"
d_input.style.bg_color = "lightyellow"
add_row(app, 'my_dropdown.style.text_color = "red"\nmy_dropdown.style.bg_color = "lightyellow"', d_input)

# Button and hover colors
d_btn = gp.Dropdown(["Blue Button", "Option 2"])
d_btn.selected = "Blue Button"
d_btn.style.button_color = "blue"
d_btn.style.button_hover_color = "red"
add_row(app, 'my_dropdown.style.button_color = "blue"\nmy_dropdown.style.button_hover_color = "red"', d_btn)

# Border Color and width
d_bc = gp.Dropdown(["Green Border", "Option 2"])
d_bc.selected = "Green Border"
d_bc.style.border_width = 5
d_bc.style.border_color = "green"
add_row(app, 'my_dropdown.style.border_color = "green"\nmy_dropdown.style.border_width = 5', d_bc)

# Corner Radius
d_rad = gp.Dropdown(["Round Corners", "Option 2"])
d_rad.selected = "Round Corners"
d_rad.style.corner_radius = 15
add_row(app, 'my_dropdown.style.corner_radius = 15', d_rad)

# Configure columns
app.set_column_weights(1, 1)

app.run()
