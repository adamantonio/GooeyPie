import gooeypie as gp


def update_dropdown(event):
    try:
        secondary_dd.values = options[primary_dd.selected]
    except KeyError:
        secondary_dd.values = []

def update_state(event):
    state_dd.disabled = not state_chk.checked


options = {
    "Colours": ["Red", "Green", "Blue"],
    "Shapes": ["Circle", "Square", "Triangle"],
    "Fruits": ["Apple", "Banana", "Cherry"]
}

app = gp.GooeyPieApp("Dropdown Test")
# app.theme = "light"

# Widgets for dependency test
dependency_lbl = gp.Label("Dependency Test")
primary_dd = gp.Dropdown(["", "Colours", "Shapes", "Fruits"])
primary_dd.add_event_listener("change", update_dropdown)
secondary_dd = gp.Dropdown()

# Widgets for state test
state_lbl = gp.Label("State Test")
state_dd = gp.Dropdown([f"Item {n}" for n in range(1, 11)])
state_chk = gp.Checkbox("Enabled")
state_chk.checked = True
state_chk.add_event_listener("change", update_state)

# Set up frame for dependency test
dependency_test_frame = gp.Frame()
dependency_test_frame.add(dependency_lbl, 1, 1, align_horizontal='center', column_span=2)
dependency_test_frame.add(primary_dd, 1, 2)
dependency_test_frame.add(secondary_dd, 2, 2)

# State frame
state_frame = gp.Frame()
state_frame.add(state_lbl, 1, 1, align_horizontal='center', column_span=2)
state_frame.add(state_dd, 1, 2) 
state_frame.add(state_chk, 2, 2)

# Add frames to app
app.add(dependency_test_frame, 1, 1,expand_horizontal=True)
app.add(state_frame, 1, 2,expand_horizontal=True)


app.set_column_weight(1, 1)

app.run()
