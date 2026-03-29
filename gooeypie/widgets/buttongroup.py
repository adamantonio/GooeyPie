import customtkinter as ctk
from .widget import GooeyPieWidget
from ..events import GooeyPieEvent

class ButtonGroup(GooeyPieWidget):
    _style_properties = (
        'bg_color',
        'border_width',
        'corner_radius',
        'font_size',
        'font_name',
        'font_style',
        'font_weight',
        'selected_color',
        'selected_disabled_color',
        'selected_hover_color',
        'unselected_color',
        'unselected_disabled_color',
        'unselected_hover_color',
        'text_disabled_color',
        'text_color'
    )

    _DEFAULT_SELECTED_DISABLED_COLOR = '#808080'

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
        self._selected_disabled_color = None
        self._saved_selected_color = None
        self._unselected_disabled_color = None
        self._saved_unselected_color = None

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
    def disabled(self):
        return super().disabled

    @disabled.setter
    def disabled(self, value):
        # Call the base class disabled setter for state management
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state)
        self._constructor_kwargs['state'] = state

        # Swap selected_color for the disabled variant
        if value:
            self._saved_selected_color = self._get_property('selected_color')
            disabled_color = self._selected_disabled_color or self._DEFAULT_SELECTED_DISABLED_COLOR
            self._set_property('selected_color', disabled_color)

            if self._unselected_disabled_color:
                self._saved_unselected_color = self._get_property('unselected_color')
                self._set_property('unselected_color', self._unselected_disabled_color)
        else:
            if self._saved_selected_color is not None:
                self._set_property('selected_color', self._saved_selected_color)
                self._saved_selected_color = None
            if self._saved_unselected_color is not None:
                self._set_property('unselected_color', self._saved_unselected_color)
                self._saved_unselected_color = None

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
