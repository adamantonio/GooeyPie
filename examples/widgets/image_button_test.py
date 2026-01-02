import gooeypie as gp

def on_image_click(event):
    print("Image Button Clicked!")
    lbl.text = "Clicked!"

app = gp.GooeyPieApp("Image Button Test")

# --- Widget Creation ---
# 'test_icon.png' must exist in the same folder as this script
img_btn = gp.ImageButton("../images/test_icon.png", on_image_click, text="With Text")
img_btn.image_position = "top"
lbl = gp.Label("Click the button")

# --- Layout ---
app.add(img_btn, 1, 1)
app.add(lbl, 1, 2)

app.run()
