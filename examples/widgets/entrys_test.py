import gooeypie as gp

app = gp.GooeyPieApp("Entry Test")
# app.theme = 'light'

empty_entry = gp.Entry()

disabled_entry = gp.Entry()
disabled_entry.disabled = True

placeholder_entry = gp.Entry("✒️ Placeholder entry")

styled_entry = gp.Entry()
styled_entry.text = 'Programmatically filled'
styled_entry.style.border_color = 'magenta'
styled_entry.style.border_width = 2
styled_entry.style.bg_color = 'thistle'
styled_entry.style.text_color = 'black'

styled_entry2 = gp.Entry('Green and square')
styled_entry2.style.placeholder_text_color = 'linen'
styled_entry2.style.border_width = 0
styled_entry2.style.corner_radius = 0
styled_entry2.style.bg_color = 'forestgreen'

long_entry = gp.Entry()
long_entry.style.font_name = 'Consolas'
long_entry.width = 300
long_entry.style.justify = 'center'

app.add(empty_entry, 1, 1)
app.add(disabled_entry, 1, 2)
app.add(placeholder_entry, 1, 3)
app.add(styled_entry, 1, 4)
app.add(styled_entry2, 1, 5)
app.add(long_entry, 1, 6)

app.run()
