import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class Checkbox(GooeyPieWidget):
    _style_properties = (
        'border_color',
        'border_width',
        'checkbox_color',
        'checkbox_disabled_color',
        'checkbox_hover_color',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'text_color',
        'text_disabled_color',
    )

    _DEFAULT_CHECKBOX_DISABLED_COLOR = '#808080'

    def __init__(self, text="", checked=False, **kwargs):
        """
        A checkbox widget.
        
        Args:
            text (str): The text to display on the checkbox.
            checked (bool): Optional - Whether the checkbox is checked by default.
            **kwargs: Additional arguments for the widget.
        """
        super().__init__(text=text, **kwargs)
        self._checkbox_disabled_color = None
        self._saved_checkbox_color = None
        
        # Set the command to dispatch our 'change' event
        self._constructor_kwargs['command'] = lambda: self._handle_event('change')

        if not text and 'width' not in kwargs:
            # If no text is provided, we want the checkbox to comfortably fit the box
            # defaulting to a smaller width so it doesn't take up unnecessary space.
            # CTk default checkbox width is around 24.
            kwargs['width'] = 24 
            self._constructor_kwargs['width'] = 24

        self._initial_checked = checked

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkCheckBox(master, **self._constructor_kwargs)
        if self._initial_checked:
            self._ctk_object.select()

    @property
    def disabled(self):
        return super().disabled

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state

        # Swap checkbox color for the disabled variant
        if value:
            self._saved_checkbox_color = self._get_property('fg_color')
            disabled_color = self._checkbox_disabled_color or self._DEFAULT_CHECKBOX_DISABLED_COLOR
            self._set_property('fg_color', disabled_color)
        else:
            if self._saved_checkbox_color is not None:
                self._set_property('fg_color', self._saved_checkbox_color)
                self._saved_checkbox_color = None

    @property
    def checked(self):
        if self._ctk_object:
            return bool(self._ctk_object.get())
        return self._initial_checked

    @checked.setter
    def checked(self, value):
        if self._ctk_object:
            if value:
                self._ctk_object.select()
            else:
                self._ctk_object.deselect()
        else:
            self._initial_checked = bool(value)

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
            
            if not value and self.width == 0: 
                 # If we treat 0 or None as "auto" or "default"
                 pass
            
            if value:
                 # Adding text
                 if self._constructor_kwargs.get('width') == 24 and self.width == 24:
                     # It was likely our default "no text" width. Reset it.
                     self.width = 0
                     self._ctk_object.configure(width=0) 

        self._constructor_kwargs['text'] = value


    @property
    def size(self):
        return self._get_property('checkbox_width')

    @size.setter
    def size(self, value):
        if self._ctk_object:
            self._ctk_object.configure(checkbox_width=value, checkbox_height=value)
        self._constructor_kwargs['checkbox_width'] = value
        self._constructor_kwargs['checkbox_height'] = value

    def toggle(self):
        if self._ctk_object:
            self._ctk_object.toggle()

    def on_change(self, event_function):
        """Sets the event to be called when the checkbox state changes."""
        self._set_event('change', event_function)