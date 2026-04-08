import gooeypie as gp

app = gp.GooeyPieApp("Weights Test")

btn1 = gp.Button("Button 1", None)
btn2 = gp.Button("Button 2", None)
btn3 = gp.Button("Button 3", None)

btn1.style.corner_radius = 5

app.add(btn1, 1, 1, expand_horizontal=True)
app.add(btn2, 2, 1, expand_horizontal=True)
app.add(btn3, 3, 1, expand_horizontal=True)

app.set_column_weights(0, 1, 2)

app.run()
