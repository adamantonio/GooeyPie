import gooeypie as gp

def on_button_click(event):
    print(f"Button pressed: {event.widget.text}")

app = gp.GooeyPieApp("Scrollable Frame Test")

# Create a scrollable frame
scroll_frame = gp.ScrollableFrame()
scroll_frame.style.border_color = "green"
scroll_frame.style.border_width = 1
app.add(scroll_frame, 1, 1, expand_horizontal=True, expand_vertical=True)
app.set_row_weights(1)
app.set_column_weights(1)

# Add many items to demonstrate scrolling
for i in range(1, 11):
    lbl = gp.Label(f"Label {i}")
    scroll_frame.add(lbl, 1, i)
    
    btn = gp.Button(f"Button {i}", on_button_click)
    scroll_frame.add(btn, 2, i)

app.run()
