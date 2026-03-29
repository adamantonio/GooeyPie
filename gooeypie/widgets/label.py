import customtkinter as ctk
from .widget import GooeyPieWidget

class Label(GooeyPieWidget):
    _style_properties = ('active_bg_color', 'bg_color', 'border_color', 'border_width', 'button_color', 'button_hover_color', 'corner_radius', 'disabled_text_color', 'dropdown_bg_color', 'dropdown_font_name', 'dropdown_font_size', 'dropdown_hover_color', 'dropdown_text_color', 'font_name', 'font_size', 'font_style', 'font_weight', 'inactive_bg_color', 'justify', 'off_bg_color', 'on_bg_color', 'padding', 'placeholder_text_color', 'progress_color', 'selected_color', 'selected_hover_color', 'text_color', 'unselected_color', 'unselected_hover_color')

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
