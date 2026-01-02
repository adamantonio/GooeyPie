import gooeypie as gp

app = gp.GooeyPieApp("Values Test")

# --- Widget Creation ---
btn1 = gp.Button("1,1")
btn2 = gp.Button("2,1 (Span Col 2)")
btn3 = gp.Button("1,2 (Span Row 2)")
btn4 = gp.Button("2,2")
btn5 = gp.Button("3,2")

# --- Layout ---
# Row 1
app.add(btn1, 1, 1)
app.add(btn2, 2, 1, column_span=2) # Spans col 2 and 3

# Row 2 & 3
app.add(btn3, 1, 2, row_span=2)    # Spans row 2 and 3
app.add(btn4, 2, 2)
app.add(btn5, 3, 2)

# Row 3 (filling in the rest)
btn6 = gp.Button("2,3")
btn7 = gp.Button("3,3")
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
