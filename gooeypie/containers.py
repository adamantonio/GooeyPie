import customtkinter as ctk
from .base import GooeyPieObject, CONTAINER_PADDING, WIDGET_PADDING
from .widgets.widget import GooeyPieWidget

class GooeyPieContainer(GooeyPieObject):
    """Mixin/Base for objects that can contain other widgets."""
    def __init__(self):
        super().__init__()
        self._children = []
        self._pending_children = []
        self._pending_column_weights = {}
        self._pending_row_weights = {}
        self._user_column_weights = set()  # columns explicitly weighted by the user
        self._num_columns = 0  # highest column index seen (1-based)
        self._num_rows = 0     # highest row index seen (1-based)
        self._grid_master = None # Will be set by subclasses

    def _get_grid_master(self):
        """Returns the widget that acts as the parent for the grid (geometry master)."""
        return self._grid_master or self._ctk_object

    def add(self, widget, column, row, row_span=1, column_span=1, expand_horizontal=False, expand_vertical=False, align_horizontal="center", align_vertical="center", **kwargs):
        """Adds a widget to this container at grid position (column, row)."""
        if not isinstance(widget, GooeyPieWidget):
            raise ValueError(f"Can only add GooeyPieWidgets to a window or container. Received {type(widget).__name__}.")

        if column == 0:
            raise ValueError("Columns start at 1, not 0. Use column = 1 for the first column.")
        if row == 0:
            raise ValueError("Rows start at 1, not 0. Use row = 1 for the first row.")

        # Silently accept "middle" as an alias for "center"
        if align_horizontal == "middle":
            align_horizontal = "center"
        if align_vertical == "middle":
            align_vertical = "center"

        _valid_h = ("left", "center", "right")
        _valid_v = ("top", "center", "bottom")
        if align_horizontal not in _valid_h:
            raise ValueError(
                f"'{align_horizontal}' is not a valid value for align_horizontal. "
                f"Choose one of: {', '.join(repr(v) for v in _valid_h)}."
            )
        if align_vertical not in _valid_v:
            raise ValueError(
                f"'{align_vertical}' is not a valid value for align_vertical. "
                f"Choose one of: {', '.join(repr(v) for v in _valid_v)}."
            )

        if not isinstance(expand_horizontal, bool):
            raise TypeError(
                f"expand_horizontal must be True or False, not {type(expand_horizontal).__name__} ({expand_horizontal!r})."
            )
        if not isinstance(expand_vertical, bool):
            raise TypeError(
                f"expand_vertical must be True or False, not {type(expand_vertical).__name__} ({expand_vertical!r})."
            )

        target_master = self._get_grid_master()
        
        if target_master is None:
            # Container not created yet, store for later
            self._pending_children.append({
                'widget': widget, 'column': column, 'row': row,
                'row_span': row_span, 'column_span': column_span,
                'expand_horizontal': expand_horizontal, 'expand_vertical': expand_vertical,
                'align_horizontal': align_horizontal, 'align_vertical': align_vertical,
                'kwargs': kwargs
            })
            self._num_columns = max(self._num_columns, column + column_span - 1)
            self._num_rows = max(self._num_rows, row + row_span - 1)
            return

        # Create the widget if it hasn't been created
        if widget._ctk_object is None:
            widget._create_widget(target_master)
            widget._apply_pending_properties()
            widget._apply_bindings()
        
        # Set default padding if not provided, using the widget's preference if available
        default_padding = getattr(widget, '_default_grid_padding', WIDGET_PADDING)
        kwargs.setdefault('padx', default_padding)
        kwargs.setdefault('pady', default_padding)
        
        # Determine sticky value based on stretch flags and alignment
        sticky = ""
        
        # Horizontal
        if expand_horizontal:
            sticky += "ew"
        elif align_horizontal == "left":
            sticky += "w"
        elif align_horizontal == "right":
            sticky += "e"
        elif align_horizontal == "center":
            pass # Default
            
        # Vertical
        if expand_vertical:
            sticky += "ns"
        elif align_vertical == "top":
            sticky += "n"
        elif align_vertical == "bottom":
            sticky += "s"
        elif align_vertical == "center":
            pass # Default
        
        # Grid it
        widget._ctk_object.grid(row=row, column=column, rowspan=row_span, columnspan=column_span, sticky=sticky, **kwargs)
        self._children.append(widget)
        self._num_columns = max(self._num_columns, column + column_span - 1)
        self._num_rows = max(self._num_rows, row + row_span - 1)

        # Auto-assign weight=1 to each column spanned, unless the user has set a custom weight
        for col in range(column, column + column_span):
            if col not in self._user_column_weights:
                target_master.grid_columnconfigure(col, weight=1)

        if hasattr(self, '_update_sizes'):
            self._update_sizes()

    def _process_pending_children(self):
        """Adds any children that were added before the container was created."""
        for child in self._pending_children:
            self.add(child['widget'], child['column'], child['row'], 
                     row_span=child['row_span'], column_span=child['column_span'],
                     expand_horizontal=child['expand_horizontal'], expand_vertical=child['expand_vertical'],
                     align_horizontal=child['align_horizontal'], align_vertical=child['align_vertical'],
                     **child['kwargs'])
        self._pending_children = []

    def _set_column_weight(self, index, weight):
        self._user_column_weights.add(index)
        master = self._get_grid_master()
        if master:
            master.grid_columnconfigure(index, weight=weight)
        else:
            self._pending_column_weights[index] = weight

    def set_column_weights(self, *weights):
        """Sets the weight of all columns at once. The number of weights must match the number of columns."""
        if len(weights) != self._num_columns:
            raise ValueError(
                f"set_column_weights() expected {self._num_columns} argument(s) "
                f"(one per column) but received {len(weights)}."
            )
        for i, weight in enumerate(weights, start=1):
            self._set_column_weight(i, weight)

    def _set_row_weight(self, index, weight):
        master = self._get_grid_master()
        if master:
            master.grid_rowconfigure(index, weight=weight)
        else:
            self._pending_row_weights[index] = weight

    def set_row_weights(self, *weights):
        """Sets the weight of all rows at once. The number of weights must match the number of rows."""
        if len(weights) != self._num_rows:
            raise ValueError(
                f"set_row_weights() expected {self._num_rows} argument(s) "
                f"(one per row) but received {len(weights)}."
            )
        for i, weight in enumerate(weights, start=1):
            self._set_row_weight(i, weight)

    def _apply_pending_container_properties(self):
        """Applies pending grid configurations."""
        master = self._get_grid_master()
        if master:
            for index, weight in self._pending_column_weights.items():
                master.grid_columnconfigure(index, weight=weight)
            self._pending_column_weights.clear()

            for index, weight in self._pending_row_weights.items():
                master.grid_rowconfigure(index, weight=weight)
            self._pending_row_weights.clear()



