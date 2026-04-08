import gooeypie as gp
import time

def selection(event):       
    if event.widget == selection_set_btn:
        selection_dd.selected = "Item 2"
    selection_status.text = f"Selected item is {selection_dd.selected}"

def update_dropdown(event):
    try:
        secondary_dd.values = options[primary_dd.selected]
    except KeyError:
        secondary_dd.values = []

def update_state(event):
    selection_dd.disabled = not selection_chk.checked


def standard_event(event):
    std_events_status.text = f"Event: {event.name} at {time.strftime('%H:%M:%S')}"
    if event.name == 'key_press':
        print(event.key)


options = {
    "Colours": ["Red", "Green", "Blue"],
    "Shapes": ["Circle", "Square", "Triangle"],
    "Fruits": ["Apple", "Banana", "Cherry"]
}

app = gp.GooeyPieApp("Dropdown Test")
# app.theme = "light"


# Test for selection
selection_lbl = gp.Label("Selection Test")
selection_dd = gp.Dropdown(["Item 1", "Item 2", "Item 3"])
selection_dd.on_change(selection)

selection_chk = gp.Checkbox("Enabled")
selection_chk.checked = True
selection_chk.on_change(update_state)
selection_get_btn = gp.Button("Get Selection", selection)
selection_set_btn = gp.Button("Set selection to Item 2", selection)
selection_status = gp.Label("Status")

selection_frame = gp.Frame()
selection_frame.add(selection_lbl, 1, 1)
selection_frame.add(selection_dd, 2, 1)
selection_frame.add(selection_chk, 3, 1)
selection_frame.add(selection_get_btn, 4, 1)
selection_frame.add(selection_set_btn, 5, 1)
selection_frame.add(selection_status, 6, 1)


# Test for change event and setting values dynamically
dependency_lbl = gp.Label("Dependency Test")
primary_dd = gp.Dropdown(["", "Colours", "Shapes", "Fruits"])
primary_dd.on_change(update_dropdown)
secondary_dd = gp.Dropdown()

dependency_test_frame = gp.Frame()
dependency_test_frame.add(dependency_lbl, 1, 1)
dependency_test_frame.add(primary_dd, 2, 1)
dependency_test_frame.add(secondary_dd, 3, 1)


# Standard events
std_events_lbl = gp.Label("Standard Events")
std_events_dd = gp.Dropdown(["Item 1", "Item 2", "Item 3"])
std_events_status = gp.Label("Status")

def add_all_events(w):
    w.on_mouse_down(standard_event)
    w.on_mouse_up(standard_event)
    w.on_double_click(standard_event)
    w.on_middle_click(standard_event)
    w.on_right_click(standard_event)
    w.on_mouse_enter(standard_event)
    w.on_mouse_leave(standard_event)
    w.on_focus_gained(standard_event)
    w.on_focus_lost(standard_event)
    w.on_key_press(standard_event)

add_all_events(std_events_dd)


std_events_frame = gp.Frame()
std_events_frame.add(std_events_lbl, 1, 1)
std_events_frame.add(std_events_dd, 2, 1)
std_events_frame.add(std_events_status, 3, 1)


# Add frames to app
app.add(selection_frame, 1, 1, align_horizontal="left")
app.add(dependency_test_frame, 1, 2, align_horizontal="left")
app.add(std_events_frame, 1, 3, align_horizontal="left")

app.run()
