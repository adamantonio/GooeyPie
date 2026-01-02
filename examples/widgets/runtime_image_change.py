import gooeypie as gp

def toggle_image(event):
    if btn.image == "test_icon.png":
        btn.image = "blue_icon.png"
        lbl.text = "Now showing blue icon"
    else:
        btn.image = "test_icon.png"
        lbl.text = "Now showing red icon"

app = gp.GooeyPieApp("Runtime Image Change")

# --- Widget Creation ---
# Starts with red square
btn = gp.ImageButton("test_icon.png", toggle_image, text="Click to Toggle")
btn.image_position = "top"

lbl = gp.Label("Current: Red Icon")

# --- Layout ---
app.add(btn, 1, 1)
app.add(lbl, 1, 2)

app.run()
