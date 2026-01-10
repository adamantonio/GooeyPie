import gooeypie as gp

app = gp.GooeyPieApp("Label Styles")
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
add_row(app, 2, 'gp.Label("Default Label")', gp.Label("Default Label"))

# Row 3: Font Size
l_size = gp.Label("Large Text")
l_size.style.font_size = 24
add_row(app, 3, 'my_label.style.font_size = 24', l_size)

# Row 4: Font Weight
l_bold = gp.Label("Bold Text")
l_bold.style.font_weight = "bold"
add_row(app, 4, 'my_label.style.font_weight = "bold"', l_bold)

# Row 5: Font Style
l_italic = gp.Label("Italic Text")
l_italic.style.font_style = "italic"
add_row(app, 5, 'my_label.style.font_style = "italic"', l_italic)

# Row 6: Font Family
l_serif = gp.Label("Serif Font")
l_serif.style.font_name = "serif"
add_row(app, 6, 'my_label.style.font_name = "serif"', l_serif)

# Row 7: Text Color
l_color = gp.Label("Purple/Plum Text")
l_color.style.text_color = ("purple", "plum")
add_row(app, 7, 'my_label.style.text_color = ("purple", "plum")', l_color)

# Row 8: Background & Radius
l_bg = gp.Label("  Teal Background  ") # Spaces for padding effect
l_bg.style.bg_color = "teal"
l_bg.style.text_color = "white"
l_bg.style.corner_radius = 10
add_row(app, 8, 'my_label.style.bg_color = "teal"\nmy_label.style.corner_radius = 10', l_bg)

# Row 9: Justify
l_just = gp.Label("This is a multiline\nlabel verified with\njustify='right'")
l_just.style.justify = "right"
add_row(app, 9, 'my_label.style.justify = "right"', l_just)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
