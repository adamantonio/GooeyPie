import gooeypie as gp

app = gp.GooeyPieApp("Textbox Styles")
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
t_default = gp.Textbox()
t_default.text = "This is a default textbox."

add_row(app, 'my_textbox = gp.Textbox()', t_default)

# Disabled
t_disabled = gp.Textbox()
# t_disabled.style.text_disabled_color = 'skyblue'
t_disabled.disabled = True
t_disabled.text = "This is a disabled textbox."
add_row(app, 'my_textbox.disabled = True', t_disabled)

# Border and colours
t_border = gp.Textbox()
t_border.style.border_width = 5
t_border.style.border_color = "green"
t_border.style.corner_radius = 0
t_border.style.bg_color = "darkblue"
t_border.style.text_color = "white"
t_border.text = "This textbox has a border but no corner radius."
add_row(app, 'my_textbox.style.border_width = 5\nmy_textbox.style.border_color = "green"\nmy_textbox.style.corner_radius = 10\nmy_textbox.style.bg_color = "darkblue"\nmy_textbox.style.text_color = "white"', t_border)

# Fonts
t_font = gp.Textbox()
t_font.style.font_name = "monospace"
t_font.style.font_size = 16
t_font.style.font_style = "italic"
t_font.style.font_weight = "bold"
t_font.text = "This textbox has a custom font."
add_row(app, 'my_textbox.style.font_name = "monospace"\nmy_textbox.style.font_size = 16\nmy_textbox.style.font_style = "italic"\nmy_textbox.style.font_weight = "bold"', t_font)

# Reduce height of all textboxes
for textbox in [t_default, t_disabled, t_border, t_font]:
    textbox.height = 100

# Configure columns
app.set_column_weights(1, 1)


app.run()