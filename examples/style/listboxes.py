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
    # Reduce height of all listboxes
    widget.height = 100
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

# Multiple Selection
lb_multi = gp.Listbox(options, multiple_selection=True)
lb_multi.selected = ["Apple", "Cherry"]
add_row(app, 'multiple_selection=True', lb_multi)

# Disabled
lb_disabled = gp.Listbox(options)
lb_disabled.disabled = True
lb_disabled.selected = "Apple"
add_row(app, 'disabled = True', lb_disabled)

# Corner Radius & Border Width
lb_style = gp.Listbox(options)
lb_style.height = 100
lb_style.selected = "Apple"
lb_style.style.text_color = 'white'
lb_style.style.bg_color = "midnightblue"
lb_style.style.border_width = 1
lb_style.style.border_color = "magenta"
lb_style.style.corner_radius = 0
add_row(app, 'style.text_color = "white"\nstyle.bg_color = "midnightblue"\nstyle.border_width = 1\nstyle.border_color = "magenta"\nstyle.corner_radius = 0', lb_style)

# Unselected Color
lb_colors = gp.Listbox(options)
lb_colors.selected = "Fig"
lb_colors.style.text_color = 'black'
lb_colors.style.hover_color = "skyblue"
lb_colors.style.unselected_color = "lightblue"
lb_colors.style.selected_color = "steelblue"
add_row(app, 'style.text_color = "black"\nstyle.unselected_color = "lightblue"\nstyle.hover_color = "skyblue"\nstyle.selected_color = "steelblue"', lb_colors)

# # Text
lb_text = gp.Listbox(options)
lb_text.height = 100
lb_text.selected = "Grape"
lb_text.style.font_name = "monospace"
lb_text.style.font_size = 18
add_row(app, 'style.font_name = "monospace"\nstyle.font_size = 18', lb_text)

app.run()
