import customtkinter as ctk
from .widget import GooeyPieWidget

class Progressbar(GooeyPieWidget):
    _style_properties = (
        'track_color', 
        'border_color', 
        'border_width', 
        'corner_radius', 
        'progress_color'
    )

    """A progressbar widget to show the loading status for long running operations."""
    
    def __init__(self, container, mode="determinate", **kwargs):
        super().__init__(**kwargs)
        self._container = container
        self._constructor_kwargs['mode'] = mode
        self._constructor_kwargs['width'] = kwargs.get('width', 200) # Default width
        
        # Initial value to set once created
        self._initial_value = 0

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkProgressBar(master, **self._constructor_kwargs)
        self._ctk_object.set(self._initial_value)

    @property
    def value(self):
        """Current value of the progressbar (0-100)."""
        if self._ctk_object:
            # CTk uses 0-1, we use 0-100
            return self._ctk_object.get() * 100
        return self._initial_value * 100

    @value.setter
    def value(self, v):
        # Clamp between 0 and 100
        v = max(0, min(100, v))
        
        normalized_value = v / 100.0
        
        if self._ctk_object:
            self._ctk_object.set(normalized_value)
        else:
            self._initial_value = normalized_value

    def start(self, interval=50):
        """Starts the progressbar animation."""
        if self._ctk_object:
            # CTk doesn't support interval tuning in start() natively in the same way as ttk
            # But we pass it if we ever find a way, or just call start
            self._ctk_object.start()

    def stop(self):
        """Stops the progressbar animation."""
        if self._ctk_object:
            self._ctk_object.stop()

    @property
    def width(self):
        return self._get_property('width')

    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(width=value)
        self._constructor_kwargs['width'] = value
