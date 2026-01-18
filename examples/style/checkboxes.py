import gooeypie as gp

app = gp.GooeyPieApp("Checkbox Styles")
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


# Row 1: Standard
standard_chk = gp.Checkbox("Standard")
add_row(app, 2, "standard_chk = gp.Checkbox('Standard')", standard_chk)


# Row 2: Size
size_chk = gp.Checkbox("Large checkbox")
size_chk.checkbox_width = 40
size_chk.checkbox_height = 40
add_row(app, 3, "size_chk.checkbox_width = 40\nsize_chk.checkbox_height = 40", size_chk)

# Row 3: Corner radius
corner_chk = gp.Checkbox("Corner radius")
corner_chk.style.corner_radius = 15
add_row(app, 4, "corner_chk.style.corner_radius = 15", corner_chk)

# Row 4: Border width
border_chk = gp.Checkbox("Border width")
border_chk.style.border_width = 5
add_row(app, 5, "border_chk.style.border_width = 5", border_chk)

# Row 5: Border color
border_color_chk = gp.Checkbox("Border color")
border_color_chk.style.border_color = "blue", "skyblue"
add_row(app, 6, "border_color_chk.style.border_color = 'blue'", border_color_chk)

# Row 6: Background color and hover color
bg_chk = gp.Checkbox("Background and hover colors")
bg_chk.style.bg_color = "red", "salmon"
bg_chk.style.hover_bg_color = "darkred"
add_row(app, 7, "bg_chk.style.bg_color = 'red'\nbg_chk.style.hover_bg_color = 'red'", bg_chk)

# Row 8: Text color
text_chk = gp.Checkbox("Text color")
text_chk.style.text_color = "blue", "skyblue"
add_row(app, 8, "text_chk.style.text_color = 'blue'", text_chk)

# Row 9: Disabled text color
disabled_chk = gp.Checkbox("Disabled text color")
disabled_chk.disabled = True
disabled_chk.style.disabled_text_color = "limegreen", "lightgreen"
add_row(app, 9, "disabled_chk.style.disabled_text_color = 'limegreen'", disabled_chk)

# Row 10: Font
font_chk = gp.Checkbox("Font")
font_chk.style.font_name = "serif"
font_chk.style.font_size = 16
add_row(app, 10, "font_chk.style.font_name = 'serif'\nfont_chk.style.font_size = 16", font_chk)

app.run()
