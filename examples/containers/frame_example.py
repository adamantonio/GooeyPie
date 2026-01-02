import gooeypie as gp

def submit_form(event):
    result_label.text = f"Submitted: {name_entry.text} ({param_entry.text})"

app = gp.GooeyPieApp("Frame Example")
# app.theme = "light"

# --- Widget Creation ---
header = gp.Label("Main App Window")
header2 = gp.Label("<-- Is over there")
form_frame = gp.Frame()
form_frame.style.border_color = "limegreen"
form_frame.style.border_width = 1
result_label = gp.Label("Results will appear here")

# Frame contents
frame_title = gp.Label("Inside the Frame")
name_label = gp.Label("Name:")
name_entry = gp.Entry("Enter name")
param_label = gp.Label("Parameter:")
param_entry = gp.Entry()
submit_btn = gp.Button("Submit", submit_form)

# --- Layout ---

# Main App Layout
app.add(header, 1, 1)
app.add(header2, 2, 1)
app.add(form_frame, 1, 2, column_span=2)
app.add(result_label, 1, 3)

# Frame Layout
form_frame.add(frame_title, 1, 1)
form_frame.add(name_label, 1, 2)
form_frame.add(name_entry, 2, 2)
form_frame.add(param_label, 1, 3)
form_frame.add(param_entry, 2, 3)
form_frame.add(submit_btn, 1, 4)

app.run()
