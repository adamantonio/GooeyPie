import gooeypie as gp

app = gp.GooeyPieApp("Values Test")

# --- Widget Creation ---
btn1 = gp.Button("1,1", None)
btn2 = gp.Button("2,1 (Span Col 2)", None)
btn3 = gp.Button("1,2 (Span Row 2)", None)
btn4 = gp.Button("2,2", None)
btn5 = gp.Button("3,2", None)

# --- Layout ---
# Row 1
app.add(btn1, 1, 1)
app.add(btn2, 2, 1, column_span=2, expand_horizontal=True) # Spans col 2 and 3

# Row 2 & 3
app.add(btn3, 1, 2, row_span=2, expand_vertical=True)    # Spans row 2 and 3
app.add(btn4, 2, 2)
app.add(btn5, 3, 2)

# Row 3 (filling in the rest)
btn6 = gp.Button("2,3", None)
btn7 = gp.Button("3,3", None)
app.add(btn6, 2, 3)
app.add(btn7, 3, 3)

# Configure weights so we can see the spanning effect when resizing
app.set_column_weight(1, 1)
app.set_column_weight(2, 1)
app.set_column_weight(3, 1)
app.set_row_weight(1, 1)
app.set_row_weight(2, 1)
app.set_row_weight(3, 1)

app.run()
