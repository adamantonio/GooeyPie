from ..base import GooeyPieObject, WIDGET_PADDING
from ..style import GooeyPieStyle
from ..events import GooeyPieEvent
import tkinter

class GooeyPieWidget(GooeyPieObject):
    """Base class for widgets."""
    
    # Default padding when added to a grid
    _default_grid_padding = WIDGET_PADDING

    _EVENT_MAP = {
        'mouse_down': '<Button-1>',
        'mouse_up': '<ButtonRelease-1>',
        'double_click': '<Double-Button-1>',
        'triple_click': '<Triple-Button-1>',
        'middle_click': '<Button-2>',
        'right_click': '<Button-3>',
        'mouse_over': '<Enter>',
        'mouse_out': '<Leave>',
        'focus': '<FocusIn>',
        'blur': '<FocusOut>',
        'key_press': '<KeyPress>',
    }

    def __init__(self, **kwargs):
        super().__init__()
        self._constructor_kwargs = kwargs
        self._parent = None
        self.style = GooeyPieStyle(self)
        self._event_listeners = {} 
        self._pending_bindings = []

    def add_event_listener(self, event_name, callback):
        """Adds a callback function for the specified event."""
        if event_name not in self._event_listeners:
            self._event_listeners[event_name] = []
            
            # If it's a standard event, set up the binding
            tk_sequence = self._EVENT_MAP.get(event_name)
            if tk_sequence:
                self._bind_event(event_name, tk_sequence)
        
        self._event_listeners[event_name].append(callback)

    def remove_event_listener(self, event_name, callback=None):
        """Removes the callback function for the specified event.
        
        If callback is not provided, all listeners for the event are removed.
        Does not raise an error if the event or callback is not found.
        """
        if event_name not in self._event_listeners:
            return

        if callback is None:
            del self._event_listeners[event_name]
        else:
            try:
                self._event_listeners[event_name].remove(callback)
                # Cleanup empty list
                if not self._event_listeners[event_name]:
                    del self._event_listeners[event_name]
            except ValueError:
                pass

    def _bind_event(self, event_name, sequence):
        """Binds the event to the underlying widget or queues it."""
        if self._ctk_object:
            def handler(event):
                self._handle_event(event_name, event)
            self._ctk_object.bind(sequence, handler, add='+')
        else:
            self._pending_bindings.append((event_name, sequence))

    def _handle_event(self, event_name, original_event=None):
        """Dispatches the event to all registered listeners."""
        gp_event = GooeyPieEvent(event_name, self, original_event)
        
        for callback in self._event_listeners.get(event_name, []):
            callback(gp_event)

    def _apply_bindings(self):
        """Applies any pending event bindings."""
        if self._ctk_object and self._pending_bindings:
            for event_name, sequence in self._pending_bindings:
                # Re-bind using the helper to ensure closure correctness if needed,
                # though _bind_event handles the immediate binding.
                # However, _bind_event logic above checks self._ctk_object.
                # Since we are iterating pending, we know object exists now.
                
                # Careful with closure in loop
                name = event_name
                def handler(event, name=name):
                    self._handle_event(name, event)
                self._ctk_object.bind(sequence, handler, add='+')
            self._pending_bindings = []

    def focus(self):
        """Sets the focus to this widget."""
        if self._ctk_object:
            self._ctk_object.focus_set()

    def _create_widget(self, master):
        """Creates the underlying customtkinter widget. Must be implemented by subclasses."""
        raise NotImplementedError

    @property
    def disabled(self):
        val = self._get_property('state') 
        return val == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        # Also update constructor args in case it's not created yet
        self._constructor_kwargs['state'] = state

    @property
    def width(self):
        return self._get_property('width')

    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(width=value)
        self._constructor_kwargs['width'] = value

    @property
    def height(self):
        return self._get_property('height')

    @height.setter
    def height(self, value):
        if self._ctk_object:
            self._ctk_object.configure(height=value)
        self._constructor_kwargs['height'] = value
