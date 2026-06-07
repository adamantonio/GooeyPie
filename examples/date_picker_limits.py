import gooeypie as gp
from datetime import date, timedelta

app = gp.GooeyPieApp("Date Picker Limits Demo")
app.theme = "light"

# Create date picker with limits
dp = gp.DatePicker()
today = date.today()
future_28_days = today + timedelta(days=28)

dp.minimum_date = today
dp.maximum_date = future_28_days

# UI Layout
lbl_info = gp.Label("DatePicker with range bounds:")
lbl_info.style.font_weight = "bold"

lbl_range = gp.Label(f"Allowed range: {today} to {future_28_days}")
lbl_range.style.font_style = "italic"

lbl_status = gp.Label("Select a date from the datepicker")

def on_date_change(event):
    if dp.date:
        lbl_status.text = f"Selected Date: {dp.date}"
    else:
        lbl_status.text = "No date selected"

dp.on_change(on_date_change)

app.add(lbl_info, 1, 1, align_horizontal="left")
app.add(lbl_range, 1, 2, align_horizontal="left")
app.add(dp, 1, 3, align_horizontal="left")
app.add(lbl_status, 1, 4, align_horizontal="left")

# Demonstrate friendly validation error handling
print("Attempting to set maximum_date to yesterday (which is before minimum_date)...")
try:
    dp.maximum_date = today - timedelta(days=1)
except ValueError as e:
    print(f"Caught expected friendly error: {e}")

app.run()
