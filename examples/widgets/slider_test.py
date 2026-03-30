import gooeypie as gp

def toggle_disabled(event):
    slider.disabled = not slider.disabled
    status_lbl.text = f"Disabled: {slider.disabled}"

def set_val_50(event):
    slider.value = 50
    status_lbl.text = f"Value set to 50"

def get_val(event):
    status_lbl.text = f"Current Value: {slider.value}"

def set_inc_10(event):
    slider.increment = 10
    status_lbl.text = "Increment set to 10"

def set_inc_1(event):
    slider.increment = 1
    status_lbl.text = "Increment set to 1"

def toggle_orientation(event):
    try:
        if slider.orientation == 'vertical':
            slider.orientation = 'horizontal'
        else:
            slider.orientation = 'vertical'
        status_lbl.text = f"Orientation: {slider.orientation}"
    except RuntimeError as e:
        status_lbl.text = f"Error: {e}"

def on_change(event):
    status_lbl.text = f"Change event: {slider.value}"

def toggle_colors(event):
    if slider.style.active_bg_color == "red":
        slider.style.active_bg_color = "blue"
        slider.style.inactive_bg_color = "gray"
    else:
        slider.style.active_bg_color = "red"
        slider.style.inactive_bg_color = "lightgray"
    status_lbl.text = f"Colors toggled"

app = gp.GooeyPieApp("Slider Test")
app.width = 600

slider = gp.Slider(0, 10)
slider.increment = 1
slider.on_change(on_change)

# Controls
btn_disable = gp.Button("Enable/Disable", toggle_disabled)
btn_set_50 = gp.Button("Set Value 50", set_val_50)
btn_get = gp.Button("Get Value", get_val)
btn_inc_10 = gp.Button("Inc 10", set_inc_10)
btn_inc_1 = gp.Button("Inc 1", set_inc_1)
btn_orient = gp.Button("Toggle Orient", toggle_orientation)
btn_colors = gp.Button("Toggle Colors", toggle_colors)
status_lbl = gp.Label("Status: Ready")

main = gp.Frame()
main.set_column_weight(1, 1)
main.add(slider, 1, 1, expand_horizontal=True)
main.add(btn_disable, 2, 1)
main.add(btn_set_50, 3, 1)
main.add(btn_get, 4, 1)
main.add(btn_inc_10, 5, 1)
main.add(btn_inc_1, 6, 1)
main.add(btn_orient, 7, 1)
main.add(btn_colors, 8, 1)
main.add(status_lbl, 9, 1)

app.set_column_weight(1, 1)
app.add(main, 1, 1, expand_horizontal=True)

app.run()
