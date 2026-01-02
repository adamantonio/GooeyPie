import gooeypie as gp
import random

def term_changed(event):
    if accept_terms.checked:
        print("Terms accepted")
    else:
        print("Terms not accepted")

def random_checkboxes(event):
    for chk in checkboxes:
        chk.checked = random.choice([True, False])

app = gp.GooeyPieApp("Checkbox Example")
app.set_column_weight(1, 1)

accept_terms = gp.Checkbox("Accept terms")
accept_terms.add_event_listener("change", term_changed)

check_frame = gp.Frame()
checkboxes = []
for x in range(5):
    for y in range(5):
        checkboxes.append(gp.Checkbox())
        check_frame.add(checkboxes[-1], x, y, align_horizontal="left")

random_btn = gp.Button("Random checkbox", random_checkboxes)
check_frame.add(random_btn, 0, 5, column_span=5)

styled_chk = gp.Checkbox("Styled checkbox")
styled_chk.style.bg_color = "salmon"
styled_chk.style.hover_bg_color = "darksalmon"
styled_chk.style.text_color = "white"
styled_chk.style.corner_radius = 20
styled_chk.style.border_width = 2
styled_chk.style.border_color = "forestgreen"
styled_chk.style.text_color = "forestgreen"

disabled_chk = gp.Checkbox("Disabled checkbox")
disabled_chk.disabled = True

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
app.add(styled_chk, 1, 4)
app.add(disabled_chk, 1, 5)
app.add(large_chk, 1, 6)

app.run()
