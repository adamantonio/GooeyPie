import gooeypie as gp

app = gp.GooeyPieApp("Progressbar Styles")
app.width = 500

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

# Default
pb_default = gp.Progressbar(app)
pb_default.value = 50
add_row(app, 'gp.Progressbar(app)', pb_default)

# Custom Width
pb_width = gp.Progressbar(app)
pb_width.value = 60
pb_width.width = 300
add_row(app, 'width = 300', pb_width)

# Custom Height
pb_height = gp.Progressbar(app)
pb_height.value = 60
pb_height.height = 30
add_row(app, 'height = 30', pb_height)

# Progress Color
pb_color = gp.Progressbar(app)
pb_color.value = 70
pb_color.style.progress_color = "orange"
add_row(app, 'style.progress_color = "orange"', pb_color)

# Track (Trough) Color
pb_bg = gp.Progressbar(app)
pb_bg.value = 40
pb_bg.style.progress_color = "purple"
pb_bg.style.track_color = "lightgrey"
add_row(app, 'style.progress_color = "purple"\nstyle.track_color = "lightgrey"', pb_bg)

# Border
pb_border = gp.Progressbar(app)
pb_border.value = 30
pb_border.style.border_width = 2
pb_border.style.border_color = "red"
pb_border.style.progress_color = "red"
add_row(app, 'style.border_width = 2\nstyle.border_color = "red"', pb_border)

# Corner Radius (Round)
pb_round = gp.Progressbar(app)
pb_round.value = 80
pb_round.width = 250
pb_round.style.corner_radius = 10  # Less rounded (default is approx height/2)
# Note: CTkProgressBar is usually fully rounded by default. Setting corner_radius changes that.
add_row(app, 'style.corner_radius = 10', pb_round)

# Square edges
pb_square = gp.Progressbar(app)
pb_square.value = 50
pb_square.style.corner_radius = 0
add_row(app, 'style.corner_radius = 0', pb_square)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
