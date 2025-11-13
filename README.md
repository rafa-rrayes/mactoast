# Mactoast 🍞

A simple, elegant Python library for creating customizable toast notifications on macOS.

## Features

- 🎨 **Customizable**: Colors, size, position, timing, and more
- 💊 **Modern Design**: Borderless, modern UI with no title bar or buttons
- ⚡ **Non-Blocking**: Works with existing event loops and standalone scripts
- 🎭 **Animated**: Fade-out animation
- 🖱️ **Non-Clickable**: Notifications don't interfere with your workflow
- 🪶 **Lightweight**: Minimal dependencies, uses native macOS APIs
- 🤖 **Auto-Detection**: Automatically detects whether to use blocking or non-blocking mode

## Installation

```bash
pip install mactoast
```

Or install from source:

```bash
git clone https://github.com/rafa-rrayes/mactoast.git
cd mactoast
pip install -e .
```

## Quick Start

```python
from mactoast import show_toast

# Simple toast with default dark theme
show_toast('Hello from macOS!')
```

## Usage Examples

### Basic Toast with Custom Colors

```python
from mactoast import show_toast

# Blue toast
show_toast(
    'Operation completed!',
    bg_color=(0.0, 0.5, 1.0),  # RGB values (0.0-1.0)
    text_color=(1.0, 1.0, 1.0)
)

# Green success toast
show_toast(
    'Success!',
    bg_color=(0.0, 0.8, 0.0),
    text_color=(0.0, 0.0, 0.0)
)
```

### Custom Size and Timing

```python
show_toast(
    'Custom popup!',
    width=400,
    height=100,
    display_duration=5.0,  # Show for 5 seconds
    fade_duration=2.0       # Fade out over 2 seconds
)
```

### Positioned Toast

```python
# Position at specific coordinates (x, y from bottom-left)
show_toast(
    'Top right corner',
    bg_color=(0.0, 0.8, 0.0),  # Green
    text_color=(0.0, 0.0, 0.0),  # Black text
    position=(1200, 800)
)
```

### Custom Corner Radius

```python
# Square corners
show_toast(
    'Squared corners',
    corner_radius=5  # Default is height/2 for pill shape
)
```

### Larger Text

```python
show_toast(
    'Big announcement!',
    font_size=24,
    width=350,
    height=120
)
```

## API Reference
    
### `show_toast()`

Display a customizable popup toast on macOS.

#### Parameters

- **message** (`str`): Text to display in the toast
- **width** (`int`, default=`280`): Width of the toast window in pixels
- **height** (`int`, default=`80`): Height of the toast window in pixels
- **bg_color** (`Tuple[float, float, float]`, default=`(1.0, 0.0, 0.0)`): Background color as RGB tuple (0.0-1.0 for each component)
- **text_color** (`Tuple[float, float, float]`, default=`(1.0, 1.0, 1.0)`): Text color as RGB tuple (0.0-1.0 for each component)
- **position** (`Optional[Tuple[int, int]]`, default=`None`): (x, y) position from bottom-left of screen, or None to center
- **corner_radius** (`Optional[float]`, default=`None`): Corner radius in pixels, or None for pill shape (height/2)
- **display_duration** (`float`, default=`2.0`): How long to display before fading (seconds)
- **fade_duration** (`float`, default=`1.0`): How long the fade-out takes (seconds)
- **font_size** (`float`, default=`16.0`): Font size for the text
- **window_level** (`int`, default=`3`): Window level (higher = more on top, 0=normal, 3=floating)


## Requirements

- macOS (tested on macOS 10.15+)
- Python 3.8+
- PyObjC (automatically installed)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with PyObjC and native macOS Cocoa APIs.
