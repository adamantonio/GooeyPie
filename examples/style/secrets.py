import gooeypie as gp

app = gp.GooeyPieApp("Secret Styles")
# app.theme = "light"
# 
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

# Row 2: Default
e1 = gp.Secret()
e1.text = "Default Entry"
add_row(app, 'my_entry = gp.Entry()', e1)

# Row 3: Width
e_width = gp.Secret()
e_width.width = 50
add_row(app, 'my_entry.width = 50', e_width)

# Row 4: Placeholder
e_ph = gp.Secret()
e_ph.placeholder = "Type here..."
add_row(app, 'my_entry.placeholder = "Type here..."', e_ph)

# Row 5: Placeholder Color
e_ph_color = gp.Secret()
e_ph_color.placeholder = "Placeholder Color"
e_ph_color.style.placeholder_color = "MediumOrchid"
add_row(app, 'my_entry.style.placeholder_color = "MediumOrchid"', e_ph_color)

# Row 6: Disabled Text Color
e_disabled = gp.Secret()
e_disabled.text = "This text is disabled"
e_disabled.disabled = True
e_disabled.style.text_disabled_color = "MediumSeaGreen"
add_row(app, 'my_entry.style.disabled = True\nmy_entry.style.text_disabled_color = "MediumSeaGreen"', e_disabled)

# Row 9: Text Color
e_color = gp.Secret()
e_color.style.text_color = "Steelblue"
add_row(app, 'my_entry.style.text_color = "Steelblue"', e_color)

# Row 11: Border Width
e_border_w = gp.Secret()
e_border_w.style.border_width = 5
e_border_w.style.border_color = "green"
add_row(app, 'my_entry.style.border_width = 5\nmy_entry.style.border_color = "green"', e_border_w)

# Row 13: Corner Radius
e_radius = gp.Secret()
e_radius.style.corner_radius = 15
e_radius.style.justify = "center"
add_row(app, 'my_entry.style.corner_radius = 15\nmy_entry.style.justify = "center"', e_radius)

# Configure columns
app.set_column_weights(1, 1)

app.run()
