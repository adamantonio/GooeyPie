import gooeypie as gp

def say_hi(event):
    """Update the greeting label based on the selected language."""
    if language_dd.selected == "English":
        greeting_lbl.text = "Hello!"
    elif language_dd.selected == "Spanish":
        greeting_lbl.text = "Hola!"
    elif language_dd.selected == "Japanese":
        greeting_lbl.text = "Konnichiwa!"
    elif language_dd.selected == "Chinese":
        greeting_lbl.text = "Nǐ hǎo!"


app = gp.GooeyPieApp("Say Hi")
app.theme = "light"

# Create label text and dropdown
say_hi_lbl = gp.Label("Say hi in:")
language_dd = gp.Dropdown(["English", "Spanish", "Japanese", "Chinese"])

# Create greeting label (initially empty)
greeting_lbl = gp.Label("")
greeting_lbl.style.font_size = 20
greeting_lbl.style.font_weight = "bold"
greeting_lbl.style.text_color = "blue", "skyblue"

# Add widgets to app
app.add(say_hi_lbl, 1, 1)
app.add(language_dd, 2, 1)
app.add(greeting_lbl, 1, 2, column_span=2)

# Call say_hi() when the dropdown selection changes
language_dd.on_change(say_hi)

app.run()
