import gooeypie as gp

def add_task(event):
    """Add the task to the task list if the Enter/Return key is pressed."""
    if event.key == "Return":
        todo_list.add_item(todo_entry.text)
        todo_entry.text = ""

def remove_task(event):
    """Remove the selected task from the task list if the double-click event is triggered."""
    todo_list.remove_selected()


app = gp.GooeyPieApp("Simple To-Do List")
# app.theme = 'light'

# Create widgets
instruction_lbl = gp.Label("Enter a task and press Enter to add it to the list.\nDouble-click a task to remove it.")
todo_entry = gp.Entry()
todo_list = gp.Listbox()

# Add event listener for entry widget to add new tasks
todo_entry.on_key_press(add_task)

# Add event listener for listbox widget to remove tasks
todo_list.on_double_click(remove_task)

app.add(instruction_lbl, 1, 1)
app.add(todo_entry, 1, 2, expand_horizontal=True)
app.add(todo_list, 1, 3, expand_horizontal=True)

todo_entry.focus()

app.run()
