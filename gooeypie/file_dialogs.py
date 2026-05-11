import os
from tkinter import filedialog


def _get_parent():
    """Resolves the parent CTk window from the running GooeyPieApp."""
    from .app import GooeyPieApp
    app = GooeyPieApp._main_app
    return app._ctk_object if app is not None else None


class FileWindow:
    """Abstract base class for opening files and folders

    Inherited by OpenSaveFileWindow
    """
    def __init__(self, title):
        """Creates a new FileWindow with the given title"""
        self._title = title
        self._options = {}

    def _build_options(self):
        """Returns the options dict, resolving the parent at call time."""
        options = dict(self._options)
        options['parent'] = _get_parent()
        options['title'] = self._title
        return options

    def set_initial_folder(self, folder_name, *paths):
        """Sets an initial named folder that the FileWindow will open to

        The initial folder name is a common name used across operating systems, corresponding to either the location of
        the currently running app, or the user's home directory, documents directory or desktop.

        Args:
            folder_name (str): the named folder where the window will initially open to. Must be one of 'home',
                'documents', 'desktop' or 'app'
            *paths: additional subfolders under the initial folder
        """
        folder_name = folder_name.lower()
        if folder_name not in ('home', 'documents', 'desktop', 'app'):
            raise ValueError("Argument 'folder_name' must be one of 'home', 'documents', 'desktop' or 'app'")

        home = os.path.expanduser('~')
        if folder_name == 'home':
            self._options['initialdir'] = home
        if folder_name == 'documents':
            if os.name == 'nt':
                import ctypes.wintypes
                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf) # CSIDL_PERSONAL = 5
                self._options['initialdir'] = buf.value
            else:
                self._options['initialdir'] = os.path.join(home, 'Documents')
        if folder_name == 'desktop':
            if os.name == 'nt':
                import ctypes.wintypes
                buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
                ctypes.windll.shell32.SHGetFolderPathW(None, 16, None, 0, buf) # CSIDL_DESKTOPDIRECTORY = 16
                self._options['initialdir'] = buf.value
            else:
                self._options['initialdir'] = os.path.join(home, 'Desktop')
        if folder_name == 'app':
            self._options['initialdir'] = os.path.abspath(os.getcwd())

        self._options['initialdir'] = os.path.join(self._options['initialdir'], *paths)

    @property
    def initial_path(self):
        """Gets or sets the full path of the location that the FileWindow will open to.

        The path will vary by operating system - e.g. Windows fonts could be in 'C:\\\\Windows\\\\Fonts\\\\', but the
        equivalent in macOS is '\"'/Library/Fonts'
        """
        return self._options.get('initialdir', None)

    @initial_path.setter
    def initial_path(self, path):
        self._options['initialdir'] = path


class OpenSaveFileWindow(FileWindow):
    """Abstract base class for opening and saving file window

    Inherited by OpenFileWindow and SaveFileWindow
    """
    def __init__(self, title):
        """Create a new Open or Save window with the given title"""
        super().__init__(title)
        self._options['filetypes'] = [('All files', '*.*')]

    def add_file_type(self, description, extension):
        """Adds a new file type to be displayed as a filter when opening or saving files

        Args:
            description (str): A description of the file type(s)
            extension (str): The file pattern(s) to filter, multiple types should be separated with a space
        """
        if self._options['filetypes'] == [('All files', '*.*')]:
            # Replace the default "All files" file type if it is the only one.
            self._options['filetypes'] = [(description, extension)]
        else:
            self._options['filetypes'].append((description, extension))

    def remove_file_type(self, description, extension):
        """Removes an existing file type from the filter list when opening or saving files

        Args:
            description (str): A description of the file type(s)
            extension (str): The file pattern(s) to filter, multiple types should be separated with a space

        Raises:
            ValueError: if the (description, extension) has not previously been added with a call to add_file_type
        """
        try:
            self._options['filetypes'].remove((description, extension))
        except ValueError:
            raise ValueError(f'Cannot remove file type ({description}, {extension}) as it has not been previously '
                             f'added to the list of file types for this file window')

        if not self._options['filetypes']:
            self._options['filetypes'] = [('All files', '*.*')]


class OpenFileWindow(OpenSaveFileWindow):
    """Open file dialog"""
    def __init__(self, title):
        """Creates a new Open File Window

        Args:
            title (str): The title that appears on the Open File Window title bar
        """
        super().__init__(title)
        self._select_multiple_files = False

    @property
    def allow_multiple(self):
        """Gets or sets whether to allow the user to select multiple files when the Open File Window is initiated"""
        return self._select_multiple_files

    @allow_multiple.setter
    def allow_multiple(self, allow):
        self._select_multiple_files = bool(allow)

    def open(self):
        """Launches the file open dialog and returns the selected and path filename(s),

        Returns:
            The filename as a string including the full path, or if multiple files are selected a list of all
            path-filenames, or None if the user clicks cancel or otherwise dismisses the window
        """
        options = self._build_options()
        if self.allow_multiple:
            return filedialog.askopenfilenames(**options) or None
        else:
            return filedialog.askopenfilename(**options) or None


class SaveFileWindow(OpenSaveFileWindow):
    """Save File window"""
    def __init__(self, title):
        """Creates a new Save File Window

        Args:
            title (str): The title that appears on the Save File Window title bar
        """
        super().__init__(title)

    def open(self):
        """Launches the file save window

        Returns:
            The selected/entered filename(s) and its full path, including the extension added with add_file_type
                Returns None if the user clicks cancel or otherwise dismisses the window
        """

        # If the default extension is not specified, no extension is added even when one is selected
        return filedialog.asksaveasfilename(**self._build_options(), defaultextension='') or None


class OpenFolderWindow(FileWindow):
    """Allows a user to select a folder on their local system, returns the full path to the folder"""
    def __init__(self, title):
        """Creates a new Open Folder Window

        Args:
            title (str): The title that appears on the Open Folder Window title bar
        """
        super().__init__(title)

    def open(self):
        """Launches the Open Folder window

        Returns:
            The complete path to the selected folder as a string, or None if the user selects Cancel or otherwise
                dismisses the window
        """
        return filedialog.askdirectory(**self._build_options(), mustexist=True) or None
