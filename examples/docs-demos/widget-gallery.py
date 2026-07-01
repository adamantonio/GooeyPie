import gooeypie as gp

def change_theme(e):
    if app.theme == "dark":
        app.theme = "light"
    else:
        app.theme = "dark"
        
    dp.clear()
    tb.select_none()

app = gp.GooeyPieApp("Widget Gallery")
app.theme = "dark"
app.width = 1500

widgets = []

image_button = gp.ImageButton("gooeypie_logo.png", None, "Image Button")
image_button.image_position = "top"
image_button.style.padding = 10

listbox = gp.Listbox(['Listbox 1', 'Listbox 2', 'Listbox 3'])
listbox.height = 120

textbox = gp.Textbox("")
textbox.height = 120

dp = gp.DatePicker()

tb = gp.Table(["Header 1", "Header 2"])
tb.add_row(["Data 1", "Data 2"])
tb.add_row(["Data 3", "Data 4"])
tb.add_row(["Data 5", "Data 6"])
tb.add_row(["Data 7", "Data 8"])
tb.height = 6

widgets.append(gp.Button("Button", None))
widgets.append(gp.ButtonGroup(['Button 1', 'Button 2', 'Button 3']))
widgets.append(gp.Checkbox("Checkbox"))
widgets.append(gp.Dropdown(['Dropdown 1', 'Dropdown 2', 'Dropdown 3']))
widgets.append(gp.Entry("Entry"))
widgets.append(image_button)
widgets.append(gp.Image("gooeypie_logo.png"))
widgets.append(gp.Label("Label"))
widgets.append(listbox)
widgets.append(gp.RadioGroup(['Radio 1', 'Radio 2', 'Radio 3']))
widgets.append(gp.Secret("Secret"))
widgets.append(gp.Slider(1, 10))
widgets.append(gp.Switch("Switch"))
widgets.append(textbox)
widgets.append(dp)
widgets.append(tb)

cols = 6
rows = (len(widgets) + 4) // 5

for i, widget in enumerate(widgets):
    col = i % cols + 1
    row = i // cols + 1

    if widget.__class__.__name__ in ['NOTDropdown', 'DatePicker']:
        app.add(widget, col, row, align_vertical='top')
    else:
        app.add(widget, col, row)



theme_switch = gp.Switch("Theme")
theme_switch.on_change(change_theme)

app.add(theme_switch, 1, 4, column_span=5)

# app.set_row_weights(*([1]*rows + [0]))

app.run()
