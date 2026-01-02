import customtkinter as ctk

# Material Design implementation
# 24px outer margins
# 16px gutter between elements (8px per side per element)
EDGE_PADDING = 24
WIDGET_PADDING = 8
CONTAINER_PADDING = EDGE_PADDING - WIDGET_PADDING # 16px padding on container so 16+8=24px total

class GooeyPieObject:
    """Base class for all GooeyPie objects that wrap customtkinter widgets."""
    def __init__(self):
        self._ctk_object = None
        self._pending_properties = {}

    def _set_property(self, key, value):
        if self._ctk_object:
            self._ctk_object.configure(**{key: value})
            
            # Special handling for some properties if needed
            # e.g. if key == 'disabled': ...
            # But standard ctk use state='disabled'/'normal'
        else:
            # Store it to apply later
            self._pending_properties[key] = value

    def _apply_pending_properties(self):
        """Applies any properties set before the widget was created."""
        if self._ctk_object and self._pending_properties:
            self._ctk_object.configure(**self._pending_properties)
            self._pending_properties.clear()

    def _get_property(self, key):
        if self._ctk_object:
            try:
                return self._ctk_object.cget(key)
            except ValueError:
                return None
        return self._pending_properties.get(key)

