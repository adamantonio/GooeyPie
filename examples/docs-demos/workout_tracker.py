import gooeypie as gp

app = gp.GooeyPieApp("Workout Tracker")
app.theme = 'light'

def add_exercise(event):
    """Adds the workout to the table and clears the entry fields."""
    exercise_tbl.add_row([exercise_entry.text, reps_entry.text])
    exercise_entry.clear()
    reps_entry.clear()
    exercise_entry.focus()

exercise_lbl = gp.Label('Exercise')
exercise_entry = gp.Entry()
reps_lbl = gp.Label('Reps')
reps_entry = gp.Entry()
add_btn = gp.Button('Add', add_exercise)

# Create table
exercise_tbl = gp.Table(['Exercise', 'Reps'])
exercise_tbl.set_column_widths(140, 80)
exercise_tbl.height = 5

app.add(exercise_lbl, 1, 1, align_horizontal="left")
app.add(exercise_entry, 2, 1, expand_horizontal=True)
app.add(reps_lbl, 1, 2, align_horizontal="left")
app.add(reps_entry, 2, 2, expand_horizontal=True)
app.add(add_btn, 2, 3, expand_horizontal=True)
app.add(exercise_tbl, 1, 4, expand_horizontal=True, column_span=2)

app.set_column_weights(0, 1)

app.run()
