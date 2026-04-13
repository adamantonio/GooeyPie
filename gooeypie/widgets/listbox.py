from ..base import GooeyPieObject, WIDGET_PADDING
from .widget import GooeyPieWidget
from CTkListbox import CTkListbox
import tkinter
import contextlib

class Listbox(GooeyPieWidget):
    _style_properties = (
        'align',
        'bg_color',
        'border_color',
        'border_width',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'hover_color',
        'selected_color',
        'text_color',
        'text_disabled_color',
        'unselected_color',
    )

    """
    A listbox widget that allows the user to select one or more items from a list.
    Wraps CTkListbox.
    """

    def _set_property(self, key, value):
        if key == 'align':
            super()._set_property('justify', value)
        elif key == 'text_disabled_color':
            self._text_disabled_color = value
            if self._ctk_object:
                for btn in self._ctk_object.buttons.values():
                    btn.configure(text_color_disabled=value)
        else:
            super()._set_property(key, value)

    def __init__(self, items=None, **kwargs):
        """
        :param items: Initial list of items.
        :param kwargs: Additional arguments (height, width, multiple_selection, etc).
        """
        super().__init__(**kwargs)
        
        self._items = list(items) if items is not None else []
        
        # Apply defaults if not present
        self._constructor_kwargs.setdefault('height', 200)
        self._constructor_kwargs.setdefault('width', 200)
        self._constructor_kwargs.setdefault('multiple_selection', False)
        self._suppress_count = 0
        self._disabled_state = False
        self._text_disabled_color = ('gray74', 'gray60')

        # Initialize internal state from constructor kwargs
        self._height = self._constructor_kwargs['height']
        self._multiple_selection = self._constructor_kwargs['multiple_selection']
        
        # We handle the items manually after creation to ensure correct state hooks
        # But CTkListbox doesn't take items in init, strict sense? 
        # It takes listvariable or we insert.
        
        # Hook command for change event
        self._constructor_kwargs['command'] = self._on_select_command
    
    def _create_widget(self, master):
        self._ctk_object = CTkListbox(master, **self._constructor_kwargs)
        
        # Initial population
        if self._items:
            for item in self._items:
                self._ctk_object.insert("END", item)
                
        # Monkey-patch check_if_master_is_canvas to block scroll wheel events over the frame when disabled
        original_check = self._ctk_object.check_if_master_is_canvas
        def custom_check(widget):
            if self._disabled_state:
                return False
            return original_check(widget)
        self._ctk_object.check_if_master_is_canvas = custom_check

        # Monkey-patch the scrollbar to prevent manual dragging and highlighting
        if hasattr(self._ctk_object, '_scrollbar'):
            scrollbar = self._ctk_object._scrollbar
            
            orig_clicked = scrollbar._clicked
            def safe_clicked(event):
                if not self._disabled_state:
                    orig_clicked(event)
            scrollbar._clicked = safe_clicked
            
            orig_mouse_scroll = scrollbar._mouse_scroll_event
            def safe_mouse_scroll(event=None):
                if not self._disabled_state:
                    orig_mouse_scroll(event)
            scrollbar._mouse_scroll_event = safe_mouse_scroll
            
            orig_on_enter = scrollbar._on_enter
            def safe_on_enter(event=0):
                if not self._disabled_state:
                    orig_on_enter(event)
            scrollbar._on_enter = safe_on_enter

        # Apply delayed states
        for btn in self._ctk_object.buttons.values():
            btn.configure(text_color_disabled=self._text_disabled_color)
            if self._disabled_state:
                btn.configure(state='disabled')

    def _on_select_command(self, selected_value):
        """Callback from CTkListbox when selection changes."""
        self._handle_event('change')

    @contextlib.contextmanager
    def _suppress_events(self):
        """Suppresses native selection events during programmatic selection changes and fires exactly one event at the end."""
        if not self._ctk_object:
            yield
            return
            
        self._suppress_count += 1
        
        if self._suppress_count == 1:
            self._ctk_object.configure(command=None)
            if hasattr(self._ctk_object, 'command'):
                self._ctk_object.command = None
                
        try:
            yield
        finally:
            self._suppress_count -= 1
            if self._suppress_count == 0:
                self._ctk_object.configure(command=self._on_select_command)
                if hasattr(self._ctk_object, 'command'):
                    self._ctk_object.command = self._on_select_command
                self._handle_event('change')

    def _refresh_items(self):
        """Clears and re-populates the listbox from self._items."""
        if not self._ctk_object:
            return
            
        # Intercept and patch buttons before mass deletion to prevent CTkListbox TclError bug
        try:
            for btn in self._ctk_object.buttons.values():
                orig = btn.configure
                def safe_config(*args, orig_fn=orig, **kwargs):
                    try:
                        orig_fn(*args, **kwargs)
                    except Exception:
                        pass
                btn.configure = safe_config
        except Exception:
            pass

        # Clear existing
        # CTkListbox delete("all") clears buttons and keys
        self._ctk_object.delete("all")
        
        # Insert all
        for item in self._items:
            self._ctk_object.insert("END", item)
            
        # Re-apply our button states
        for btn in self._ctk_object.buttons.values():
            btn.configure(text_color_disabled=self._text_disabled_color)
            if self._disabled_state:
                btn.configure(state='disabled')

    @property
    def items(self):
        return tuple(self._items)
    
    @items.setter
    def items(self, value):
        if not isinstance(value, (list, tuple)):
            raise TypeError("Items must be a list or tuple")
        self._items = list(value)
        self._refresh_items()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        if self._ctk_object:
            self._ctk_object.configure(height=value)
        self._constructor_kwargs['height'] = value

    @property
    def width(self):
        return self._get_property('width')
    
    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(width=value)
        self._constructor_kwargs['width'] = value

    @property
    def multiple_selection(self):
        return self._multiple_selection

    @multiple_selection.setter
    def multiple_selection(self, value):
        self._multiple_selection = bool(value)
        if self._ctk_object:
            self._ctk_object.configure(multiple_selection=self._multiple_selection)
        self._constructor_kwargs['multiple_selection'] = self._multiple_selection

    @property
    def selected(self):
        if not self._ctk_object:
            return None
            
        # CTkListbox.get() returns None, valid item string, or list of strings
        val = self._ctk_object.get()
        # If multiple, returns list. If single, returns item/None.
        # User requirement: "Returns None if no option ... If multiple ... items will be returned in a list (even if only a single item is selected)"
        
        if self._multiple_selection:
            # CTkListbox returns list for multiple=True
            if val is None:
                return []
            if not isinstance(val, list):
                return [val]
            return val
        else:
            return val

    @selected.setter
    def selected(self, value):
        if self._ctk_object is None:
            # TODO: Store initial selection if widget not created?
            # Current design relies on creating widget early.
            # If not created, ignoring for now or storing?
            # We don't have a way to store "pending selection" easily without complicating.
            # Assuming widget mostly exists. If not, it's ignored (limitation).
            return

        with self._suppress_events():
            self.select_none()
            
            if value is None:
                return

            if self._multiple_selection:
                values_to_select = value if isinstance(value, (list, tuple)) else [value]
                for v in values_to_select:
                    try:
                        idx = self._items.index(v)
                        self._ctk_object.select(idx)
                    except ValueError:
                        raise ValueError(f"Item '{v}' not found in Listbox")
            else:
                if isinstance(value, (list, tuple)):
                    raise ValueError("Cannot select multiple items when multiple_selection is False")
                
                try:
                    idx = self._items.index(value)
                    self._ctk_object.select(idx)
                except ValueError:
                    raise ValueError(f"Item '{value}' not found in Listbox")

    @property
    def selected_index(self):
        if not self._ctk_object:
            return None
            
        # CTkListbox.curselection()
        # Returns int index, or tuple of ints, or generator?
        # CTkListbox src: returns iterator or index?
        # Line 171: return tuple(indexes) (if multiple)
        # Line 176: return index (int) (if single)
        
        sel = self._ctk_object.curselection()
        
        if self._multiple_selection:
            if isinstance(sel, int):
                return [sel]
            if sel is None: # CTkListbox might return None? src check needed. src doesn't seem to return None explicitly, maybe empty tuple?
                # Line 164 index=0. Loops. if multiple, returns tuple(indexes). Empty tuple if none.
                return []
            return list(sel)
        else:
            # Single selection
            # Line 174 loops. If found, returns index.
            # If not found (loop finishes)? Returns None (default python return).
            return sel

    @selected_index.setter
    def selected_index(self, index):
        if self._ctk_object:
            # "only one index can be specified and will add to any existing selection"
            # So just select it.
            if index is None:
                # Interpret as clear? Or do nothing?
                # "Returns None if no item selected".
                # Setter usually mirrors getter logic or standard set logic.
                # If None passed, maybe we should maintain "None selected"?
                # But requirement says "add to any existing".
                # If I set None, maybe I should deselect all?
                # User says "select_none()" method exists.
                # I'll assume index is int.
                return
                
            with self._suppress_events():
                self._ctk_object.select(index)

    @property
    def disabled(self):
        return self._disabled_state

    @disabled.setter
    def disabled(self, value):
        self._disabled_state = bool(value)
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            for btn in self._ctk_object.buttons.values():
                btn.configure(state=state)

    # Methods
    def add_item(self, item):
        self._items.append(item)
        if self._ctk_object:
            btn = self._ctk_object.insert("END", item)
            # CTkListbox returns the button from insert
            if btn:
                btn.configure(text_color_disabled=self._text_disabled_color)
                if self._disabled_state:
                    btn.configure(state='disabled')

    def add_item_to_start(self, item):
        self._items.insert(0, item)
        self._refresh_items()

    def add_item_at_index(self, item, index):
        if index < 0 or index >= len(self._items):
            self._items.append(item)
        else:
            self._items.insert(index, item)
        self._refresh_items()

    def remove_item_at_index(self, index):
        """Removes and returns the item at the given index."""
        if index < 0 or index >= len(self._items):
            raise IndexError("Listbox index out of range")
            
        item = self._items.pop(index)
        if self._ctk_object:
            # We monkey-patch the button's configure method before deleting it 
            # to swallow the _tkinter.TclError thrown by CTkListbox's scheduled hover reset callbacks
            try:
                key = list(self._ctk_object.buttons.keys())[index]
                btn = self._ctk_object.buttons[key]
                orig = btn.configure
                def safe_config(*args, orig_fn=orig, **kwargs):
                    try:
                        orig_fn(*args, **kwargs)
                    except Exception:
                        pass
                btn.configure = safe_config
            except Exception:
                pass
            
            self._ctk_object.delete(index)
        return item

    def remove_selected(self):
        """Removes and returns any items currently selected."""
        # Get selected indices
        indices = self.selected_index
        if indices is None or indices == []:
            return [] if self._multiple_selection else None
            
        if not isinstance(indices, list):
            indices = [indices]
        
        # Sort indices descending to remove from back without shifting issues
        indices.sort(reverse=True)
        
        removed_items = []
        for idx in indices:
            removed_items.append(self.remove_item_at_index(idx))
            
        # Return list if multiple, else item?
        # "Returns any items currently selected". Implies list or single item?
        # "Returns None if no option... If multiple... list".
        # Assume same return type as 'selected'.
        if self._multiple_selection:
            return removed_items # Note: order will be reversed due to pop order? 
            # User might expect original order.
            # remove_item returns item.
            # I popped from end.
            # removed_items has [last_selected, ..., first_selected]
            # Reverse it back.
            return removed_items[::-1]
        else:
            return removed_items[0] if removed_items else None

    def select_all(self):
        if self._multiple_selection and self._ctk_object:
            with self._suppress_events():
                self._ctk_object.select("all")

    def select_none(self):
        if self._ctk_object:
            with self._suppress_events():
                if self._multiple_selection:
                    self._ctk_object.deactivate("all")
                else:
                    # Single selection clear
                    self._ctk_object.deselect(0)

    def clear(self):
        self._items = []
        self._refresh_items()

    def on_change(self, event_function):
        """Sets the event to be called when the selection changes."""
        self._set_event('change', event_function)

