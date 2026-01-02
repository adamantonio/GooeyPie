import gooeypie as gp

def toggle_style(event):
    if btn.style.bg_color == "green":
        btn.style.bg_color = "red"
        btn.text = "Now Red"
    else:
        btn.style.bg_color = "green"
        btn.text = "Now Green"

app = gp.GooeyPieApp("Style Test")

# --- Widget Creation ---
btn = gp.Button("Styled Button", toggle_style)
btn.style.bg_color = "green"
btn.style.hover_bg_color = "blue"
btn.style.corner_radius = 20

# --- Layout ---
app.add(btn, 1, 1)

app.run()
