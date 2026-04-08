import gooeypie as gp

def dummy_event(event):
    print(f"Button '{event.widget.text}' pressed")

app = gp.GooeyPieApp("Button Styles")
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

# Default Button
default_btn = gp.Button("Default", dummy_event)
add_row(app, 'my_button = gp.Button("Default", event_function)', default_btn)

# Disabled button (standard)
default_disabled_btn = gp.Button("Disabled", dummy_event)
default_disabled_btn.disabled = True
add_row(app, 'my_button.disabled = True', default_disabled_btn)

# Disabled text and button color
disabled_color_btn = gp.Button("Disabled", dummy_event)
disabled_color_btn.disabled = True
disabled_color_btn.style.text_disabled_color = 'pink'
disabled_color_btn.style.button_disabled_color = 'darkred'
add_row(app, "my_button.disabled = True\nmy_button.style.text_disabled_color = 'pink'\nmy_button.style.button_disabled_color = 'darkred'", disabled_color_btn)

# Width and height
width_height_btn = gp.Button("Wider and Taller", dummy_event)
width_height_btn.width = 200
width_height_btn.height = 50
add_row(app, 'my_button.width = 200\nmy_button.height = 50', width_height_btn)

# Button and text colour
text_hover_btn = gp.Button("Crimson", dummy_event)
text_hover_btn.style.text_color = 'black'
text_hover_btn.style.button_color = 'skyblue'
text_hover_btn.style.button_hover_color = 'lightgreen'
add_row(app, "my_button.style.text_color = 'black'\nmy_button.style.button_color = 'skyblue'\nmy_button.style.button_hover_color = 'lightgreen'", text_hover_btn)

# Corner Radius
corner_radius_btn = gp.Button("Rounded", dummy_event)
corner_radius_btn.style.corner_radius = 20
add_row(app, 'my_button.style.corner_radius = 20', corner_radius_btn)

# Border
border_btn = gp.Button("Bordered", dummy_event)
border_btn.style.border_width = 5
border_btn.style.border_color = "orange"
add_row(app, 'my_button.style.border_width = 5 \n(and border_color or no effect)', border_btn)

# Font
font_btn = gp.Button("Big Text", dummy_event)
font_btn.style.font_size = 20
font_btn.style.font_weight = "bold"
font_btn.style.font_name = "Consolas", "monospace"
add_row(app, 'my_button.style.font_size = 20\nmy_button.style.font_weight = "bold"\nmy_button.style.font_name = "Consolas", "monospace"', font_btn)

# Border spacing
padding_btn = gp.Button("Spacious button", dummy_event)
padding_btn.style.padding = 20
add_row(app, 'my_button.style.padding = 20', padding_btn)

app.run()
