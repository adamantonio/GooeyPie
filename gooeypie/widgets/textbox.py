import customtkinter as ctk
from contextlib import contextmanager
from .widget import GooeyPieWidget


class Textbox(GooeyPieWidget):
    """A multi-line text input widget."""
    _style_properties = (
        'bg_color',
        'border_color',
        'border_width',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'text_color',
        'text_disabled_color',
    )

    def __init__(self, text="", **kwargs):
        self._disabled_text_color = kwargs.pop('text_color_disabled', None)
        self._original_text_color = None
        self._default_disabled_color = ["gray60", "gray40"]  # Lighter text for disabled state
        super().__init__(**kwargs)
        self._initial_text = text

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkTextbox(master, wrap="word", **self._constructor_kwargs)
        
        # Store original text color
        if self._original_text_color is None:
            self._original_text_color = self._ctk_object.cget('text_color')
            
        # Apply initial state color if needed
        self._update_text_color()

        if self._initial_text:
            with self._writeable():
                self._ctk_object.insert("1.0", self._initial_text)

    def _set_property(self, key, value):
        if key == 'text_disabled_color' or key == 'text_color_disabled':
            self._disabled_text_color = value
            self._update_text_color()
        elif key == 'text_color':
            self._original_text_color = value
            if not self.disabled:
                 super()._set_property(key, value)
        elif key == 'state':
            super()._set_property(key, value)
            self._update_text_color()
        else:
            super()._set_property(key, value)

    def _update_text_color(self):
        """Updates the text color based on current state (disabled/normal)."""
        if self.disabled:
            color = self._disabled_text_color
            if not color:
                color = self._default_disabled_color
            if self._ctk_object:
                self._ctk_object.configure(text_color=color)
        else:
            if self._original_text_color and self._ctk_object:
                self._ctk_object.configure(text_color=self._original_text_color)

    @contextmanager
    def _writeable(self):
        """Context manager that temporarily enables the widget if disabled, then restores its state."""
        was_disabled = self.disabled
        if was_disabled:
            self._ctk_object.configure(state='normal')
        try:
            yield
        finally:
            if was_disabled:
                self._ctk_object.configure(state='disabled')

    # --- text property ---

    @property
    def text(self):
        if self._ctk_object:
            return self._ctk_object.get("1.0", "end-1c")
        return self._initial_text

    @text.setter
    def text(self, value):
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.delete("1.0", "end")
                self._ctk_object.insert("1.0", value)
        else:
            self._initial_text = value

    # --- disabled property ---

    @property
    def disabled(self):
        # CTkTextbox does not support cget('state') directly, so track via constructor kwargs
        return self._constructor_kwargs.get('state', 'normal') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state
        self._update_text_color()

    # --- scrollbar property ---

    @property
    def scrollbar(self):
        return self._constructor_kwargs.get('activate_scrollbars', True)

    @scrollbar.setter
    def scrollbar(self, value):
        self._constructor_kwargs['activate_scrollbars'] = bool(value)

    # --- Methods ---

    def append(self, text):
        """Adds the string text to the end of the Textbox."""
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.insert("end", text)
        else:
            self._initial_text += text

    def prepend(self, text):
        """Adds the string text to the start of the Textbox."""
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.insert("1.0", text)
        else:
            self._initial_text = text + self._initial_text

    def append_line(self, text):
        """Adds the string text to the end of the Textbox on a new line."""
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.insert("end", "\n" + text)
        else:
            self._initial_text += "\n" + text

    def prepend_line(self, text):
        """Adds the string text to the start of the Textbox with a newline character."""
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.insert("1.0", text + "\n")
        else:
            self._initial_text = text + "\n" + self._initial_text

    def clear(self):
        """Clears all text from the Textbox."""
        if self._ctk_object:
            with self._writeable():
                self._ctk_object.delete("1.0", "end")
        else:
            self._initial_text = ""

    def scroll_to_start(self):
        """Scrolls the Textbox so that the text at the start is in view."""
        if self._ctk_object:
            self._ctk_object.see("1.0")

    def scroll_to_end(self):
        """Scrolls the Textbox so that the text at the end is in view."""
        if self._ctk_object:
            self._ctk_object.see("end")
