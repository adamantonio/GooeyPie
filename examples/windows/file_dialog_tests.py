import gooeypie as gp

app = gp.GooeyPieApp()

def open_window(e):
    if window_dd.selected == "OpenFileWindow":
        open_file_window = gp.OpenFileWindow("Open File")
        open_file_window.add_file_type("Python files", "*.py")
        open_file_window.add_file_type("All files", "*.*")
        open_file_window.set_initial_folder(location_dd.selected)
        print(f'Open file path: {open_file_window.open()}')
    elif window_dd.selected == "OpenFolderWindow":
        open_folder_window = gp.OpenFolderWindow("Open Folder")
        open_folder_window.set_initial_folder(location_dd.selected)
        print(f'Open folder path: {open_folder_window.open()}')
    elif window_dd.selected == "SaveFileWindow":
        save_file_window = gp.SaveFileWindow("Save File")
        save_file_window.add_file_type("Text files", "*.txt")
        save_file_window.add_file_type("All files", "*.*")
        save_file_window.set_initial_folder(location_dd.selected)
        print(f'Save file path: {save_file_window.open()}')


window_dd = gp.Dropdown(['OpenFileWindow', 'OpenFolderWindow', 'SaveFileWindow'])
location_dd = gp.Dropdown(['home', 'documents', 'desktop', 'app'])
open_btn = gp.Button("Open", open_window)

window_dd.selected_index = location_dd.selected_index = 0

app.add(window_dd, 1, 1)
app.add(location_dd, 2, 1)
app.add(open_btn, 3, 1)

app.run()
