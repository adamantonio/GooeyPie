import customtkinter as ctk
from .widget import GooeyPieWidget

class Slider(GooeyPieWidget):
    """A slider widget for selecting a value from a range."""

    def __init__(self, min_value, max_value, command=None, **kwargs):
        # We handle min/max/increment differently than base kwargs
        self._min_value = min_value
        self._max_value = max_value
        self._increment = 1
        
        # Calculate steps based on default increment of 1
        steps = self._calculate_steps(min_value, max_value, self._increment)
        
        # Prepare kwargs for CtkSlider
        kwargs['from_'] = min_value
        kwargs['to'] = max_value
        kwargs['number_of_steps'] = steps
        
        # Initialize base
        super().__init__(**kwargs)
        
        self._constructor_kwargs['command'] = lambda v: self._handle_event('change')
        self._current_value = min_value

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkSlider(master, **self._constructor_kwargs)
        self._ctk_object.set(self._current_value)

    def _calculate_steps(self, min_val, max_val, inc):
        if inc <= 0:
            return None # Continuous
        try:
            return (max_val - min_val) / inc
        except ZeroDivisionError:
            return None

    @property
    def _should_return_int(self):
        """Returns True if min, max, and increment are all integers."""
        return (isinstance(self._min_value, int) and 
                isinstance(self._max_value, int) and 
                isinstance(self._increment, int))

    def _get_decimal_places(self, number):
        """Returns the number of decimal places in a number."""
        s = str(number)
        if '.' not in s:
            return 0
        return len(s.split('.')[1])

    @property
    def value(self):
        """Current value of the slider."""
        val = 0
        if self._ctk_object:
            val = self._ctk_object.get()
        else:
            val = self._current_value
        
        if self._should_return_int:
            return int(val)
        
        # Round to match increment precision
        decimals = self._get_decimal_places(self._increment)
        return round(val, decimals)

    @value.setter
    def value(self, v):
        if self._ctk_object:
            # Enable if disabled to allow programmatic change
            disabled = self._ctk_object.cget('state') == 'disabled'
            if disabled:
                self._ctk_object.configure(state='normal')
                
            self._ctk_object.set(v)
            
            if disabled:
                self._ctk_object.configure(state='disabled')
        
        self._current_value = v

    @property
    def increment(self):
        return self._increment

    @increment.setter
    def increment(self, v):
        self._increment = v
        steps = self._calculate_steps(self._min_value, self._max_value, v)
        if self._ctk_object:
            self._ctk_object.configure(number_of_steps=steps)
        self._constructor_kwargs['number_of_steps'] = steps

    @property
    def orientation(self):
        return self._get_property('orientation')

    @orientation.setter
    def orientation(self, v):
        if self._ctk_object:
            if self._ctk_object.winfo_ismapped():
                raise RuntimeError("Cannot change orientation after widget has been created/run")
            self._ctk_object.configure(orientation=v)
        self._constructor_kwargs['orientation'] = v
