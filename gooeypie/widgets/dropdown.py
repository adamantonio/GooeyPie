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

        if 'hover_color' in self._constructor_kwargs:
            self._hover_color = self._constructor_kwargs.pop('hover_color')

        self._ctk_object = ctk.CTkComboBox(master, **self._constructor_kwargs)
        
        # Bind unified hover events to all components
        components = [self._ctk_object]
        if hasattr(self._ctk_object, '_entry'):
            components.append(self._ctk_object._entry)
            # Click to open
            self._ctk_object._entry.bind('<Button-1>', self._on_entry_click, add='+')
            # Use arrow cursor instead of text cursor
            self._ctk_object._entry.configure(cursor="arrow")
            
        if hasattr(self._ctk_object, '_canvas'):
            components.append(self._ctk_object._canvas)
            
        for comp in components:
            comp.bind('<Enter>', self._on_enter, add='+')
            comp.bind('<Leave>', self._on_leave, add='+')

        if self._initial_selected is not None:
             self.selected = self._initial_selected
        elif not self._constructor_kwargs.get('values'):
             # If no values and no initial selection, CTk defaults to "CTkComboBox" text. Clear it.
             self._ctk_object.set("")

    def _set_property(self, key, value):
        if key == 'hover_color':
            self._hover_color = value
        else:
            super()._set_property(key, value)

    def _apply_pending_properties(self):
        # Handle hover_color manually to prevent it reaching configure()
        if 'hover_color' in self._pending_properties:
            self._hover_color = self._pending_properties.pop('hover_color')
        super()._apply_pending_properties()

    def _on_enter(self, event):
        if self.disabled:
            return

        # 1. Apply Button Hover Color
        try:
            btn_hover = self._ctk_object.cget('button_hover_color')
            if btn_hover:
                # Capture normal button color if not already captured
                # Use a flag to ensure we don't capture the hover color itself if re-entering
                if not hasattr(self, '_temp_button_color'):
                    self._temp_button_color = self._ctk_object.cget('button_color')
                
                self._ctk_object.configure(button_color=btn_hover)
        except Exception:
            pass

        # 2. Apply Background (FG) Hover Color
        if hasattr(self, '_hover_color'):
             if not hasattr(self, '_temp_fg_color'):
                self._temp_fg_color = self._ctk_object.cget('fg_color')
             self._ctk_object.configure(fg_color=self._hover_color)

    def _on_leave(self, event):
        if self.disabled:
            return

        # Check if mouse is still inside the widget tree (Entry, Canvas, or Frame)
        # This prevents flickering when moving between Entry and Canvas
        try:
            x, y = self._ctk_object.winfo_pointerxy()
            widget_under_mouse = self._ctk_object.winfo_containing(x, y)
            
            # If the widget under mouse is one of our components, don't leave yet
            if widget_under_mouse is self._ctk_object or \
               (hasattr(self._ctk_object, '_entry') and widget_under_mouse is self._ctk_object._entry) or \
               (hasattr(self._ctk_object, '_canvas') and widget_under_mouse is self._ctk_object._canvas):
                return
        except Exception:
            # If checking fails (e.g. widget destroyed), proceed to restore
            pass

        # Restore button color
        if hasattr(self, '_temp_button_color'):
            self._ctk_object.configure(button_color=self._temp_button_color)
            del self._temp_button_color

        # Restore fg color
        if hasattr(self, '_temp_fg_color'):
            self._ctk_object.configure(fg_color=self._temp_fg_color)
            del self._temp_fg_color

    def _on_entry_click(self, event):
        if self.disabled:
            return
        # Open the dropdown menu
        if hasattr(self._ctk_object, '_open_dropdown_menu'):
            self._ctk_object._open_dropdown_menu()

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

