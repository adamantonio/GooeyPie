import gooeypie as gp

app = gp.GooeyPieApp('Radiogroup Test')

main_container = gp.Frame()
main_container.set_column_weight(0, 1)

def on_change(event):
    print(f"Selection changed to: {event.widget.selected} (Index: {event.widget.selected_index})")
    lbl.text = f"Selected: {event.widget.selected} [{event.widget.selected_index}]"

# Vertical Radiogroup
rg_vertical = gp.Radiogroup(
    options=["Option 1", "Option 2", "Option 3"], 
    selected="Option 1"
)
rg_vertical.add_event_listener('change', on_change)
main_container.add(rg_vertical, 1, 1)

# Horizontal Radiogroup
rg_horizontal = gp.Radiogroup(
    options=["Item A", "Item B", "Item C"], 
    orientation="horizontal",
    selected="Item B"
)
main_container.add(rg_horizontal, 1, 2)

lbl = gp.Label("Selected: Option 1")
main_container.add(lbl, 1, 3)

def toggle_orientation(event):
    current = rg_vertical.orientation
    new_orientation = 'horizontal' if current == 'vertical' else 'vertical'
    rg_vertical.orientation = new_orientation
    print(f"Changed orientation to {new_orientation}")

btn = gp.Button("Toggle Orientation", toggle_orientation)
main_container.add(btn, 1, 4)

def toggle_disable_opt2_index(event):
    rg_vertical.disable_index(1) 
    print("Disabled index 1 (Option 2)")

btn_disable = gp.Button("Disable 'Option 2' (idx)", toggle_disable_opt2_index)
main_container.add(btn_disable, 1, 5)

def toggle_enable_opt2_item(event):
    rg_vertical.enable_item("Option 2")
    print("Enabled 'Option 2' (item)")

btn_enable = gp.Button("Enable 'Option 2' (text)", toggle_enable_opt2_item)
main_container.add(btn_enable, 1, 6)

def set_index_last(event):
    idx = len(rg_vertical.options) - 1
    rg_vertical.selected_index = idx
    print(f"Set selection to index {idx}")

btn_idx = gp.Button("Select Last Index", set_index_last)
main_container.add(btn_idx, 1, 7)

def new_handler(event):
    print(f"NEW HANDLER: Selection changed to: {event.widget.selected}")

def change_command(event):
    rg_vertical.remove_event_listener('change', on_change)
    rg_vertical.add_event_listener('change', new_handler)
    print("Changed command handler for Vertical Radiogroup")

btn_cmd = gp.Button("Set New Command", change_command)
main_container.add(btn_cmd, 1, 8)

app.set_column_weight(1, 1)
app.set_row_weight(1, 1)
app.add(main_container, 1, 1)

app.run()
