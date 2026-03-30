import gooeypie as gp

def log_event(event):
    log_lbl.text = f"{event.name} on {event.widget.__class__.__name__}\n{log_lbl.text}"
    
    details = f"Event: {event.name}\n"
    details += f"Widget: {event.widget.__class__.__name__}\n"
    details += f"Key: {event.key}\n"
    details += f"X: {event.x}\n"
    details += f"Y: {event.y}\n"
    details += f"Original Event: {event.original_event}\n"
    
    detail_lbl.text = details

    if event.widget == btn and event.name == 'activate':
        btn.on_mouse_enter(None)


app = gp.GooeyPieApp("Event Test")

app.width = 1100
app.set_column_weight(1, 0)

app.set_column_weight(2, 1)
app.set_column_weight(3, 1)

lbl = gp.Label("I am a simple label")
btn = gp.Button("I am a simple button", log_event)
chk = gp.Checkbox("I am a simple checkbox")
dd = gp.Dropdown([f"Option {n}" for n in range(1,4)])

entry = gp.Entry()
entry.width = 200

def add_all_events(w):
    w.on_mouse_down(log_event)
    w.on_mouse_up(log_event)
    w.on_click(log_event)
    w.on_double_click(log_event)
    w.on_right_click(log_event)
    w.on_middle_click(log_event)
    w.on_mouse_enter(log_event)
    w.on_mouse_leave(log_event)
    w.on_focus_gained(log_event)
    w.on_focus_lost(log_event)
    w.on_key_press(log_event)
    if hasattr(w, 'on_change'):
        w.on_change(log_event)

add_all_events(lbl)
add_all_events(btn)
add_all_events(chk)
add_all_events(entry)

log_frame = gp.ScrollableFrame()
log_lbl = gp.Label()
log_frame.add(log_lbl, 1, 1)
log_frame.height = 500

detail_frame = gp.ScrollableFrame()
detail_lbl = gp.Label("Event Details")
detail_frame.add(detail_lbl, 1, 1)
detail_frame.height = 500

test_widgets = [
    lbl,
    btn,
    chk,
    entry,
    dd
]

for pos, widget in enumerate(test_widgets, 1):
    app.add(widget, 1, pos)

app.add(log_frame, 2, 1, row_span=len(test_widgets), expand_horizontal=True, expand_vertical=True)
app.add(detail_frame, 3, 1, row_span=len(test_widgets), expand_horizontal=True, expand_vertical=True)

app.run()

