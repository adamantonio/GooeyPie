import gooeypie as gp

def on_click(event):
    print(f"Event Name: {event.name}")
    print(f"Event Widget: {event.widget}")
    lbl.text = f"Event from: {type(event.widget).__name__}"

app = gp.GooeyPieApp("Event Test")

# --- Widget Creation ---
btn = gp.Button("Click Me", on_click)
lbl = gp.Label("Waiting for event...")

# --- Layout ---
app.add(btn, 1, 1)
app.add(lbl, 1, 2)

app.run()
