import customtkinter as ctk
from .widget import GooeyPieWidget

class Dropdown(GooeyPieWidget):
    def __init__(self, values=None, selected_value=None, **kwargs):
        """
        :param values: A list or tuple of string values to populate the dropdown.
        :param selected_value: The initially selected value (optional).
        :param kwargs: Additional arguments for the widget.
        """
        if values is None:
            values = []
        
        # Validation: values MUST be a list or tuple, specifically NOT a string
        if isinstance(values, str):
            raise ValueError("Dropdown 'values' must be a list or tuple, not a string.")
        if not isinstance(values, (list, tuple)):
            raise ValueError("Dropdown 'values' must be a list or tuple.")

        # Convert to strings to ensure compatibility with underlying widget
        values = [str(v) for v in values]

        # If selected_value is provided, ensure it's in values (or handle nicely? Plan said raise error on setter)
        # For init, CTK usually defaults to first item if not set, or empty.
        # We will handle the initial selection event/logic.

        super().__init__(**kwargs)
        
        self._constructor_kwargs['values'] = values

        # Wire up the command to our event system
        # CTkComboBox calls command with the selected value
        self._constructor_kwargs['command'] = self._on_change

        self._initial_selected = selected_value

    def _create_widget(self, master):
        # Ensure default state is readonly unless explicitly disabled
        if self._constructor_kwargs.get('state') != 'disabled':
            self._constructor_kwargs['state'] = 'readonly'

        self._ctk_object = ctk.CTkComboBox(master, **self._constructor_kwargs)
        
        
        if self._initial_selected is not None:
             self.selected = self._initial_selected
        elif not self._constructor_kwargs['values']:
             # If no values and no initial selection, CTk defaults to "CTkComboBox" text. Clear it.
             self._ctk_object.set("")

    def _on_change(self, value):
        """Internal callback to handle CTk command and fire 'change' event"""
        self._handle_event('change')

    @property
    def selected(self):
        if self._ctk_object:
            return self._ctk_object.get()
        return self._initial_selected

    @selected.setter
    def selected(self, value):
        # Validation: value must be in current values
        current_values = self.values
        if value not in current_values:
            raise ValueError(f"Value '{value}' is not in the current values list: {current_values}")

        if self._ctk_object:
            self._ctk_object.set(value)
        else:
            self._initial_selected = value

    @property
    def values(self):
        if self._ctk_object:
            return self._ctk_object.cget('values')
        return self._constructor_kwargs['values']

    @values.setter
    def values(self, new_values):
        if isinstance(new_values, str):
            raise ValueError("Dropdown 'values' must be a list or tuple, not a string.")
        if not isinstance(new_values, (list, tuple)):
             raise ValueError("Dropdown 'values' must be a list or tuple.")

        # Convert to strings
        new_values = [str(v) for v in new_values]

        if self._ctk_object:
            self._ctk_object.configure(values=new_values)
            # If current selection is not in new values, reset to first item
            if self.selected not in new_values:
                if new_values:
                    self.selected = new_values[0]
                else:
                    self._ctk_object.set("") 
                    
        self._constructor_kwargs['values'] = new_values

    @property
    def disabled(self):
        return self._get_property('state') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'readonly'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state

