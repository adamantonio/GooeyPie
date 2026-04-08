import gooeypie as gp

def say_hello(event):
    hello_lbl.text = "Hello GooeyPie!"

app = gp.GooeyPieApp("Hi!")
# app.theme = "light"
app.width = 400

hello_btn = gp.Button("Say hello", say_hello)
hello_lbl = gp.Label("")

app.add(hello_btn, 1, 1)
app.add(hello_lbl, 1, 2)

app.run()
