import customtkinter as ctk
import tkinter.font

class GooeyPieStyle:
    """Helper class to access widget style properties."""
    
    _available_fonts = None

    def __init__(self, widget):
        self._widget = widget

    def __init__(self, widget):
        self._widget = widget

    def __getattr__(self, name):
        """Called when an attribute lookup has not found the attribute in the usual places."""
        valid_styles = getattr(self._widget, '_style_properties', [])
        raise AttributeError(f"'{type(self._widget).__name__}' widget style has no attribute '{name}'. Available styles: {', '.join(sorted(valid_styles))}")

    def __setattr__(self, name, value):
        """Called when an attribute assignment is attempted."""
        # Allow internal attributes (starting with _) to be set normally
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        # Check if the attribute is a property on the class and in the allow-list
        if hasattr(type(self), name) and isinstance(getattr(type(self), name), property):
            # Check against widget's allowed styles
            valid_styles = getattr(self._widget, '_style_properties', None)
            if valid_styles is not None and name not in valid_styles:
                 # It is a valid GooeyPie property, but NOT for this widget
                 raise AttributeError(f"'{type(self._widget).__name__}' widget style has no attribute '{name}'. Available styles: {', '.join(sorted(valid_styles))}")

            # It's valid, let standard mechanism handle the setter invocation
            super().__setattr__(name, value)
        else:
            # It's not a known property at all
            valid_styles = getattr(self._widget, '_style_properties', [])
            raise AttributeError(f"'{type(self._widget).__name__}' widget style has no attribute '{name}'. Available styles: {', '.join(sorted(valid_styles))}")

    @classmethod
    def _get_available_fonts(cls):
        if cls._available_fonts is None:
            try:
                # This requires a Tk root window to be initialized
                cls._available_fonts = set(f.lower() for f in tkinter.font.families())
            except Exception:
                # If no root window yet, return empty set or default
                return set()
        return cls._available_fonts

    def _resolve_font_family(self, font_spec):
        """Resolves a font specification (name, tuple, or keyword) to an available system font."""
        if not font_spec:
            return "Arial"

        # Normalize to tuple of candidates
        candidates = []
        if isinstance(font_spec, (str)):
            candidates.append(font_spec)
        elif isinstance(font_spec, (tuple, list)):
            candidates.extend(font_spec)
        else:
            return "Arial"

        available = self._get_available_fonts()
        
        # Keyword mappings
        keywords = {
            'serif': ["Times New Roman", "Times", "Georgia", "serif"],
            'sans-serif': ["Arial", "Helvetica", "Verdana", "sans-serif"],
            'monospace': ["Courier New", "Consolas", "Monaco", "monospace"],
            'system': ["Segoe UI", "San Francisco", "Arial"], # Platform dependentish
        }

        for family in candidates:
            # Check keywords first
            expanded = keywords.get(family.lower(), [family])
            
            for f in expanded:
                if f.lower() in available:
                    return f
                
                # Some fonts might be passed that are valid but not in the set 
                # But typically we want to return the first match.
        
        # If available fonts was empty (no root), checking is impossible.
        # Just return the first candidate to be safe, or default.
        if not available:
            return candidates[0]
            
        # Default if nothing matched
        return "Arial"

    def _get_font(self):
        font = self._get('font')
        if font is None:
            # Return a default-like structure to avoid crashes (Name, Size)
            return ("Arial", 12)
        return font

    def _update_font(self, family=None, size=None, weight=None, slant=None):
        current_font = self._get_font()
        
        # Normalize current font to object or create new one
        if isinstance(current_font, ctk.CTkFont):
            new_font = current_font
            if family: 
                resolved = self._resolve_font_family(family)
                new_font.configure(family=resolved)
            if size: new_font.configure(size=size)
            if weight: new_font.configure(weight=weight)
            if slant: new_font.configure(slant=slant)
        else:
            # It's a tuple or string (Tkinter style) or None
            # e.g. ("Arial", 12) or ("Arial", 12, "bold", "italic")
            c_family, c_size, c_weight, c_slant = "Arial", 12, "normal", "roman"
            if isinstance(current_font, (tuple, list)):
                if len(current_font) > 0: c_family = current_font[0]
                if len(current_font) > 1: c_size = current_font[1]
                if len(current_font) > 2: 
                    # Simplify tkinter style string parsing for now
                    style_str = str(current_font[2]).lower()
                    if "bold" in style_str: c_weight = "bold"
                    if "italic" in style_str: c_slant = "italic"
            elif isinstance(current_font, str):
                pass 
                
            new_family_spec = family if family else c_family
            resolved_family = self._resolve_font_family(new_family_spec)
            
            new_size = size if size else c_size
            new_weight = weight if weight else c_weight
            new_slant = slant if slant else c_slant
            
            # Create a CTkFont object for better handling
            new_font = ctk.CTkFont(family=resolved_family, size=new_size, weight=new_weight, slant=new_slant)

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

    @property
    def font_weight(self):
        font = self._get_font()
        if isinstance(font, ctk.CTkFont): return font.cget("weight")
        # Legacy tuple support (imperfect but better than nothing)
        if isinstance(font, (tuple, list)) and len(font) > 2: 
             if "bold" in str(font[2]).lower(): return "bold"
        return "normal"

    @font_weight.setter
    def font_weight(self, v):
        if v not in ("bold", "normal"):
            raise ValueError(f"Invalid font weight '{v}'. The only valid options are 'bold' or 'normal'.")
        self._update_font(weight=v)

    @property
    def font_style(self):
        font = self._get_font()
        val = "roman"
        if isinstance(font, ctk.CTkFont): val = font.cget("slant")
        elif isinstance(font, (tuple, list)) and len(font) > 2:
            if "italic" in str(font[2]).lower(): val = "italic"
        
        return "italic" if val == "italic" else "normal"

    @font_style.setter
    def font_style(self, v):
        if v not in ("italic", "normal"):
            raise ValueError(f"Invalid font style '{v}'. The only valid options are 'italic' or 'normal'.")
        # Map "normal" to "roman" for CTkFont
        slant = "italic" if v == "italic" else "roman"
        self._update_font(slant=slant)

    def _get(self, key):
        return self._widget._get_property(key)

    def _set(self, key, value):
        self._widget._set_property(key, value)

    @property
    def corner_radius(self): return self._get('corner_radius')
    @corner_radius.setter
    def corner_radius(self, v): self._set('corner_radius', v)

    @property
    def size(self): return self._get('size')
    @size.setter
    def size(self, v): self._set('size', v)

    @property
    def border_width(self): return self._get('border_width')
    @border_width.setter
    def border_width(self, v): self._set('border_width', v)

    @property
    def checked_border_width(self): return self._get('checked_border_width')
    @checked_border_width.setter
    def checked_border_width(self, v): self._set('checked_border_width', v)

    @property
    def unchecked_border_width(self): return self._get('unchecked_border_width')
    @unchecked_border_width.setter
    def unchecked_border_width(self, v): self._set('unchecked_border_width', v)

    @property
    def checked_border_color(self): return self._get('checked_border_color')
    @checked_border_color.setter
    def checked_border_color(self, v): self._set('checked_border_color', v)

    @property
    def unchecked_border_color(self): return self._get('unchecked_border_color')
    @unchecked_border_color.setter
    def unchecked_border_color(self, v): self._set('unchecked_border_color', v)

    @property
    def padding(self): return self._get('border_spacing')
    @padding.setter
    def padding(self, v): self._set('border_spacing', v)

    @property
    def padding_x(self): return self._get('padding_x')
    @padding_x.setter
    def padding_x(self, v): self._set('padding_x', v)

    @property
    def padding_y(self): return self._get('padding_y')
    @padding_y.setter
    def padding_y(self, v): self._set('padding_y', v)

    @property
    def bg_color(self): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            raise AttributeError("'Button' object has no attribute 'bg_color'. Use 'button_color' instead.")
        return self._get('fg_color')
    
    @bg_color.setter
    def bg_color(self, v): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            raise AttributeError("'Button' object has no attribute 'bg_color'. Use 'button_color' instead.")
        self._set('fg_color', v)

    @property
    def hover_bg_color(self): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            raise AttributeError("'Button' object has no attribute 'hover_bg_color'. Use 'hover_button_color' instead.")
        return self._get('hover_color')
    
    @hover_bg_color.setter
    def hover_bg_color(self, v): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            raise AttributeError("'Button' object has no attribute 'hover_bg_color'. Use 'hover_button_color' instead.")
        self._set('hover_color', v)

    @property
    def hover_color(self): return self._get('hover_color')
    @hover_color.setter
    def hover_color(self, v): self._set('hover_color', v)

    @property
    def border_color(self): return self._get('border_color')
    @border_color.setter
    def border_color(self, v): self._set('border_color', v)

    @property
    def text_color(self): return self._get('text_color')
    @text_color.setter
    def text_color(self, v): self._set('text_color', v)


    @property
    def text_disabled_color(self): return self._get('text_color_disabled')
    @text_disabled_color.setter
    def text_disabled_color(self, v):
        self._set('text_color_disabled', v)
        if hasattr(self._widget, '_has_custom_text_disabled_color'):
            self._widget._has_custom_text_disabled_color = True

    @property
    def placeholder_color(self): return self._get('placeholder_text_color')
    @placeholder_color.setter
    def placeholder_color(self, v): self._set('placeholder_text_color', v)

    @property
    def align(self): return self._get('align')
    @align.setter
    def align(self, v): self._set('align', v)

    @property
    def justify(self): return self._get('justify')
    @justify.setter
    def justify(self, v): self._set('justify', v)

    @property
    def button_color(self): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            return self._get('fg_color')
        return self._get('button_color')
    
    @button_color.setter
    def button_color(self, v): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            self._set('fg_color', v)
        else:
            self._set('button_color', v)

    @property
    def button_disabled_color(self):
        return self._widget._button_disabled_color

    @button_disabled_color.setter
    def button_disabled_color(self, v):
        self._widget._button_disabled_color = v
        # If currently disabled, apply the new disabled colour immediately.
        # For Button/ImageButton we call _apply_disabled_color() which uses the
        # _applying_disabled_color guard, preventing _set_property from treating
        # this as an external enabled-colour write.
        if self._widget.disabled:
            if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
                self._widget._apply_disabled_color(v)
            else:
                self._set('button_color', v)

    @property
    def checkbox_color(self):
        return self._get('fg_color')

    @checkbox_color.setter
    def checkbox_color(self, v):
        self._set('fg_color', v)

    @property
    def checkbox_disabled_color(self):
        return self._widget._checkbox_disabled_color

    @checkbox_disabled_color.setter
    def checkbox_disabled_color(self, v):
        self._widget._checkbox_disabled_color = v
        # If currently disabled, apply the new disabled colour immediately via the
        # guarded helper so _set_property doesn't intercept it as an external write.
        if self._widget.disabled:
            self._widget._apply_disabled_color(v)

    @property
    def checkbox_hover_color(self):
        return self._get('hover_color')

    @checkbox_hover_color.setter
    def checkbox_hover_color(self, v):
        self._set('hover_color', v)

    @property
    def button_hover_color(self): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            return self._get('hover_color')
        return self._get('button_hover_color')
    
    @button_hover_color.setter
    def button_hover_color(self, v): 
        if self._widget.__class__.__name__ in ('Button', 'ImageButton'):
            self._set('hover_color', v)
        else:
            self._set('button_hover_color', v)

    @property
    def dropdown_bg_color(self): return self._get('dropdown_fg_color')
    @dropdown_bg_color.setter
    def dropdown_bg_color(self, v): self._set('dropdown_fg_color', v)

    @property
    def dropdown_hover_color(self): return self._get('dropdown_hover_color')
    @dropdown_hover_color.setter
    def dropdown_hover_color(self, v): self._set('dropdown_hover_color', v)

    @property
    def dropdown_text_color(self): return self._get('dropdown_text_color')
    @dropdown_text_color.setter
    def dropdown_text_color(self, v): self._set('dropdown_text_color', v)

    def _update_dropdown_font(self, family=None, size=None):
        # CTkComboBox uses 'dropdown_font' which expects a tuple or font object
        current_font = self._get('dropdown_font')
        
        if isinstance(current_font, ctk.CTkFont):
            new_font = current_font
            if family: 
                resolved = self._resolve_font_family(family)
                new_font.configure(family=resolved)
            if size: new_font.configure(size=size)
        else:
            c_family, c_size = "Arial", 12
            if isinstance(current_font, (tuple, list)):
                if len(current_font) > 0: c_family = current_font[0]
                if len(current_font) > 1: c_size = current_font[1]
            
            new_family = family if family else c_family
            resolved_family = self._resolve_font_family(new_family)
            new_size = size if size else c_size
            
            new_font = ctk.CTkFont(family=resolved_family, size=new_size)

        self._set('dropdown_font', new_font)

    @property
    def dropdown_font_name(self):
        font = self._get('dropdown_font')
        if isinstance(font, ctk.CTkFont): return font.cget("family")
        if isinstance(font, (tuple, list)) and len(font) > 0: return font[0]
        return "Arial"

    @dropdown_font_name.setter
    def dropdown_font_name(self, v):
        self._update_dropdown_font(family=v)

    @property
    def dropdown_font_size(self):
        font = self._get('dropdown_font')
        if isinstance(font, ctk.CTkFont): return font.cget("size")
        if isinstance(font, (tuple, list)) and len(font) > 1: return font[1]
        return 12

    @dropdown_font_size.setter
    def dropdown_font_size(self, v):
        self._update_dropdown_font(size=v)

    @property
    def on_bg_color(self): return self._get('progress_color')
    @on_bg_color.setter
    def on_bg_color(self, v): self._set('progress_color', v)

    @property
    def off_bg_color(self): return self._get('fg_color')
    @off_bg_color.setter
    def off_bg_color(self, v): self._set('fg_color', v)

    @property
    def active_bg_color(self): return self._get('fg_color')
    @active_bg_color.setter
    def active_bg_color(self, v): self._set('fg_color', v)

    @property
    def inactive_bg_color(self): return self._get('progress_color')
    @inactive_bg_color.setter
    def inactive_bg_color(self, v): self._set('progress_color', v)

    @property
    def selected_color(self): 
        if self._widget.__class__.__name__ == 'Listbox':
            return self._get('highlight_color')
        return self._get('selected_color')
    
    @selected_color.setter
    def selected_color(self, v): 
        if self._widget.__class__.__name__ == 'Listbox':
            self._set('highlight_color', v)
        else:
            self._set('selected_color', v)

    @property
    def selected_disabled_color(self):
        return self._widget._selected_disabled_color

    @selected_disabled_color.setter
    def selected_disabled_color(self, v):
        self._widget._selected_disabled_color = v
        # If currently disabled, apply via guarded helper.
        if self._widget.disabled:
            self._widget._apply_disabled_color(selected_color=v)

    @property
    def unselected_disabled_color(self):
        return self._widget._unselected_disabled_color

    @unselected_disabled_color.setter
    def unselected_disabled_color(self, v):
        self._widget._unselected_disabled_color = v
        # If currently disabled, apply via guarded helper.
        if self._widget.disabled:
            self._widget._apply_disabled_color(unselected_color=v)

    @property
    def unselected_color(self): 
        if self._widget.__class__.__name__ == 'Listbox':
            return self._get('button_color')
        return self._get('unselected_color')
    
    @unselected_color.setter
    def unselected_color(self, v): 
        if self._widget.__class__.__name__ == 'Listbox':
            self._set('button_color', v)
        else:
            self._set('unselected_color', v)

    @property
    def selected_hover_color(self): 
        if self._widget.__class__.__name__ == 'Listbox':
            return self._get('hover_color')
        return self._get('selected_hover_color')

    @selected_hover_color.setter
    def selected_hover_color(self, v): 
        if self._widget.__class__.__name__ == 'Listbox':
            self._set('hover_color', v)
        else:
            self._set('selected_hover_color', v)

    @property
    def unselected_hover_color(self): 
        if self._widget.__class__.__name__ == 'Listbox':
            return self._get('hover_color')
        return self._get('unselected_hover_color')

    @unselected_hover_color.setter
    def unselected_hover_color(self, v):
        if self._widget.__class__.__name__ == 'Listbox':
            self._set('hover_color', v)
        else:
            self._set('unselected_hover_color', v)

    @property
    def progress_color(self): return self._get('progress_color')
    @progress_color.setter
    def progress_color(self, v): self._set('progress_color', v)

    @property
    def track_color(self): return self._get('fg_color')
    @track_color.setter
    def track_color(self, v): self._set('fg_color', v)

    # DatePicker specific styles
    @property
    def month_font_name(self): return self._get('month_font_name')
    @month_font_name.setter
    def month_font_name(self, v): self._set('month_font_name', v)

    @property
    def month_font_size(self): return self._get('month_font_size')
    @month_font_size.setter
    def month_font_size(self, v): self._set('month_font_size', v)

    @property
    def month_font_style(self): return self._get('month_font_style')
    @month_font_style.setter
    def month_font_style(self, v): self._set('month_font_style', v)

    @property
    def month_font_weight(self): return self._get('month_font_weight')
    @month_font_weight.setter
    def month_font_weight(self, v): self._set('month_font_weight', v)

    @property
    def month_text_color(self): return self._get('month_text_color')
    @month_text_color.setter
    def month_text_color(self, v): self._set('month_text_color', v)

    @property
    def day_font_name(self): return self._get('day_font_name')
    @day_font_name.setter
    def day_font_name(self, v): self._set('day_font_name', v)

    @property
    def day_font_size(self): return self._get('day_font_size')
    @day_font_size.setter
    def day_font_size(self, v): self._set('day_font_size', v)

    @property
    def day_font_style(self): return self._get('day_font_style')
    @day_font_style.setter
    def day_font_style(self, v): self._set('day_font_style', v)

    @property
    def day_font_weight(self): return self._get('day_font_weight')
    @day_font_weight.setter
    def day_font_weight(self, v): self._set('day_font_weight', v)

    @property
    def day_text_color(self): return self._get('day_text_color')
    @day_text_color.setter
    def day_text_color(self, v): self._set('day_text_color', v)

    @property
    def month_button_bg_color(self): return self._get('month_button_bg_color')
    @month_button_bg_color.setter
    def month_button_bg_color(self, v): self._set('month_button_bg_color', v)



    # DatePicker specific styles
    @property
    def month_font_name(self): return self._get('month_font_name')
    @month_font_name.setter
    def month_font_name(self, v): self._set('month_font_name', v)

    @property
    def month_font_size(self): return self._get('month_font_size')
    @month_font_size.setter
    def month_font_size(self, v): self._set('month_font_size', v)

    @property
    def month_font_style(self): return self._get('month_font_style')
    @month_font_style.setter
    def month_font_style(self, v): self._set('month_font_style', v)

    @property
    def month_font_weight(self): return self._get('month_font_weight')
    @month_font_weight.setter
    def month_font_weight(self, v): self._set('month_font_weight', v)

    @property
    def month_text_color(self): return self._get('month_text_color')
    @month_text_color.setter
    def month_text_color(self, v): self._set('month_text_color', v)

    @property
    def day_font_name(self): return self._get('day_font_name')
    @day_font_name.setter
    def day_font_name(self, v): self._set('day_font_name', v)

    @property
    def day_font_size(self): return self._get('day_font_size')
    @day_font_size.setter
    def day_font_size(self, v): self._set('day_font_size', v)

    @property
    def day_font_style(self): return self._get('day_font_style')
    @day_font_style.setter
    def day_font_style(self, v): self._set('day_font_style', v)

    @property
    def day_font_weight(self): return self._get('day_font_weight')
    @day_font_weight.setter
    def day_font_weight(self, v): self._set('day_font_weight', v)

    @property
    def day_text_color(self): return self._get('day_text_color')
    @day_text_color.setter
    def day_text_color(self, v): self._set('day_text_color', v)

    @property
    def month_button_bg_color(self): return self._get('month_button_bg_color')
    @month_button_bg_color.setter
    def month_button_bg_color(self, v): self._set('month_button_bg_color', v)

    @property
    def month_button_text_color(self): return self._get('month_button_text_color')
    @month_button_text_color.setter
    def month_button_text_color(self, v): self._set('month_button_text_color', v)

    @property
    def date_bg_color(self): return self._get('date_bg_color')
    @date_bg_color.setter
    def date_bg_color(self, v): self._set('date_bg_color', v)

    @property
    def date_border_color(self): return self._get('date_border_color')
    @date_border_color.setter
    def date_border_color(self, v): self._set('date_border_color', v)

    @property
    def date_border_width(self): return self._get('date_border_width')
    @date_border_width.setter
    def date_border_width(self, v): self._set('date_border_width', v)

    @property
    def open_button_bg_color(self): return self._get('open_button_bg_color')
    @open_button_bg_color.setter
    def open_button_bg_color(self, v): self._set('open_button_bg_color', v)

    @property
    def open_button_text_color(self): return self._get('open_button_text_color')
    @open_button_text_color.setter
    def open_button_text_color(self, v): self._set('open_button_text_color', v)
