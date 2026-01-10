import gooeypie as gp

app = gp.GooeyPieApp("Entry Styles")
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
def add_row(app, row, code_text, widget, align_code="left", align_widget="center"):
    l = gp.Label(code_text)
    l.style.font_name = "Consolas", "monospace"
    l.style.justify = "left"
    app.add(l, 1, row, align_horizontal=align_code)
    app.add(widget, 2, row, align_horizontal=align_widget)

# Row 2: Default
e1 = gp.Entry()
e1.text = "Default Entry"
add_row(app, 2, 'gp.Entry()', e1)

# Row 3: Width
e_width = gp.Entry()
e_width.width = 250
e_width.text = "Width = 250"
add_row(app, 3, 'my_entry.width = 250', e_width)

# Row 4: Placeholder
e_ph = gp.Entry()
e_ph.placeholder = "Type here..."
add_row(app, 4, 'my_entry.placeholder = "Type here..."', e_ph)

# Row 5: Placeholder Color
e_ph_color = gp.Entry()
e_ph_color.placeholder = "Placeholder Color"
e_ph_color.style.placeholder_text_color = "red", "salmon"
add_row(app, 5, 'my_entry.style.placeholder_text_color = "red", "salmon"', e_ph_color)

# Row 6: Font Size
e_size = gp.Entry()
e_size.text = "Large Text"
e_size.style.font_size = 20
add_row(app, 6, 'my_entry.style.font_size = 20', e_size)

# Row 7: Font Family
e_mono = gp.Entry()
e_mono.text = "Monospace Font"
e_mono.style.font_name = "monospace"
add_row(app, 7, 'my_entry.style.font_name = "monospace"', e_mono)

# Row 8: Text Color
e_color = gp.Entry()
e_color.text = "Blue Text"
e_color.style.text_color = "blue", "skyblue"
add_row(app, 8, 'my_entry.style.text_color = "blue", "skyblue"', e_color)

# Row 9: Background Color (fg_color)
e_bg = gp.Entry()
e_bg.text = "Yellow Background"
e_bg.style.bg_color = "lightyellow"
e_bg.style.text_color = "black"
add_row(app, 9, 'my_entry.style.bg_color = "lightyellow"', e_bg)

# Row 10: Border Width
e_border_w = gp.Entry()
e_border_w.text = "Thick Border"
e_border_w.style.border_width = 5
add_row(app, 10, 'my_entry.style.border_width = 5', e_border_w)

# Row 11: Border Color
e_border_c = gp.Entry()
e_border_c.text = "Green Border"
e_border_c.style.border_color = "green"
add_row(app, 11, 'my_entry.style.border_color = "green"', e_border_c)

# Row 12: Corner Radius
e_radius = gp.Entry()
e_radius.text = "Round Corners"
e_radius.style.corner_radius = 15
add_row(app, 12, 'my_entry.style.corner_radius = 15', e_radius)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
