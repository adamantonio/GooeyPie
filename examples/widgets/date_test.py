import gooeypie as gp
from datetime import date, timedelta

def date_change(event):
    print(event.widget.date)


app = gp.GooeyPieApp("Dates test")

# Standard widget
standard_lbl = gp.Label('Standard')
standard_dt = gp.DatePicker()
app.add(standard_lbl, 1, 1)
app.add(standard_dt, 2, 1)

# Minimum and maximum dates
min_max_lbl = gp.Label('Min and max')
min_max_dt = gp.DatePicker()
min_max_dt.minimum_date = date.today() - timedelta(days=10)
min_max_dt.maximum_date = date.today() + timedelta(days=10)
app.add(min_max_lbl, 1, 2)
app.add(min_max_dt, 2, 2)

# Different date format
"""
Date Components:
%Y: Year with century (e.g., 2026).
%y: Year without century, zero-padded (e.g., 26).
%m: Month as a zero-padded decimal (e.g., 05).
%B: Full month name (e.g., May).
%b: Abbreviated month name (e.g., May).
%d: Day of the month, zero-padded (e.g., 31).
%A: Full weekday name (e.g., Sunday).
%a: Abbreviated weekday name (e.g., Sun).
"""
format_lbl = gp.Label(f'Format: %A, %B %d, %Y')
format_dt = gp.DatePicker()
format_dt.format = '%A %B %d, %Y'
app.add(format_lbl, 1, 3)
app.add(format_dt, 2, 3)

# No manual input
no_manual_input_lbl = gp.Label('No manual input')
no_manual_input_dt = gp.DatePicker()
no_manual_input_dt.allow_manual_input = False
app.add(no_manual_input_lbl, 1, 4)
app.add(no_manual_input_dt, 2, 4)

# Disabled
disabled_lbl = gp.Label("Disabled and set_today()")
disabled_dt = gp.DatePicker()
disabled_dt.set_today()
disabled_dt.disabled = True
app.add(disabled_lbl, 1, 5)
app.add(disabled_dt, 2, 5)

# Add/subtract months
add_months_lbl = gp.Label("Add/subtract months")
add_months_dt = gp.DatePicker()
add_months_dt.set_today()
add_months_dt.add_months(1)
app.add(add_months_lbl, 1, 6)
app.add(add_months_dt, 2, 6)

# Add/subtract
add_sub_frame = gp.Frame()
add_sub_lbl = gp.Label("Add/subtract")
add_days_dt = gp.DatePicker()
add_days_dt.set_today()
add_days_btn = gp.Button("Add 1 day", lambda event: add_days_dt.add_days(1))
minus_days_btn = gp.Button("Minus 1 day", lambda event: add_days_dt.add_days(-1))
add_months_btn = gp.Button("Add 1 month", lambda event: add_days_dt.add_months(1))
minus_months_btn = gp.Button("Minus 1 month", lambda event: add_days_dt.add_months(-1))
add_years_btn = gp.Button("Add 1 year", lambda event: add_days_dt.add_years(1))
minus_years_btn = gp.Button("Minus 1 year", lambda event: add_days_dt.add_years(-1))

add_sub_frame.add(add_sub_lbl, 1, 1)
add_sub_frame.add(add_days_dt, 2, 1)
add_sub_frame.add(add_days_btn, 3, 1)
add_sub_frame.add(minus_days_btn, 4, 1)
add_sub_frame.add(add_months_btn, 5, 1)
add_sub_frame.add(minus_months_btn, 6, 1)
add_sub_frame.add(add_years_btn, 7, 1)
add_sub_frame.add(minus_years_btn, 8, 1)

app.add(add_sub_frame, 1, 7, column_span=2)

# Operations
operations_lbl = gp.Label("Operations")
operations_frame = gp.Frame()
operations_dt = gp.DatePicker()
operations_dt.set_today()
open_btn = gp.Button("Open", lambda event: operations_dt.open())
clear_btn = gp.Button("Clear", lambda event: operations_dt.clear())
today_btn = gp.Button("Today", lambda event: operations_dt.set_today())
operations_frame.add(operations_lbl, 1, 1)
operations_frame.add(operations_dt, 2, 1)
operations_frame.add(open_btn, 3, 1)
operations_frame.add(clear_btn, 4, 1)
operations_frame.add(today_btn, 5, 1)

app.add(operations_frame, 1, 8, column_span=2)

# Get/set test
def set_date(event):
    get_set_dt.date_str = get_set_entry.text
    print(get_set_dt.date)

get_set_frame = gp.Frame()
get_set_lbl = gp.Label("Get and set")
get_set_dt = gp.DatePicker()
get_set_entry = gp.Entry()
get_set_btn = gp.Button("Set", set_date)

get_set_frame.add(get_set_lbl, 1, 1)
get_set_frame.add(get_set_dt, 2, 1)
get_set_frame.add(get_set_entry, 3, 1)
get_set_frame.add(get_set_btn, 4, 1)

app.add(get_set_frame, 1, 9, column_span=2)


# Events
def report_event(event):
    event_log.prepend_line(event.name)

event_frame = gp.Frame()
event_lbl = gp.Label("Events")
event_dt = gp.DatePicker()
event_log = gp.Textbox()
event_frame.add(event_lbl, 1, 1)
event_frame.add(event_dt, 2, 1)
event_frame.add(event_log, 3, 1)

# Events
event_dt.on_change(report_event)
event_dt.on_click(report_event)
event_dt.on_mouse_down(report_event)
event_dt.on_mouse_enter(report_event)
event_dt.on_mouse_leave(report_event)
event_dt.on_key_press(report_event)
event_dt.on_focus_gained(report_event)
event_dt.on_focus_lost(report_event)


app.add(event_frame, 1, 10, column_span=2)


standard_dt.on_change(date_change)
min_max_dt.on_change(date_change)


print(standard_dt.localization)

app.run()
