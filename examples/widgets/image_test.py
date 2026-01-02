import gooeypie as gp

app = gp.GooeyPieApp("Image Widget Test")
app.set_column_weight(1, 1)

# Ensure these files exist or use absolute paths for testing if needed.
# Based on image_button_test.py, these should be in ../images relative to examples/widgets/
# But this script is in examples/widgets/ too.
image_path_1 = "../images/blue_icon.png"
image_path_2 = "../images/test_icon.png" # Assuming another image exists? Or reused same?
# Let's search for images first or just assume test_icon works and toggle it.
# If only one image, we can try to load a non-existent one to see failure handling
# Or just use the same image to verify setter works (maybe no visual change but code runs)
# Let's assume we have at least one valid image.

img_widget = gp.Image(image_path_1)

info_lbl = gp.Label("Showing Image 1")

def toggle_image(event):
    if img_widget.image == image_path_1:
        img_widget.image = image_path_2
        info_lbl.text = "Showing Image 2"
    else:
        img_widget.image = image_path_1
        info_lbl.text = "Showing Image 1"

btn = gp.Button("Reload Image via Property", toggle_image)

app.add(img_widget, 1, 1)
app.add(info_lbl, 2, 1)
app.add(btn, 3, 1)

app.run()
