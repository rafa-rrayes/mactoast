# Mactoast 🍞

A simple, elegant Python library for creating customizable toast notifications on macOS.

## Features

- 🎨 **Fully Customizable**: Colors, size, position, timing, and more
- 💊 **Pill-Shaped Design**: Borderless, modern UI with no title bar or buttons
- ⚡ **Non-Blocking**: Works seamlessly with existing event loops (perfect for menu bar apps)
- 🎭 **Smooth Animations**: Beautiful fade-out effects
- 🖱️ **Non-Clickable**: Notifications don't interfere with your workflow
- 🪶 **Lightweight**: Minimal dependencies, uses native macOS APIs

## Installation

```bash
pip install mactoast
```

Or install from source:

```bash
git clone https://github.com/yourusername/mactoast.git
cd mactoast
pip install -e .
```

## Quick Start

```python
from mactoast import show_popup

# Simple red toast
show_popup('Hello from macOS!')
```

## Usage Examples

### Basic Toast with Custom Colors

```python
from mactoast import show_popup

# Blue toast
show_popup(
    'Operation completed!',
    bg_color=(0.0, 0.5, 1.0),  # RGB values (0.0-1.0)
    text_color=(1.0, 1.0, 1.0)
)
```

### Custom Size and Timing

```python
show_popup(
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
show_popup(
    'Top right corner',
    bg_color=(0.0, 0.8, 0.0),  # Green
    text_color=(0.0, 0.0, 0.0),  # Black text
    position=(1200, 800)
)
```

### Custom Corner Radius

```python
# Square corners
show_popup(
    'Squared corners',
    corner_radius=5  # Default is height/2 for pill shape
)
```

### Larger Text

```python
show_popup(
    'Big announcement!',
    font_size=24,
    width=350,
    height=120
)
```

### Blocking Mode

```python
# Block until the toast closes (useful for scripts)
show_popup(
    'Script completed!',
    blocking=True
)
```

### Non-Blocking Mode (Default)

```python
# Perfect for menu bar apps using rumps or similar
show_popup('Background task started')
# Code continues immediately
```

## API Reference

### `show_popup()`

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
- **blocking** (`bool`, default=`False`): If True, blocks until popup closes. If False, returns immediately

## Use Cases

- **Menu Bar Applications**: Show notifications from your rumps/menubar apps
- **Build Scripts**: Display completion messages or errors
- **Background Tasks**: Notify users when long-running tasks complete
- **Desktop Automation**: Add visual feedback to your automation scripts
- **Development Tools**: Show status updates during development

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
