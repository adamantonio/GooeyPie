import gooeypie as gp

app = gp.GooeyPieApp("Checkbox Styles")
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


# Standard
standard_chk = gp.Checkbox("Standard")
add_row(app, "my_checkbox = gp.Checkbox('Standard')", standard_chk)

# Standard disabled
standard_disabled_chk = gp.Checkbox("Disabled")
standard_disabled_chk.disabled = True
# standard_disabled_chk.checked = True
add_row(app, "my_checkbox.disabled = True", standard_disabled_chk)

# Disabled text color
disabled_chk = gp.Checkbox("Disabled text color")
disabled_chk.disabled = True
disabled_chk.checked = True
disabled_chk.style.text_disabled_color = "limegreen", "lightgreen"
disabled_chk.style.checkbox_disabled_color = "darkred"
add_row(app, "my_checkbox.disabled = True\nmy_checkbox.style.text_disabled_color = 'limegreen'\nmy_checkbox.style.checkbox_disabled_color = 'darkred'", disabled_chk)

# Size
size_chk = gp.Checkbox("Large checkbox")
size_chk.size = 40
add_row(app, "my_checkbox.size = 40", size_chk)

# Corner radius
corner_chk = gp.Checkbox("Corner radius")
corner_chk.style.corner_radius = 15
add_row(app, "my_checkbox.style.corner_radius = 15", corner_chk)

# Border width
border_chk = gp.Checkbox("Border width")
border_chk.style.border_width = 5
add_row(app, "my_checkbox.style.border_width = 5", border_chk)

# Border color
border_color_chk = gp.Checkbox("Border color")
border_color_chk.style.border_color = "blue", "skyblue"
add_row(app, "my_checkbox.style.border_color = 'blue'", border_color_chk)

# Checkbox color and hover color
bg_chk = gp.Checkbox("Checkbox and hover colors")
bg_chk.style.checkbox_color = "red", "salmon"
bg_chk.style.checkbox_hover_color = "darkred"
add_row(app, "my_checkbox.style.checkbox_color = 'red'\nmy_checkbox.style.checkbox_hover_color = 'darkred'", bg_chk)

# Text color
text_chk = gp.Checkbox("Text color")
text_chk.style.text_color = "blue", "skyblue"
add_row(app, "my_checkbox.style.text_color = 'blue'", text_chk)

# Font
font_chk = gp.Checkbox("Font")
font_chk.style.font_name = "serif"
font_chk.style.font_size = 16
add_row(app, "my_checkbox.style.font_name = 'serif'\nmy_checkbox.style.font_size = 16", font_chk)

app.run()
