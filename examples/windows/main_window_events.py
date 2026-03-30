import gooeypie as gp

app = gp.GooeyPieApp("Main Window Events")

def confirm_quit(event):
    print('Quit event!')
    if event.widget == app:
        print("Quit event triggered by closing the window")
    if event.widget == quit_btn:
        print("Quit event triggered by quit button")
    return app.ask_yes_no('Are you sure?', 'This will end the application. Do you really want to quit?', 'question')


def window_ready(event):
    print("Main window is ready")
    app.title = 'Main Window Events'



quit_btn = gp.Button("Quit", confirm_quit)
force_quit_btn = gp.Button("Force Quit", app.force_quit)


app.on_quit(confirm_quit)
app.on_load(window_ready)

app.add(quit_btn, 1, 1)
app.add(force_quit_btn, 1, 2)

app.run()
