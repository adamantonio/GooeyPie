import gooeypie as gp

app = gp.GooeyPieApp("Table Styles")
# app.theme = "light"

# Header
code_header = gp.Label("Code")
code_header.style.font_size = 16
code_header.style.font_weight = "bold"
result_header = gp.Label("Result")
result_header.style.font_size = 16
result_header.style.font_weight = "bold"

app.add(code_header, 1, 1)
app.add(result_header, 2, 1)

# Helper for code labels
_next_row = 2
def add_row(app, code_text, widget, align_code="left", align_widget="center"):
    global _next_row
    l = gp.Label(code_text)
    l.style.font_name = "Consolas", "monospace"
    l.style.justify = "left"
    app.add(l, 1, _next_row, align_horizontal=align_code)
    app.add(widget, 2, _next_row, align_horizontal=align_widget)
    _next_row += 1

# Default
t_default = gp.Table(['First name', 'Family name'])
t_default.height = 5
t_default.data = [
    ["Bruce", "Wayne"],
    ["Clark", "Kent"],
    ["Peter", "Parker"],
    ["Diana", "Prince"]
]

add_row(app, 'my_table = gp.Table(["First name", "Family name"])', t_default)

# Disabled
t_disabled = gp.Table(['First name', 'Family name'])
t_disabled.height = 5
t_disabled.disabled = True
t_disabled.data = [
    ["Bruce", "Wayne"],
    ["Clark", "Kent"],
    ["Peter", "Parker"],
    ["Diana", "Prince"]
]

add_row(app, 'my_table = gp.Table(["First name", "Family name"])\nmy_table.disabled = True', t_disabled)


# Styled
t_styled = gp.Table(['First name', 'Family name'])
t_styled.height = 5
t_styled.data = [
    ["Bruce", "Wayne"],
    ["Clark", "Kent"],
    ["Peter", "Parker"],
    ["Diana", "Prince"],
    ["Stephen", "Strange"],
    ["Wade", "Wilson"],
    ["Lois", "Lane"],
    ["Tony", "Stark"],
]

# Colours
t_styled.style.header_bg_color = "midnightblue"
t_styled.style.header_text_color = "cyan"
t_styled.style.table_bg_color = "black"
t_styled.style.text_color = "springgreen"
t_styled.style.selected_color = "darkmagenta"

# Text
t_styled.style.header_font_weight = 'bold'
t_styled.style.header_font_size = 14

add_row(app, 'my_table.style.header_bg_color = "midnightblue"\nmy_table.style.header_text_color = "cyan"\nmy_table.style.table_bg_color = "black"\nmy_table.style.text_color = "springgreen"\nmy_table.style.selected_color = "darkmagenta"\nmy_table.style.header_font_weight = "bold"', t_styled)

app.run()