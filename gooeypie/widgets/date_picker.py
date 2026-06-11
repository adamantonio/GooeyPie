import tkinter as tk
import customtkinter as ctk
import datetime as dt
from datetime import datetime, timedelta
import calendar
import locale
from .widget import GooeyPieWidget

def _get_os_date_format():
    try:
        current_locale = locale.getlocale(locale.LC_TIME)
        locale.setlocale(locale.LC_TIME, '')  # Set to user's default
        test_date = datetime(1999, 10, 22)
        formatted = test_date.strftime('%x')
        # Restore old locale
        locale.setlocale(locale.LC_TIME, current_locale)
        
        # Replace 1999 with %Y, 99 with %y, 10 with %m, 22 with %d
        fmt = formatted.replace('1999', '%Y').replace('99', '%y').replace('10', '%m').replace('22', '%d')
        
        # Validate format works
        datetime.strptime(formatted, fmt)
        return fmt
    except Exception:
        return '%Y-%m-%d'

class _CTkDatePicker(ctk.CTkFrame):
    def __init__(self, master=None, parent_widget=None, **kwargs):
        """
        Initialize the _CTkDatePicker instance.
        """
        width_val = kwargs.get('width')
        super().__init__(master, **kwargs)
        self.parent_widget = parent_widget

        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=0)
        # Bind key events for manual entry detection
        self.date_entry.bind("<KeyRelease>", self._on_entry_change)

        self.calendar_button = ctk.CTkButton(self, text="▼", width=20, font=("Helvetica", 12, "bold"), command=self.open_calendar)
        self.calendar_button.grid(row=0, column=1, sticky="ew", padx=0, pady=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        if width_val is not None:
            entry_width = max(10, width_val - 40)
            self.date_entry.configure(width=entry_width)

        self.popup = None
        self.selected_date = None
        self.date_format = _get_os_date_format()
        self.allow_manual_input = True
        self.allow_change_month = True
        self.add_months_amount = 0
        self.subtract_months_amount = 0
        self._disabled = False
        self.minimum_date = None
        self.maximum_date = None

        self._original_text_color = self.date_entry.cget('text_color')
        self._default_disabled_color = self.date_entry.cget('placeholder_text_color')

        # Intercept configure on the raw entry to capture dynamic style changes
        self.date_entry._original_configure = self.date_entry.configure
        self.date_entry.configure = self._configure_date_entry

    def _configure_date_entry(self, **kwargs):
        if 'text_color' in kwargs:
            self._original_text_color = kwargs['text_color']
            if self.disabled:
                disabled_color = self._default_disabled_color
                if self.parent_widget:
                    custom_color = self.parent_widget._get_property('text_disabled_color')
                    if custom_color:
                        disabled_color = custom_color
                kwargs['text_color'] = disabled_color
        self.date_entry._original_configure(**kwargs)

    def _on_entry_change(self, event=None):
        if self.parent_widget:
            self.parent_widget._check_change()

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value
        if value:
            self.date_entry.configure(state='disabled')
            disabled_color = self._default_disabled_color
            if self.parent_widget:
                custom_color = self.parent_widget._get_property('text_disabled_color')
                if custom_color:
                    disabled_color = custom_color
            self.date_entry.configure(text_color=disabled_color)
            self.calendar_button.configure(state='disabled')
        else:
            self.calendar_button.configure(state='normal')
            if self.allow_manual_input:
                self.date_entry.configure(state='normal')
            else:
                self.date_entry.configure(state='disabled')
            self.date_entry.configure(text_color=self._original_text_color)

    def configure(self, require_redraw=False, **kwargs):
        if 'state' in kwargs:
            state_val = kwargs.pop('state')
            self.disabled = (state_val == 'disabled')
        if 'width' in kwargs:
            width_val = kwargs.get('width')
            entry_width = max(10, width_val - 40)
            self.date_entry.configure(width=entry_width)
        super().configure(require_redraw=require_redraw, **kwargs)

    def cget(self, attribute_name: str):
        if attribute_name == 'state':
            return 'disabled' if self.disabled else 'normal'
        return super().cget(attribute_name)

    def set_date_format(self, date_format):
        self.date_format = date_format

    def set_minimum_date(self, val):
        self.minimum_date = val

    def set_maximum_date(self, val):
        self.maximum_date = val

    def set_localization(self, localization):
        try:
            locale.setlocale(locale.LC_ALL, localization)
            locale.setlocale(locale.LC_NUMERIC, "C")
        except Exception:
            pass

    def open_calendar(self):
        if self.disabled:
            return
        if self.popup is not None:
            self.popup.destroy()
        self.popup = ctk.CTkToplevel(self)
        self.popup.overrideredirect(True)
        self.popup.geometry("+%d+%d" % (self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()))
        self.popup.resizable(False, False)

        self.popup.after(100, lambda: self.popup.focus())
        self.popup.bind("<FocusOut>", self._on_focus_out)

        # Default to present month/year
        year = datetime.now().year
        month = datetime.now().month

        entry_val = self.get_date()
        if entry_val:
            try:
                parsed_dt = datetime.strptime(entry_val, self.date_format)
                year = parsed_dt.year
                month = parsed_dt.month
            except ValueError:
                pass

        self.current_year = year
        self.current_month = month
        self.build_calendar()

    def _on_focus_out(self, event=None):
        self.popup.after(10, self._check_focus)

    def _check_focus(self):
        if self.popup:
            focused = self.popup.focus_get()
            if focused is None or not str(focused).startswith(str(self.popup)):
                self.popup.destroy()
                self.popup = None

    def _assemble_font(self, prefix):
        if not self.parent_widget:
            return None
        pw = self.parent_widget
        name = pw._get_property(f'{prefix}_font_name')
        size = pw._get_property(f'{prefix}_font_size') or 12
        style = pw._get_property(f'{prefix}_font_style') or "normal"
        weight = pw._get_property(f'{prefix}_font_weight') or "normal"
        
        if name:
            slant = "roman" if style == "normal" else style
            return (name, size, weight, slant)
        elif size != 12 or style != "normal" or weight != "normal":
            # Just default family, but modified
            slant = "roman" if style == "normal" else style
            return ("Helvetica", size, weight, slant)
        return None

    def build_calendar(self):
        if hasattr(self, 'calendar_frame'):
            self.calendar_frame.destroy()

        self.calendar_frame = ctk.CTkFrame(self.popup)
        self.calendar_frame.grid(row=0, column=0)

        month_tc = None
        day_tc = None
        month_btn_bg = None
        month_btn_tc = None
        
        month_font = None
        day_font = None

        if self.parent_widget:
            pw = self.parent_widget
            month_tc = pw._get_property('month_text_color')
            day_tc = pw._get_property('day_text_color')
            day_hc = pw._get_property('day_hover_color')
            month_btn_bg = pw._get_property('month_button_bg_color')
            month_btn_tc = pw._get_property('month_button_text_color')
            month_btn_hc = pw._get_property('month_button_hover_color')
            
            month_font = self._assemble_font('month')
            day_font = self._assemble_font('day')

        # Add months
        if self.add_months_amount < 0:
            raise ValueError("add_months_amount cannot be negative")
        for i in range(self.add_months_amount):
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1

        # Subtract months
        if self.subtract_months_amount < 0:
            raise ValueError("subtract_months_amount cannot be negative")
        for i in range(self.subtract_months_amount):
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else:
                self.current_month -= 1

        # Month and Year Selector
        month_label_kwargs = {"text": f"{calendar.month_name[self.current_month].capitalize()}, {self.current_year}"}
        if month_tc: month_label_kwargs["text_color"] = month_tc
        if month_font: month_label_kwargs["font"] = month_font

        month_label = ctk.CTkLabel(self.calendar_frame, **month_label_kwargs)
        month_label.grid(row=0, column=1, columnspan=5)

        if self.allow_change_month:
            prev_kwargs = {"text": "<", "width": 5, "command": self.prev_month}
            if month_btn_bg and month_btn_bg != 'transparent': prev_kwargs["fg_color"] = month_btn_bg
            if month_btn_tc: prev_kwargs["text_color"] = month_btn_tc
            if month_btn_hc: prev_kwargs["hover_color"] = month_btn_hc
            prev_month_button = ctk.CTkButton(self.calendar_frame, **prev_kwargs)
            prev_month_button.grid(row=0, column=0)

            next_kwargs = {"text": ">", "width": 5, "command": self.next_month}
            if month_btn_bg and month_btn_bg != 'transparent': next_kwargs["fg_color"] = month_btn_bg
            if month_btn_tc: next_kwargs["text_color"] = month_btn_tc
            if month_btn_hc: next_kwargs["hover_color"] = month_btn_hc
            next_month_button = ctk.CTkButton(self.calendar_frame, **next_kwargs)
            next_month_button.grid(row=0, column=6)

        # Days of the week header
        days = [calendar.day_name[i][:3].capitalize() for i in range(7)]
        for i, day in enumerate(days):
            lbl_kwargs = {"text": day}
            if day_tc: lbl_kwargs["text_color"] = day_tc
            if day_font: lbl_kwargs["font"] = day_font
            lbl = ctk.CTkLabel(self.calendar_frame, **lbl_kwargs)
            lbl.grid(row=1, column=i)

        # Days in month
        month_days = calendar.monthrange(self.current_year, self.current_month)[1]
        start_day = calendar.monthrange(self.current_year, self.current_month)[0]
        day = 1
        for week in range(2, 8):
            for day_col in range(7):
                if week == 2 and day_col < start_day:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                elif day > month_days:
                    lbl = ctk.CTkLabel(self.calendar_frame, text="")
                    lbl.grid(row=week, column=day_col)
                else:
                    current_date = dt.date(self.current_year, self.current_month, day)
                    is_selectable = True
                    if self.minimum_date is not None and current_date < self.minimum_date:
                        is_selectable = False
                    if self.maximum_date is not None and current_date > self.maximum_date:
                        is_selectable = False

                    btn_kwargs = {
                        "text": str(day),
                        "width": 3,
                        "fg_color": "transparent"
                    }
                    if is_selectable:
                        btn_kwargs["command"] = lambda d=day: self.select_date(d)
                        if day_hc:
                            btn_kwargs["hover_color"] = day_hc
                        elif ctk.get_appearance_mode() == "Light":
                            btn_kwargs["hover_color"] = "#3b8ed0" # default ctk hover

                        if ctk.get_appearance_mode() == "Light":
                            btn_kwargs["text_color"] = day_tc or "black"
                        elif day_tc:
                            btn_kwargs["text_color"] = day_tc
                    else:
                        btn_kwargs["state"] = "disabled"
                        if ctk.get_appearance_mode() == "Light":
                            btn_kwargs["text_color"] = "#a0a0a0"
                        else:
                            btn_kwargs["text_color"] = "#505050"

                    if day_font:
                        btn_kwargs["font"] = day_font

                    btn = ctk.CTkButton(self.calendar_frame, **btn_kwargs)
                    btn.grid(row=week, column=day_col)
                    day += 1

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.build_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.build_calendar()

    def select_date(self, day):
        selected = datetime(self.current_year, self.current_month, day).date()
        if self.minimum_date is not None and selected < self.minimum_date:
            return
        if self.maximum_date is not None and selected > self.maximum_date:
            return
        self.selected_date = datetime(self.current_year, self.current_month, day)
        self.date_entry.configure(state='normal')
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, self.selected_date.strftime(self.date_format))
        if not self.allow_manual_input:
            self.date_entry.configure(state='disabled')
        self.popup.destroy()
        self.popup = None
        
        # Trigger change on parent
        if self.parent_widget:
            self.parent_widget._check_change()

    def get_date(self):
        return self.date_entry.get()

    def set_allow_manual_input(self, value):
        self.allow_manual_input = value
        if not self.disabled:
            if not value:
                self.date_entry.configure(state='disabled')
            else:
                self.date_entry.configure(state='normal')

    def set_change_months(self, add_or_sub, value):
        if add_or_sub == "add":
            self.add_months_amount = value
        elif add_or_sub == "sub":
            self.subtract_months_amount = value


