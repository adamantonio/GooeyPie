import os
import sys
import customtkinter as ctk
from PIL import Image as PILImage
from .widget import GooeyPieWidget


class Image(GooeyPieWidget):
    """A widget that displays an image."""

    def __init__(self, image_path, **kwargs):
        """
        Args:
            image_path (str): Path to the image file (relative to script or absolute).
            **kwargs: Standard widget arguments.
        """
        super().__init__(**kwargs)
        self._image_path = image_path
        self._ctk_image = self._load_image(image_path)
        
        # Ensure image is passed to constructor kwargs so it's created with it
        if self._ctk_image:
            self._constructor_kwargs['image'] = self._ctk_image
        
        # Force no text
        self._constructor_kwargs['text'] = ""

    def _create_widget(self, master):
        self._ctk_object = ctk.CTkLabel(master, **self._constructor_kwargs)

    def _resolve_path(self, path):
        # Resolve path relative to the running script
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        return os.path.join(script_dir, path)

    def _load_image(self, path):
        full_path = self._resolve_path(path)
        try:
            if full_path.lower().endswith('.svg'):
                try:
                    from svglib.svglib import svg2rlg
                    from reportlab.graphics import renderPM
                except ImportError:
                    print(f"Error: SVG support requires extra dependencies. Install with 'pip install gooeypie[svg]'")
                    return None

                # Convert SVG to ReportLab drawing
                drawing = svg2rlg(full_path)
                # Render to PIL Image
                pil_image = renderPM.drawToPIL(drawing)
            else:
                pil_image = PILImage.open(full_path)
            
            return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=pil_image.size)
        except Exception as e:
            print(f"Error loading image '{full_path}': {e}")
            return None

    @property
    def image(self):
        """Gets or sets the path to the image."""
        return self._image_path

    @image.setter
    def image(self, path):
        self._image_path = path
        self._ctk_image = self._load_image(path)
        
        # Update the widget if it exists
        if self._ctk_object:
            # If load failed, _ctk_image is None. 
            # CTkLabel image update needs a CTkImage or valid image object (or None to remove?)
            # Usually we keep the old one or show empty if failed? 
            # Impl implies we clear if failed or show nothing.
            if self._ctk_image:
                self._ctk_object.configure(image=self._ctk_image)
            else:
                # If image load fails, maybe clear the image from the label?
                self._ctk_object.configure(image=None)
        
        # Update constructor args for potential recreation
        self._constructor_kwargs['image'] = self._ctk_image
