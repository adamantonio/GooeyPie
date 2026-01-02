import customtkinter as ctk

class GooeyPieStyle:
    """Helper class to access widget style properties."""
    def __init__(self, widget):
        self._widget = widget

    def _get_font(self):
        font = self._get('font')
        if font is None:
            # Return a default-like structure to avoid crashes (Name, Size)
            return ("Arial", 12)
        return font

    def _update_font(self, family=None, size=None):
        current_font = self._get_font()
        
        # Normalize current font to object or create new one
        if isinstance(current_font, ctk.CTkFont):
            new_font = current_font
            if family: new_font.configure(family=family)
            if size: new_font.configure(size=size)
        else:
            # It's a tuple or string (Tkinter style) or None
            # e.g. ("Arial", 12)
            c_family, c_size = "Arial", 12
            if isinstance(current_font, (tuple, list)):
                if len(current_font) > 0: c_family = current_font[0]
                if len(current_font) > 1: c_size = current_font[1]
            elif isinstance(current_font, str):
                # Simple string parsing might be needed, but CTk often uses tuples
                pass 
                
            new_family = family if family else c_family
            new_size = size if size else c_size
            
            # Create a CTkFont object for better handling
            new_font = ctk.CTkFont(family=new_family, size=new_size)

        self._set('font', new_font)

    @property
    def font_name(self):
        font = self._get_font()
        if isinstance(font, ctk.CTkFont): return font.cget("family")
        if isinstance(font, (tuple, list)) and len(font) > 0: return font[0]
        return "Arial"

    @font_name.setter
    def font_name(self, v):
        self._update_font(family=v)

    @property
    def font_size(self):
        font = self._get_font()
        if isinstance(font, ctk.CTkFont): return font.cget("size")
        if isinstance(font, (tuple, list)) and len(font) > 1: return font[1]
        return 12

    @font_size.setter
    def font_size(self, v):
        self._update_font(size=v)

    def _get(self, key):
        return self._widget._get_property(key)

    def _set(self, key, value):
        self._widget._set_property(key, value)

    @property
    def corner_radius(self): return self._get('corner_radius')
    @corner_radius.setter
    def corner_radius(self, v): self._set('corner_radius', v)

    @property
    def border_width(self): return self._get('border_width')
    @border_width.setter
    def border_width(self, v): self._set('border_width', v)

    @property
    def border_spacing(self): return self._get('border_spacing')
    @border_spacing.setter
    def border_spacing(self, v): self._set('border_spacing', v)

    @property
    def bg_color(self): return self._get('fg_color')
    @bg_color.setter
    def bg_color(self, v): self._set('fg_color', v)

    @property
    def hover_bg_color(self): return self._get('hover_color')
    @hover_bg_color.setter
    def hover_bg_color(self, v): self._set('hover_color', v)

    @property
    def border_color(self): return self._get('border_color')
    @border_color.setter
    def border_color(self, v): self._set('border_color', v)

    @property
    def text_color(self): return self._get('text_color')
    @text_color.setter
    def text_color(self, v): self._set('text_color', v)

    @property
    def disabled_text_color(self): return self._get('text_color_disabled')
    @disabled_text_color.setter
    def disabled_text_color(self, v): self._set('text_color_disabled', v)

    @property
    def placeholder_text_color(self): return self._get('placeholder_text_color')
    @placeholder_text_color.setter
    def placeholder_text_color(self, v): self._set('placeholder_text_color', v)

    @property
    def justify(self): return self._get('justify')
    @justify.setter
    def justify(self, v): self._set('justify', v)
