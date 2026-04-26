import gooeypie as gp

initially_disabled = True

def change_button_state(event):
    btn.disabled = not btn.disabled
    print(btn.disabled)

def button_press(event):
    print('Button pressed')

app = gp.GooeyPieApp('Bug?')

btn = gp.Button('Hello', button_press)
btn.disabled = initially_disabled
# btn.style.button_color = 'firebrick'
btn.style.button_disabled_color = 'skyblue'


chk = gp.Checkbox('Disable the button', initially_disabled)
chk.on_change(change_button_state)

app.add(btn, 1, 1)
app.add(chk, 1, 2)

app.run()
