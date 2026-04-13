import gooeypie as gp

def toggle_theme(event):
    """Toggles the theme of the application."""
    if app.theme == "light":
        app.theme = "dark"
    else:
        app.theme = "light"

app = gp.GooeyPieApp("Theme Switch")

# Create the frame and weather status image and text
weather_frame = gp.Frame()
weather_img = gp.Image("mostly-sunny.png")  # https://www.iconarchive.com/
weather_lbl = gp.Label("Mostly Sunny")
weather_lbl.style.font_size = 16

weather_frame.add(weather_img, 1, 1)
weather_frame.add(weather_lbl, 2, 1)

theme_switch = gp.Switch("Dark Mode")

# Set the initial position of the switch
if app.theme == "dark":
    theme_switch.value = True

# Add event listener for switch
theme_switch.on_change(toggle_theme)

app.add(weather_frame, 1, 1)
app.add(theme_switch, 1, 2)

app.run()
