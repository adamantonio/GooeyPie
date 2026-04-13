import gooeypie as gp

app = gp.GooeyPieApp("Metric conversion")

def convert(event):
    try:
        value = float(unit_entry.text)
        unit = unit_button.selected
        if unit == "inches":
            converted_label.text = f"{unit_entry.text} inches = {value * 2.54:0.4f} cm"
        elif unit == "feet":
            converted_label.text = f"{unit_entry.text} feet = {value * 0.3048:0.4f} m"
        elif unit == "miles":
            converted_label.text = f"{unit_entry.text} miles = {value * 1.60934:0.4f} km"
    except ValueError:
        converted_label.text = "Please enter a valid number"

# Create widgets
unit_entry = gp.Entry()
unit_button = gp.ButtonGroup(["inches", "feet", "miles"])
converted_label = gp.Label("")

# Call convert when the unit changes or the entry changes
unit_button.on_change(convert)
unit_entry.on_change(convert)

# Add widgets to the app
app.add(unit_entry, 1, 1)
app.add(unit_button, 2, 1)
app.add(converted_label, 1, 2, column_span=2)

app.run()
