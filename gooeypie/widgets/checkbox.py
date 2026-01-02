import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class Checkbox(GooeyPieWidget):
    def __init__(self, text="", checked=False, **kwargs):
        super().__init__(text=text, **kwargs)
        
        # Set the command to dispatch our 'change' event
        # This lambda needs to be pickle-safe? No, standard GUI. 
        # But we need to ensure it works in constructor kwargs.
        self._constructor_kwargs['command'] = lambda: self._handle_event('change')

        if not text and 'width' not in kwargs:
            # If no text is provided, we want the checkbox to comfortably fit the box
            # defaulting to a smaller width so it doesn't take up unnecessary space.
            # CTk default checkbox width is around 24.
            kwargs['width'] = 24 
            self._constructor_kwargs['width'] = 24

        # Determine initial variable value based on checked state
        # CTkCheckBox uses variable for state management usually, but can also use select/deselect methods.
        # However, to support 'checked' property easily, we can use methods after creation or variable.
        # Let's rely on methods for simplicity in the setter, but for init we can just set it.
        # Actually CTkCheckBox has `onvalue` and `offvalue` (default 1 and 0).
        # We'll just use the default behavior.
        self._initial_checked = checked

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkCheckBox(master, **self._constructor_kwargs)
        if self._initial_checked:
            self._ctk_object.select()

    @property
    def checked(self):
        if self._ctk_object:
            return bool(self._ctk_object.get())
        return self._initial_checked

    @checked.setter
    def checked(self, value):
        if self._ctk_object:
            if value:
                self._ctk_object.select()
            else:
                self._ctk_object.deselect()
        else:
            self._initial_checked = bool(value)

    @property
    def text(self):
        return self._get_property('text')
    
    @text.setter
    def text(self, value):
        if self._ctk_object:
            self._ctk_object.configure(text=value)
            
            # Logic to auto-resize if user hasn't fixed a width? 
            # This is tricky because we don't know if 'width' was manually set by user 
            # *after* init without tracking it closely.
            # For now, let's just update the text. If the user clears text, they might 
            # expect it to shrink, but CTk might not do that automatically if width was set before.
            # But based on our init logic:
            if not value and self.width == 0: 
                 # If we treat 0 or None as "auto" or "default"
                 pass
            
            if not value:
                # If clearing text, maybe shrink? 
                # But safer to leave as is unless we know we are in "auto" mode.
                # Let's simple check: if current width is the default small one, expand?
                # Or if it was small, and we add text, we need to expand.
                # CTk usually handles expansion if width is not fixed.
                # If we passed width=24 in init, CTk "fixes" it to 24. 
                # So if we later add text "Hello", it will be cut off! 
                # FIX: If we forced width to 24, and now we add text, we MUST reset width to None (auto)
                # UNLESS the user explicitly set width property.
                
                # We need to check if we should "release" the width.
                pass
            else:
                 # Adding text
                 if self._constructor_kwargs.get('width') == 24 and self.width == 24:
                     # It was likely our default "no text" width. Reset it.
                     self.width = 0 # 0 usually means auto/wrap in some frameworks, or just unset.
                     # In CTk, setting width to 0 or removing it... 
                     # configure(width=0) ? 
                     # Let's try setting a larger default or just unset it via 0? 
                     self._ctk_object.configure(width=0) 

        self._constructor_kwargs['text'] = value


    @property
    def checkbox_width(self):
        return self._get_property('checkbox_width')

    @checkbox_width.setter
    def checkbox_width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(checkbox_width=value)
        self._constructor_kwargs['checkbox_width'] = value

    @property
    def checkbox_height(self):
        return self._get_property('checkbox_height')

    @checkbox_height.setter
    def checkbox_height(self, value):
        if self._ctk_object:
            self._ctk_object.configure(checkbox_height=value)
        self._constructor_kwargs['checkbox_height'] = value

    def toggle(self):
        if self._ctk_object:
            self._ctk_object.toggle()