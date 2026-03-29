import gooeypie as gp

app = gp.GooeyPieApp("Dropdown Styles")
# app.theme = "light"

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
add_row(app, 'gp.Dropdown(vals)', d1)

# Disabled
d_disabled = gp.Dropdown(VALS)
d_disabled.disabled = True
d_disabled.selected = "Option 1"
add_row(app, 'my_drop.disabled = True', d_disabled)

# Disabled colour
d_disabled_colour = gp.Dropdown(VALS)
d_disabled_colour.disabled = True
d_disabled_colour.selected = "Option 1"
d_disabled_colour.style.disabled_text_color = "firebrick"
add_row(app, 'my_drop.disabled = True\nstyle.disabled_text_color = "firebrick"', d_disabled_colour)

# Width
d_width = gp.Dropdown(["Width = 250", "Option 2"])
d_width.width = 250
d_width.selected = "Width = 250"
add_row(app, 'my_drop.width = 250', d_width)

# Font
d_font = gp.Dropdown(["Serif 18", "Option 2"])
d_font.style.font_size = 18
d_font.style.font_name = "serif"
d_font.selected = "Serif 18"
add_row(app, 'style.font_size = 18\nstyle.font_name = "serif"', d_font)

# Input Colors
d_input = gp.Dropdown(["Red Text", "Yellow BG"])
d_input.selected = "Red Text"
d_input.style.text_color = "red"
d_input.style.bg_color = "lightyellow"
add_row(app, 'style.text_color = "red"\nstyle.bg_color = "lightyellow"', d_input)

# Button Colors
d_btn = gp.Dropdown(["Blue Button", "Option 2"])
d_btn.selected = "Blue Button"
d_btn.style.button_color = "blue"
d_btn.style.button_hover_color = "red"
add_row(app, 'style.button_color = "blue"\nstyle.button_hover_color = "red"', d_btn)

# Dropdown Hover Color
d_menu = gp.Dropdown(["Hover Color", "Option 2"])
d_menu.selected = "Hover Color"
d_menu.style.dropdown_hover_color = "gray"
add_row(app, 'style.dropdown_hover_color = "gray"', d_menu)

# Border Width
d_bw = gp.Dropdown(["Thick Border", "Option 2"])
d_bw.selected = "Thick Border"
d_bw.style.border_width = 5
add_row(app, 'style.border_width = 5', d_bw)

# Border Color
d_bc = gp.Dropdown(["Green Border", "Option 2"])
d_bc.selected = "Green Border"
d_bc.style.border_width = 3
d_bc.style.border_color = "green"
add_row(app, 'style.border_color = "green"\n(and width=3)', d_bc)

# Corner Radius
d_rad = gp.Dropdown(["Round Corners", "Option 2"])
d_rad.selected = "Round Corners"
d_rad.style.corner_radius = 15
add_row(app, 'style.corner_radius = 15', d_rad)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
