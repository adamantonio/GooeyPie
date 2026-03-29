import gooeypie as gp

app = gp.GooeyPieApp("ButtonGroup Styles")
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

options = ["One", "Two", "Three"]

# Default
bg_default = gp.ButtonGroup(options)
bg_default.selected = "One"
add_row(app, 'gp.ButtonGroup(options)', bg_default)

# Default disabled
bg_default_disabled = gp.ButtonGroup(options)
bg_default_disabled.selected = "One"
bg_default_disabled.disabled = True
add_row(app, 'gp.ButtonGroup(options)\ndisabled = True', bg_default_disabled)

# Width and height
bg_wh = gp.ButtonGroup(options)
bg_wh.selected = "One"
bg_wh.width = 200
bg_wh.height = 50
add_row(app, 'width = 200\nheight = 50', bg_wh)

# Selected Color
bg_sel = gp.ButtonGroup(options)
bg_sel.selected = "One"
bg_sel.style.selected_color = "red"
bg_sel.style.selected_hover_color = "darkred"
add_row(app, 'style.selected_color = "red"\nstyle.selected_hover_color = "darkred"', bg_sel)

# Unselected Color
bg_unsel = gp.ButtonGroup(options)
bg_unsel.selected = "Two"
bg_unsel.style.unselected_color = "lightblue"
bg_unsel.style.unselected_hover_color = "skyblue"
add_row(app, 'style.unselected_color = "lightblue"\nstyle.unselected_hover_color = "skyblue"', bg_unsel)

# Text Color
bg_text = gp.ButtonGroup(options)
bg_text.selected = "Three"
bg_text.style.font_name = "monospace"
bg_text.style.font_weight = "bold"
bg_text.style.font_size = 18
bg_text.style.text_color = "purple", "magenta"
add_row(app, 'style.font_name = "monospace"\nstyle.font_weight = "bold"\nstyle.font_size = 18\nstyle.text_color = "purple", "magenta"', bg_text)

# Corner Radius, border Width and background color
bg_style = gp.ButtonGroup(options)
bg_style.selected = "One"
bg_style.style.corner_radius = 20
bg_style.style.border_width = 5
bg_style.style.bg_color = "orange"
add_row(app, 'style.corner_radius = 20\nstyle.border_width = 5\nstyle.bg_color = "orange"', bg_style)

# Disabled text color
bg_disabled = gp.ButtonGroup(options)
bg_disabled.selected = "One"
bg_disabled.disabled = True
bg_disabled.style.text_disabled_color = "yellow"
add_row(app, 'disabled = True\nstyle.text_disabled_color = "yellow"', bg_disabled)

# Selected disabled color
bg_sel_disabled = gp.ButtonGroup(options)
bg_sel_disabled.selected = "Two"
bg_sel_disabled.style.selected_disabled_color = "tomato"
bg_sel_disabled.disabled = True
add_row(app, 'disabled = True\nstyle.selected_disabled_color = "tomato"', bg_sel_disabled)

# Unselected disabled color
bg_unsel_disabled = gp.ButtonGroup(options)
bg_unsel_disabled.selected = "Two"
bg_unsel_disabled.style.unselected_disabled_color = "lightcoral"
bg_unsel_disabled.disabled = True
add_row(app, 'disabled = True\nstyle.unselected_disabled_color = "lightcoral"', bg_unsel_disabled)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
