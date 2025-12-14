# Mactoast 🍞

An elegant and super easy to use Python library for creating customizable toast notifications on macOS.

## Features

- 🎨 **Customizable**: Colors, size, position, timing, and more
- 💊 **Modern Design**: Borderless, modern UI with no title bar or buttons
- ⚡ **Non-Blocking**: Run toasts asynchronously without blocking your script
- 🎭 **Animated**: Smooth fade-in and fade-out animations
- 🪶 **Lightweight**: Minimal dependencies, uses a bundled native macOS app
- 🎯 **Icons**: Native SF Symbols support for beautiful icons
- 👆 **Click to Dismiss**: Tap any toast to dismiss it immediately
- 📏 **Auto-Size**: Automatically calculates optimal dimensions for your message
- 🔊 **Sound Effects**: Built-in notification sounds with custom sound support

## Toast Styles

| Success | Error | Warning | Info |
|---------|-------|---------|------|
| ![Success Toast](https://github.com/rafa-rrayes/mactoast/blob/master/screenshots/success_toast.png) | ![Error Toast](https://github.com/rafa-rrayes/mactoast/blob/master/screenshots/error_toast.png) | ![Warning Toast](https://github.com/rafa-rrayes/mactoast/blob/master/screenshots/warning_toast.png) | ![Info Toast](https://github.com/rafa-rrayes/mactoast/blob/master/screenshots/info_toast.png) |

## Installation

```bash
pip install mactoast
```

## Quick Start

```python
from mactoast import toast

# Simple toast
toast("Hello from macOS!")

# With icon and sound
toast("Success!", icon="checkmark.circle.fill", sound="confirmation1")

# Preset styles
from mactoast import show_success, show_error, show_warning, show_info
show_success("File saved!")
show_error("Connection failed!")
```

## Key Examples

### Colors & Positioning

```python
from mactoast import toast, ToastPosition

# Custom colors
toast("Blue toast", bg="#0080FF", text_color="#FFFFFF")

# Position
toast("Top Right", position=ToastPosition.TOP_RIGHT)
toast("Custom", position=(500, 500))
```

### Auto-Size

```python
# Automatically sizes to fit content
toast("Short!", auto_size=True)
toast("This is a longer message that wraps", auto_size=True)
```

### Non-Blocking Mode

```python
# Launch toast and continue immediately
process = toast("Background", blocking=False)
print(f"Toast PID: {process.pid}")

# Launch multiple toasts at once
for i in range(4):
    toast(f"Toast {i+1}", blocking=False)
```

### Sound Effects

```python
# 16 bundled sounds in 4 categories
toast("Beep!", sound="beep1")
toast("Success", sound="confirmation1")
toast("Pop!", sound="pop2")
toast("Sci-fi", sound="scifi1.m4a")

# Custom sound file
toast("Custom", sound="/path/to/sound.wav")
```

### Icons (SF Symbols)

```python
# Use any SF Symbol name
toast("Download complete", icon="arrow.down.circle.fill")
toast("Settings", icon="gearshape.fill")
toast("Message", icon="paperplane.fill")
```

## Complete Documentation

For comprehensive documentation including:
- Full API reference
- ToastHUD Swift app architecture
- Sound system details
- Building from source
- Advanced examples
- Troubleshooting

**See [DOCS.md](DOCS.md)**

## Requirements

- macOS 10.15+
- Python 3.8+

## Links

- **Documentation**: [DOCS.md](DOCS.md)
- **PyPI**: https://pypi.org/project/mactoast/
- **GitHub**: https://github.com/rafa-rrayes/mactoast
- **SF Symbols**: https://developer.apple.com/sf-symbols/

## License

MIT License - see LICENSE file for details
