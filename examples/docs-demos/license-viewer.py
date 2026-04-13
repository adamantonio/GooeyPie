import gooeypie as gp

app = gp.GooeyPieApp("License Viewer")
app.width = 300

# Read the license file
with open("license.txt", "r") as f:
    license_text = f.read()

# Display the license text in a textbox and make a button
license_txt = gp.Textbox(license_text)

# Make a button to close the window
close_btn = gp.Button("I accept the terms and conditions", None)

# Add widgets to window
app.add(license_txt, 1, 1, expand_horizontal=True)
app.add(close_btn, 1, 2)

app.run()
