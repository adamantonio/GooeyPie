import customtkinter as ctk
from .widget import GooeyPieWidget

class Slider(GooeyPieWidget):
    _style_properties = (
        'active_bg_color',
        'border_color',
        'border_width',
        'button_color',
        'button_disabled_color',
        'button_hover_color',
        'inactive_bg_color',
    )

    _DEFAULT_BUTTON_DISABLED_COLOR = '#555555'

    def __init__(self, min_value, max_value, initial_value=None, **kwargs):
        """
        A slider widget for selecting a value from a range.

        Args:
            min_value (int or float): The minimum value of the slider.
            max_value (int or float): The maximum value of the slider.
            initial_value (int or float): Optional - The initial value of the slider.
            **kwargs: Standard widget arguments.
        """
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
        self._button_disabled_color = None
        self._saved_button_color = None
        
        self._constructor_kwargs['command'] = self._on_change_internal
        
        if initial_value is None:
            initial_value = min_value
            
        self._current_value = initial_value
        self._last_reported_value = initial_value

    def _on_change_internal(self, v):
        new_val = self.value
        if new_val != self._last_reported_value:
            self._last_reported_value = new_val
            self._handle_event('change')

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
            self._saved_button_color = self._get_property('button_color')
            disabled_color = self._button_disabled_color or self._DEFAULT_BUTTON_DISABLED_COLOR
            self._set_property('button_color', disabled_color)
        else:
            if self._saved_button_color is not None:
                self._set_property('button_color', self._saved_button_color)
                self._saved_button_color = None

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

    def on_change(self, event_function):
        """Sets the event to be called when the slider's rounded value changes."""
        self._set_event('change', event_function)
