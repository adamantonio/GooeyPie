import gooeypie as gp

app = gp.GooeyPieApp("Textbox Test")
# app.theme = "light"

def textbox_test(event):
    if event.widget == text_btn:
        print(textbox.text)
    elif event.widget == set_text_btn:
        textbox.text = "Hello World"
    elif event.widget == clear_btn:
        textbox.clear()
    elif event.widget == append_btn:
        textbox.append("Appended text")
    elif event.widget == prepend_btn:
        textbox.prepend("Prepended text")
    elif event.widget == append_line_btn:
        textbox.append_line("Appended line")
    elif event.widget == prepend_line_btn:
        textbox.prepend_line("Prepended line")
    elif event.widget == scroll_to_start_btn:
        textbox.scroll_to_start()
    elif event.widget == scroll_to_end_btn:
        textbox.scroll_to_end()


def change_state(event):
    if event.widget == disable_chk:
        textbox.disabled = disable_chk.checked

# Column 1: Operations

# Print text to console
text_btn = gp.Button("Print Text", textbox_test)

# Set text
set_text_btn = gp.Button("Set Text", textbox_test)

# Disable
disable_chk = gp.Checkbox("Disable", textbox_test)
disable_chk.checked = False
disable_chk.on_change(change_state)

# Clear text
clear_btn = gp.Button("Clear Text", textbox_test)

# Append text
append_btn = gp.Button("Append Text", textbox_test)

# Prepend text
prepend_btn = gp.Button("Prepend Text", textbox_test)

# Append line
append_line_btn = gp.Button("Append Line", textbox_test)

# Prepend line
prepend_line_btn = gp.Button("Prepend Line", textbox_test)

# Scroll to start
scroll_to_start_btn = gp.Button("Scroll to Start", textbox_test)

# Scroll to end
scroll_to_end_btn = gp.Button("Scroll to End", textbox_test)


# Column 2: Textbox
textbox = gp.Textbox()

operations_frame = gp.Frame()
widget_frame = gp.Frame()


for i, widget in enumerate([text_btn, set_text_btn, disable_chk, clear_btn, append_btn, prepend_btn, append_line_btn, prepend_line_btn, scroll_to_start_btn, scroll_to_end_btn]):
    operations_frame.add(widget, 1, i+1)

widget_frame.add(textbox, 1, 1, expand_vertical=True)
widget_frame.set_row_weights(1)

app.add(operations_frame, 1, 1)
app.add(widget_frame, 2, 1, expand_vertical=True)

app.set_column_weights(1, 1)

app.run()