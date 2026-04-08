import gooeypie as gp

def on_image_click(event):
    print("Image Button Clicked!")
    lbl.text = "Clicked!"

app = gp.GooeyPieApp("Image Button Test")

# --- Widget Creation ---
# Image button with text below
edit_btn = gp.ImageButton("../images/edit.png", on_image_click, "Edit")
edit_btn.image_position = "top"

# Image button with text to the right
save_btn = gp.ImageButton("../images/save.png", on_image_click, "Save")
save_btn.image_position = "left"

# Image button with no text
folder_btn = gp.ImageButton("../images/folder.png", on_image_click)


# Button styling

edit_btn.style.font_size = 20
edit_btn.style.padding = 10
save_btn.style.font_size = 20
save_btn.style.padding = 10
folder_btn.style.padding = 10

# edit_btn.style.button_color = 'white'
# edit_btn.style.button_hover_color = 'grey'
# edit_btn.style.text_color = 'black'
# save_btn.style.button_color = 'white'
# save_btn.style.button_hover_color = 'grey'
# save_btn.style.text_color = 'black'
# folder_btn.style.button_color = 'white'
# folder_btn.style.button_hover_color = 'grey'

lbl = gp.Label("Click the button")

# --- Layout ---
app.add(edit_btn, 1, 1)
app.add(save_btn, 1, 2)
app.add(folder_btn, 1, 3)
app.add(lbl, 1, 4)

app.run()


#  <a href="https://www.flaticon.com/free-icons/pencil" title="pencil icons">Pencil icons created by Freepik - Flaticon</a>
#  <a href="https://www.flaticon.com/free-icons/folder" title="folder icons">Folder icons created by Freepik - Flaticon</a>
#  <a href="https://www.flaticon.com/free-icons/save" title="save icons">Save icons created by Freepik - Flaticon</a>

