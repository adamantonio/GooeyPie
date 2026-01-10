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
def add_row(app, row, code_text, widget, align_code="left", align_widget="center"):
    l = gp.Label(code_text)
    l.style.font_name = "Consolas", "monospace"
    l.style.justify = "left"
    app.add(l, 1, row, align_horizontal=align_code)
    app.add(widget, 2, row, align_horizontal=align_widget)

VALS = ["Option 1", "Option 2", "Option 3"]

# Row 2: Default
d1 = gp.Dropdown(VALS)
d1.selected = "Option 1"
add_row(app, 2, 'gp.Dropdown(vals)', d1)

# Row 3: Width
d_width = gp.Dropdown(["Width = 250", "Option 2"])
d_width.width = 250
d_width.selected = "Width = 250"
add_row(app, 3, 'my_drop.width = 250', d_width)

# Row 4: Font
d_font = gp.Dropdown(["Serif 18", "Option 2"])
d_font.style.font_size = 18
d_font.style.font_name = "serif"
d_font.selected = "Serif 18"
add_row(app, 4, 'style.font_size = 18\nstyle.font_name = "serif"', d_font)

# Row 5: Input Colors
d_input = gp.Dropdown(["Red Text", "Yellow BG"])
d_input.selected = "Red Text"
d_input.style.text_color = "red"
d_input.style.bg_color = "lightyellow"
add_row(app, 5, 'style.text_color = "red"\nstyle.bg_color = "lightyellow"', d_input)

# Row 6: Button Colors
d_btn = gp.Dropdown(["Blue Button", "Option 2"])
d_btn.selected = "Blue Button"
d_btn.style.button_color = "blue"
d_btn.style.button_hover_color = "red"
add_row(app, 6, 'style.button_color = "blue"\nstyle.button_hover_color = "red"', d_btn)

# Row 7: Dropdown Menu Colors
d_menu = gp.Dropdown(["Menu Colors", "Option 2"])
d_menu.selected = "Menu Colors"
d_menu.style.dropdown_bg_color = "black"
d_menu.style.dropdown_text_color = "white"
d_menu.style.dropdown_hover_color = "gray"
add_row(app, 7, 'style.dropdown_bg_color = "black"\nstyle.dropdown_text_color = "white"\nstyle.dropdown_hover_color = "gray"', d_menu)

# Row 8: Dropdown Menu Font
d_mfont = gp.Dropdown(["Menu Font", "Option 2"])
d_mfont.selected = "Menu Font"
d_mfont.style.dropdown_font_name = "monospace"
d_mfont.style.dropdown_font_size = 16
add_row(app, 8, 'style.dropdown_font_name = "monospace"\nstyle.dropdown_font_size = 16', d_mfont)

# Row 9: Border Width
d_bw = gp.Dropdown(["Thick Border", "Option 2"])
d_bw.selected = "Thick Border"
d_bw.style.border_width = 5
add_row(app, 9, 'style.border_width = 5', d_bw)

# Row 10: Border Color
d_bc = gp.Dropdown(["Green Border", "Option 2"])
d_bc.selected = "Green Border"
d_bc.style.border_width = 3
d_bc.style.border_color = "green"
add_row(app, 10, 'style.border_color = "green"\n(and width=3)', d_bc)

# Row 11: Corner Radius
d_rad = gp.Dropdown(["Round Corners", "Option 2"])
d_rad.selected = "Round Corners"
d_rad.style.corner_radius = 15
add_row(app, 11, 'style.corner_radius = 15', d_rad)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
