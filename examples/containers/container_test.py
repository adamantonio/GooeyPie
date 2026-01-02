import gooeypie as gp

app = gp.GooeyPieApp("Container Test")

# Create all widgets
direct_lbl = gp.Label('This label and the button below is added directly to the window')
direct_btn = gp.Button('This button is on the window', None)

frame_lbl = gp.Label('This label and the button below is added to a frame')
frame_btn1 = gp.Button('Button 1 in frame', None)
frame_btn2 = gp.Button('Button 2 in frame', None)

container_lbl = gp.Label('This label and the button below is added to a container')
container_btn1 = gp.Button('Button 1 in container', None)
container_btn2 = gp.Button('Button 2 in container', None)

# Create containers
frame = gp.Frame()
container = gp.Container()

# Add widgets
app.add(direct_lbl, 1, 1)
app.add(direct_btn, 1, 2, align_horizontal='left')

frame.add(frame_lbl, 1, 1, column_span=2)
frame.add(frame_btn1, 1, 2)
frame.add(frame_btn2, 2, 2)

container.add(container_lbl, 1, 1, column_span=2)
container.add(container_btn1, 1, 2)
container.add(container_btn2, 2, 2)

app.add(container, 1, 3, align_horizontal='left')
app.add(frame, 1, 4, align_horizontal='left')

app.run()
