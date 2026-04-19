import gooeypie as gp

app = gp.GooeyPieApp("Volume Control")
app.width = 500
app.height = 500
# app.theme = 'light'

def update_volume(event):
    volume_level_lbl.text = f"Volume: {volume_slider.value}"

# Create widgets
volume_slider = gp.Slider(0, 100)
volume_slider.value = 50
volume_slider.orientation = "vertical"

volume_level_lbl = gp.Label("Volume: 50")
volume_level_lbl.style.font_size = 24
volume_level_lbl.style.font_weight = "bold"
volume_level_lbl.style.text_color = "darkmagenta", "hotpink"

# Add widgets to app
app.add(volume_slider, 1, 1)
app.add(volume_level_lbl, 2, 1)

app.set_column_weights(0, 1)

# Add event listener for slider
volume_slider.on_change(update_volume)

app.run()
