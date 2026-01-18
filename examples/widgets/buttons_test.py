import gooeypie as gp
import time


def button_press(event):
    simple_status.text = f"Button Pressed at {time.strftime('%H:%M:%S')}"

def toggle_state(event):
    disabled_btn.disabled = not disabled_btn.disabled

def button_status(event):
    disabled_status.text = f"Button Pressed at {time.strftime('%H:%M:%S')}"

def change_text(event):
    change_text_btn.text = "Text Changed"
    change_text_status.text = f"Button text is '{change_text_btn.text}'"


app = gp.GooeyPieApp("Buttons Test")
# app.theme = "light"


# Test the press event
simple_lbl = gp.Label("Simple Button")
simple_btn = gp.Button("Click Me", button_press)
simple_status = gp.Label("Status")

app.add(simple_lbl, 1, 1)
app.add(simple_btn, 3, 1)
app.add(simple_status, 4, 1)


# Test the disabled property
disabled_lbl = gp.Label("Disabled Button")
disable_action_btn = gp.Button("Toggle state", toggle_state)
disabled_btn = gp.Button("Try to click Me", button_status)
disabled_status = gp.Label("Status")

app.add(disabled_lbl, 1, 2)
app.add(disable_action_btn, 2, 2)
app.add(disabled_btn, 3, 2)
app.add(disabled_status, 4, 2)


# Test the text property
change_text_lbl = gp.Label("Change Text Button")
change_text_btn = gp.Button("Change Text", change_text)
change_text_status = gp.Label("Status")

app.add(change_text_lbl, 1, 3)
app.add(change_text_btn, 3, 3)
app.add(change_text_status, 4, 3)


app.run()
