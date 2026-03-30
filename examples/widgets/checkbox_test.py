import gooeypie as gp
import random

def term_changed(event):
    print(accept_terms.text)
    if accept_terms.checked:
        print("Terms accepted")
    else:
        print("Terms not accepted")


def random_checkboxes(event):
    for chk in checkboxes:
        chk.checked = random.choice([True, False])

def toggle_state(event):
    disabled_chk.disabled = not disabled_chk.disabled

def get_set(event):
    if event.widget.text == "Get state":
        if disabled_chk.checked:
            status_lbl.text = "Checked"
        else:
            status_lbl.text = "Not checked"
    else:
        disabled_chk.checked = not disabled_chk.checked


app = gp.GooeyPieApp("Checkbox Example")
app.set_column_weight(1, 1)

accept_terms = gp.Checkbox("Accept terms")
accept_terms.on_change(term_changed)

check_frame = gp.Frame()
checkboxes = []
for x in range(5):
    for y in range(5):
        checkboxes.append(gp.Checkbox())
        check_frame.add(checkboxes[-1], x, y, align_horizontal="left")

random_btn = gp.Button("Random checkbox", random_checkboxes)
check_frame.add(random_btn, 0, 5, column_span=5)


disabled_btn = gp.Button("Disable/Enable", toggle_state)
disabled_chk = gp.Checkbox("Disable-able checkbox")
get_check_value = gp.Button("Get state", get_set)
set_check_value = gp.Button("Set state", get_set)
status_lbl = gp.Label("Status")

disabled_frame = gp.Frame()
disabled_frame.add(disabled_btn, 1, 1)
disabled_frame.add(disabled_chk, 2, 1)
disabled_frame.add(get_check_value, 3, 1)
disabled_frame.add(set_check_value, 4, 1)
disabled_frame.add(status_lbl, 5, 1)

large_chk = gp.Checkbox("Novelty checkbox")
large_chk.checkbox_width = 100
large_chk.checkbox_height = 100

app.add(accept_terms, 1, 1)
app.add(check_frame, 1, 2)

todo_frame = gp.Frame()
todo_frame.set_column_weight(2, 1)
for count in range(3):
    todo_chk = gp.Checkbox()
    todo_task = gp.Entry()
    todo_task.width = 400
    todo_frame.add(todo_chk, 1, count)
    todo_frame.add(todo_task, 2, count, expand_horizontal=True)

app.add(todo_frame, 1, 3, expand_horizontal=True)
app.add(disabled_frame, 1, 5)
app.add(large_chk, 1, 6)

app.run()
