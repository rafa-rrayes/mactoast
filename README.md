# Mactoast 🍞

An elegant and super easy to use Python library for creating customizable toast notifications on macOS.

## Features

- 🎨 **Customizable**: Colors, size, position, timing, and more
- 💊 **Modern Design**: Borderless, modern UI with no title bar or buttons
- ⚡ **Non-Blocking**: Run toasts asynchronously without blocking your script
- 🎭 **Animated**: Smooth fade-in and fade-out animations
- 🪶 **Lightweight**: Minimal dependencies, uses a bundled native macOS app

## Toast Styles

| Success | Error | Warning | Info |
|---------|-------|---------|------|
| ![Success Toast](screenshots/success_toast.png) | ![Error Toast](screenshots/error_toast.png) | ![Warning Toast](screenshots/warning_toast.png) | ![Info Toast](screenshots/info_toast.png) |

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
from mactoast import toast

# Simple toast
toast("Hello from macOS!")
```

## Usage Examples

### Basic Toast with Custom Colors

```python
from mactoast import toast

# Blue toast using hex color
toast(
    "Operation completed!",
    bg="#0080FF",
    text_color="#FFFFFF"
)

# Green success toast using RGB tuple (0.0-1.0)
toast(
    "Success!",
    bg=(0.0, 0.8, 0.0),
    text_color=(0.0, 0.0, 0.0)
)
```

### Positioning

You can use the `ToastPosition` enum for standard locations or a tuple for custom coordinates.

```python
from mactoast import toast, ToastPosition

# Standard positions: TOP_RIGHT, TOP_LEFT, BOTTOM_RIGHT, BOTTOM_LEFT, CENTER
toast("Top Right", position=ToastPosition.TOP_RIGHT)

# Custom coordinates (x, y) from bottom-left of screen
toast("Custom Spot", position=(500, 500))
```

### Window Levels

Control the z-index of your toast. Useful for showing notifications over full-screen apps or screensavers.

```python
from mactoast import toast, WindowLevel

# Show above everything, including screensavers
toast("Wake Up!", window_level=WindowLevel.SCREENSAVER)

# Floating window (always on top of normal windows)
toast("Always on top", window_level=WindowLevel.FLOATING)
```

### Non-Blocking Mode

By default, `toast()` blocks until the notification fades out. You can run it asynchronously:

```python
from mactoast import toast
import time

# This returns immediately
process = toast("I won't stop you!", blocking=False)

print("Script continues running...")
time.sleep(2)

# You can wait for it later if needed
# process.wait()
```

### Helper Functions

Mactoast includes presets for common notification types:

```python
from mactoast import show_success, show_error, show_warning, show_info

show_success("File saved successfully")
show_error("Connection failed")
show_warning("Disk space low")
show_info("Update available")
```

## API Reference

### `toast()`

Display a customizable popup toast on macOS.

#### Parameters

- **message** (`str`): Text to display in the toast.
- **width** (`float`, optional): Width in points. Default: 280.
- **height** (`float`, optional): Height in points. Default: 80.
- **bg** (`str` | `tuple`, optional): Background color. Can be hex string (`#RRGGBB` or `#RRGGBBAA`) or RGB/RGBA tuple of floats (0.0-1.0).
- **text_color** (`str` | `tuple`, optional): Text color. Same format as `bg`.
- **position** (`ToastPosition` | `str` | `tuple`, optional): 
    - Enum: `ToastPosition.TOP_RIGHT`, `ToastPosition.CENTER`, etc.
    - Tuple: `(x, y)` coordinates.
- **font_size** (`float`, optional): Font size in points. Default: 14.
- **corner_radius** (`float`, optional): Corner radius. Default: 16.
- **display_duration** (`float`, optional): Seconds to stay visible. Default: 2.5.
- **fade_in_duration** (`float`, optional): Seconds to fade in. Default: 0.2.
- **fade_out_duration** (`float`, optional): Seconds to fade out. Default: 0.2.
- **window_level** (`WindowLevel` | `str`, optional): 
    - Enum: `WindowLevel.NORMAL`, `WindowLevel.FLOATING`, `WindowLevel.SCREENSAVER`, etc.
- **blocking** (`bool`, default=`True`): If `True`, waits for the toast to finish. If `False`, returns immediately.

## Requirements

- macOS 10.15+
- Python 3.8+

## License

MIT License - see LICENSE file for details
