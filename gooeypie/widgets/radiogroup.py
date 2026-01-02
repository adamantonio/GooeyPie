import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class Radiogroup(GooeyPieWidget):
    """A widget that displays a list of radio buttons."""

    def __init__(self, options, orientation='vertical', selected=None, **kwargs):
        """
        Args:
            options (list): A list of strings for the radio buttons.
            orientation (str): 'vertical' (default) or 'horizontal'.
            selected (str, optional): The initially selected option.
            **kwargs: Standard widget arguments.
        """
        super().__init__(**kwargs)
        self._options = options
        self._orientation = orientation
        self._initial_selected = selected
        self._radio_buttons = {}
        self._variable = None

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkFrame(master, fg_color="transparent", **self._constructor_kwargs)
        self._variable = ctk.StringVar(value=self._initial_selected if self._initial_selected else "")

        self._layout_radio_buttons()

    def _layout_radio_buttons(self):
        """Creates and places the radio buttons based on orientation."""
        # Clear existing buttons if any (though usually this is called once on creation, 
        # but if orientation changes we need to repack)
        for rb in self._radio_buttons.values():
            rb.destroy()
        self._radio_buttons.clear()

        for idx, option in enumerate(self._options):
            rb = ctk.CTkRadioButton(
                self._ctk_object, 
                text=option, 
                value=option, 
                variable=self._variable,
                command=lambda: self._handle_event('change')
            )
            self._radio_buttons[option] = rb
            
            if self._orientation == 'horizontal':
                rb.grid(row=0, column=idx, padx=(0, 10), pady=0, sticky="w")
            else:
                rb.grid(row=idx, column=0, padx=0, pady=(0, 10), sticky="w")

    @property
    def selected(self):
        if self._variable:
            return self._variable.get()
        return self._initial_selected

    @selected.setter
    def selected(self, value):
        if self._variable:
            self._variable.set(value)
        else:
            self._initial_selected = value

    @property
    def selected_index(self):
        """Gets or sets the index of the selected item."""
        current_selection = self.selected
        if not current_selection:
            return None
        try:
            return self._options.index(current_selection)
        except ValueError:
            return None

    @selected_index.setter
    def selected_index(self, index):
        if index is None:
            # Maybe clear selection? CtkRadiobutton group always needs a value or empty string.
            self.selected = ""
            return
            
        if not isinstance(index, int):
            raise TypeError("Index must be an integer")
            
        if 0 <= index < len(self._options):
            self.selected = self._options[index]
        else:
            raise IndexError(f"Index {index} out of range for Radiogroup options")

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        if value not in ('vertical', 'horizontal'):
            raise ValueError("Orientation must be 'vertical' or 'horizontal'")
        self._orientation = value
        if self._ctk_object:
            self._layout_radio_buttons()

    @property
    def options(self):
        return self._options
    
    # We generally don't support changing options dynamically in this simple version, 
    # but strictly speaking we could. For now let's keep it read-only or re-layout if needed.

    def disable_item(self, option):
        """Disables an individual radio button by its option text."""
        if option in self._radio_buttons:
            self._radio_buttons[option].configure(state='disabled')
        else:
            raise ValueError(f"Option '{option}' not found in Radiogroup")

    def enable_item(self, option):
        """Enables an individual radio button by its option text."""
        if option in self._radio_buttons:
            self._radio_buttons[option].configure(state='normal')
        else:
            raise ValueError(f"Option '{option}' not found in Radiogroup")

    def disable_index(self, index):
        """Disables an individual radio button by its index."""
        if 0 <= index < len(self._options):
            option = self._options[index]
            self.disable_item(option)
        else:
            raise IndexError(f"Index {index} out of range for Radiogroup options")

    def enable_index(self, index):
        """Enables an individual radio button by its index."""
        if 0 <= index < len(self._options):
            option = self._options[index]
            self.enable_item(option)
        else:
            raise IndexError(f"Index {index} out of range for Radiogroup options")
