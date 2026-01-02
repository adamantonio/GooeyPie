import gooeypie as gp

app = gp.GooeyPieApp("Stretch Test")
app.width = 400

# --- Widget Creation ---
btn_normal = gp.Button("Normal Button")
btn_stretch_x = gp.Button("Stretch X")
btn_stretch_y = gp.Button("Stretch Y")
btn_stretch_both = gp.Button("Stretch Both")

# --- Layout ---
# Use weights to allow stretching
app.set_column_weight(1, 1)
app.set_row_weight(1, 1)
app.set_row_weight(2, 1)
app.set_row_weight(3, 1)
app.set_row_weight(4, 1)

app.add(btn_normal, 1, 1)
app.add(btn_stretch_x, 1, 2, expand_horizontal=True)
app.add(btn_stretch_y, 1, 3, expand_vertical=True)
app.add(btn_stretch_both, 1, 4, expand_horizontal=True, expand_vertical=True)

app.run()
