import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class Button(GooeyPieWidget):

    _style_properties = (
        'border_color',
        'border_width',
        'button_color',
        'button_disabled_color',
        'button_hover_color',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'padding',
        'text_color',
        'text_disabled_color',
    )

    _DEFAULT_BUTTON_DISABLED_COLOR = '#808080'

    def __init__(self, text, event_function, **kwargs):
        super().__init__(text=text, **kwargs)
        self._button_disabled_color = None
        self._saved_button_color = None
        if event_function:
            self.add_event_listener('press', event_function)
        
        self._constructor_kwargs['command'] = lambda: self._handle_event('press')
    
    def _create_widget(self, master):
        self._ctk_object = ctk.CTkButton(master, **self._constructor_kwargs)

    @property
    def disabled(self):
        return super().disabled

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state

        # Swap button color for the disabled variant
        if value:
            self._saved_button_color = self._get_property('fg_color')
            disabled_color = self._button_disabled_color or self._DEFAULT_BUTTON_DISABLED_COLOR
            self._set_property('fg_color', disabled_color)
        else:
            if self._saved_button_color is not None:
                self._set_property('fg_color', self._saved_button_color)
                self._saved_button_color = None

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
        self._constructor_kwargs['text'] = value


