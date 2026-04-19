import gooeypie as gp
import time

def toggle_secret(event):
    test_secret.toggle()


app = gp.GooeyPieApp("Secret Test")


test_secret = gp.Secret("placeholder text")

test_secret.style.text_color = "red"
test_secret.style.placeholder_text_color = "blue"
test_secret.style.font_size = 24

toggle_button = gp.Button("Toggle", toggle_secret)

app.add(test_secret, 1, 1)
app.add(toggle_button, 1, 2)

app.run()
