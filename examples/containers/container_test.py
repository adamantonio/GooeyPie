import gooeypie as gp

def change_container_state(event):
    if event.widget == disable_container_switch:
        container.disabled = disable_container_switch.value
    else:
        frame.disabled = disable_frame_switch.value

app = gp.GooeyPieApp("Container Test")

# Create all widgets
direct_lbl = gp.Label('This label and the button below is added directly to the window')
direct_btn = gp.Button('This button is on the window', None)

container_lbl = gp.Label('This label and the button below is added to a container')
container_btn1 = gp.Button('Button 1 in container', None)
container_btn2 = gp.Button('Button 2 in container', None)

disable_container_switch = gp.Switch('Disable container')
disable_container_switch.on_change(change_container_state)

frame_lbl = gp.Label('This label and the button below is added to a frame')
frame_btn1 = gp.Button('Button 1 in frame', None)
frame_btn2 = gp.Button('Button 2 in frame', None)

disable_frame_switch = gp.Switch('Disable frame')
disable_frame_switch.on_change(change_container_state)

# Create containers
container = gp.Container()
container.style.border_color = "green"
container.style.border_width = 1

frame = gp.Frame()
frame.style.border_color = "red"
frame.style.border_width = 1

# Add widgets
app.add(direct_lbl, 1, 1)
app.add(direct_btn, 1, 2, align_horizontal='left')

container.add(container_lbl, 1, 1, column_span=2)
container.add(container_btn1, 1, 2)
container.add(container_btn2, 2, 2)

frame.add(frame_lbl, 1, 1, column_span=2)
frame.add(frame_btn1, 1, 2)
frame.add(frame_btn2, 2, 2)

app.add(container, 1, 3, align_horizontal='left')
app.add(disable_container_switch, 1, 4)

app.add(frame, 1, 5, align_horizontal='left')
app.add(disable_frame_switch, 1, 6)
app.run()
