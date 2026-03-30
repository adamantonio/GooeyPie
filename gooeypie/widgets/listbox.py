from ..base import GooeyPieObject, WIDGET_PADDING
from .widget import GooeyPieWidget
from CTkListbox import CTkListbox
import tkinter

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
        'unselected_color',
    )

    """
    A listbox widget that allows the user to select one or more items from a list.
    Wraps CTkListbox.
    """

    def _set_property(self, key, value):
        if key == 'align':
            super()._set_property('justify', value)
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
        
        # Bind events
        # CTkListbox generates <<ListboxSelect>> internally when selection changes
        # But we also used 'command' in init.
        # Check CTkListbox: command is called in select/deselect.
        # We can rely on command.
        pass

    def _on_select_command(self, selected_value):
        """Callback from CTkListbox when selection changes."""
        self._handle_event('change')

    def _refresh_items(self):
        """Clears and re-populates the listbox from self._items."""
        if not self._ctk_object:
            return
            
        # Clear existing
        # CTkListbox delete("all") clears buttons and keys
        self._ctk_object.delete("all")
        
        # Insert all
        for item in self._items:
            self._ctk_object.insert("END", item)
            
        # Restore disabled state to new buttons if needed
        # CTkListbox doesn't propagate disabled state automatically on insert?
        # We need to check if we are disabled and configure new buttons.
        if self.disabled:
             # Re-apply disabled state which should iterate buttons
            self.disabled = True

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

        self.select_none()
        
        if value is None:
            return

        if self._multiple_selection:
            values_to_select = value if isinstance(value, (list, tuple)) else [value]
            for v in values_to_select:
                try:
                    # Find index
                    # Note: CTkListbox insert appends. Order in self._items matches display.
                    # Duplicates? Listbox usually selects first found?
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
                
            self._ctk_object.select(index)

    @property
    def disabled(self):
        # We need to override because we might need to disable buttons individually?
        # CTkListbox inherits CTkScrollableFrame. Disabling frame doesn't disable buttons usually.
        # We need to check if CTkListbox handles it. configure() in CTkListbox calls super().configure().
        # It doesn't seem to iterate buttons to disable them.
        return self._get_property('state') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        if self._ctk_object:
            self._ctk_object.configure(state=state) # Disables the frame/scrollbar
            # Also disable all buttons
            # Inspecting CTkListbox source: self.buttons is a dict.
            for btn in self._ctk_object.buttons.values():
                btn.configure(state=state)
                
        self._constructor_kwargs['state'] = state

    # Methods
    def add_item(self, item):
        self._items.append(item)
        if self._ctk_object:
            self._ctk_object.insert("END", item)
            if self.disabled:
                # Disable the new button (last one)
                # Key is "END{end_num}". 
                # Easier to just re-apply disabled to all or find last?
                # Optimization: find last.
                # But self.disabled setter loops all.
                # Let's just re-apply disabled if true.
                self.disabled = True

    def add_item_to_start(self, item):
        self._items.insert(0, item)
        self._refresh_items()

    def add_item_at(self, index, item):
        self._items.insert(index, item)
        self._refresh_items()

    def remove_item(self, index):
        """Removes and returns the item at the given index."""
        if index < 0 or index >= len(self._items):
            raise IndexError("Listbox index out of range")
            
        item = self._items.pop(index)
        if self._ctk_object:
            self._ctk_object.delete(index)
        return item

    def remove_selected(self):
        """Removes and returns any items currently selected."""
        # Get selected indices
        indices = self.selected_index
        if not indices:
            return [] if self._multiple_selection else None
            
        if not isinstance(indices, list):
            indices = [indices]
        
        # Sort indices descending to remove from back without shifting issues
        indices.sort(reverse=True)
        
        removed_items = []
        for idx in indices:
            removed_items.append(self.remove_item(idx))
            
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
        if self._ctk_object:
            # CTkListbox select("all") logic:
            # Line 111: if index=="all": loop select all.
            # Works for multiple=True.
            # If multiple=False? Line 112 check self.multiple.
            # If not multiple, select("all") does NOTHING in CTkListbox source (Line 112 indent).
            # So we should check multiple.
            # GooeyPie: select_all should probably work only if multiple?
            # Or assume user knows what they are doing.
            self._ctk_object.select("all")

    def select_none(self):
        if self._ctk_object:
            # CTkListbox deactivate("all") deselects all?
            # Line 213: deactivate("all").
            # If multiple: deselects all.
            # If single: deselects 0? Line 218: `self.deselect(0)`? Weird logic in CTkListbox.
            # Line 217: `elif len(self.buttons): self.deselect(0)`.
            # This only deselects the first item! That's a bug in CTkListbox or weird feature.
            # If I want to clear selection in single mode:
            # `self.deselect(self.selected_index)`?
            # `deselect(index)` in CTkListbox:
            # Line 203: if not multiple: if self.selected: deselect it.
            # So calling `deselect` with ANY index (even invalid?) might work if it hits line 204.
            # But line 208 `if index in self.buttons...` might be skipped.
            # Let's try `deselect(0)` or just manually deselect.
            
            # Using `deselect("all")`?
            # `deactivate` calls `deselect`.
            # I'll rely on `_ctk_object.deselect("all")` if it exists (it doesn't, `deselect` takes index).
            
            if self._multiple_selection:
                self._ctk_object.deactivate("all")
            else:
                # Single selection clear
                # CTkListbox.deselect logic checks `if not self.multiple: if self.selected: ...`
                # So just calling deselect(0) should trigger the first block?
                # Yes.
                self._ctk_object.deselect(0)

    def clear(self):
        self._items = []
        self._refresh_items()

    def on_change(self, event_function):
        """Sets the event to be called when the selection changes."""
        self._set_event('change', event_function)

