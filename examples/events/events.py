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

    if event.widget == btn and event.name == 'press':
        btn.remove_event_listener('mouse_over')


app = gp.GooeyPieApp("Event Test")

app.width = 1100
app.set_column_weight(1, 0)

app.set_column_weight(2, 1)
app.set_column_weight(3, 1)

lbl = gp.Label("I am a simple label")
btn = gp.Button("I am a simple button", log_event)
chk = gp.Checkbox("I am a simple checkbox")
entry = gp.Entry()
entry.width = 200

events = [
    'mouse_down',
    'mouse_up',
    'double_click',
    'triple_click',
    'middle_click',
    'right_click',
    'mouse_over',
    'mouse_out',
    'focus',
    'blur',
    'key_press',
    'change',
    'select',
]

for event in events:
    lbl.add_event_listener(event, log_event)
    btn.add_event_listener(event, log_event)
    chk.add_event_listener(event, log_event)
    entry.add_event_listener(event, log_event)

log_frame = gp.ScrollableFrame()
log_lbl = gp.Label()
log_frame.add(log_lbl, 1, 1)
log_frame.height = 500

detail_frame = gp.ScrollableFrame()
detail_lbl = gp.Label("Event Details")
detail_frame.add(detail_lbl, 1, 1)
detail_frame.height = 500

app.add(lbl, 1, 1)
app.add(btn, 1, 2)
app.add(chk, 1, 3)
app.add(entry, 1, 4)
app.add(log_frame, 2, 1, row_span=4, expand_horizontal=True, expand_vertical=True)
app.add(detail_frame, 3, 1, row_span=4, expand_horizontal=True, expand_vertical=True)

app.run()

