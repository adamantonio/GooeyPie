import gooeypie as gp

def on_button_click(event):
    print(f"Button pressed: {event.widget.text}")

app = gp.GooeyPieApp("Scrollable Frame Test")

# Create a scrollable frame
scroll_frame = gp.ScrollableFrame()
app.add(scroll_frame, 0, 0, expand_horizontal=True, expand_vertical=True)
app.set_row_weight(0, 1)
app.set_column_weight(0, 1)

# Add many items to demonstrate scrolling
for i in range(1, 11):
    lbl = gp.Label(f"Label {i}")
    scroll_frame.add(lbl, 0, i)
    
    btn = gp.Button(f"Button {i}", command=on_button_click)
    scroll_frame.add(btn, 1, i)

app.run()
