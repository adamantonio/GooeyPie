import gooeypie as gp

app = gp.GooeyPieApp("Switch Styles")
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

# Default
s_default = gp.Switch("Default")
add_row(app, 'gp.Switch("Default")', s_default)

# Disabled
s_disabled = gp.Switch("Disabled")
s_disabled.value = True
s_disabled.disabled = True
add_row(app, 'my_switch.disabled = True', s_disabled)

# Disabled text color
s_disabled_text = gp.Switch("Disabled text color")
s_disabled_text.style.text_disabled_color = "red"
s_disabled_text.disabled = True
add_row(app, 'style.text_disabled_color = "red"', s_disabled_text)

# Button disabled color
s_disabled_btn = gp.Switch("Button disabled color")
s_disabled_btn.style.button_disabled_color = "darkred"
s_disabled_btn.disabled = True
add_row(app, 'style.button_disabled_color = "darkred"', s_disabled_btn)

# Width
s_width = gp.Switch("Wide switch")
s_width.switch_width = 100
add_row(app, 'my_switch.switch_width = 100', s_width)

# Height
s_height = gp.Switch("Big switch")
s_height.switch_height = 50
s_height.switch_width = 100
add_row(app, 'my_switch.switch_height = 50\nmy_switch.switch_width = 100', s_height)

# Font
s_font = gp.Switch(text="Serif 18")
s_font.style.font_size = 18
s_font.style.font_name = "serif"
s_font.style.text_color = "blue", "skyblue"
add_row(app, 'style.font_size = 18\nstyle.font_name = "serif"\nstyle.text_color = "blue", "skyblue"', s_font)

# Background Colors
s_input = gp.Switch("Background colours")
s_input.style.off_bg_color = "darkgreen"
s_input.style.on_bg_color = "limegreen"
add_row(app, 'style.off_bg_color = "darkgreen"\nstyle.on_bg_color = "limegreen"', s_input)

# Button Colors
s_btn = gp.Switch(text="Blue Button")
s_btn.style.button_color = "skyblue"
s_btn.style.button_hover_color = "gold"
add_row(app, 'style.button_color = "skyblue"\nstyle.button_hover_color = "gold"', s_btn)

# Border Width
s_bw = gp.Switch(text="Thick Border")
s_bw.style.border_width = 5
add_row(app, 'style.border_width = 5', s_bw)

# Border Color
s_bc = gp.Switch("Colored border")
s_bc.style.border_color = "hotpink"
add_row(app, 'style.border_color = "hotpink"', s_bc)

# Corner Radius
s_rad = gp.Switch("Not so round")
s_rad.style.corner_radius = 5
add_row(app, 'style.corner_radius = 5', s_rad)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()