import gooeypie as gp

# --- Sub-window 2 (opened from sub-window 1) ---

app = gp.GooeyPieApp("Main Window")
app.width = 350

def close_second_window(event):
    second_window.hide()

second_window = gp.Window("Second Sub-Window")
second_window.width = 350

second_lbl = gp.Label("This is the second sub-window,\nopened from the first sub-window.")
close_btn2 = gp.Button("Close", close_second_window)

second_window.add(second_lbl, 1, 1)
second_window.add(close_btn2, 1, 2)

# --- Sub-window 1 (opened from the main window) ---

def open_second_window(event):
    second_window.show()

def close_first_window(event):
    first_window.hide()

first_window = gp.Window("First Sub-Window")
first_window.width = 350

first_lbl = gp.Label("This is the first sub-window,\nopened from the main window.")
open_second_btn = gp.Button("Open Second Sub-Window", open_second_window)
close_btn1 = gp.Button("Close", close_first_window)

first_window.add(first_lbl, 1, 1)
first_window.add(open_second_btn, 1, 2)
first_window.add(close_btn1, 1, 3)

# --- Main window ---

def open_first_window(event):
    first_window.show()



main_lbl = gp.Label("This is the main window.")
open_first_btn = gp.Button("Open Sub-Window", open_first_window)

app.add(main_lbl, 1, 1)
app.add(open_first_btn, 1, 2)

app.run()
