import gooeypie as gp

def light_switch_changed(event):
    """Changes the image based on the switch state."""
    if light_switch.value == True:
        light_img.image = "light-on.png"
    else:
        light_img.image = "light-off.png"


app = gp.GooeyPieApp("Light Switcher")
app.width = 300
# app.theme = "light"

# Create image widget
light_img = gp.Image("light-off.png")

# Create switch widget and set event listener
light_switch = gp.Switch("Turn on light")
light_switch.on_change(light_switch_changed)

# Add widgets to window
app.add(light_img, 1, 1)
app.add(light_switch, 1, 2)

app.run()
