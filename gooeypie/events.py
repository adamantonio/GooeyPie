class GooeyPieEvent:
    """Event object passed to callback functions."""
    def __init__(self, name, widget, original_event=None):
        self.name = name
        self.widget = widget
        self.original_event = original_event

    @property
    def key(self):
        """The key definition of the event (e.g. 'a', 'Return', 'Tab')."""
        if self.original_event:
            return self.original_event.keysym
        return None

    @property
    def x(self):
        """The x coordinate of the mouse event."""
        if self.original_event:
            return self.original_event.x
        return None

    @property
    def y(self):
        """The y coordinate of the mouse event."""
        if self.original_event:
            return self.original_event.y
        return None
        
    def __repr__(self):
        return f"<GooeyPieEvent name='{self.name}' widget={self.widget} original_event={self.original_event}>"
