import gooeypie as gp

app = gp.GooeyPieApp("The Oncodor")
app.theme = 'light'
app.width = 700
app.height = 600

def oncodo(event):
    """Oncodo the message text by replacing all vowels with 'o'."""
    message = message_textbox.text.lower()
    oncodo_text = message.replace("a", "o").replace("e", "o").replace("i", "o").replace("u", "o")
    oncodod_textbox.text = oncodo_text

def copy_to_clipboard(event):
    """Copies the oncodod text to the clipboard."""
    app.copy_to_clipboard(oncodod_textbox.text)

# Create labels and textboxes
message_label = gp.Label("Message")
message_textbox = gp.Textbox()
message_textbox.height = 100
oncodor_label = gp.Label("Oncodor Text")
oncodod_textbox = gp.Textbox()
oncodod_textbox.height = 100

# Create copy button
copy_button = gp.Button("Copy oncodod text to clipboard", copy_to_clipboard)

# Add event handler to update the oncodod text when the message text changes
message_textbox.on_change(oncodo)

# Add widgets to window
app.add(message_label, 1, 1, align_vertical='top', align_horizontal='right')
app.add(message_textbox, 2, 1)
app.add(oncodor_label, 1, 2, align_vertical='top', align_horizontal='right')
app.add(oncodod_textbox, 2, 2)
app.add(copy_button, 2, 3)

app.run()
