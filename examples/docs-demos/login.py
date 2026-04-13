import gooeypie as gp

def check_login(event):
    if user_entry.text == 'admin' and pass_entry.text == 'bestpassword':
        status_label.text = '✔ Access granted!'
    else:
        status_label.text = '❌ Access denied!'

app = gp.GooeyPieApp('Login')

user_label = gp.Label("Username")
user_entry = gp.Entry()
pass_label = gp.Label("Password")
pass_entry = gp.Secret()
login_btn = gp.Button('Login', check_login)
status_label = gp.Label('')

app.add(user_label, 1, 1)
app.add(user_entry, 2, 1)
app.add(pass_label, 1, 2)
app.add(pass_entry, 2, 2)
app.add(login_btn, 2, 3)
app.add(status_label, 2, 4)

app.run()
