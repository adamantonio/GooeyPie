import gooeypie as gp


def disable(event):
    event.widget.disabled = True

def change_text(event):
    event.widget.text = "Text Changed"

app = gp.GooeyPieApp("Buttons Test")
# app.theme = "light"

button_standard = gp.Button("Standard button (click to disable)", disable)

button_disabled = gp.Button("Disabled button", None)
button_disabled.disabled = True
button_disabled.style.disabled_text_color = "darkgray"

button_outline = gp.Button("Outline button", change_text)
button_outline.style.border_color = "violet"
button_outline.style.border_width = 2

button_square = gp.Button("Square button", None)
button_square.style.corner_radius = 0

button_colored = gp.Button("Colored button", None)
button_colored.style.bg_color = ("green", "tomato")
button_colored.style.hover_bg_color = ("darkgreen", "darkred")
button_colored.style.text_color = "white"

button_pill = gp.Button("Pill button", None)
button_pill.style.corner_radius = 20

button_spacious = gp.Button("Spacious button", None)
button_spacious.style.padding = 20

button_large = gp.Button("Large button", None)
button_large.style.text_color = "white"
button_large.width = 200
button_large.height = 100

app.add(button_standard, 1, 1)
app.add(button_disabled, 1, 2)
app.add(button_outline, 1, 3)
app.add(button_square, 1, 4)
app.add(button_colored, 1, 5)
app.add(button_pill, 1, 6)
app.add(button_spacious, 1, 7)
app.add(button_large, 1, 8)

app.run()