class DatePicker(GooeyPieWidget):
    _style_properties = (
        'text_color',
        'text_disabled_color',
        'text_color_disabled',
        'corner_radius',
        'month_font_name',
        'month_font_size',
        'month_font_style',
        'month_font_weight',
        'month_text_color',
        'day_font_name',
        'day_font_size',
        'day_font_style',
        'day_font_weight',
        'day_text_color',
        'day_hover_color',
        'month_button_bg_color',
        'month_button_text_color',
        'month_button_hover_color',
        'open_button_bg_color',
        'open_button_icon_color',
        'open_button_hover_color',
        'date_bg_color',
        'date_border_color',
        'date_border_width',
        'date_font_name',
        'date_font_size',
        'date_font_style',
        'date_font_weight'
    )
    
    def __init__(self, **kwargs):
        min_date = kwargs.pop('minimum_date', None)
        max_date = kwargs.pop('maximum_date', None)
        super().__init__(**kwargs)
        self._last_date_str = ""
        self._localization = ""
        self._minimum_date = None
        self._maximum_date = None
        self.minimum_date = min_date
        self.maximum_date = max_date
        
    def _create_widget(self, master):
        kwargs = self._constructor_kwargs.copy()
        kwargs.pop('state', None)
        self._ctk_object = _CTkDatePicker(master, parent_widget=self, fg_color="transparent", **kwargs)
        # Apply cached state
        if hasattr(self, '_format'):
            self._ctk_object.set_date_format(self._format)
        if hasattr(self, '_localization') and self._localization:
            self._ctk_object.set_localization(self._localization)
        if hasattr(self, '_allow_manual_input'):
            self._ctk_object.set_allow_manual_input(self._allow_manual_input)
        if hasattr(self, '_minimum_date') and self._minimum_date:
            self._ctk_object.set_minimum_date(self._minimum_date)
        if hasattr(self, '_maximum_date') and self._maximum_date:
            self._ctk_object.set_maximum_date(self._maximum_date)
        if self._last_date_str:
            self.date_str = self._last_date_str
            
        # Apply disabled state if set
        if self._constructor_kwargs.get('state') == 'disabled':
            self._ctk_object.disabled = True
            
        # Apply initial styles
        for prop in self._style_properties:
            val = self._get_property(prop)
            if val is not None:
                self._set_property(prop, val)
        
    def _set_property(self, key, value):
        if key in self._style_properties and key not in ('text_color', 'corner_radius'):
            if not hasattr(self, '_custom_styles'):
                self._custom_styles = {}
            if key in ('text_disabled_color', 'text_color_disabled'):
                self._custom_styles['text_disabled_color'] = value
                self._custom_styles['text_color_disabled'] = value
            else:
                self._custom_styles[key] = value
            # Apply to open button if needed
            if self._ctk_object:
                if key == 'open_button_bg_color':
                    self._ctk_object.calendar_button.configure(fg_color=value)
                elif key == 'open_button_icon_color':
                    self._ctk_object.calendar_button.configure(text_color=value)
                elif key == 'open_button_hover_color':
                    self._ctk_object.calendar_button.configure(hover_color=value)
                elif key == 'date_bg_color':
                    self._ctk_object.date_entry.configure(fg_color=value)
                elif key == 'date_border_color':
                    self._ctk_object.date_entry.configure(border_color=value)
                elif key == 'date_border_width':
                    self._ctk_object.date_entry.configure(border_width=value)
                elif key in ('text_disabled_color', 'text_color_disabled'):
                    if self.disabled:
                        self._ctk_object.date_entry.configure(text_color=value)
                elif key in ('date_font_name', 'date_font_size', 'date_font_style', 'date_font_weight'):
                    font = self._ctk_object._assemble_font('date')
                    if font:
                        self._ctk_object.date_entry.configure(font=font)
            return
            
        super()._set_property(key, value)
        if self._ctk_object:
            if key in ('text_color', 'corner_radius'):
                kwargs = {key: value}
                try:
                    self._ctk_object.date_entry.configure(**kwargs)
                except Exception:
                    pass

    def _apply_pending_properties(self):
        if 'text_color' in self._pending_properties:
            text_color = self._pending_properties.pop('text_color')
            if self._ctk_object:
                self._ctk_object.date_entry.configure(text_color=text_color)
        for key in ('text_disabled_color', 'text_color_disabled'):
            if key in self._pending_properties:
                val = self._pending_properties.pop(key)
                if self._ctk_object and self.disabled:
                    self._ctk_object.date_entry.configure(text_color=val)
        super()._apply_pending_properties()

    def _get_property(self, key):
        if key in self._style_properties and key not in ('text_color', 'corner_radius'):
            if not hasattr(self, '_custom_styles'):
                self._custom_styles = {}
            if key in ('text_disabled_color', 'text_color_disabled'):
                return self._custom_styles.get('text_disabled_color') or self._custom_styles.get('text_color_disabled')
            return self._custom_styles.get(key)
        return super()._get_property(key)

    def _check_change(self):
        current_date_str = self._ctk_object.get_date()
        if current_date_str != self._last_date_str:
            self._last_date_str = current_date_str
            self._handle_event('change')

    @property
    def date(self):
        date_str = self.date_str
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, self.format).date()
        except ValueError:
            return None

    @date.setter
    def date(self, value):
        if value is None:
            self.clear()
        elif isinstance(value, dt.date):
            d_val = value.date() if isinstance(value, datetime) else value
            if self.minimum_date is not None and d_val < self.minimum_date:
                raise ValueError(f"Date {d_val} is before the minimum allowed date {self.minimum_date}")
            if self.maximum_date is not None and d_val > self.maximum_date:
                raise ValueError(f"Date {d_val} is after the maximum allowed date {self.maximum_date}")
            self.date_str = value.strftime(self.format)
        elif isinstance(value, datetime):
            d_val = value.date()
            if self.minimum_date is not None and d_val < self.minimum_date:
                raise ValueError(f"Date {d_val} is before the minimum allowed date {self.minimum_date}")
            if self.maximum_date is not None and d_val > self.maximum_date:
                raise ValueError(f"Date {d_val} is after the maximum allowed date {self.maximum_date}")
            self.date_str = d_val.strftime(self.format)
        else:
            raise ValueError("date must be a datetime.date object")

    @property
    def date_str(self):
        if self._ctk_object:
            return self._ctk_object.get_date()
        return self._last_date_str

    @date_str.setter
    def date_str(self, value):
        if value:
            try:
                datetime.strptime(value, self.format)
            except ValueError:
                raise ValueError(f"Date string '{value}' does not match the required format '{self.format}'")

        if self._ctk_object:
            current_state = self._ctk_object.date_entry.cget('state')
            self._ctk_object.date_entry.configure(state='normal')
            
            self._ctk_object.date_entry.delete(0, 'end')
            if value:
                self._ctk_object.date_entry.insert(0, value)
            
            self._ctk_object.date_entry.configure(state=current_state)
            self._check_change()
        else:
            self._last_date_str = value

    @property
    def format(self):
        if self._ctk_object:
            return self._ctk_object.date_format
        return getattr(self, '_format', _get_os_date_format())

    @format.setter
    def format(self, value):
        self._format = value
        if self._ctk_object:
            self._ctk_object.set_date_format(value)

    @property
    def localization(self):
        return self._localization

    @localization.setter
    def localization(self, value):
        self._localization = value
        if self._ctk_object:
            self._ctk_object.set_localization(value)

    @property
    def allow_manual_input(self):
        if self._ctk_object:
            return self._ctk_object.allow_manual_input
        return getattr(self, '_allow_manual_input', True)

    @allow_manual_input.setter
    def allow_manual_input(self, value):
        self._allow_manual_input = value
        if self._ctk_object:
            self._ctk_object.set_allow_manual_input(value)

    def open(self):
        if self._ctk_object:
            self._ctk_object.open_calendar()

    def set_today(self):
        self.date = datetime.now().date()

    def add_days(self, days):
        current_date = self.date or datetime.now().date()
        self.date = current_date + timedelta(days=days)

    def subtract_days(self, days):
        self.add_days(-days)
        
    def _shift_months(self, months):
        current = self.date or datetime.now().date()
        new_month = current.month - 1 + months
        year = current.year + new_month // 12
        new_month = new_month % 12 + 1
        day = min(current.day, calendar.monthrange(year, new_month)[1])
        self.date = dt.date(year, new_month, day)

    def add_months(self, months):
        self._shift_months(months)

    def subtract_months(self, months):
        self._shift_months(-months)

    def add_years(self, years):
        current = self.date or datetime.now().date()
        try:
            self.date = dt.date(current.year + years, current.month, current.day)
        except ValueError:
            # Leap year logic (Feb 29 -> Feb 28)
            self.date = dt.date(current.year + years, current.month, 28)

    def subtract_years(self, years):
        self.add_years(-years)

    def clear(self):
        self.date_str = ""

    @property
    def width(self):
        if self._ctk_object:
            return self._ctk_object.cget('width')
        return self._constructor_kwargs.get('width')

    @width.setter
    def width(self, value):
        if self._ctk_object:
            self._ctk_object.configure(width=value)
        self._constructor_kwargs['width'] = value

    @property
    def minimum_date(self):
        return self._minimum_date

    @minimum_date.setter
    def minimum_date(self, value):
        if value is not None:
            if isinstance(value, datetime):
                value = value.date()
            if not isinstance(value, dt.date):
                raise TypeError("minimum_date must be a datetime.date object")
            if self._maximum_date is not None and value > self._maximum_date:
                raise ValueError(f"Invalid date range: The minimum date ({value}) cannot be later than the maximum date ({self._maximum_date}).")
        self._minimum_date = value
        if self._ctk_object:
            self._ctk_object.set_minimum_date(value)

    @property
    def maximum_date(self):
        return self._maximum_date

    @maximum_date.setter
    def maximum_date(self, value):
        if value is not None:
            if isinstance(value, datetime):
                value = value.date()
            if not isinstance(value, dt.date):
                raise TypeError("maximum_date must be a datetime.date object")
            if self._minimum_date is not None and value < self._minimum_date:
                raise ValueError(f"Invalid date range: The maximum date ({value}) cannot be earlier than the minimum date ({self._minimum_date}).")
        self._maximum_date = value
        if self._ctk_object:
            self._ctk_object.set_maximum_date(value)

    def on_change(self, event_function):
        self._set_event('change', event_function)

    def _bind_event(self, event_name, sequence):
        if self._ctk_object:
            def handler(event):
                self._handle_event(event_name, event)
            
            # Keyboard and focus events should go directly to the text entry component
            if event_name in ('focus_gained', 'focus_lost', 'key_press'):
                self._ctk_object.date_entry.bind(sequence, handler, add='+')
            else:
                # Mouse/click/hover events bind to the outer frame, entry component, and button
                self._ctk_object.bind(sequence, handler, add='+')
                self._ctk_object.date_entry.bind(sequence, handler, add='+')
                self._ctk_object.calendar_button.bind(sequence, handler, add='+')
        else:
            self._pending_bindings.append((event_name, sequence))