import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class ButtonGroup(GooeyPieWidget):
    """A widget that displays a set of segmented buttons (mutually exclusive options)."""

    def __init__(self, options, **kwargs):
        """
        Args:
            options (list): A list of strings for the buttons.
            **kwargs: Standard widget arguments.
        """
        if 'width' in kwargs:
            kwargs['dynamic_resizing'] = False
            
        super().__init__(**kwargs)
        self._options = options
        self._variable = None
        self._initial_selected = None
        
        # We need to store the initial selection if provided in kwargs, 
        # though standard widget kwargs usually don't have 'selected' or 'value'.
        # But we might want to support it if passed. 
        # For now, let's stick to the plan: constructor takes options.
        # Selection can be set via property or user interaction.

    def _create_widget(self, master):
        self._variable = ctk.StringVar(value=self._initial_selected if self._initial_selected else "")
        
        # Create validation command wrapper
        def command_wrapper(value):
            self._handle_event('change')

        self._ctk_object = ctk.CTkSegmentedButton(
            master,
            values=self._options,
            variable=self._variable,
            command=command_wrapper,
            **self._constructor_kwargs
        )

    @property
    def width(self):
        return super().width

    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(dynamic_resizing=False, width=value)
        self._constructor_kwargs['width'] = value
        self._constructor_kwargs['dynamic_resizing'] = False

    @property
    def selected(self):
        """Gets or sets the currently selected option. Returns None if nothing is selected."""
        if self._variable:
            val = self._variable.get()
            return val if val else None
        return self._initial_selected

    @selected.setter
    def selected(self, value):
        if self._variable:
            if value is None:
                self._variable.set("")
            else:
                if value in self._options:
                    self._variable.set(value)
                else:
                    raise ValueError(f"Value '{value}' not in options {self._options}")
        else:
            if value is not None and value not in self._options:
                 raise ValueError(f"Value '{value}' not in options {self._options}")
            self._initial_selected = value
