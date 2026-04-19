import gooeypie as gp

def toggle_secret(event):
    secret_entry.toggle()

app = gp.GooeyPieApp('Secret')
app.width = 800
app.height = 320
# app.theme = 'light'

# Create widgets
question_lbl = gp.Label("What's your secret?")
question_lbl.style.font_size = 16

secret_entry = gp.Secret()
secret_chk = gp.Checkbox("Show secret")

# Set event listener for checkbox to show or hide the secret
secret_chk.on_change(toggle_secret)

# Add widgets to window
app.add(question_lbl, 1, 1)
app.add(secret_entry, 1, 2, expand_horizontal=True)
app.add(secret_chk, 1, 3)

app.run()
