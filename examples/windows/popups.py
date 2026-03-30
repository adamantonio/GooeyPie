import gooeypie as gp

app = gp.GooeyPieApp("Popups Test")
# app.theme = 'light'

def show_popup(event):
    title = title_entry.text
    message = message_entry.text
    category = category_dropdown.selected

    if event.widget == alert_btn:
        app.alert(title, message, category)
        result = -1  # No return value
    elif event.widget == ok_cancel_btn:
        result = app.ask_ok_cancel(title, message, category)
    elif event.widget == yes_no_btn:
        result = app.ask_yes_no(title_entry.text, message_entry.text, category_dropdown.selected)
    elif event.widget == yes_no_cancel_btn:
        result = app.ask_yes_no_cancel(title_entry.text, message_entry.text, category_dropdown.selected)

    if result != -1:
        status.text = f"Result: {repr(result)}"


title_lbl = gp.Label("Popup title")
title_entry = gp.Entry()
title_entry.text = "Popup Title"

message_lbl = gp.Label("Popup message")
message_entry = gp.Textbox()
message_entry.text = "This is the message that will be displayed on the popup"

category_lbl = gp.Label("Select a category")
category_dropdown = gp.Dropdown(["info", "warning", "error", "question", "invalid category"])
category_dropdown.selected = "info"

alert_btn = gp.Button("Alert", show_popup)
ok_cancel_btn = gp.Button("OK/Cancel", show_popup)
yes_no_btn = gp.Button("Yes/No", show_popup)
yes_no_cancel_btn = gp.Button("Yes/No/Cancel", show_popup)

status = gp.Label()

app.add(title_lbl, 1, 1)
app.add(title_entry, 1, 2)
app.add(message_lbl, 1, 3)
app.add(message_entry, 1, 4)
app.add(category_lbl, 1, 5)
app.add(category_dropdown, 1, 6)
app.add(alert_btn, 1, 7)
app.add(ok_cancel_btn, 1, 8)
app.add(yes_no_btn, 1, 9)
app.add(yes_no_cancel_btn, 1, 10)
app.add(status, 1, 11)


app.run()