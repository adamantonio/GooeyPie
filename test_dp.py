import gooeypie as gp
import datetime as dt

app = gp.GooeyPieApp('Date Picker Test')

dp = gp.DatePicker()
dp.date = dt.date(2023, 10, 15)

lbl = gp.Label('Selected Date:')

def on_date_change(event):
    lbl.text = f'Selected Date: {event.widget.date_str}'

dp.on_change(on_date_change)

def set_min_months(event):
    dp.subtract_months(1)
    
btn_sub = gp.Button('Sub', set_min_months)

def set_add_months(event):
    dp.add_months(1)

btn_add = gp.Button('Add', set_add_months)

app.add(dp, 1, 1)
app.add(lbl, 1, 2)
app.add(btn_sub, 1, 3)
app.add(btn_add, 1, 4)

# Test Styles
# dp.style.month_font_weight = "bold"
# dp.style.day_text_color = "red"
# dp.style.month_text_color = "blue"

app.run()
