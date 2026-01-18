import customtkinter as ctk
from .widget import GooeyPieWidget

class Switch(GooeyPieWidget):
    """A switch widget that can be toggled on and off."""
    
    def __init__(self, text="", value=False, command=None, **kwargs):
        super().__init__(text=text, **kwargs)
        
        # Set the command to dispatch our 'change' event
        # If a command was passed, we wrap it?
        # Standard pattern in GooeyPie is to emit events. 
        # The user can bind 'change' event.
        # But we also want to support 'command' arg if passed? 
        # Base Widget doesn't standardly handle 'command' for all widgets, but button/checkbox etc do.
        # Let's ensure our internal handler fires 'change'.
        
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

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkSwitch(master, **self._constructor_kwargs)
        if self._initial_value:
            self._ctk_object.select()

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
