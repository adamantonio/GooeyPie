import customtkinter as ctk
from .widget import GooeyPieWidget

class Label(GooeyPieWidget):
    _style_properties = (
        'align',
        'bg_color',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'justify',
        'padding_x',
        'padding_y',
        'text_color',
        'text_disabled_color',
    )

    def __init__(self, text="", **kwargs):
        """
        A label widget.

        Args:
            text (str): The text to display on the label.
            **kwargs: Additional arguments for the widget.
        """
        kwargs.setdefault('text_color_disabled', ('gray74', 'gray60'))
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
        if key == 'align':
            # Map align values to CTk anchor
            align_to_anchor = {
                'left': 'w',
                'right': 'e',
                'center': 'center'
            }
            anchor = align_to_anchor.get(value, 'center')
            super()._set_property('anchor', anchor)
        elif key == 'padding_x':
            super()._set_property('padx', value)
        elif key == 'padding_y':
            super()._set_property('pady', value)
        elif key == 'text_disabled_color':
            super()._set_property('text_color_disabled', value)
        else:
            super()._set_property(key, value)
