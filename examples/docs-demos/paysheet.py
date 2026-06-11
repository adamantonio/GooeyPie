import gooeypie as gp
import datetime as dt

app = gp.GooeyPieApp('Pay Calculator')
# app.theme = "light"

def add_hours(event):
    summary_tbl.add_row_to_top([date_dt.date, hours_inp.text])

def calculate_total_pay(event):
    hours = 0
    for row in summary_tbl.data:
        hours += float(row[1])
    total_pay = hours * float(rate_inp.text)
    total_lbl.text = f'Total pay: ${total_pay:.2f}'


date_lbl = gp.Label('Date')
date_dt = gp.DatePicker()
date_dt.format = '%d/%m/%Y'
date_dt.date_str = '25/12/2026'
hours_lbl = gp.Label('Hours worked')
hours_inp = gp.Entry()
add_btn = gp.Button('Add', add_hours)
summary_tbl = gp.Table(['Date', 'Hours'])
summary_tbl.set_column_widths(120, 50)
summary_tbl.height = 6
summary_tbl.set_column_alignments('center', 'center')
rate_lbl = gp.Label('Hourly rate')
rate_inp = gp.Entry()
calculate_btn = gp.Button('Calculate', calculate_total_pay)
total_lbl = gp.Label()
total_lbl.style.font_size = 14

app.width = 300
app.add(date_lbl, 1, 1, align_horizontal='right')
app.add(date_dt, 2, 1, align_horizontal='left')
app.add(hours_lbl, 1, 2, align_horizontal='right')
app.add(hours_inp, 2, 2, align_horizontal='left')
app.add(add_btn, 2, 3, align_horizontal='left')
app.add(summary_tbl, 1, 4, column_span=2, expand_horizontal=True)
app.add(rate_lbl, 1, 5, align_horizontal='right')
app.add(rate_inp, 2, 5, align_horizontal='left')
app.add(calculate_btn, 2, 6, align_horizontal='left')
app.add(total_lbl, 1, 7, column_span=2, align_horizontal='center')

app.run()
