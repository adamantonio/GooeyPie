from ..base import GooeyPieObject, WIDGET_PADDING
from ..style import GooeyPieStyle
from ..events import GooeyPieEvent
import tkinter

class GooeyPieWidget(GooeyPieObject):
    """Base class for widgets."""
    _style_properties = ()

    
    # Default padding when added to a grid
    _default_grid_padding = WIDGET_PADDING

    _EVENT_MAP = {
        'mouse_down': '<Button-1>',
        'mouse_up': '<ButtonRelease-1>',
        'click': '<ButtonRelease-1>',
        'double_click': '<Double-Button-1>',
        'middle_click': '<Button-2>',
        'right_click': '<Button-3>',
        'mouse_enter': '<Enter>',
        'mouse_leave': '<Leave>',
        'focus_gained': '<FocusIn>',
        'focus_lost': '<FocusOut>',
        'key_press': '<KeyPress>',
    }

    def __init__(self, **kwargs):
        super().__init__()
        self._constructor_kwargs = kwargs
        self._parent = None
        self.style = GooeyPieStyle(self)
        self._event_listeners = {} 
        self._pending_bindings = []

    def _set_event(self, event_name, event_function):
        """Sets or removes an event listener."""
        if event_function is None:
            self._event_listeners.pop(event_name, None)
        else:
            # Bind if not already bound
            if event_name not in self._event_listeners:
                tk_sequence = self._EVENT_MAP.get(event_name)
                if tk_sequence:
                    self._bind_event(event_name, tk_sequence)
            self._event_listeners[event_name] = event_function

    def _bind_event(self, event_name, sequence):
        """Binds the event to the underlying widget or queues it."""
        if self._ctk_object:
            def handler(event):
                self._handle_event(event_name, event)
            self._ctk_object.bind(sequence, handler, add='+')
        else:
            self._pending_bindings.append((event_name, sequence))

    def _handle_event(self, event_name, original_event=None):
        """Dispatches the event to the registered listener."""
        if event_name in self._event_listeners:
            gp_event = GooeyPieEvent(event_name, self, original_event)
            self._event_listeners[event_name](gp_event)

    def _apply_bindings(self):
        """Applies any pending event bindings."""
        if self._ctk_object and self._pending_bindings:
            bindings = list(self._pending_bindings)
            self._pending_bindings = []
            for event_name, sequence in bindings:
                self._bind_event(event_name, sequence)


    def on_click(self, event_function):
        self._set_event('click', event_function)

    def on_double_click(self, event_function):
        self._set_event('double_click', event_function)

    def on_right_click(self, event_function):
        self._set_event('right_click', event_function)

    def on_middle_click(self, event_function):
        self._set_event('middle_click', event_function)

    def on_mouse_down(self, event_function):
        self._set_event('mouse_down', event_function)

    def on_mouse_up(self, event_function):
        self._set_event('mouse_up', event_function)

    def on_mouse_enter(self, event_function):
        self._set_event('mouse_enter', event_function)

    def on_mouse_leave(self, event_function):
        self._set_event('mouse_leave', event_function)

    def on_key_press(self, event_function):
        self._set_event('key_press', event_function)

    def on_focus_gained(self, event_function):
        self._set_event('focus_gained', event_function)

    def on_focus_lost(self, event_function):
        self._set_event('focus_lost', event_function)

    def focus(self):
        """Sets the focus to this widget."""
        if self._ctk_object:
            self._ctk_object.focus_set()

    def _create_widget(self, master):
        """Creates the underlying customtkinter widget. Must be implemented by subclasses."""
        raise NotImplementedError

    @property
    def disabled(self):
        if self._ctk_object:
            val = self._get_property('state')
        else:
            # Before placement, state is stored in _constructor_kwargs, not _pending_properties
            val = self._constructor_kwargs.get('state', 'normal')
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
