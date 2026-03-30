import customtkinter
import tkinter


def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())

app = customtkinter.CTk()
radio_var = tkinter.IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(
    app,
    text="CTkRadioButton 1",
    command=radiobutton_event,
    variable= radio_var,
    value=1,
    border_color='firebrick',
    fg_color='limegreen'
    )


radiobutton_2 = customtkinter.CTkRadioButton(app, text="CTkRadioButton 2",
                                             command=radiobutton_event, variable= radio_var, value=2)

radiobutton_1.pack(pady=40, padx=40)
radiobutton_2.pack(pady=40, padx=40)

app.mainloop()
