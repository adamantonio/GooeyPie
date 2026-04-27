import gooeypie as gp

app = gp.GooeyPieApp("ButtonGroup Styles")
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

options = ["One", "Two", "Three"]

# Default
bg_default = gp.ButtonGroup(options)
bg_default.selected = "One"
add_row(app, 'my_group = gp.ButtonGroup(labels)', bg_default)

# Default disabled
bg_default_disabled = gp.ButtonGroup(options)
bg_default_disabled.selected = "One"
bg_default_disabled.disabled = True
add_row(app, 'my_group.disabled = True', bg_default_disabled)

# Disabled colours
bg_sel_disabled = gp.ButtonGroup(options)
bg_sel_disabled.selected = "Two"
bg_sel_disabled.style.text_disabled_color = "black"
bg_sel_disabled.style.selected_disabled_color = "tomato"
bg_sel_disabled.style.unselected_disabled_color = "lightcoral"
bg_sel_disabled.disabled = True
add_row(app, 'my_group.disabled = True\nmy_group.style.text_disabled_color = "black"\nmy_group.style.selected_disabled_color = "tomato"\nmy_group.style.unselected_disabled_color = "lightcoral"', bg_sel_disabled)

# Width and height
bg_wh = gp.ButtonGroup(options)
bg_wh.selected = "One"
bg_wh.width = 200
bg_wh.height = 50
add_row(app, 'my_group.width = 200\nmy_group.height = 50', bg_wh)

# Selected and unselected colors
bg_sel = gp.ButtonGroup(options)
bg_sel.selected = "One"
bg_sel.style.selected_color = "IndianRed"
bg_sel.style.selected_hover_color = "FireBrick"
bg_sel.style.unselected_color = "DarkOrange"
bg_sel.style.unselected_hover_color = "Gray"
add_row(app, 'my_group.style.selected_color = "IndianRed"\nmy_group.style.selected_hover_color = "FireBrick"\nmy_group.style.unselected_color = "DarkOrange"\nmy_group.style.unselected_hover_color = "Gray"', bg_sel)

# Text Color
bg_text = gp.ButtonGroup(options)
bg_text.selected = "Three"
bg_text.style.font_name = "monospace"
bg_text.style.font_weight = "bold"
bg_text.style.font_size = 18
bg_text.style.text_color = "darkblue"
add_row(app, 'my_group.style.font_name = "monospace"\nmy_group.style.font_weight = "bold"\nmy_group.style.font_size = 18\nmy_group.style.text_color = "darkblue"', bg_text)

# Corner Radius, border Width and background color
bg_style = gp.ButtonGroup(options)
bg_style.selected = "One"
bg_style.style.corner_radius = 20
bg_style.style.border_width = 5
bg_style.style.bg_color = "orange"
add_row(app, 'my_group.style.corner_radius = 20\nmy_group.style.border_width = 5\nmy_group.style.bg_color = "orange"', bg_style)

# Configure columns
app.set_column_weights(1, 1)

app.run()
