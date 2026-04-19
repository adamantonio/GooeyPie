import gooeypie as gp

def display_minimum_spend(event):
    """Display the minimum spend for the selected plan."""
    plan = plan_radios.selected
    if plan == "Super saver":
        result_label.text = "Minimum spend: $180"
    elif plan == "Standard":
        result_label.text = "Minimum spend: $250"
    elif plan == "Premium":
        result_label.text = "Minimum spend: $350"

app = gp.GooeyPieApp("Plan Selector")
# app.theme = 'light'
app.width = 500
app.height = 550

# Plan selection label and radio buttons
plan_label = gp.Label("Select your plan:")
plan_radios = gp.RadioGroup(["Super saver", "Standard", "Premium"])

# Update minimum spend when the selection changes
plan_radios.on_change(display_minimum_spend)

# Frame for plan details
plan_frame = gp.Frame()
plan_frame.add(plan_label, 1, 1, align_horizontal="left")
plan_frame.add(plan_radios, 1, 2, align_horizontal="left")

# Result label
result_label = gp.Label()

# Add widgets to window
app.add(plan_frame, 1, 1, expand_horizontal=True)
app.add(result_label, 1, 2)

app.run()