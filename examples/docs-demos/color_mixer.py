import gooeypie as gp

app = gp.GooeyPieApp("Color Mixer")
# app.theme = 'light'

def update_color(event):
    # Convert RGB values to hex
    red_hex = f"{red_slider.value:02x}"
    green_hex = f"{green_slider.value:02x}"
    blue_hex = f"{blue_slider.value:02x}"

    # Set bg color
    color_swatch_lbl.style.bg_color = f"#{red_hex}{green_hex}{blue_hex}"

    # Update label
    color_code_lbl.text = f"RGB: ({red_slider.value}, {green_slider.value}, " \
        f"{blue_slider.value})\nHEX: #{red_hex}{green_hex}{blue_hex}"


# Create sliders
red_slider = gp.Slider(0, 255, 0)
green_slider = gp.Slider(0, 255, 0)
blue_slider = gp.Slider(0, 255, 0)

# Create frame for color swatch and label
color_frame = gp.Frame()
color_swatch_lbl = gp.Label()
color_swatch_lbl.width = 100
color_swatch_lbl.height = 100

color_code_lbl = gp.Label()
color_code_lbl.width = 150

# Add widgets to frame
color_frame.add(color_swatch_lbl, 1, 1)
color_frame.add(color_code_lbl, 1, 2)

# Add widgets to app
app.add(red_slider, 1, 1)
app.add(green_slider, 1, 2)
app.add(blue_slider, 1, 3)
app.add(color_frame, 2, 1, row_span=3)

# Add event listeners for sliders
red_slider.on_change(update_color)
green_slider.on_change(update_color)
blue_slider.on_change(update_color)

# Initialise the color swatch and label
update_color(None)

app.run()