import gooeypie as gp

def update_progress(event):
    val = event.widget.value
    prog.value = val
    lbl_val.text = f"{val:.0f}%"

def start_indeterminate(event):
    prog_ind.start()

def stop_indeterminate(event):
    prog_ind.stop()

def toggle_width(event):
    current = prog.width
    new = 400 if current == 200 else 200
    prog.width = new
    prog_ind.width = new
    lbl_width.text = f"Width: {new}px"

app = gp.GooeyPieApp("Progressbar Test")
app.width = 500

# Determinate
lbl_det = gp.Label("Determinate Mode")
app.add(lbl_det, 1, 1)

prog = gp.Progressbar(app, mode='determinate')
prog.value = 50
app.add(prog, 1, 2)

lbl_val = gp.Label("50%")
app.add(lbl_val, 1, 3)

slider = gp.Slider(0, 100)
slider.value = 50
slider.on_change(update_progress)
app.add(slider, 1, 4)

# Indeterminate
lbl_ind = gp.Label("Indeterminate Mode")
app.add(lbl_ind, 1, 5, pady=(20, 5))

prog_ind = gp.Progressbar(app, mode='indeterminate')
app.add(prog_ind, 1, 6)

btn_start = gp.Button("Start", start_indeterminate)
app.add(btn_start, 1, 7)

btn_stop = gp.Button("Stop", stop_indeterminate)
app.add(btn_stop, 1, 8)

# Width Test
lbl_width = gp.Label("Width: 200px")
app.add(lbl_width, 1, 9, pady=(20, 5))

btn_width = gp.Button("Toggle Width", toggle_width)
app.add(btn_width, 1, 10)

app.run()
