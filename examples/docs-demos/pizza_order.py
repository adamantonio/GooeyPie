import gooeypie as gp

def update_order(event):
    """Count the number of toppings selected"""
    order_lbl.text = f"You have selected {len(toppings_list.selected)} toppings."

def select_all(event):
    """Select all of the toppings!"""
    toppings_list.select_all()


# List of toppings
toppings = ["Pepperoni", "Mushrooms", "Extra Cheese", "Onions", "Ham", "Olives", "Pineapple", "Spinach", "Bacon"]

app = gp.GooeyPieApp("Pizza Order")
# app.theme = 'light'
app.height = 400

# Create toppings listbox and allow multiple selection
toppings_list = gp.Listbox(toppings)
toppings_list.multiple_selection = True

# Add event listener for listbox widget to update order
toppings_list.on_change(update_order)

# Create select all button and output label
select_all_btn = gp.Button("Select All", select_all)
order_lbl = gp.Label("")

# Add widgets to app
app.add(toppings_list, 1, 1, expand_horizontal=True, expand_vertical=True)
app.add(select_all_btn, 1, 2)
app.add(order_lbl, 1, 3)

# Set row weights so that the listbox takes up all available space
app.set_row_weights(1, 0, 0)

app.run()
