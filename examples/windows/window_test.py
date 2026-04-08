import gooeypie as gp

def show_alert(event):
    # Depending on which button is clicked, we call alert on the appropriate window.
    # To demonstrate inheritance of icons, we will set an icon for the app, or just call alert.
    # We will use 'info' icon for the app, and 'warning' on the child window
    if event.widget == alert_btn:
        app.alert("Main App Alert", "This alert was generated from the Main App. It blocked the main app.", "info")
    elif event.widget == window_alert_btn:
        window.alert("Child Alert", "This alert comes from the child window.", "warning")

def show_window(event):
    if event.widget == show_btn:
        window.show()
    elif event.widget == show_on_top_btn:
        window.show_on_top()

def on_close(event):
    print("Close button pressed on child window")
    print(event)
    # Return True/None to allow hiding, False to prevent hiding
    return True

def on_show(event):
    print("Child window was shown")
    window.title = 'New Title'


app = gp.GooeyPieApp("Main Application")
# app.theme = "light"
app.width = 400

lbl = gp.Label("This is the main app.")
app.add(lbl, 1, 1)

window = gp.Window("Child Window")
window.width = 500
window.height = 500

window_lbl = gp.Label("This is the child window.")
window.add(window_lbl, 1, 1)

window.on_close(on_close)
window.on_show(on_show)

show_btn = gp.Button("Show Window", show_window)
show_on_top_btn = gp.Button("Show on top", show_window)
alert_btn = gp.Button("Alert Main", show_alert)
app.add(show_btn, 1, 2)
app.add(show_on_top_btn, 1, 3)
app.add(alert_btn, 1, 4)

window_alert_btn = gp.Button("Alert Child", show_alert)
window.add(window_alert_btn, 1, 2)

def trigger_alert():
    app.alert("Auto Alert", "This is an automatic alert trigger." * 10, "info")

# app._ctk_object.after(3000, end_test)
app._ctk_object.after(500, trigger_alert)

app.run()
