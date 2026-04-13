import gooeypie as gp

def check_answer(event):
    """Checks the answers and gives feedback in a popup."""
    if python_chk.checked and java_chk.checked and not html_chk.checked and not css_chk.checked:
        feedback_lbl.text = 'You got it!'
    else:
        feedback_lbl.text = 'Not quite - try again!'


app = gp.GooeyPieApp("Quiz time!")

# Create question label and checkboxes
question_label = gp.Label("Which of the following are programming languages?")
python_chk = gp.Checkbox("Python")
html_chk = gp.Checkbox("HTML")
css_chk = gp.Checkbox("Esperanto")
java_chk = gp.Checkbox("Java")

# Create question frame and add question and answer checkboxes
question_frame = gp.Frame()
question_frame.add(question_label, 1, 1, align_horizontal="left")
question_frame.add(python_chk, 1, 2, align_horizontal="left")
question_frame.add(html_chk, 1, 3, align_horizontal="left")
question_frame.add(css_chk, 1, 4, align_horizontal="left")
question_frame.add(java_chk, 1, 5, align_horizontal="left")

# Create button and feedback label
check_answer_btn = gp.Button("Check Answer", check_answer)
feedback_lbl = gp.Label("")

# Add frame and widgets to the app
app.add(question_frame, 1, 1)
app.add(check_answer_btn, 1, 2)
app.add(feedback_lbl, 1, 3)

app.run()