class Frame(GooeyPieContainer, GooeyPieWidget):
    _style_properties = (
        'bg_color',
        'border_color',
        'border_width',
    )

    def __init__(self, **kwargs):
        """
        A container that is also a widget.

        Args:
            **kwargs: Standard widget arguments.
        """
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)

    @property
    def width(self):
        return GooeyPieWidget.width.fget(self)

    @width.setter
    def width(self, value):
        GooeyPieWidget.width.fset(self, value)
        if self._ctk_object:
            self._ctk_object.pack_propagate(False)
            self._update_sizes()

    @property
    def height(self):
        return GooeyPieWidget.height.fget(self)

    @height.setter
    def height(self, value):
        GooeyPieWidget.height.fset(self, value)
        if self._ctk_object:
            self._ctk_object.pack_propagate(False)
            self._update_sizes()

    def _update_sizes(self):
        if not self._ctk_object:
            return
        
        custom_w = self._constructor_kwargs.get('width')
        custom_h = self._constructor_kwargs.get('height')
        
        if custom_w is None and custom_h is None:
            return
            
        self._ctk_object.update_idletasks()
        
        req_w = self._grid_master.winfo_reqwidth() + (2 * CONTAINER_PADDING)
        req_h = self._grid_master.winfo_reqheight() + (2 * CONTAINER_PADDING)
        
        w = custom_w if custom_w is not None else req_w
        h = custom_h if custom_h is not None else req_h
        
        self._ctk_object.configure(width=w, height=h)

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkFrame(master, **self._constructor_kwargs)
        
        if 'width' in self._constructor_kwargs or 'height' in self._constructor_kwargs:
            self._ctk_object.pack_propagate(False)
            
        # Create the internal grid frame with transparent background
        # This handles the extra padding needed to reach 24px from edge (16 + 8 from widget)
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both", padx=CONTAINER_PADDING, pady=CONTAINER_PADDING)
        self._apply_pending_container_properties()
        self._process_pending_children()
        self._update_sizes()


