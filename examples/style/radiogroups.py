import gooeypie as gp

app = gp.GooeyPieApp("Progressbar Styles")
# app.theme = 'light'

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


sizes = ['Small', 'Medium', 'Large']

# Default
default_radios = gp.RadioGroup(sizes)
add_row(app, 'gp.RadioGroup(sizes)', default_radios)

# Styled
styled_radios = gp.RadioGroup(sizes)
styled_radios.style.checked_border_color = 'limegreen'
styled_radios.style.checked_border_width = 8
styled_radios.style.unchecked_border_color = 'firebrick'
styled_radios.style.hover_color = 'orange'
styled_radios.style.text_color = 'dodgerblue'
styled_radios.style.font_name = 'Serif'
styled_radios.style.font_size = 18
styled_radios.style.font_weight = 'bold'
styled_radios.style.size = 30
add_row(app, 'style.checked_border_color = "limegreen"\nstyle.checked_border_width = 8\nstyle.unchecked_border_color = "firebrick"\nstyle.hover_color = "orange"\nstyle.text_color = "dodgerblue"\nstyle.font_size = 18\nstyle.font_weight = "bold"\nstyle.size = 30', styled_radios)

app.run()
