import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class Button(GooeyPieWidget):
    def __init__(self, text, event_function, **kwargs):
        super().__init__(text=text, **kwargs)
        if event_function:
            self.add_event_listener('press', event_function)
        
        self._constructor_kwargs['command'] = lambda: self._handle_event('press')
    
    def _create_widget(self, master):
        self._ctk_object = ctk.CTkButton(master, **self._constructor_kwargs)

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
        self._constructor_kwargs['text'] = value


