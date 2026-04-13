import gooeypie as gp

def update_greeting(event):
    """Updates the greeting message based on the user's name."""
    if name_entry.text:
        greeting_lbl.text = f"Hello, {name_entry.text}!"
    else:
        greeting_lbl.text = "Hello, friend!"

app = gp.GooeyPieApp("Hello, You!")

# Create widgets
question_lbl = gp.Label("What's your name?")

# Create entry widget and set event listener
name_entry = gp.Entry()
name_entry.width = 200

say_hello_btn = gp.Button("Say Hello", update_greeting)

greeting_lbl = gp.Label("")

# Add widgets to window
app.add(question_lbl, 1, 1)
app.add(name_entry, 1, 2)
app.add(say_hello_btn, 1, 3)
app.add(greeting_lbl, 1, 4)

app.run()
