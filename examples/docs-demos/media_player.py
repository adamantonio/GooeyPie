import gooeypie as gp

def media_control(event):
    if event.widget == play_btn:
        status_lbl.text = "Now playing"
    elif event.widget == pause_btn:
        status_lbl.text = "Media paused"
    elif event.widget == shuffle_btn:
        status_lbl.text = "Starting shuffle..."

app = gp.GooeyPieApp("Media Player")
app.theme = 'light'

# Create widgets
play_btn = gp.ImageButton("play.png", media_control)
pause_btn = gp.ImageButton("pause.png", media_control)
shuffle_btn = gp.ImageButton("shuffle.png", media_control, "Shuffle all")
status_lbl = gp.Label("Nothing playing")

# Add some additional space around the button
play_btn.style.padding = 10
pause_btn.style.padding = 10
shuffle_btn.style.padding = 10

# Add widgets to app
app.add(play_btn, 1, 1)
app.add(pause_btn, 2, 1)
app.add(shuffle_btn, 3, 1)
app.add(status_lbl, 1, 2, column_span=3)

app.run()
