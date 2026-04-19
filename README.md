# GooeyPie

GooeyPie is an intuitive and beginner-friendly Python GUI library built as a wrapper around [customtkinter](https://github.com/TomSchimansky/CustomTkinter). It simplifies the process of building modern, attractive user interfaces in Python while providing a clean and accessible API.

## Installation

You can install GooeyPie using `pip` (or your preferred package manager like `uv`):

```bash
python -m pip install gooeypie
```

## Documentation

For the complete documentation, lots of examples and other resources, visit the official documentation site at [gooeypie.dev](https://gooeypie.dev).


## Quick Start

Creating an application with GooeyPie is straightforward. The design focuses on simplicity: widgets are created standalone and the grid layout is managed directly when adding them to your application window.

```python
import gooeypie as gp

def say_hello(event):
    # Events are handled securely with access to the triggering widget state
    hello_lbl.text = "Hello GooeyPie!"

# Initialize the main application window
app = gp.GooeyPieApp("Welcome!")
app.width = 400

# Create widgets (notice no parent declaration is required)
hello_btn = gp.Button("Say Hello", say_hello)
hello_lbl = gp.Label("")

# Add widgets to the application by specifying their column and row position
app.add(hello_btn, 1, 1)
app.add(hello_lbl, 1, 2)

# Start the application loop
app.run()
```

## Features

- **Beginner-Friendly:** A simplified API that reduces boilerplate code and makes developing GUI applications fast and accessible.
- **Modern Look:** Built on top of `customtkinter`, meaning your applications look sleek and adhere to dark/light themes straight out of the box.
- **Dynamic Layout system:** Grids expand automatically to fit added widgets without needing extensive predefined setups.
- **Standalone Widgets:** Instantiate your widgets cleanly without needing to pass parent container arguments everywhere.
- **Event Handling Made Easy:** Simply define your event functions and pass them through to widgets effortlessly.


## Documentation Context

**Note: Version 0.14.0 introduced major breaking changes to the library's API.**

The traditional user interface aesthetic has been modernised, replacing older styling conventions with a sleeker, contemporary design that natively supports dark and light themes.

If you are looking for the documentation for older versions of GooeyPie prior to 0.14.0, that had a more traditional look and feel, please visit [legacy.gooeypie.dev](https://legacy.gooeypie.dev).

For the modern API, please refer to the updated official site at [gooeypie.dev](https://gooeypie.dev).
