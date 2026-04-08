import gooeypie as gp


def on_change(event):
    lbl_status.text = f"Selection: {event.widget.selected}"
    print(f"Event triggered: {event.name}, Value: {event.widget.selected}")


def clear_selection(event):
    bg.selected = None
    lbl_status.text = "Selection: None"
    print("Selection cleared via property")

def select_opt2(event):
    bg.selected = "Option 2"
    # Note: setting property manually usually doesn't trigger the change event in some widgets 
    # unless implemented to do so. Our implementation doesn't explicit trigger it on setter,
    # which is standard behavior (events for user interaction).
    lbl_status.text = f"Selection: {bg.selected}"
    print("Set to Option 2 via property")



app = gp.GooeyPieApp("Button Group Test")
app.theme = "light"

lbl_status = gp.Label("Selection: None")
lbl_status.width = 150

options = ["Option 1", "Option 2", "Option 3"]
bg = gp.ButtonGroup(options)

bg.selected = "Option 2"
bg.on_change(on_change)

btn_clear = gp.Button("Clear Selection", clear_selection)
btn_select2 = gp.Button("Select Option 2", select_opt2)

app.add(lbl_status, 1, 1)
app.add(bg, 2, 1)
app.add(btn_clear, 3, 1)
app.add(btn_select2, 4, 1)

app.run()
