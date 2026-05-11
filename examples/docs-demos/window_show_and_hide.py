import gooeypie as gp

def open_on_top_window(event):
    on_top_window.show_on_top()

def open_other_window(event):
    other_window.show()

# Create main window
app = gp.GooeyPieApp('Other windows')
app.width = 250

on_top_btn = gp.Button('Open on top', open_on_top_window)
open_other_btn = gp.Button('Open other window', open_other_window)
app.add(on_top_btn, 1, 1)
app.add(open_other_btn, 1, 2)

# Create on top window
on_top_window = gp.Window('On top window')
on_top_window.width = 300
on_top_message = gp.Label('This window is on top')
on_top_window.add(on_top_message, 1, 1)

# Create other window
other_window = gp.Window('Other window')
other_window.width = 300
other_message = gp.Label('This is another window')
other_window.add(other_message, 1, 1)

def change_theme(event):
    app.theme = 'dark' if app.theme == 'light' else 'light'

on_top_btn.on_right_click(change_theme)

app.run()
