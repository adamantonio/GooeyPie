import customtkinter as ctk
import tkinter
from .widget import GooeyPieWidget

class Entry(GooeyPieWidget):
    _style_properties = (
        'bg_color', 
        'border_color', 
        'border_width', 
        'corner_radius', 
        'text_disabled_color', 
        'font_name', 
        'font_size', 
        'font_style', 
        'font_weight', 
        'justify', 
        'placeholder_text_color', 
        'text_color'
    )

    def __init__(self, placeholder_text="", **kwargs):
        # Extract disabled text color if present, as it's not a valid CTk argument
        self._disabled_text_color = kwargs.pop('text_color_disabled', None)
        self._original_text_color = None
        
        super().__init__(placeholder_text=placeholder_text, **kwargs)
        self._last_text = ""
    
    def _create_widget(self, master):
        self._ctk_object = ctk.CTkEntry(master, **self._constructor_kwargs)
        
        # Store the original text color
        if self._original_text_color is None:
            self._original_text_color = self._ctk_object.cget('text_color')
        
        # Store default placeholder color for disabled state fallback
        self._default_disabled_color = self._ctk_object.cget('placeholder_text_color')

        # Apply initial disabled state color if needed
        self._update_text_color()
        
        # Apply any initial text set via property before creation
        if self._last_text:
            # If the widget is disabled, we need to temporarily enable it to insert text
            current_state = self._constructor_kwargs.get('state', 'normal')
            if current_state == 'disabled':
                self._ctk_object.configure(state='normal')
            
            self._ctk_object.insert(0, self._last_text)
            
            if current_state == 'disabled':
                self._ctk_object.configure(state='disabled')

        # Bind events to detect changes
        self._ctk_object.bind("<KeyRelease>", self._check_change)

    def _set_property(self, key, value):
        if key == 'text_disabled_color' or key == 'text_color_disabled':
            self._disabled_text_color = value
            self._update_text_color()
        elif key == 'text_color':
            self._original_text_color = value
            # Only apply to widget if we are NOT disabled currently, 
            # or if we want to update the underlying logic. 
            # If disabled, we just update the stored original.
            if not self.disabled:
                 super()._set_property(key, value)
        elif key == 'state':
            super()._set_property(key, value)
            self._update_text_color()
        else:
            super()._set_property(key, value)

    def _update_text_color(self):
        """Updates the text color based on the current state (disabled/normal)."""
        if self.disabled:
            color = self._disabled_text_color
            if not color:
                # Default to the captured default placeholder color
                color = getattr(self, '_default_disabled_color', self._get_property('placeholder_text_color'))
            
            if self._ctk_object:
                self._ctk_object.configure(text_color=color)
        else:
            # Restore original text color
            if self._original_text_color and self._ctk_object:
                self._ctk_object.configure(text_color=self._original_text_color)
    
    def _check_change(self, event=None):
        current_text = self.text
        if current_text != self._last_text:
            self._last_text = current_text
            self._handle_event('change')

    @property
    def text(self):
        if self._ctk_object:
            return self._ctk_object.get()
        return self._last_text or ""
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            # Check if disabled
            was_disabled = self.disabled
            if was_disabled:
                self._ctk_object.configure(state='normal')
            
            self._ctk_object.delete(0, 'end')
            self._ctk_object.insert(0, value)
            
            if was_disabled:
                self._ctk_object.configure(state='disabled')
        
        # Initial text handling if not created yet is tricky with setters?
        # GooeyPieWidget.__init__ calls setter? No, it passes kwargs.
        # So we should be fine if we set _last_text.
        
        if value != self._last_text:
            self._last_text = value
            self._handle_event('change')
    
    @property
    def placeholder(self):
         return self._get_property('placeholder_text')

    @placeholder.setter
    def placeholder(self, value):
        if self._ctk_object:
            self._ctk_object.configure(placeholder_text=value)
        self._constructor_kwargs['placeholder_text'] = value

    @property
    def disabled(self):
        return super().disabled

    @disabled.setter
    def disabled(self, value):
        # Update state using parent logic (duplicated here or via super setter if possible, 
        # but straightforward to re-implement for clarity and to ensure hook)
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state
        
        # Trigger color update
        self._update_text_color()

    def clear(self):
        """Clears the text in the entry."""
        self.text = ""

    def select(self):
        """Selects all text in the entry."""
        if self._ctk_object:
            self.focus()
            self._ctk_object.select_range(0, 'end')
