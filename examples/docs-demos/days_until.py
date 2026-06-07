import gooeypie as gp
from datetime import date

def show_days_until(event):
    if target_date.date:
        days_until = (target_date.date - date.today()).days
        days_until_lbl.text = f'{days_until} days to go!'
    else:
        days_until_lbl.text = ''


app = gp.GooeyPieApp('How long until...')

# Create widgets
target_date = gp.DatePicker()
target_date.minimum_date = date.today()
days_until_lbl = gp.Label()
days_until_lbl.style.font_size = 24

# Add widgets to window
app.add(target_date, 1, 1)
app.add(days_until_lbl, 1, 2)

target_date.on_change(show_days_until)

### For recording
def reset_and_switch(event):
    target_date.clear()
    days_until_lbl.text = ''
    app.theme = 'light' if app.theme == 'dark' else 'dark'

days_until_lbl.on_click(reset_and_switch)
###

app.run()
