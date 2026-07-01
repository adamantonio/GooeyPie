import customtkinter as ctk
import tkinter.ttk as ttk
from .widget import GooeyPieWidget

class Table(GooeyPieWidget):
    """For displaying tabular data"""
    _style_properties = (
        'table_bg_color',
        'border_color',
        'border_width',
        'corner_radius',
        'font_name',
        'font_size',
        'font_style',
        'font_weight',
        'text_color',
        'selected_color',
        'header_bg_color',
        'header_text_color',
        'header_font_name',
        'header_font_size',
        'header_text_size',
        'header_font_weight',
        'header_font_style',
    )

    icon_spacing = '   '
    sort_ascending_icon = f'{icon_spacing}▲'
    sort_descending_icon = f'{icon_spacing}▼'

    def __init__(self, headings, **kwargs):
        """Creates a new Table widget

        Args:
            headings: A list of strings corresponding the heading of the Table
        """
        super().__init__(**kwargs)

        # Check that the heading are in a list
        if not isinstance(headings, (list, tuple)):
            raise ValueError(f'Headings must be a list. Argument was: {type(headings)}')

        self._headings = list(headings)
        self._num_columns = len(headings)
        self._sortable = True
        
        self._constructor_kwargs.setdefault('multiple_selection', False)
        self._multiple_selection = self._constructor_kwargs['multiple_selection']
        self._cached_data = []
        self._custom_style = {}
        
        self._style_name = f"Table_{id(self)}.Treeview"
        self._heading_style_name = f"{self._style_name}.Heading"
        
        self._constructor_kwargs['column_widths'] = {}
        self._constructor_kwargs['column_alignments'] = {}

    def _set_property(self, key, value):
        if key in self._style_properties or key in ('font', 'header_font'):
            self._custom_style[key] = value
            if self._ctk_object:
                self._apply_ctk_style(self._ctk_object.master)
        else:
            super()._set_property(key, value)
                
    def _get_property(self, key):
        if key in self._style_properties or key in ('font', 'header_font'):
            return self._custom_style.get(key)
        return super()._get_property(key)

    def _create_widget(self, master):
        bw = 2
        border_color = ctk.ThemeManager.theme["CTkEntry"]["border_color"]
        bg_color = ctk.ThemeManager.theme["CTkEntry"]["fg_color"]
        
        # Subclass CTkFrame to properly hook into appearance mode changes and scaling
        class TableFrame(ctk.CTkFrame):
            def _set_appearance_mode(inner_self, mode_string):
                super()._set_appearance_mode(mode_string)
                if hasattr(self, '_treeview') and self._treeview:
                    self._apply_ctk_style(master)
                    
            def _set_scaling(inner_self, *args, **kwargs):
                super()._set_scaling(*args, **kwargs)
                if hasattr(self, '_treeview') and self._treeview:
                    self._apply_ctk_style(master)
                    self._update_scrollbar()

        self._ctk_object = TableFrame(
            master, 
            fg_color=bg_color, 
            border_color=border_color, 
            border_width=bw, 
            corner_radius=6,
            width=0,
            height=0
        )
        
        # Set container to fill cell
        self._ctk_object.columnconfigure(0, weight=1)
        self._ctk_object.rowconfigure(0, weight=1)

        # Style configuration to match customtkinter
        self._apply_ctk_style(master)

        # Create and configure treeview
        selectmode = 'extended' if self._multiple_selection else 'browse'
        column_ids = tuple(range(self._num_columns))  # tuple of form (0, 1, 2, etc)
        self._treeview = ttk.Treeview(
            self._ctk_object, 
            columns=column_ids, 
            show='headings', 
            selectmode=selectmode, 
            style=self._style_name
        )
        
        if self.disabled:
            self._treeview.state(['disabled'])
            self._treeview.configure(selectmode='none')
        
        for index, heading in enumerate(self._headings):
            self._treeview.heading(index, text=heading, command=lambda col_id=index: self._sort_data(col_id))
            self._treeview.column(index, anchor='w')

        # Create vertical scrollbar configure behaviour
        self._v_scrollbar = ctk.CTkScrollbar(self._ctk_object, orientation='vertical', command=self._treeview.yview, height=0)
        self._treeview.configure(yscrollcommand=self._v_scrollbar.set)

        # create horizontal scrollbar and configure behaviour
        self._h_scrollbar = ctk.CTkScrollbar(self._ctk_object, orientation='horizontal', command=self._treeview.xview, width=0)
        self._treeview.configure(xscrollcommand=self._h_scrollbar.set)

        # Add to parent Container (initial padding is handled in _update_scrollbar)
        self._treeview.grid(row=0, column=0, sticky='nsew')
        self._v_scrollbar.grid(row=0, column=1, sticky='ns')
        self._h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Force initial scrollbar update to apply padding
        self._update_scrollbar()

        # Default scrollbar settings and bindings to update visibility of scrollbars
        self._treeview.bind('<Configure>', self._update_scrollbar)  # Update scrollbar visibility when widget changes size
        self._treeview.bind('<ButtonRelease-1>', self._update_scrollbar)
        self._treeview.bind('<<TreeviewSelect>>', self._on_select)

        if 'width' in self._constructor_kwargs:
            self._ctk_object.configure(width=self._constructor_kwargs['width'])
            self._ctk_object.grid_propagate(False)
            # update_idletasks needed to correctly determine reqheight for the first time
            self._ctk_object.update_idletasks()
            self._update_height()

        # Populate cached data
        if self._cached_data:
            for row in self._cached_data:
                self._treeview.insert('', 'end', values=row)

        # Apply cached height
        if 'height' in self._constructor_kwargs:
            self._treeview.configure(height=self._constructor_kwargs['height'])

        # Apply cached column properties
        for col, width in self._constructor_kwargs.get('column_widths', {}).items():
            self.set_column_width(col, width)
        for col, align in self._constructor_kwargs.get('column_alignments', {}).items():
            self.set_column_alignment(col, align)

    def _apply_ctk_style(self, master):
        style = ttk.Style(master)
        
        # Base colors from CTk Theme or custom overrides
        bg_color = self._custom_style.get('table_bg_color', ctk.ThemeManager.theme["CTkEntry"]["fg_color"])
        text_color = self._custom_style.get('text_color', ctk.ThemeManager.theme["CTkEntry"]["text_color"])
        selected_color = self._custom_style.get('selected_color', ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        heading_bg = self._custom_style.get('header_bg_color', ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        heading_fg = self._custom_style.get('header_text_color', "white")
        heading_hover = ctk.ThemeManager.theme["CTkButton"]["hover_color"]
        
        bg = self._ctk_object._apply_appearance_mode(bg_color) if isinstance(bg_color, (list, tuple)) else bg_color
        fg = self._ctk_object._apply_appearance_mode(text_color) if isinstance(text_color, (list, tuple)) else text_color
        sel = self._ctk_object._apply_appearance_mode(selected_color) if isinstance(selected_color, (list, tuple)) else selected_color
        
        h_bg = self._ctk_object._apply_appearance_mode(heading_bg) if isinstance(heading_bg, (list, tuple)) else heading_bg
        h_fg = self._ctk_object._apply_appearance_mode(heading_fg) if isinstance(heading_fg, (list, tuple)) else heading_fg
        h_hover = self._ctk_object._apply_appearance_mode(heading_hover) if isinstance(heading_hover, (list, tuple)) else heading_hover

        from customtkinter.windows.widgets.scaling import ScalingTracker
        scaling = ScalingTracker.get_widget_scaling(self._ctk_object)

        def _get_font_tuple(ctk_font, scaling):
            if ctk_font is None: return None
            if isinstance(ctk_font, ctk.CTkFont):
                family, size, style_str = ctk_font.create_scaled_tuple(scaling)
                style_str = style_str.replace("normal", "").replace("roman", "").strip()
                if not style_str:
                    return (family, size)
                return (family, size, style_str)
            
            # If it's a manual tuple, we try to scale its size manually
            if isinstance(ctk_font, (list, tuple)) and len(ctk_font) > 1:
                try:
                    scaled_size = round(abs(int(ctk_font[1])) * scaling)
                    new_font = list(ctk_font)
                    new_font[1] = -scaled_size  # Ensure pixel size
                    return tuple(new_font)
                except Exception:
                    pass
            return ctk_font

        table_font = self._custom_style.get('font')
        if table_font is None:
            table_font = ctk.CTkFont()
            
        header_font = self._custom_style.get('header_font')
        if header_font is None:
            header_font = ctk.CTkFont()

        font_tuple = _get_font_tuple(table_font, scaling)
        header_font_tuple = _get_font_tuple(header_font, scaling)

        # Fix for Windows: remove the 'Treeview.field' element which draws a white background in vista theme
        style.layout(self._style_name, [('Treeview.treearea', {'sticky': 'nswe'})])
        
        # Fix for Windows: use 'clam' theme's heading element to respect background color
        try:
            style.element_create("CustomHeading.heading", "from", "clam", "Treeheading.cell")
        except Exception:
            pass

        style.layout(self._heading_style_name, [
            ("CustomHeading.heading", {'sticky': 'nswe', 'children': [
                ('Treeheading.padding', {'sticky': 'nswe', 'children': [
                    ('Treeheading.image', {'side': 'right', 'sticky': ''}),
                    ('Treeheading.text', {'sticky': 'we'})
                ]})
            ]})
        ])

        style_kwargs = {
            'background': bg,
            'foreground': fg,
            'fieldbackground': bg,
            'borderwidth': 0
        }
        
        # Calculate scaled rowheight
        base_size = 13
        font = self._custom_style.get('font')
        if font:
            if isinstance(font, ctk.CTkFont):
                base_size = font.cget('size')
            elif isinstance(font, (list, tuple)) and len(font) > 1:
                try:
                    base_size = int(font[1])
                except Exception:
                    pass
        else:
            base_size = ctk.ThemeManager.theme["CTkFont"]["size"]
            
        scaled_size = round(abs(base_size) * scaling)
        style_kwargs['rowheight'] = scaled_size + 12

        if font_tuple:
            style_kwargs['font'] = font_tuple

        style.configure(self._style_name, **style_kwargs)
                        
        disabled_fg = ["gray50", "gray60"]
        fg_disabled = self._ctk_object._apply_appearance_mode(disabled_fg) if isinstance(disabled_fg, (list, tuple)) else disabled_fg

        style.map(self._style_name,
                  background=[('selected', sel)],
                  foreground=[('disabled', fg_disabled), ('selected', fg)])

        scaled_padding = round(5 * scaling)
        heading_kwargs = {
            'background': h_bg,
            'foreground': h_fg,
            'borderwidth': 1,
            'relief': "flat",
            'padding': (scaled_padding, scaled_padding)
        }
        if header_font_tuple:
            heading_kwargs['font'] = header_font_tuple

        style.configure(self._heading_style_name, **heading_kwargs)
                        
        style.map(self._heading_style_name,
                  background=[('active', h_hover)])

    def _on_select(self, event):
        self._handle_event('change')

    def on_change(self, event_function):
        self._set_event('change', event_function)

    def __str__(self):
        headings = []
        if getattr(self, '_treeview', None):
            headings = [self._treeview.heading(col_id)['text'] for col_id in range(self._num_columns)]
            # Remove any sort icons from the headings
            for index, heading in enumerate(headings):
                if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                    headings[index] = heading[:-len(self.sort_descending_icon)]
        else:
            headings = self._headings
            
        return f"<Table {tuple(headings)}>"

    def __repr__(self):
        return self.__str__()

    @property
    def height(self):
        """Gets or sets the height of the Table as the number of visible lines"""
        if self._ctk_object:
            return self._treeview.cget('height')
        return self._constructor_kwargs.get('height', 10)

    @height.setter
    def height(self, lines):
        if self._ctk_object:
            self._treeview.configure(height=lines)
            self._update_height()
        self._constructor_kwargs['height'] = lines

    @property
    def width(self):
        """Gets or sets the width of the table in pixels"""
        if self._ctk_object:
            return self._ctk_object.cget('width')
        return self._constructor_kwargs.get('width')

    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(width=value)
            self._ctk_object.grid_propagate(False)
        self._constructor_kwargs['width'] = value

    @property
    def disabled(self):
        return self._constructor_kwargs.get('state', 'normal') == 'disabled'

    @disabled.setter
    def disabled(self, value):
        state = 'disabled' if value else 'normal'
        self._constructor_kwargs['state'] = state
        if self._ctk_object:
            if value:
                self._treeview.state(['disabled'])
                self._treeview.configure(selectmode='none')
                self.select_none()
            else:
                self._treeview.state(['!disabled'])
                mode = 'extended' if self._multiple_selection else 'browse'
                self._treeview.configure(selectmode=mode)

    @property
    def sortable(self):
        """Gets or sets whether the data can be sorted by clicking on the headings"""
        return self._sortable

    @sortable.setter
    def sortable(self, value):
        self._sortable = bool(value)
        if not self._sortable and self._ctk_object:
            self._clear_sort_icons()

    def _update_scrollbar(self, _event=None):
        """Adds/removes the scrollbars as needed"""
        horizontal_scrollbar_needed = self._treeview.xview() != (0.0, 1.0)
        vertical_scrollbar_needed = self._treeview.yview() != (0.0, 1.0)

        row_span = 1 if horizontal_scrollbar_needed else 2
        col_span = 1 if vertical_scrollbar_needed else 2

        bw = self._ctk_object.cget("border_width")
        bw = int(bw) if bw else 2

        self._treeview.grid_remove()
        self._v_scrollbar.grid_remove()
        self._h_scrollbar.grid_remove()

        tree_pady = (bw, 0) if horizontal_scrollbar_needed else (bw, bw)
        tree_padx = (bw, 0) if vertical_scrollbar_needed else (bw, bw)
        self._treeview.grid(row=0, column=0, rowspan=row_span, columnspan=col_span, sticky='nsew', padx=tree_padx, pady=tree_pady)
        
        if vertical_scrollbar_needed:
            vscroll_pady = (bw, 0) if horizontal_scrollbar_needed else (bw, bw)
            self._v_scrollbar.grid(row=0, column=1, rowspan=row_span, sticky='ns', padx=(0, bw), pady=vscroll_pady)
        
        if horizontal_scrollbar_needed:
            hscroll_padx = (bw, 0) if vertical_scrollbar_needed else (bw, bw)
            self._h_scrollbar.grid(row=1, column=0, columnspan=col_span, sticky='ew', padx=hscroll_padx, pady=(0, bw))

        self._update_height()

    def _update_height(self):
        """Updates the height of the container if it's fixed in width"""
        if not self._ctk_object or self._ctk_object.grid_propagate():
            return
            
        bw = self._ctk_object.cget("border_width")
        bw = int(bw) if bw else 2
        
        req_h = self._treeview.winfo_reqheight()
        total_h = req_h + (bw * 2)
        
        horizontal_scrollbar_needed = self._treeview.xview() != (0.0, 1.0)
        if horizontal_scrollbar_needed:
            total_h += self._h_scrollbar.winfo_reqheight() + bw
            
        self._ctk_object.configure(height=total_h)

    def _sort_data(self, column_id):
        """When the column heading is clicked on, the data are sorted according to that column"""
        # Do not allow sorting if the table is disabled
        if self.disabled or not self._sortable:
            return

        # Update heading text with icon
        sort_descending = False
        for col_id in range(self._num_columns):
            heading = self._treeview.heading(col_id)['text']
            if col_id == column_id:
                # Set the sort icon according to whatever is already there
                if heading.endswith(self.sort_ascending_icon):
                    # Change from ascending icon to descending
                    heading_descending = f'{heading[:-len(self.sort_descending_icon)]}{self.sort_descending_icon}'
                    self._treeview.heading(col_id, text=heading_descending)
                    sort_descending = True
                elif heading.endswith(self.sort_descending_icon):
                    # Change from descending icon to ascending
                    heading_ascending = f'{heading[:-len(self.sort_descending_icon)]}{self.sort_ascending_icon}'
                    self._treeview.heading(col_id, text=heading_ascending)
                else:
                    # No current icon - set to descending by default
                    heading_ascending = f'{heading}{self.sort_ascending_icon}'
                    self._treeview.heading(col_id, text=heading_ascending)
            else:
                # Clear the icon from the heading text if it exists
                if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                    self._treeview.heading(col_id, text=heading[:-len(self.sort_descending_icon)])

        # Sort the data
        self.data = sorted(self.data, key=lambda l: l[column_id], reverse=sort_descending)

    def _clear_sort_icons(self):
        """Clear any icons that have been appended to column headings"""
        for col_id in range(self._num_columns):
            heading = self._treeview.heading(col_id)['text']
            if heading.endswith(self.sort_ascending_icon) or heading.endswith(self.sort_descending_icon):
                self._treeview.heading(col_id, text=heading[:-len(self.sort_descending_icon)])

    @property
    def data(self):
        """Gets or sets all data in the table as a list of lists"""
        if not self._ctk_object:
            return list(self._cached_data)
        return [self._treeview.item(line)['values'] for line in self._treeview.get_children()]

    @data.setter
    def data(self, values):
        if not all(isinstance(row, (list, tuple)) for row in values):
            raise ValueError('Table data must be a list of lists')
        if not all(len(row) == self._num_columns for row in values):
            raise ValueError('Could not set table data - the number of columns of the table does not match')

        if not self._ctk_object:
            self._cached_data = list(values)
            return

        self.clear()
        for line in values:
            self._treeview.insert('', 'end', values=line)
        self._update_scrollbar()

    @property
    def multiple_selection(self):
        """Gets or sets the ability to select multiple items in the Table"""
        if self._ctk_object:
            return str(self._treeview.cget('selectmode')) == 'extended'
        return self._multiple_selection

    @multiple_selection.setter
    def multiple_selection(self, multiple):
        self._multiple_selection = bool(multiple)
        if self._ctk_object:
            mode = 'extended' if multiple else 'browse'
            self._treeview.config(selectmode=mode)
            # Clear the selection if single selection is enabled
            if not multiple:
                self.select_none()
        else:
            self._constructor_kwargs['multiple_selection'] = multiple

    @property
    def selected(self):
        """Returns the selected data in the table"""
        if not self._ctk_object:
            return None
            
        selected_ids = self._treeview.selection()
        if not selected_ids:
            return None
        if self.multiple_selection:
            return [self._treeview.item(row_id)['values'] for row_id in selected_ids]
        else:
            return self._treeview.item(selected_ids)['values']

    @property
    def selected_row(self):
        """Gets or sets the index(es), starting from 0, of the selected row."""
        if not self._ctk_object:
            return None
            
        selected_ids = self._treeview.selection()
        all_ids = self._treeview.get_children()

        if not selected_ids:
            return None
        if self.multiple_selection:
            return [all_ids.index(selected) for selected in selected_ids]
        else:
            return all_ids.index(selected_ids[0])

    @selected_row.setter
    def selected_row(self, index):
        """Adds to the current selection if multiple selection is set"""
        if not self._ctk_object:
            return
            
        all_rows = self._treeview.get_children()
        if len(all_rows) == 0:
            raise ValueError(f'No items in Table to select')
        if index not in range(len(all_rows)):
            raise ValueError(f'The index must be in the range 0 to {len(all_rows) - 1}. '
                             f'The value of the index specified was {index}.')

        # Clear the current selection if single selection only
        if not self.multiple_selection:
            self.select_none()

        # Select the item specified by the index
        item_id = all_rows[index]
        self._treeview.selection_add(item_id)
        self._treeview.see(item_id)  # Show the selected row (in case it is not be in view)

    def add_row_at(self, index, data):
        """Adds a row of data to the table at a given index"""
        # Check if location is an integer
        if type(index) != int and index != 'end':
            raise TypeError(f'index must be an integer. The value provided was {index}')
        if not type(data) in (list, tuple):
            raise TypeError(f'row data must be a list')
        # Check if the number of columns in the data is correct
        if len(data) != self._num_columns:
            raise ValueError(f'The number of data arguments given ({len(data)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')

        if not self._ctk_object:
            if index == 'end':
                self._cached_data.append(data)
            else:
                self._cached_data.insert(index, data)
            return

        self._treeview.insert('', index, values=data)

        # Clear any sort icons if new data is added
        self._clear_sort_icons()
        self._update_scrollbar()

    def add_row(self, data):
        """Adds a row of data to the end of the table"""
        self.add_row_at('end', data)

    def add_row_to_top(self, data):
        """Adds a row of data to the top of the table"""
        self.add_row_at(0, data)

    def clear(self):
        """Removes all data from the table"""
        if not self._ctk_object:
            self._cached_data = []
            return
        for row_id in self._treeview.get_children():
            self._treeview.delete(row_id)
        self._update_scrollbar()

    def remove_row(self, index):
        """Removes the specified row from the table"""
        if type(index) != int:
            raise TypeError(f'index must be an integer. The value provided was {index}')
            
        if not self._ctk_object:
            if index < 0 or index >= len(self._cached_data):
                raise ValueError(f'The index must be between 0 and {len(self._cached_data) - 1}. '
                                 f'The value of index was {index}')
            return self._cached_data.pop(index)
            
        row_ids = self._treeview.get_children()
        if index < 0 or index > len(row_ids) - 1:
            raise ValueError(f'The index must be between 0 and {len(row_ids) - 1}. '
                             f'The value of index was {index}')
        row_data = self._treeview.item(row_ids[index])['values']
        self._treeview.delete(row_ids[index])
        self._update_scrollbar()
        return row_data

    def remove_selected(self):
        """Removes the currently selected row from the table"""
        if not self._ctk_object:
            return None
            
        row_data = self.selected
        self._treeview.delete(*self._treeview.selection())
        self._update_scrollbar()
        return row_data

    def set_column_width(self, column, width):
        """Sets the width in pixels of the specified column, indexed from 0"""
        if type(column) != int or column < 0:
            raise ValueError(f'Column index must be an integer > 0')
        if type(width) != int or width < 0:
            raise ValueError(f'Column width must be an integer > 0')

        if self._ctk_object:
            from customtkinter.windows.widgets.scaling import ScalingTracker
            scaling = ScalingTracker.get_widget_scaling(self._ctk_object)
            scaled_width = round(width * scaling)
            self._treeview.column(column, width=scaled_width)
        else:
            self._constructor_kwargs['column_widths'][column] = width

    def set_column_widths(self, *widths):
        """Sets the width in pixels of all columns of the table"""
        if len(widths) != self._num_columns:
            raise ValueError(f'The number of arguments supplied ({len(widths)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')
        for column, width in enumerate(widths):
            self.set_column_width(column, width)

    def set_column_alignment(self, column, align):
        """Sets the alignment of the content in the specified column, indexed from 0"""
        alignment_mapping = {'left': 'w', 'center': 'center', 'right': 'e'}

        if type(column) != int or column < 0:
            raise TypeError(f'Column number must be a positive integer. The value given was {column}')
        if align not in alignment_mapping.keys():
            raise ValueError(f'Column alignment value must be either "left", "right" or "center". '
                             f'The value provided was "{align}"')
        if self._ctk_object:
            self._treeview.column(column, anchor=alignment_mapping[align])
        else:
            self._constructor_kwargs['column_alignments'][column] = align

    def set_column_alignments(self, *aligns):
        """Sets the alignment of all columns"""
        if len(aligns) != self._num_columns:
            raise ValueError(f'The number of arguments supplied ({len(aligns)}) does not match '
                             f'the number of columns in the table ({self._num_columns})')
        for column, align in enumerate(aligns):
            self.set_column_alignment(column, align)

    def select_row(self, index):
        """Selects a given row in the table"""
        if not self._ctk_object:
            return
            
        all_rows = self._treeview.get_children()
        if len(all_rows) == 0:
            raise ValueError(f'Table has no rows to select')
        if index not in range(len(all_rows)):
            raise ValueError(f'The index must be between 0 and {len(all_rows) - 1}. '
                             f'The value of the index specified was {index}.')
        row_id = all_rows[index]
        self._treeview.selection_set(row_id)
        self._treeview.see(row_id)

    def select_all(self):
        """Selects all rows of the table if multiple selection is enabled."""
        if self.multiple_selection and self._ctk_object:
            self._treeview.selection_set(*self._treeview.get_children())

    def select_none(self):
        """Clears any selected rows in the table"""
        if self._ctk_object:
            self._treeview.selection_remove(*self._treeview.selection())
