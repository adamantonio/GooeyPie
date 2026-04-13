import gooeypie as gp

app = gp.GooeyPieApp("Slider Styles")
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

# Default
s_default = gp.Slider(0, 10)
add_row(app, 'my_slider = gp.Slider(0, 10)', s_default)

# Disabled
s_disabled = gp.Slider(0, 10)
s_disabled.disabled = True
add_row(app, 'my_slider.disabled = True', s_disabled)

# Disabled with custom button color
s_disabled_color = gp.Slider(0, 10)
s_disabled_color.disabled = True
s_disabled_color.style.button_disabled_color = "darkred"
add_row(app, 'my_slider.disabled = True\nmy_slider.style.button_disabled_color = "darkred"', s_disabled_color)

# Width
s_width = gp.Slider(0, 10)
s_width.width = 100
add_row(app, 'my_slider.width = 100', s_width)

# Height
s_height = gp.Slider(0, 10)
s_height.height = 50
add_row(app, 'my_slider.height = 50', s_height)

# Background Colors
s_input = gp.Slider(0, 10)
s_input.style.active_bg_color = "darkgreen"
s_input.style.inactive_bg_color = "limegreen"
add_row(app, 'my_slider.style.active_bg_color = "darkgreen"\nmy_slider.style.inactive_bg_color = "limegreen"', s_input)

# Button Colors
s_btn = gp.Slider(0, 10)
s_btn.style.button_color = "orangered"
s_btn.style.button_hover_color = "gold"
add_row(app, 'my_slider.style.button_color = "orangered"\nmy_slider.style.button_hover_color = "gold"', s_btn)

# Border Color
s_bc = gp.Slider(0, 10)
s_bc.style.border_color = "darkorange"
s_bc.style.border_width = 2
add_row(app, 'my_slider.style.border_color = "darkorange"\nmy_slider.style.border_width = 2', s_bc)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()