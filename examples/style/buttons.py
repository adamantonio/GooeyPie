import gooeypie as gp

def dummy_event(event):
    print(f"Button '{event.widget.text}' pressed")

app = gp.GooeyPieApp("Button Styles")
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

# Default Button
b1 = gp.Button("Submit", dummy_event)
add_row(app, 'Default Button', b1)

# Disabled button (standard)
b9 = gp.Button("Disabled", dummy_event)
b9.disabled = True
add_row(app, 'my_button.disabled = True', b9)

# Disabled text color
b10 = gp.Button("Disabled", dummy_event)
b10.disabled = True
b10.style.text_disabled_color = 'black'
add_row(app, "my_button.disabled = True\nmy_button.style.text_disabled_color = 'black'", b10)

# Disabled button color
b10b = gp.Button("Disabled", dummy_event)
b10b.style.button_disabled_color = 'darkred'
b10b.disabled = True
add_row(app, "my_button.disabled = True\nmy_button.style.button_disabled_color = 'darkred'", b10b)

# Width
b2 = gp.Button("Fixed Width", dummy_event)
b2.width = 200
add_row(app, 'my_button.width = 200', b2)

# Height
b_h = gp.Button("Fixed Height", dummy_event)
b_h.height = 50
add_row(app, 'my_button.height = 50', b_h)

# Background Color
b3 = gp.Button("Crimson", dummy_event)
b3.style.button_color = 'crimson'
add_row(app, "my_button.style.button_color = 'crimson'", b3)

# Hover Color
b4 = gp.Button("Hover Me", dummy_event)
b4.style.button_hover_color = 'green'
add_row(app, "my_button.style.button_hover_color = 'green'", b4)

# Corner Radius
b5 = gp.Button("Rounded", dummy_event)
b5.style.corner_radius = 20
add_row(app, 'my_button.style.corner_radius = 20', b5)

# Border
b6 = gp.Button("Bordered", dummy_event)
b6.style.border_width = 5
b6.style.border_color = "orange"
add_row(app, 'my_button.style.border_width = 5 \n(and border_color or no effect)', b6)

# Text Color
b7 = gp.Button("Colored Text", dummy_event)
b7.style.text_color = "yellow"
add_row(app, "my_button.style.text_color = 'yellow'", b7)

# Font Size
b8 = gp.Button("Big Text", dummy_event)
b8.style.font_size = 20
add_row(app, 'my_button.style.font_size = 20', b8)

# Border spacing
b11 = gp.Button("Spacious button", dummy_event)
b11.style.padding = 20
add_row(app, 'my_button.style.padding = 10', b11)

# Configure columns
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)

app.run()
