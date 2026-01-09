import customtkinter as ctk
from .containers import GooeyPieContainer, CONTAINER_PADDING

class GooeyPieApp(GooeyPieContainer):
    """The main application window."""
    def __init__(self, title="GooeyPie App"):
        super().__init__()
        self._ctk_object = ctk.CTk()
        self._width = None
        self._height = None
        self._running = False
        
        # Initialize basic settings
        self._ctk_object.title(title)
        # Note: We do NOT set geometry here, allowing properties to auto-size to content

        # Setup internal grid frame for consistent spacing
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both", padx=CONTAINER_PADDING, pady=CONTAINER_PADDING)

    def _update_geometry(self):
        # If not running yet, don't force geometry (let run() handle it)
        # unless user explicitly sets something, but usually better to wait for content size
        if not self._running:
            return

        if self._width is None and self._height is None:
            # Fully auto-size (default behavior), do nothing
            return

        # Calculate required size based on content including padding
        req_w = self._grid_master.winfo_reqwidth() + (2 * CONTAINER_PADDING)
        req_h = self._grid_master.winfo_reqheight() + (2 * CONTAINER_PADDING)

        # Get the scaling factor applied by CTk
        scaling = self._ctk_object._get_window_scaling()

        w = self._width if self._width is not None else req_w
        h = self._height if self._height is not None else req_h
        
        # Divide by scaling factor because CTk geometry() and minsize() apply scaling themselves
        # but winfo_reqwidth/height return physical pixels (already scaled)
        self._ctk_object.geometry(f"{int(w/scaling)}x{int(h/scaling)}")

    @property
    def title(self):
        return self._ctk_object.title()

    @title.setter
    def title(self, value):
        self._ctk_object.title(value)

    @property
    def width(self):
        return self._width if self._width is not None else self._ctk_object.winfo_reqwidth()

    @width.setter
    def width(self, value):
        self._width = value
        if self._running:
            self._update_geometry()

    @property
    def height(self):
        return self._height if self._height is not None else self._ctk_object.winfo_reqheight()

    @height.setter
    def height(self, value):
        self._height = value
        if self._running:
            self._update_geometry()
    
    @property
    def geometry(self):
        return self._ctk_object.geometry()
    
    @geometry.setter
    def geometry(self, value):
        self._ctk_object.geometry(value)

    @property
    def theme(self):
        return ctk.get_appearance_mode().lower()

    @theme.setter
    def theme(self, value):
        valid_themes = ["light", "dark", "system"]
        if value.lower() not in valid_themes:
            raise ValueError(f"Theme must be one of {valid_themes}")
        ctk.set_appearance_mode(value)

    def run(self):
        """Starts the application main loop."""
        self._running = True
        self._ctk_object.update_idletasks()
        
        # Calculate minimum size needed by the inner frame
        # We need to account for the padding we added when packing _grid_master
        min_w = self._grid_master.winfo_reqwidth() + (2 * CONTAINER_PADDING)
        min_h = self._grid_master.winfo_reqheight() + (2 * CONTAINER_PADDING)
        
        # Correct for scaling
        scaling = self._ctk_object._get_window_scaling()
        self._ctk_object.minsize(int(min_w/scaling), int(min_h/scaling))
        
        # Apply initial geometry if properties were set
        self._update_geometry()
        
        self._ctk_object.mainloop()
