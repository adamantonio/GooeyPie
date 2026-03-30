"""
This example demonstrates a visual bug with the scrollable frame as implemented in CTk, whereby the scrollbar obscures the border when it is set.
"""


import customtkinter

class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # add widgets onto the frame...
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)
        self.label.configure(text="Hello World\n" * 50)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = MyFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20 )
        self.my_frame.configure(border_color="red", border_width=5)


app = App()
app.mainloop()