class ScrollableFrame(GooeyPieContainer, GooeyPieWidget):
    _style_properties = (
        'bg_color',
        'border_color',
        'border_width',
    )

    def __init__(self, **kwargs):
        """
        A scrollable container that is also a widget.

        Args:
            **kwargs: Standard widget arguments.
        """
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)
        self._max_column = 0

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkScrollableFrame(master, **self._constructor_kwargs)
        self._grid_master = self._ctk_object
        self._apply_pending_container_properties()
        self._process_pending_children()

    def add(self, widget, x, y, **kwargs):
        """Adds a widget to the scrollable frame, ensuring proper padding for the scrollbar."""
        if self._ctk_object is None:
            super().add(widget, x, y, **kwargs)
            return

        # Get existing padx or default
        padx = kwargs.get('padx', WIDGET_PADDING)
        
        # Add extra padding to the right (second element of tuple)
        # Scrollbar is usually around 15-20px
        extra_padding = 10
        
        if isinstance(padx, int):
            # Convert int to tuple (left, right) and add extra to right
            kwargs['padx'] = (padx, padx + extra_padding)
        elif isinstance(padx, (tuple, list)) and len(padx) == 2:
            # Add to existing right padding
            kwargs['padx'] = (padx[0], padx[1] + extra_padding)
            
        super().add(widget, x, y, **kwargs)
        
        # Update column weights
        if x > self._max_column:
            self._max_column = x
            
        grid_master = self._get_grid_master()
        for i in range(self._max_column):
            grid_master.grid_columnconfigure(i, weight=0)
        grid_master.grid_columnconfigure(self._max_column, weight=1)


class Container(GooeyPieContainer, GooeyPieWidget):
    _style_properties = (
        'bg_color',
        'border_color',
        'border_width',
    )

    _default_grid_padding = 0

    def __init__(self, **kwargs):
        """
        A minimal, invisible container for layout grouping.

        Args:
            **kwargs: Standard widget arguments.
        """
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)

    @property
    def width(self):
        return GooeyPieWidget.width.fget(self)

    @width.setter
    def width(self, value):
        GooeyPieWidget.width.fset(self, value)
        if self._ctk_object:
            self._ctk_object.pack_propagate(False)
            self._update_sizes()

    @property
    def height(self):
        return GooeyPieWidget.height.fget(self)

    @height.setter
    def height(self, value):
        GooeyPieWidget.height.fset(self, value)
        if self._ctk_object:
            self._ctk_object.pack_propagate(False)
            self._update_sizes()

    def _update_sizes(self):
        if not self._ctk_object:
            return
        
        custom_w = self._constructor_kwargs.get('width')
        custom_h = self._constructor_kwargs.get('height')
        
        if custom_w is None and custom_h is None:
            return
            
        self._ctk_object.update_idletasks()
        
        req_w = self._grid_master.winfo_reqwidth()
        req_h = self._grid_master.winfo_reqheight()
        
        w = custom_w if custom_w is not None else req_w
        h = custom_h if custom_h is not None else req_h
        
        self._ctk_object.configure(width=w, height=h)

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkFrame(master, fg_color="transparent", border_width=0, corner_radius=0, **self._constructor_kwargs)
        
        if 'width' in self._constructor_kwargs or 'height' in self._constructor_kwargs:
            self._ctk_object.pack_propagate(False)
            
        # For Container, we create the internal grid frame with transparent background and no padding
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both")
        self._apply_pending_container_properties()
        self._process_pending_children()
        self._update_sizes()
