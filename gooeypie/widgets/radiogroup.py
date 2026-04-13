import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class RadioGroup(GooeyPieWidget):
    """A widget that displays a list of radio buttons."""
    _style_properties = (
        'checked_border_color',
        'checked_border_width',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'hover_color',
        'size',
        'text_color',
        'text_disabled_color',
        'unchecked_border_color',
        'unchecked_border_width',
    )

    # Properties that are applied to child radio buttons, not the frame
    _RADIO_BUTTON_KEYS = {
        'checked_border_color', 'checked_border_width',
        'unchecked_border_color', 'unchecked_border_width',
        'hover_color', 'text_color', 'text_color_disabled',
        'size', 'font',
    }


    def _configure_radio_buttons(self, key, value, **ctk_kwargs):
        """Apply a CTk configure to all child radio buttons and store for future ones."""
        for rb in self._radio_buttons.values():
            rb.configure(**ctk_kwargs)
        self._pending_properties[key] = value

    def _get_property(self, key):
        """Get property from a child radio button rather than the frame."""
        if key in self._RADIO_BUTTON_KEYS:
            if self._radio_buttons:
                first_rb = next(iter(self._radio_buttons.values()))
                try:
                    if key == 'checked_border_color':
                        return first_rb.cget('fg_color')
                    elif key == 'unchecked_border_color':
                        return first_rb.cget('border_color')
                    elif key == 'checked_border_width':
                        return first_rb.cget('border_width_checked')
                    elif key == 'unchecked_border_width':
                        return first_rb.cget('border_width_unchecked')
                    elif key == 'text_color_disabled':
                        return first_rb.cget('text_color_disabled')
                    elif key == 'size':
                        return first_rb.cget('radiobutton_width')
                    else:
                        return first_rb.cget(key)
                except ValueError:
                    pass
            return self._pending_properties.get(key)
        return super()._get_property(key)

    def _set_property(self, key, value):
        """Apply style properties to all child radio buttons."""
        if key == 'checked_border_color':
            self._configure_radio_buttons(key, value, fg_color=value)
        elif key == 'unchecked_border_color':
            self._configure_radio_buttons(key, value, border_color=value)
        elif key == 'checked_border_width':
            self._configure_radio_buttons(key, value, border_width_checked=value)
        elif key == 'unchecked_border_width':
            self._configure_radio_buttons(key, value, border_width_unchecked=value)
        elif key == 'hover_color':
            self._configure_radio_buttons(key, value, hover_color=value)
        elif key == 'text_color':
            self._configure_radio_buttons(key, value, text_color=value)
        elif key == 'text_color_disabled':
            self._configure_radio_buttons(key, value, text_color_disabled=value)
        elif key == 'size':
            self._configure_radio_buttons(key, value, radiobutton_width=value, radiobutton_height=value)
        elif key == 'font':
            self._configure_radio_buttons(key, value, font=value)
        else:
            super()._set_property(key, value)

    def _apply_pending_properties(self):
        """Override to prevent radio-button properties from being applied to the frame."""
        if self._ctk_object and self._pending_properties:
            frame_props = {k: v for k, v in self._pending_properties.items() if k not in self._RADIO_BUTTON_KEYS}
            rb_props = {k: v for k, v in self._pending_properties.items() if k in self._RADIO_BUTTON_KEYS}
            if frame_props:
                self._ctk_object.configure(**frame_props)
            # Keep radio button properties for future _layout_radio_buttons calls
            self._pending_properties.clear()
            self._pending_properties.update(rb_props)

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
        kwargs = self._constructor_kwargs.copy()
        kwargs.pop('state', None)
        self._ctk_object = ctk.CTkFrame(master, fg_color="transparent", **kwargs)
        self._variable = ctk.StringVar(value=self._initial_selected if self._initial_selected else "")

        self._layout_radio_buttons()

    def _layout_radio_buttons(self):
        """Creates and places the radio buttons based on orientation."""
        for rb in self._radio_buttons.values():
            rb.destroy()
        self._radio_buttons.clear()

        # Build CTk kwargs from pending style properties
        style_kwargs = {}
        for key, value in self._pending_properties.items():
            if key == 'checked_border_color':
                style_kwargs['fg_color'] = value
            elif key == 'unchecked_border_color':
                style_kwargs['border_color'] = value
            elif key == 'checked_border_width':
                style_kwargs['border_width_checked'] = value
            elif key == 'unchecked_border_width':
                style_kwargs['border_width_unchecked'] = value
            elif key == 'hover_color':
                style_kwargs['hover_color'] = value
            elif key == 'text_color':
                style_kwargs['text_color'] = value
            elif key == 'text_color_disabled':
                style_kwargs['text_color_disabled'] = value
            elif key == 'size':
                style_kwargs['radiobutton_width'] = value
                style_kwargs['radiobutton_height'] = value
            elif key == 'font':
                style_kwargs['font'] = value

        state = self._constructor_kwargs.get('state', 'normal')

        for idx, option in enumerate(self._options):
            rb = ctk.CTkRadioButton(
                self._ctk_object, 
                text=option, 
                value=option, 
                variable=self._variable,
                command=lambda: self._handle_event('change'),
                state=state,
                **style_kwargs
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

    @property
    def disabled(self):
        """Gets or sets whether the entire radiogroup is disabled."""
        return self._constructor_kwargs.get('state', 'normal') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        self._constructor_kwargs['state'] = state
        if self._ctk_object:
            for rb in self._radio_buttons.values():
                rb.configure(state=state)

    def on_change(self, event_function):
        """Sets the event to be called when the selected radio button changes."""
        self._set_event('change', event_function)
