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
    _DEFAULT_TEXT_DISABLED_COLOR = '#e0e0e0'

    def __init__(self, text, event_function, **kwargs):
        """
        Button widget

        Args:
            text (str): The text on the button
            event_function (function): The function to call when the button is clicked
            **kwargs: Additional arguments for the widget
        """
        if event_function is not None and not callable(event_function):
            raise TypeError(
                f"The event_function must be a function, but received {type(event_function).__name__}. "
                "Ensure that you specify only the name of the function (e.g. my_function), "
                "instead of passing the result of calling the function (e.g. my_function())."
            )
            
        super().__init__(text=text, **kwargs)
        self._button_disabled_color = None
        self._saved_button_color = None
        self._saved_text_disabled_color = None
        # Tracks whether the user has explicitly set a custom text_disabled_color via style.
        # cget() always returns a non-None value at runtime, so we can't use None as a sentinel.
        self._has_custom_text_disabled_color = False
        # Guard: True while the disabled setter is internally writing the disabled colour,
        # so _set_property won't re-route that write to _saved_button_color.
        self._applying_disabled_color = False
        if event_function:
            self.on_activate(event_function)
        
        self._constructor_kwargs['command'] = lambda: self._handle_event('activate')

    def _set_property(self, key, value):
        """Override to intercept external fg_color changes while disabled."""
        if key == 'fg_color' and self.disabled and not self._applying_disabled_color:
            # An external caller (e.g. style.button_color) is setting the button colour
            # while the button is disabled.  Store it as the value to restore on re-enable
            # rather than applying it to the live widget (which would show the enabled
            # colour while the button is still visually disabled).
            self._saved_button_color = value
            return
        super()._set_property(key, value)

    def _apply_disabled_color(self, color):
        """Applies a disabled colour directly. Uses the guard flag so _set_property
        doesn't misidentify this as an external enabled-colour write."""
        self._applying_disabled_color = True
        self._set_property('fg_color', color)
        self._applying_disabled_color = False

    def on_activate(self, event_function):
        """Sets the event to be called when the button is successfully clicked or activated."""
        self._set_event('activate', event_function)
    
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

        # Swap button colour and text colour for the disabled variants
        if value:
            saved = self._get_property('fg_color')
            if saved is None:
                # Widget not yet created — fall back to the CTk theme default
                saved = ctk.ThemeManager.theme['CTkButton']['fg_color']
            self._saved_button_color = saved
            disabled_color = self._button_disabled_color or self._DEFAULT_BUTTON_DISABLED_COLOR
            self._apply_disabled_color(disabled_color)

            if not self._has_custom_text_disabled_color:
                # No user override — apply our high-contrast default
                self._set_property('text_color_disabled', self._DEFAULT_TEXT_DISABLED_COLOR)
            # If the user has set a custom colour, CTk already has it applied — nothing to do
        else:
            if self._saved_button_color is not None:
                self._set_property('fg_color', self._saved_button_color)
                self._saved_button_color = None

            if not self._has_custom_text_disabled_color:
                # Restore CTk theme defaults
                self._set_property('text_color_disabled', ['gray74', 'gray60'])

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
        self._constructor_kwargs['text'] = value


