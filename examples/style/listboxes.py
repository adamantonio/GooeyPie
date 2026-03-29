import gooeypie as gp

app = gp.GooeyPieApp("Listbox Styles")
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

options = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape"]

# Default
lb_default = gp.Listbox(options)
lb_default.selected = "Apple"
add_row(app, 'gp.Listbox(options)', lb_default)

# Height and Width
lb_wh = gp.Listbox(options)
lb_wh.selected = "Banana"
lb_wh.height = 100
lb_wh.width = 150
add_row(app, 'height = 100\nwidth = 150', lb_wh)

# Corner Radius & Border Width
lb_style = gp.Listbox(options)
lb_style.selected = "Apple"
lb_style.style.corner_radius = 20
lb_style.style.border_width = 5
lb_style.style.border_color = "red"
add_row(app, 'style.corner_radius = 20\nstyle.border_width = 5', lb_style)

# Selected Color
lb_sel = gp.Listbox(options)
lb_sel.selected = "Date"
lb_sel.style.selected_color = "red"
lb_sel.style.selected_hover_color = "darkred"
add_row(app, 'style.selected_color = "red"\nstyle.selected_hover_color = "darkred"', lb_sel)

# Unselected Color
lb_unsel = gp.Listbox(options)
lb_unsel.selected = "Fig"
lb_unsel.style.unselected_color = "lightblue"
lb_unsel.style.unselected_hover_color = "skyblue"
add_row(app, 'style.unselected_color = "lightblue"\nstyle.unselected_hover_color = "skyblue"', lb_unsel)

# Text Color
lb_text = gp.Listbox(options)
lb_text.selected = "Grape"
lb_text.style.font_name = "monospace"
lb_text.style.font_size = 18
lb_text.style.text_color = "purple", "magenta"
add_row(app, 'style.font_name = "monospace"\nstyle.font_size = 18\nstyle.text_color = "purple", "magenta"', lb_text)

# Multiple Selection
lb_multi = gp.Listbox(options, multiple_selection=True)
lb_multi.selected = ["Apple", "Cherry"]
add_row(app, 'multiple_selection=True', lb_multi)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()