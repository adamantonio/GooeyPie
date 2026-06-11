from customtkinter.windows.widgets import theme
from customtkinter.windows.widgets import theme
from customtkinter.windows.widgets import theme
import gooeypie as gp

def select_event(event):
    print("Selected:", event.widget.selected)

def remove_row(event):
    if tbl.selected_row is not None:
        tbl.remove_selected()

def add_row(event):
    tbl.add_row(["New", "Data", "Here"])

def clear_all(event):
    tbl.clear()

def switch_theme(event):
    app.theme = "dark" if theme_switch.value else "light"

app = gp.GooeyPieApp("Table Widget Test")
# app.theme = "light"
app.width = 500

tbl = gp.Table(["First Name", "Last Name", "Age"], multiple_selection=True)
tbl.data = [
    ["John", "Doe", 30],
    ["Jane", "Smith", 25],
    ["Bob", "Johnson", 40],
    ["Alice", "Brown", 28]
]
tbl.height = 10
tbl.on_change(select_event)

btn_add = gp.Button("Add Row", add_row)
btn_remove = gp.Button("Remove Selected", remove_row)
btn_clear = gp.Button("Clear All", clear_all)
theme_switch = gp.Switch("Dark mode")
theme_switch.value = True if app.theme == "dark" else False
theme_switch.on_change(switch_theme)

app.add(tbl, 1, 1, column_span=4, expand_horizontal=True)
app.add(btn_add, 1, 2)
app.add(btn_remove, 2, 2)
app.add(btn_clear, 3, 2)
app.add(theme_switch, 4, 2)

app.run()
