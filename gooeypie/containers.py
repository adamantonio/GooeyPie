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
        self._grid_master = None # Will be set by subclasses

    def _get_grid_master(self):
        """Returns the widget that acts as the parent for the grid (geometry master)."""
        return self._grid_master or self._ctk_object

    def add(self, widget, x, y, row_span=1, column_span=1, expand_horizontal=False, expand_vertical=False, align_horizontal="center", align_vertical="center", **kwargs):
        """Adds a widget to this container at grid position (x, y)."""
        if not isinstance(widget, GooeyPieWidget):
            raise ValueError("Can only add GooeyPieWidget instances.")
        
        target_master = self._get_grid_master()
        
        if target_master is None:
            # Container not created yet, store for later
            self._pending_children.append({
                'widget': widget, 'x': x, 'y': y,
                'row_span': row_span, 'column_span': column_span,
                'expand_horizontal': expand_horizontal, 'expand_vertical': expand_vertical,
                'align_horizontal': align_horizontal, 'align_vertical': align_vertical,
                'kwargs': kwargs
            })
            return

        # Create the widget if it hasn't been created, using the target master
        # Note: If it WAS created (e.g. reparenting), we might have an issue 
        # as CTk widgets are hard to reparent. Assuming fresh widgets for now.
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
        widget._ctk_object.grid(row=y, column=x, rowspan=row_span, columnspan=column_span, sticky=sticky, **kwargs)
        self._children.append(widget)

    def _process_pending_children(self):
        """Adds any children that were added before the container was created."""
        for child in self._pending_children:
            self.add(child['widget'], child['x'], child['y'], 
                     row_span=child['row_span'], column_span=child['column_span'],
                     expand_horizontal=child['expand_horizontal'], expand_vertical=child['expand_vertical'],
                     align_horizontal=child['align_horizontal'], align_vertical=child['align_vertical'],
                     **child['kwargs'])
        self._pending_children = []

    def set_column_weight(self, index, weight):
        master = self._get_grid_master()
        if master:
            master.grid_columnconfigure(index, weight=weight)
        else:
            self._pending_column_weights[index] = weight

    def set_row_weight(self, index, weight):
        master = self._get_grid_master()
        if master:
            master.grid_rowconfigure(index, weight=weight)
        else:
            self._pending_row_weights[index] = weight

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
    """A container that is also a widget."""
    def __init__(self, **kwargs):
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkFrame(master, **self._constructor_kwargs)
        
        # Create the internal grid frame with transparent background
        # This handles the extra padding needed to reach 24px from edge (16 + 8 from widget)
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both", padx=CONTAINER_PADDING, pady=CONTAINER_PADDING)
        self._apply_pending_container_properties()
        self._process_pending_children()


class ScrollableFrame(GooeyPieContainer, GooeyPieWidget):
    """A scrollable container that is also a widget."""
    def __init__(self, **kwargs):
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)
        self._max_column = 0

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkScrollableFrame(master, **self._constructor_kwargs)
        # CTkScrollableFrame acts as the grid master for its content
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
        
        # Update column weights as requested: last column gets weight 1, others 0
        if x > self._max_column:
            self._max_column = x
            
        grid_master = self._get_grid_master()
        for i in range(self._max_column):
            grid_master.grid_columnconfigure(i, weight=0)
        grid_master.grid_columnconfigure(self._max_column, weight=1)


class Container(GooeyPieContainer, GooeyPieWidget):
    """A minimal, invisible container for layout grouping."""
    
    _default_grid_padding = 0

    def __init__(self, **kwargs):
        GooeyPieContainer.__init__(self)
        GooeyPieWidget.__init__(self, **kwargs)

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkFrame(master, fg_color="transparent", border_width=0, corner_radius=0, **self._constructor_kwargs)
        # For Container, the grid master is the widget itself (no internal padding frame)
        self._grid_master = self._ctk_object
        self._apply_pending_container_properties()
        self._process_pending_children()
