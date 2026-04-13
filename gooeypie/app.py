import customtkinter as ctk
import os
import sys
import tempfile
from pathlib import Path
from .containers import GooeyPieContainer, CONTAINER_PADDING
from .events import GooeyPieEvent

_ASSETS_DIR = Path(__file__).parent / 'assets' / 'images'
_DEFAULT_ICON = _ASSETS_DIR / 'default_app_icon.png'
_DEFAULT_ICON_WIN = _ASSETS_DIR / 'default_app_icon.ico'

# Cache the temp ICO path so we only convert once per session (for user-supplied PNGs)
_cached_ico_path: str = None

def _get_ico_for_png(png_path: Path) -> str:
    """Converts a PNG to a temporary ICO file and returns the path (Windows only)."""
    global _cached_ico_path
    if _cached_ico_path and os.path.exists(_cached_ico_path):
        return _cached_ico_path
    from PIL import Image
    img = Image.open(png_path)
    ico_path = os.path.join(tempfile.gettempdir(), '_gooeypie_icon.ico')
    img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    _cached_ico_path = ico_path
    return ico_path

class TopLevelWindow(GooeyPieContainer):
    """Base class for top-level windows to share properties."""
    def __init__(self):
        super().__init__()
        self._width = None
        self._height = None
        self._interval_ids = {}
        self._interval_counter = 0
        self._timeout_ids = {}
        self._timeout_counter = 0

    def _update_geometry(self):
        if hasattr(self, '_running') and not self._running:
            return

        if self._width is None and self._height is None:
            return

        req_w = self._grid_master.winfo_reqwidth() + (2 * CONTAINER_PADDING)
        req_h = self._grid_master.winfo_reqheight() + (2 * CONTAINER_PADDING)

        scaling = self._ctk_object._get_window_scaling()

        w = self._width if self._width is not None else req_w
        h = self._height if self._height is not None else req_h
        
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
        self._update_geometry()

    @property
    def height(self):
        return self._height if self._height is not None else self._ctk_object.winfo_reqheight()

    @height.setter
    def height(self, value):
        self._height = value
        self._update_geometry()

    @property
    def geometry(self):
        return self._ctk_object.geometry()
    
    @geometry.setter
    def geometry(self, value):
        self._ctk_object.geometry(value)

    @property
    def resizable_horizontal(self):
        return bool(self._ctk_object.resizable()[0])

    @resizable_horizontal.setter
    def resizable_horizontal(self, value):
        current_vert = self._ctk_object.resizable()[1]
        self._ctk_object.resizable(bool(value), current_vert)

    @property
    def resizable_vertical(self):
        return bool(self._ctk_object.resizable()[1])

    @resizable_vertical.setter
    def resizable_vertical(self, value):
        current_horz = self._ctk_object.resizable()[0]
        self._ctk_object.resizable(current_horz, bool(value))

    def _set_window_icon(self, ctk_win, icon_path: Path):
        """Internal: applies an icon to the given CTk window object.
        On Windows, uses iconbitmap with an ICO file (bundled or converted from PNG).
        On other platforms, uses iconphoto with a PNG.
        """
        if sys.platform.startswith('win'):
            # Prefer a native .ico file; fall back to converting a PNG
            if icon_path.suffix.lower() == '.ico':
                ico_path = str(icon_path)
            else:
                ico_path = _get_ico_for_png(icon_path)
            # Setting iconbitmap also marks CTk's _iconbitmap_method_called=True,
            # which prevents CTk's after(200) from replacing our icon with the CTk logo.
            ctk_win.iconbitmap(ico_path)
        else:
            from PIL import Image, ImageTk
            self._icon_image = ImageTk.PhotoImage(Image.open(icon_path))
            ctk_win.iconphoto(True, self._icon_image)

    def set_icon(self, icon):
        if not os.path.exists(icon):
            raise FileNotFoundError(f"Icon file not found: {icon}")
        global _cached_ico_path
        _cached_ico_path = None  # Invalidate cache so the new icon is converted fresh
        self._set_window_icon(self._ctk_object, Path(icon))


    def set_size(self, width, height):
        self._width = width
        self._height = height
        self._update_geometry()

    def set_resizable(self, resizable):
        self._ctk_object.resizable(bool(resizable), bool(resizable))

    def _create_popup(self, title, message, category, buttons):
        """Internal helper to create a generic popup dialogue."""
        valid_categories = ['error', 'info', 'question', 'warning']
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {valid_categories}")

        alert_win = ctk.CTkToplevel(master=self._ctk_object)
        alert_win.title(title)
        
        _default_icon = _DEFAULT_ICON_WIN if sys.platform.startswith('win') and _DEFAULT_ICON_WIN.exists() else _DEFAULT_ICON
        if _default_icon.exists():
            if sys.platform.startswith('win'):
                ico_path = str(_default_icon)  # Already an .ico — no conversion needed
                alert_win.after(250, lambda: alert_win.iconbitmap(ico_path))
            elif hasattr(self, '_icon_image') and self._icon_image:
                alert_win.iconphoto(False, self._icon_image)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        light_path = os.path.join(current_dir, 'assets', 'images', f'{category}_light@2x.png')
        dark_path = os.path.join(current_dir, 'assets', 'images', f'{category}_dark@2x.png')

        from PIL import Image
        light_img = Image.open(light_path)
        dark_img = Image.open(dark_path)
        ctk_icon = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=(32, 32))

        alert_win.grid_columnconfigure(0, weight=1)
        alert_win.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(alert_win, fg_color="transparent")
        content_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")

        icon_lbl = ctk.CTkLabel(content_frame, text="", image=ctk_icon)
        icon_lbl.pack(side="left", padx=(0, 15), anchor="n")

        msg_lbl = ctk.CTkLabel(content_frame, text=message, justify="left", wraplength=400)
        msg_lbl.pack(side="left", fill="both", expand=True)

        btn_frame = ctk.CTkFrame(alert_win, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        btn_frame.grid_columnconfigure(0, weight=1)

        # Use a mutable list to pull the value out of the callback scope
        result_container = [None]
        
        def on_click(val):
            result_container[0] = val
            alert_win.destroy()

        for col_idx, (btn_text, btn_value) in enumerate(buttons):
            # Default argument hack to lock the variable in the lambda iteration
            btn = ctk.CTkButton(btn_frame, text=btn_text, width=80, 
                                command=lambda v=btn_value: on_click(v))
            btn.grid(row=0, column=col_idx + 1, sticky="e", padx=(10, 0))

        # Handle 'X' close gracefully returning None
        alert_win.protocol("WM_DELETE_WINDOW", lambda: on_click(None))

        alert_win.resizable(False, False)
        alert_win.update_idletasks()
        
        # Center the dialogue relative to the calling window
        x = self._ctk_object.winfo_x() + (self._ctk_object.winfo_width() // 2) - (alert_win.winfo_reqwidth() // 2)
        y = self._ctk_object.winfo_y() + (self._ctk_object.winfo_height() // 2) - (alert_win.winfo_reqheight() // 2)
        alert_win.geometry(f"+{x}+{y}")

        alert_win.grab_set()
        alert_win.focus_set()
        alert_win.wait_window()
        
        return result_container[0]

    def alert(self, title, message, category):
        """Displays a modal alert dialog with a specific icon."""
        self._create_popup(title, message, category, [("OK", None)])

    def ask_yes_no(self, title, message, category):
        """Displays a Yes/No modal dialog, returning True or False."""
        return self._create_popup(title, message, category, [("Yes", True), ("No", False)])

    def ask_ok_cancel(self, title, message, category):
        """Displays an OK/Cancel modal dialog, returning True or False."""
        return self._create_popup(title, message, category, [("OK", True), ("Cancel", False)])

    def ask_yes_no_cancel(self, title, message, category):
        """Displays a Yes/No/Cancel modal dialog, returning True, False, or None."""
        return self._create_popup(title, message, category, [("Yes", True), ("No", False), ("Cancel", None)])


class GooeyPieApp(TopLevelWindow):
    """The main application window."""
    _main_app = None

    def __init__(self, title="GooeyPie App"):
        super().__init__()
        if GooeyPieApp._main_app is None:
            GooeyPieApp._main_app = self
        self._ctk_object = ctk.CTk()
        self._width = None
        self._height = None
        self._running = False
        self._icon_image = None

        # Apply default icon immediately.
        # On Windows: calling iconbitmap() sets CTk's internal _iconbitmap_method_called=True,
        # which prevents CTk's after(200) from replacing our icon with its own CTk logo.
        _default_icon = _DEFAULT_ICON_WIN if sys.platform.startswith('win') and _DEFAULT_ICON_WIN.exists() else _DEFAULT_ICON
        if _default_icon.exists():
            self._set_window_icon(self._ctk_object, _default_icon)

        # Initialize basic settings
        self._ctk_object.title(title)
        # Note: We do NOT set geometry here, allowing properties to auto-size to content

        self._on_quit_event_function = None
        self._on_load_event_function = None
        self._is_mapped = False
        
        self._ctk_object.protocol("WM_DELETE_WINDOW", self._handle_wm_delete_window)
        self._ctk_object.bind("<Map>", self._handle_map_event)

        # Setup internal grid frame for consistent spacing
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both", padx=CONTAINER_PADDING, pady=CONTAINER_PADDING)

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

    def on_quit(self, event_function):
        """Sets the function to call when the application close button is clicked."""
        self._on_quit_event_function = event_function

    def on_load(self, event_function):
        """Sets the function to call when the application window first loads."""
        self._on_load_event_function = event_function

    def set_interval(self, ms, function, *args):
        """Repeatedly calls a function every 'ms' milliseconds."""
        self._interval_counter += 1
        timer_id = f"interval_{self._interval_counter}"
        
        def recurring_wrapper():
            if timer_id not in self._interval_ids:
                return
            
            # Schedule the next execution first stringently 
            next_after_id = self._ctk_object.after(ms, recurring_wrapper)
            self._interval_ids[timer_id] = next_after_id
            
            # Then execute the user function
            function(*args)
            
        initial_after_id = self._ctk_object.after(ms, recurring_wrapper)
        self._interval_ids[timer_id] = initial_after_id
        return timer_id

    def clear_interval(self, timer_id):
        """Stops an interval from further execution."""
        if timer_id in self._interval_ids:
            after_id = self._interval_ids.pop(timer_id)
            self._ctk_object.after_cancel(after_id)

    def set_timeout(self, ms, function, *args):
        """Calls a function once after 'ms' milliseconds."""
        self._timeout_counter += 1
        timer_id = f"timeout_{self._timeout_counter}"
        
        def wrapper():
            if timer_id in self._timeout_ids:
                del self._timeout_ids[timer_id]
            function(*args)
            
        after_id = self._ctk_object.after(ms, wrapper)
        self._timeout_ids[timer_id] = after_id
        return timer_id
        
    def clear_timeout(self, timer_id):
        """Cancels a pending timeout from executing."""
        if timer_id in self._timeout_ids:
            after_id = self._timeout_ids.pop(timer_id)
            self._ctk_object.after_cancel(after_id)

    def quit(self, event=None):
        """Terminates the application. Executes the on_quit event if one is set."""
        if self._on_quit_event_function:
            e = GooeyPieEvent('quit', self)
            result = self._on_quit_event_function(e)
            if result is False:
                return
        self._ctk_object.destroy()

    def force_quit(self, event=None):
        """Terminates the application immediately, bypassing any on_quit events."""
        self._ctk_object.destroy()

    def _handle_wm_delete_window(self):
        """Internal handler for window close button."""
        self.quit()

    def _handle_map_event(self, event):
        """Internal handler for application load."""
        if event.widget == self._ctk_object and not self._is_mapped:
            self._is_mapped = True
            if self._on_load_event_function:
                e = GooeyPieEvent('load', self, original_event=event)
                self._on_load_event_function(e)

    def copy_to_clipboard(self, text):
        """Copies the given text to the system clipboard."""
        self._ctk_object.clipboard_clear()
        self._ctk_object.clipboard_append(text)
        self._ctk_object.update()


class Window(TopLevelWindow):
    """An additional top-level application window."""
    def __init__(self, title="GooeyPie Window"):
        super().__init__()
        
        # Attach to main app if available
        master = GooeyPieApp._main_app._ctk_object if hasattr(GooeyPieApp, '_main_app') and GooeyPieApp._main_app else None
        self._ctk_object = ctk.CTkToplevel(master=master)
        self._on_close_event_function = None
        self._on_show_event_function = None
        self._is_mapped = False
        
        # Hidden by default
        self._ctk_object.withdraw()
        
        self._ctk_object.title(title)

        # Apply default icon.
        # CTkToplevel has a hard-coded after(200) that sets the CTk logo, so we must
        # schedule our icon slightly later at after(250) to win the race.
        _default_icon = _DEFAULT_ICON_WIN if sys.platform.startswith('win') and _DEFAULT_ICON_WIN.exists() else _DEFAULT_ICON
        if _default_icon.exists():
            if sys.platform.startswith('win'):
                ico_path = str(_default_icon)  # Already an .ico — no conversion needed
                self._ctk_object.after(250, lambda: self._ctk_object.iconbitmap(ico_path))
            else:
                from PIL import Image, ImageTk
                self._icon_image = ImageTk.PhotoImage(Image.open(_default_icon))
                self._ctk_object.after(250, lambda: self._ctk_object.iconphoto(True, self._icon_image))
        
        # Default close behavior is to hide
        self._ctk_object.protocol("WM_DELETE_WINDOW", self._handle_wm_delete_window)
        # Bind Map/Unmap to know when it is actually shown
        self._ctk_object.bind("<Map>", self._handle_map_event)
        self._ctk_object.bind("<Unmap>", self._handle_unmap_event)

        # Setup internal grid frame for consistent spacing
        self._grid_master = ctk.CTkFrame(self._ctk_object, fg_color="transparent")
        self._grid_master.pack(expand=True, fill="both", padx=CONTAINER_PADDING, pady=CONTAINER_PADDING)

    @property
    def parent(self):
        """Returns the main application object."""
        return GooeyPieApp._main_app

    def show(self):
        """Shows the window natively."""
        self._ctk_object.deiconify()

    def hide(self):
        """Hides the window."""
        self._ctk_object.grab_release()  # Release any grabs if it was shown on top
        self._ctk_object.withdraw()

    def show_on_top(self):
        """Opens the window as a modal, blocking input to other windows."""
        self._ctk_object.deiconify()
        self._ctk_object.grab_set()

    def on_show(self, event_function):
        """Sets the function to call when the window is shown."""
        self._on_show_event_function = event_function

    def on_close(self, event_function):
        """Sets the function to call when the window's close button is clicked."""
        self._on_close_event_function = event_function

    def _handle_map_event(self, event):
        """Internal handler for <Map> event."""
        # Ensure the event relates to the window itself and it wasn't already mapped
        if event.widget == self._ctk_object and not self._is_mapped:
            self._is_mapped = True
            if self._on_show_event_function:
                e = GooeyPieEvent('show', self, original_event=event)
                self._on_show_event_function(e)

    def _handle_unmap_event(self, event):
        """Internal handler for <Unmap> event."""
        if event.widget == self._ctk_object:
            self._is_mapped = False

    def _handle_wm_delete_window(self):
        """Internal handler for window close button."""
        if self._on_close_event_function:
            e = GooeyPieEvent('close', self)
            result = self._on_close_event_function(e)
            # If function explicitly returns False, block closing
            if result is False:
                return
                
        # Default action is to hide the window
        self.hide()
