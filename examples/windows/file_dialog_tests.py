import gooeypie as gp

app = gp.GooeyPieApp()

open_file_window = gp.OpenFileWindow(app, "Open File")
# open_file_window.add_file_type("Text files", "*.txt")
open_file_window.add_file_type("All files", "*.*")

open_folder_window = gp.OpenFolderWindow(app, "Open Folder")

save_file_window = gp.SaveFileWindow(app, "Save File")
save_file_window.add_file_type("Text files", "*.txt")
save_file_window.add_file_type("All files", "*.*")

print(f'Open file path: {open_file_window.open()}')
print(f'Open folder path: {open_folder_window.open()}')
print(f'Save file path: {save_file_window.open()}')

app.run()
