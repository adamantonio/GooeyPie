import customtkinter as ctk
from .widget import GooeyPieWidget

class Label(GooeyPieWidget):
    def __init__(self, text="", **kwargs):
        super().__init__(text=text, **kwargs)
    
    def _create_widget(self, master):
        self._ctk_object = ctk.CTkLabel(master, **self._constructor_kwargs)

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
        self._constructor_kwargs['text'] = value

    def _set_property(self, key, value):
        if key == 'justify':
            # Map justify to anchor for single line alignment
            justify_to_anchor = {
                'left': 'w',
                'right': 'e',
                'center': 'center'
            }
            anchor = justify_to_anchor.get(value, 'center')
            super()._set_property('anchor', anchor)
            # Also set justify for multiline text
            super()._set_property('justify', value)
        else:
            super()._set_property(key, value)
