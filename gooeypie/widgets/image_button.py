import os
import sys
import customtkinter as ctk
from PIL import Image
from .button import Button


class ImageButton(Button):
    def __init__(self, image_path, event_function, text="", **kwargs):
        self._image_path = image_path
        self._ctk_image = self._load_image(image_path)

        # Initialize Button (which handles command wrapping)
        # We pass empty text initially if user didn't provide any, but CTkButton can handle both text and image
        super().__init__(text=text, event_function=event_function, **kwargs)
        
        # Add image to constructor args for when _create_widget is called
        if self._ctk_image:
            self._constructor_kwargs['image'] = self._ctk_image

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
                pil_image = Image.open(full_path)
            
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
        
        if self._ctk_image:
            if self._ctk_object:
                self._ctk_object.configure(image=self._ctk_image)
            self._constructor_kwargs['image'] = self._ctk_image
            # If text is present, compound controls where image is relative to text. Default is usually left or top.
            # CTk default is 'left' (image to left of text) if both are present.
            if self.text:
                self._constructor_kwargs['compound'] = 'left'

    @property
    def image_position(self):
        val = self._get_property('compound')
        if val is None:
            val = self._constructor_kwargs.get('compound', 'left')
        return val

    @image_position.setter
    def image_position(self, value):
        valid = ['top', 'bottom', 'left', 'right']
        if value not in valid:
            raise ValueError(f"image_position must be one of {valid}")
        
        if self._ctk_object:
            self._ctk_object.configure(compound=value)
        self._constructor_kwargs['compound'] = value

    def _create_widget(self, master):
        # We override this just to ensure our ctk_image persists in the kwargs used by the parent class's logic
        # But actually parent class `Button` uses `_constructor_kwargs` too.
        # So we can just allow the parent to create the Tk widget using the props we injected above.
        super()._create_widget(master)
