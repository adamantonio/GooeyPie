import gooeypie as gp

app = gp.GooeyPieApp("Message Form")
app.theme = "light"

# Name label and entry
name_label = gp.Label("Name")
name_entry = gp.Entry()

# Message label and textbox
message_label = gp.Label("Message")
message_entry = gp.Textbox()

submit_btn = gp.Button("Send Message", None)

# Add widgets, make sure widgets expand as needed
app.add(name_label, 1, 1)
app.add(name_entry, 2, 1, expand_horizontal=True)
app.add(message_label, 1, 2)
app.add(message_entry, 2, 2, expand_horizontal=True, expand_vertical=True)
app.add(submit_btn, 2, 3, align_horizontal="right")

# Set column weights
app.set_column_weights(0, 1)  # 2 columns, only grow the second one

# Set row weights
app.set_row_weights(0, 1, 0)  # 3 rows, only grow the middle one

# For recording
def change_theme(event):
    if app.theme == "light":
        app.theme = "dark"
    else:
        app.theme = "light"
submit_btn.on_right_click(change_theme)

app.run()
