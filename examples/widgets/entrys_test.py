import gooeypie as gp
import time


def set_text(event):
    text_entry.text = "Text Set"

def get_text(event):
    text_status.text = f"Text is {repr(text_entry.text)}"

def clear_text(event):
    text_entry.clear()

def select_text(event):
    text_entry.select()

def focus_text(event):
    text_entry.focus()

def toggle_disabled_state(event):
    disabled_entry.disabled = not disabled_entry.disabled
    disabled_status.text = f"Disabled is {disabled_entry.disabled}, Entry text is {repr(disabled_entry.text)}"

def toggle_state(event):
    state_entry.disabled = not state_entry.disabled
    state_btn.text = 'Disabled' if state_entry.disabled else 'Enabled'

def state_text(event):
    if event.widget.text.startswith('Get'):
        state_status.text = f"Text is {repr(state_entry.text)}"
    else:
        state_entry.text = f"The time is {time.strftime('%H:%M:%S')}"

def standard_event(event):
    std_events_status.text = f"Event: {event.name} at {time.strftime('%H:%M:%S')}"
    if event.name == 'key_press':
        print(event.key)

def change_event(event):
    change_event_status.text = f"Text changed at {time.strftime('%H:%M:%S')} to {repr(change_event_entry.text)}"


app = gp.GooeyPieApp("Entry Test")
# app.theme = 'light'


# Test text operations
text_lbl = gp.Label("Text operations")
text_entry = gp.Entry()
text_set_btn = gp.Button("Set Text", set_text)
text_get_btn = gp.Button("Get Text", get_text)
text_clear_btn = gp.Button("Clear", clear_text)
text_select_btn = gp.Button("Select", select_text)
text_focus_btn = gp.Button("Focus", focus_text)
text_status = gp.Label("Status")

text_frame = gp.Frame()
text_frame.add(text_lbl, 1, 1)
text_frame.add(text_entry, 2, 1)
text_frame.add(text_set_btn, 3, 1)
text_frame.add(text_get_btn, 4, 1)
text_frame.add(text_clear_btn, 5, 1)
text_frame.add(text_select_btn, 6, 1)
text_frame.add(text_focus_btn, 7, 1)
text_frame.add(text_status, 8, 1)


# Test disabled property
disabled_lbl = gp.Label("Disabled property")
disable_btn = gp.Button("Toggle state", toggle_disabled_state)
disabled_entry = gp.Entry()
disabled_entry.text = "This can be disabled"
disabled_status = gp.Label("Status")

disabled_frame = gp.Frame()
disabled_frame.add(disabled_lbl, 1, 1)
disabled_frame.add(disable_btn, 2, 1)
disabled_frame.add(disabled_entry, 3, 1)
disabled_frame.add(disabled_status, 4, 1)


# Test operations with states
state_lbl = gp.Label("Operations while disabled")
state_btn  = gp.Button("Enabled", toggle_state)
state_entry = gp.Entry()
state_set_btn = gp.Button("Set text", state_text)
state_get_btn = gp.Button("Get text", state_text)
state_status = gp.Label("Status")

state_frame = gp.Frame()
state_frame.add(state_lbl, 1, 1)
state_frame.add(state_btn, 2, 1)
state_frame.add(state_entry, 3, 1)
state_frame.add(state_set_btn, 4, 1)
state_frame.add(state_get_btn, 5, 1)
state_frame.add(state_status, 6, 1)


# Standard events
std_events_lbl = gp.Label("Standard Events")
std_events_entry = gp.Entry()
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

add_all_events(std_events_entry)


std_events_frame = gp.Frame()
std_events_frame.add(std_events_lbl, 1, 1)
std_events_frame.add(std_events_entry, 2, 1)
std_events_frame.add(std_events_status, 3, 1)

# Change event
change_event_lbl = gp.Label("Change event")
change_event_entry = gp.Entry("Change Event")
change_event_entry.on_change(change_event)
change_event_status = gp.Label("Status")

change_event_frame = gp.Frame()
change_event_frame.add(change_event_lbl, 1, 1)
change_event_frame.add(change_event_entry, 2, 1)
change_event_frame.add(change_event_status, 3, 1)


# Add all frames to window
app.add(text_frame, 1, 1, align_horizontal="left")
app.add(disabled_frame, 1, 2, align_horizontal="left")
app.add(state_frame, 1, 3, align_horizontal="left")
app.add(std_events_frame, 1, 4, align_horizontal="left")
app.add(change_event_frame, 1, 5, align_horizontal="left")


app.run()
