from .entry import Entry

# U+25CF BLACK CIRCLE — larger than the bullet (U+2022), geometrically centred
# on the text baseline, and universally supported in all modern fonts. This matches
# the mask character used by macOS and most modern web browsers for password fields.
_MASK_CHAR = '\u25cf'


class Secret(Entry):
    
    def __init__(self, placeholder_text='', **kwargs):
        """
        A secret widget that masks its content by default.

        Args:
            placeholder_text (str): Optional - The placeholder text for the entry.
            **kwargs: Standard widget arguments.
        """
        # Pass show='●' to CTkEntry so characters are masked from the start.
        kwargs['show'] = _MASK_CHAR
        super().__init__(placeholder_text=placeholder_text, **kwargs)
        self._masked = True

    def mask(self):
        """Hide all characters and replace with a large centred dot (●)."""
        if not self._masked:
            self._masked = True
            if self._ctk_object:
                self._ctk_object.configure(show=_MASK_CHAR)
            else:
                self._constructor_kwargs['show'] = _MASK_CHAR

    def unmask(self):
        """Display the text as entered (no masking)."""
        if self._masked:
            self._masked = False
            if self._ctk_object:
                self._ctk_object.configure(show='')
            else:
                self._constructor_kwargs['show'] = ''

    def toggle(self):
        """Switch between masked and unmasked states."""
        if self._masked:
            self.unmask()
        else:
            self.mask()

    @property
    def masked(self):
        """Returns True if the widget is currently masking its content."""
        return self._masked
