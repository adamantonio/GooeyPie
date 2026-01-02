import gooeypie as gp

def change_font(event):
    if event.widget == increase_font_size_btn:
        lbl.style.font_size += 5
    elif event.widget == decrease_font_size_btn:
        lbl.style.font_size -= 5


app = gp.GooeyPieApp("Font Test")

# --- Widget Creation ---
lbl = gp.Label("Default Font")
lbl.style.font_size = 30

increase_font_size_btn = gp.Button("Increase Font Size", change_font)
decrease_font_size_btn = gp.Button("Decrease Font Size", change_font)

# --- Layout ---
app.add(lbl, 1, 1)
app.add(increase_font_size_btn, 1, 2)
app.add(decrease_font_size_btn, 1, 3)

app.run()
