import gooeypie as gp


app = gp.GooeyPieApp("Alignment Test")
app.width = 500
app.height = 400

btn_tl = gp.Button("Top Left", None)
btn_tr = gp.Button("Top Right", None)
btn_bl = gp.Button("Bottom Left", None)
btn_br = gp.Button("Bottom Right", None)
btn_c = gp.Button("Center", None)

app.add(btn_tl, 1, 1, align_horizontal="left", align_vertical="top")
app.add(btn_tr, 3, 1, align_horizontal="right", align_vertical="top")
app.add(btn_bl, 1, 3, align_horizontal="left", align_vertical="bottom")
app.add(btn_br, 3, 3, align_horizontal="right", align_vertical="bottom")

# Center Button across middle row
app.add(btn_c, 1, 2)

# app.set_row_weights(0, 1, 0)

app.run()
