import gooeypie as gp

def dummy_event(event):
    print(f"Button '{event.widget.text}' pressed")

app = gp.GooeyPieApp("Button Styles")
# app.theme = "light"

# Header
code_header = gp.Label("Code")
code_header.style.font_size = 16
code_header.style.font_weight = "bold"
result_header = gp.Label("Result")
result_header.style.font_size = 16
result_header.style.font_weight = "bold"

# app.add(widget, column, row)
app.add(code_header, 1, 1)
app.add(result_header, 2, 1)

# Row 2: Default Button
l1 = gp.Label("Default Button")
l1.style.justify = "left"
b1 = gp.Button("Submit", dummy_event)
app.add(l1, 1, 2, align_horizontal='left')
app.add(b1, 2, 2, align_horizontal='center')

# Row 3: Disabled button (standard)
l9 = gp.Label("my_button.disabled = True")
l9.style.font_name = "Consolas", "monospace"
l9.style.justify = "left"
b9 = gp.Button("Disabled", dummy_event)
b9.disabled = True
app.add(l9, 1, 3, align_horizontal='left')
app.add(b9, 2, 3, align_horizontal='center')

# Row 4: Disabled button (style)
l10 = gp.Label("my_button.disabled = True\nmy_button.style.disabled_text_color = 'black'")
l10.style.font_name = "Consolas", "monospace"
l10.style.justify = "left"
b10 = gp.Button("Disabled", dummy_event)
b10.disabled = True
b10.style.disabled_text_color = 'black'
app.add(l10, 1, 4, align_horizontal='left')
app.add(b10, 2, 4, align_horizontal='center')

# Row 5: Width
l2 = gp.Label("my_button.width = 200")
l2.style.font_name = "Consolas", "monospace"
l2.style.justify = "left"
b2 = gp.Button("Fixed Width", dummy_event)
b2.width = 200
app.add(l2, 1, 5, align_horizontal='left')
app.add(b2, 2, 5, align_horizontal='center')

# Row 6: Height (NEW)
l_h = gp.Label("my_button.height = 50")
l_h.style.font_name = "Consolas", "monospace"
l_h.style.justify = "left"
b_h = gp.Button("Fixed Height", dummy_event)
b_h.height = 50
app.add(l_h, 1, 6, align_horizontal='left')
app.add(b_h, 2, 6, align_horizontal='center')

# Row 7: Background Color
l3 = gp.Label("my_button.style.bg_color = 'crimson'")
l3.style.font_name = "Consolas", "monospace"
l3.style.justify = "left"
b3 = gp.Button("Crimson", dummy_event)
b3.style.bg_color = 'crimson'
app.add(l3, 1, 7, align_horizontal='left')
app.add(b3, 2, 7, align_horizontal='center')

# Row 8: Hover Color
l4 = gp.Label("my_button.style.hover_bg_color = 'green'")
l4.style.font_name = "Consolas", "monospace"
l4.style.justify = "left"
b4 = gp.Button("Hover Me", dummy_event)
b4.style.hover_bg_color = 'green'
app.add(l4, 1, 8, align_horizontal='left')
app.add(b4, 2, 8, align_horizontal='center')

# Row 9: Corner Radius
l5 = gp.Label("my_button.style.corner_radius = 20")
l5.style.font_name = "Consolas", "monospace"
l5.style.justify = "left"
b5 = gp.Button("Rounded", dummy_event)
b5.style.corner_radius = 20
app.add(l5, 1, 9, align_horizontal='left')
app.add(b5, 2, 9, align_horizontal='center')

# Row 10: Border
l6 = gp.Label("my_button.style.border_width = 5 \n(and border_color or no effect)")
l6.style.font_name = "Consolas", "monospace"
l6.style.justify = "left"
b6 = gp.Button("Bordered", dummy_event)
b6.style.border_width = 5
b6.style.border_color = "orange"
app.add(l6, 1, 10, align_horizontal='left')
app.add(b6, 2, 10, align_horizontal='center')

# Row 11: Text Color (SPLIT)
l7 = gp.Label("my_button.style.text_color = 'yellow'")
l7.style.font_name = "Consolas", "monospace"
l7.style.justify = "left"
b7 = gp.Button("Colored Text", dummy_event)
b7.style.text_color = "yellow"
app.add(l7, 1, 11, align_horizontal='left')
app.add(b7, 2, 11, align_horizontal='center')

# Row 12: Font Size (SPLIT)
l8 = gp.Label("my_button.style.font_size = 20")
l8.style.font_name = "Consolas", "monospace"
l8.style.justify = "left"
b8 = gp.Button("Big Text", dummy_event)
b8.style.font_size = 20
app.add(l8, 1, 12, align_horizontal='left')
app.add(b8, 2, 12, align_horizontal='center')


# Row 13: Border spacing
l11 = gp.Label("my_button.style.padding = 10")
l11.style.font_name = "Consolas", "monospace"
l11.style.justify = "left"
b11 = gp.Button("Spacious button", dummy_event)
b11.style.padding = 20
app.add(l11, 1, 13, align_horizontal='left')
app.add(b11, 2, 13, align_horizontal='center')

app.run()
