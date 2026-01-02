import customtkinter as ctk
from .widget import GooeyPieWidget

class Entry(GooeyPieWidget):
    def __init__(self, placeholder_text="", **kwargs):
        super().__init__(placeholder_text=placeholder_text, **kwargs)
        self._initial_text = None
    
    def _create_widget(self, master):
        self._ctk_object = ctk.CTkEntry(master, **self._constructor_kwargs)
        if self._initial_text:
            self._ctk_object.insert(0, self._initial_text)

    @property
    def text(self):
        if self._ctk_object:
            return self._ctk_object.get()
        return self._initial_text or ""
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.delete(0, 'end')
            self._ctk_object.insert(0, value)
        else:
            self._initial_text = value
    
    @property
    def placeholder(self):
         return self._get_property('placeholder_text')

    @placeholder.setter
    def placeholder(self, value):
        if self._ctk_object:
            self._ctk_object.configure(placeholder_text=value)
        self._constructor_kwargs['placeholder_text'] = value

    def clear(self):
        """Clears the text in the entry."""
        if self._ctk_object:
            self._ctk_object.delete(0, 'end')
        self._initial_text = None

    def select(self):
        """Selects all text in the entry."""
        if self._ctk_object:
            self._ctk_object.select_range(0, 'end')
