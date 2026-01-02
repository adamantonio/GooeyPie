import gooeypie as gp

def on_button_click(event):
    print(f"Entry text: {my_entry.text}")
    my_label.text = "Button Clicked!"
    my_button.text = "Well done!"


app = gp.GooeyPieApp("Hello GooeyPie")
app.theme = "dark"

my_label = gp.Label("Start typing...")
my_entry = gp.Entry("Type here")
my_button = gp.Button("Click Me", on_button_click)

app.add(my_label, 1, 1)
app.add(my_entry, 1, 2)
app.add(my_button, 1, 3)

app.run()
