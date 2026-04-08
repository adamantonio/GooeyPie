import gooeypie as gp

app = gp.GooeyPieApp("Clicker")
# app.theme = "light"

clicks = 0  # Number of times the button has been clicked

def click(event):
    """Increments the number of clicks and updates the button text."""
    global clicks
    clicks += 1
    if clicks < 10:
        clicker_btn.text = f"You have clicked me {clicks} times!"
    else:
        clicker_btn.disabled = True
        clicker_btn.text = "Okay, that's enough for one day"

# Create the button
clicker_btn = gp.Button("You have not clicked me yet!", click)
clicker_btn.width = 250

# Add button to the app
app.add(clicker_btn, 1, 1)

app.run()
