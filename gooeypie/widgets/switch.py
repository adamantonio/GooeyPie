import customtkinter as ctk
from .widget import GooeyPieWidget

class Switch(GooeyPieWidget):
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
        'off_bg_color',
        'on_bg_color',
        'text_color',
        'text_disabled_color',
    )

    _DEFAULT_BUTTON_DISABLED_COLOR = '#555555'

    def __init__(self, text="", value=False, **kwargs):
        """
        A switch widget that can be toggled on and off.

        Args:
            text (str): Optional - The text to display on the switch.
            value (bool): Optional - The initial value of the switch.
            **kwargs: Standard widget arguments.
        """
        super().__init__(text=text, **kwargs)
        self._button_disabled_color = None
        self._saved_button_color = None
        # Guard: True while the disabled setter is internally writing the disabled colour,
        # so _set_property won't re-route that write to _saved_button_color.
        self._applying_disabled_color = False
        
        # Set the command to dispatch our 'change' event
        self._constructor_kwargs['command'] = lambda: self._handle_event('change')

        # Handle initial value
        self._initial_value = value
        
        # Handle custom props not in style
        # switch_width and switch_height are size properties so they belong on the widget
        if 'switch_width' in kwargs:
             self._constructor_kwargs['switch_width'] = kwargs['switch_width']
        if 'switch_height' in kwargs:
             self._constructor_kwargs['switch_height'] = kwargs['switch_height']
             
        # Default width behavior
        # Like Checkbox, if no text is provided, we default to a smaller width 
        # so it doesn't take up unnecessary space.
        if not text and 'width' not in kwargs:
            kwargs['width'] = 36 # Approx default switch width
            self._constructor_kwargs['width'] = 36

    def _set_property(self, key, value):
        """Override to intercept external button_color changes while disabled."""
        if key == 'button_color' and self.disabled and not self._applying_disabled_color:
            # An external caller (e.g. style.button_color) is setting the colour
            # while the switch is disabled.  Store it to restore on re-enable.
            self._saved_button_color = value
            return
        super()._set_property(key, value)

    def _apply_disabled_color(self, color):
        """Applies a disabled colour directly, bypassing the _set_property intercept."""
        self._applying_disabled_color = True
        self._set_property('button_color', color)
        self._applying_disabled_color = False

    def _create_widget(self, master):
        # Temporarily remove disabled state so select() works during creation
        saved_state = self._constructor_kwargs.pop('state', None)
        self._ctk_object = ctk.CTkSwitch(master, **self._constructor_kwargs)
        if self._initial_value:
            self._ctk_object.select()
        if saved_state:
            self._constructor_kwargs['state'] = saved_state
            self._ctk_object.configure(state=saved_state)

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
            saved = self._get_property('button_color')
            if saved is None:
                # Widget not yet created — fall back to the CTk theme default
                saved = ctk.ThemeManager.theme['CTkSwitch']['button_color']
            self._saved_button_color = saved
            disabled_color = self._button_disabled_color or self._DEFAULT_BUTTON_DISABLED_COLOR
            self._apply_disabled_color(disabled_color)
        else:
            if self._saved_button_color is not None:
                self._set_property('button_color', self._saved_button_color)
                self._saved_button_color = None

    @property
    def value(self):
        """Current boolean state of the switch."""
        if self._ctk_object:
            return bool(self._ctk_object.get())
        return self._initial_value

    @value.setter
    def value(self, v):
        if self._ctk_object:
            # CTk might block changes if disabled, so we temporarily enable
            disabled = self._ctk_object.cget('state') == 'disabled'
            if disabled:
                self._ctk_object.configure(state='normal')

            if v:
                self._ctk_object.select()
            else:
                self._ctk_object.deselect()
            
            if disabled:
                self._ctk_object.configure(state='disabled')
        else:
            self._initial_value = bool(v)

    def toggle(self):
        """Toggles the switch state."""
        if self._ctk_object:
            # CTk might block changes if disabled, so we temporarily enable
            disabled = self._ctk_object.cget('state') == 'disabled'
            if disabled:
                self._ctk_object.configure(state='normal')
                
            self._ctk_object.toggle()
            
            if disabled:
                self._ctk_object.configure(state='disabled')
        else:
            self._initial_value = not self._initial_value

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
            
            # Auto-resize logic similar to Checkbox
            if not value and self.width == 36:
                 # If we are effectively "default/auto", stay same.
                 pass
            elif value and self._constructor_kwargs.get('width') == 36 and self.width == 36:
                 # If adding text to a default-width switch, reset width to auto
                 self.width = 0 # Or whatever unsets it in CTk, usually 0 or removing config
                 self._ctk_object.configure(width=0)

        self._constructor_kwargs['text'] = value

    @property
    def switch_width(self):
        return self._get_property('switch_width')

    @switch_width.setter
    def switch_width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(switch_width=value)
        self._constructor_kwargs['switch_width'] = value

    @property
    def switch_height(self):
        return self._get_property('switch_height')

    @switch_height.setter
    def switch_height(self, value):
        if self._ctk_object:
            self._ctk_object.configure(switch_height=value)
        self._constructor_kwargs['switch_height'] = value

    def on_change(self, event_function):
        """Sets the event to be called when the switch state changes."""
        self._set_event('change', event_function)
