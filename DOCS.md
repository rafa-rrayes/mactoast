# Mactoast Documentation

Complete documentation for mactoast - an elegant Python library for creating customizable toast notifications on macOS.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Python API Reference](#python-api-reference)
- [Usage Examples](#usage-examples)
- [ToastHUD Swift App](#toasthud-swift-app)
- [Sound System](#sound-system)
- [Building from Source](#building-from-source)
- [Parameter Validation](#parameter-validation)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

Mactoast uses a hybrid Python + Swift architecture:

```
┌─────────────────┐            ┌──────────────────┐
│  Python Package │ ──────────>│  ToastHUD.app    │
│  (mactoast)     │ subprocess │  (Swift/SwiftUI) │
└─────────────────┘            └──────────────────┘
        │                            │
        │                            │
    User Code              Native macOS Rendering
```

### Components

1. **Python Layer** (`src/mactoast/`)
   - Public API (`toast()`, `show_success()`, etc.)
   - Auto-size calculation
   - Color normalization
   - Command-line argument construction
   - Process management (blocking/non-blocking)

2. **Swift App** (`ToastHUD.app`)
   - Native macOS window rendering
   - SF Symbols icon display
   - Sound playback (AVFoundation)
   - Animations (fade in/out)
   - Click-to-dismiss handling
   - Window positioning and levels

3. **Communication**
   - Python launches ToastHUD via subprocess
   - Configuration passed as CLI arguments
   - No inter-process communication during runtime
   - Each toast is an independent process

## Installation

### From PyPI

```bash
pip install mactoast
```

### From Source

```bash
git clone https://github.com/rafa-rrayes/mactoast.git
cd mactoast
pip install -e .
```

### Requirements

- macOS 10.15+ (Catalina or later)
- Python 3.8+
- No external Python dependencies

## Python API Reference

### Main Function: `toast()`

```python
def toast(
    message: str,
    width: Optional[float] = None,
    height: Optional[float] = None,
    bg: Optional[ColorType] = None,
    position: Optional[Union[ToastPosition, str, Tuple[float, float]]] = None,
    font_size: Optional[float] = None,
    text_color: Optional[ColorType] = None,
    corner_radius: Optional[float] = None,
    display_duration: Optional[float] = None,
    fade_out_duration: Optional[float] = None,
    fade_in_duration: Optional[float] = None,
    window_level: Optional[Union[WindowLevel, str]] = None,
    icon: Optional[str] = None,
    click_to_dismiss: bool = True,
    auto_size: bool = False,
    min_width: Optional[float] = None,
    max_width: Optional[float] = None,
    sound: Optional[str] = None,
    blocking: bool = True,
    check: bool = False,
) -> Union[subprocess.CompletedProcess, subprocess.Popen]
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `str` | *required* | Text to display in the toast |
| `width` | `float` | `280` | Width in points (ignored if `auto_size=True`) |
| `height` | `float` | `80` | Height in points (ignored if `auto_size=True`) |
| `bg` | `str` or `tuple` | Dark gray | Background color (hex or RGB tuple) |
| `text_color` | `str` or `tuple` | White | Text color (hex or RGB tuple) |
| `position` | `ToastPosition` or `tuple` | `BOTTOM_RIGHT` | Screen position or (x, y) coordinates |
| `font_size` | `float` | `14` | Font size in points |
| `corner_radius` | `float` | `16` | Corner radius (auto-adjusted if `auto_size=True`) |
| `display_duration` | `float` | `2.5` | Seconds to stay visible |
| `fade_in_duration` | `float` | `0.2` | Fade in animation duration |
| `fade_out_duration` | `float` | `0.2` | Fade out animation duration |
| `window_level` | `WindowLevel` or `str` | `SCREENSAVER` | Window z-index level |
| `icon` | `str` | `None` | SF Symbol name |
| `click_to_dismiss` | `bool` | `True` | Allow click to dismiss |
| `auto_size` | `bool` | `False` | Automatically calculate dimensions |
| `min_width` | `float` | `100` | Minimum width when `auto_size=True` |
| `max_width` | `float` | `400` | Maximum width when `auto_size=True` |
| `sound` | `str` | `None` | Sound name or path to audio file |
| `blocking` | `bool` | `True` | Wait for toast to finish |
| `check` | `bool` | `False` | Raise exception if subprocess fails |

#### Color Formats

Colors can be specified in two formats:

1. **Hex String**: `"#RRGGBB"` or `"#RRGGBBAA"`
   ```python
   toast("Hello", bg="#FF5733")
   toast("With alpha", bg="#FF5733CC")
   ```

2. **RGB/RGBA Tuple**: Values from 0.0 to 1.0
   ```python
   toast("Hello", bg=(1.0, 0.34, 0.2))
   toast("With alpha", bg=(1.0, 0.34, 0.2, 0.8))
   ```

#### Position Options

**Enum Values** (`ToastPosition`):
- `TOP_RIGHT`
- `TOP_LEFT`
- `BOTTOM_RIGHT` (default)
- `BOTTOM_LEFT`
- `CENTER`

**Custom Coordinates**:
```python
# (x, y) from bottom-left of screen
toast("Custom", position=(100, 200))
```

#### Window Levels

**Enum Values** (`WindowLevel`):
- `NORMAL` - Normal window level
- `FLOATING` - Floating above normal windows
- `STATUS` - Status bar level
- `MODAL` - Modal panel level
- `SCREENSAVER` - Above everything (default)

### Helper Functions

#### `show_success()`

```python
def show_success(message: str, **kwargs)
```

Green toast with checkmark icon and confirmation1 sound.

**Default Style:**
- Background: `(0.2, 0.8, 0.3)` (green)
- Text color: `(0.0, 0.0, 0.0)` (black)
- Icon: `checkmark.circle.fill`
- Sound: `confirmation1`

#### `show_error()`

```python
def show_error(message: str, **kwargs)
```

Red toast with X mark icon and beep1 sound.

**Default Style:**
- Background: `(0.9, 0.2, 0.2)` (red)
- Text color: `(1.0, 1.0, 1.0)` (white)
- Icon: `xmark.circle.fill`
- Sound: `beep1`

#### `show_warning()`

```python
def show_warning(message: str, **kwargs)
```

Orange toast with warning icon and beep1 sound.

**Default Style:**
- Background: `(1.0, 0.6, 0.0)` (orange)
- Text color: `(0.0, 0.0, 0.0)` (black)
- Icon: `exclamationmark.triangle.fill`
- Sound: `beep1`

#### `show_info()`

```python
def show_info(message: str, **kwargs)
```

Blue toast with info icon and confirmation2 sound.

**Default Style:**
- Background: `(0.2, 0.5, 0.9)` (blue)
- Text color: `(1.0, 1.0, 1.0)` (white)
- Icon: `info.circle.fill`
- Sound: `confirmation2`

### Enums

#### `ToastPosition`

```python
class ToastPosition(str, Enum):
    TOP_RIGHT = "top-right"
    TOP_LEFT = "top-left"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_LEFT = "bottom-left"
    CENTER = "center"
```

#### `WindowLevel`

```python
class WindowLevel(str, Enum):
    NORMAL = "normal"
    FLOATING = "floating"
    STATUS = "status"
    MODAL = "modal"
    MAX = "max"
    SCREENSAVER = "screensaver"
```

## Usage Examples

### Basic Examples

```python
from mactoast import toast

# Simple toast
toast("Hello from macOS!")

# Custom colors
toast("Blue toast", bg="#0080FF", text_color="#FFFFFF")

# RGB tuple colors
toast("Green", bg=(0.0, 0.8, 0.0), text_color=(0.0, 0.0, 0.0))
```

### Positioning

```python
from mactoast import toast, ToastPosition

# Predefined positions
toast("Top Right", position=ToastPosition.TOP_RIGHT)
toast("Center", position=ToastPosition.CENTER)

# Custom coordinates (x, y from bottom-left)
toast("Custom Spot", position=(500, 500))
```

### Icons

```python
from mactoast import toast

# SF Symbols - see https://developer.apple.com/sf-symbols/
toast("Success!", icon="checkmark.circle.fill")
toast("Download", icon="arrow.down.circle.fill")
toast("Settings", icon="gearshape.fill")
toast("Message", icon="paperplane.fill")
```

### Sounds

```python
from mactoast import toast

# Bundled sounds
toast("Beep!", sound="beep1")
toast("Confirmation", sound="confirmation1")
toast("Pop", sound="pop2")
toast("Sci-fi", sound="scifi1.m4a")

# Custom sound file
toast("Custom", sound="/path/to/sound.wav")

# Disable sound
toast("Silent", sound=None)
```

### Auto-Size

```python
from mactoast import toast

# Auto-size for short message
toast("Done!", auto_size=True, icon="checkmark")

# Auto-size with long message (wraps automatically)
toast(
    "This is a longer message that will wrap to multiple lines",
    auto_size=True,
    icon="text.alignleft"
)

# Custom size constraints
toast(
    "Constrained",
    auto_size=True,
    min_width=150,
    max_width=350
)
```

**Auto-Size Features:**
- Adaptive corner radius: `min(16, height/2 - 2)`
- Smart wrapping: Only wraps when text exceeds `max_width`
- Icon-aware: Accounts for icon size in calculations
- Python-calculated: All sizing done before launching Swift app

### Non-Blocking Mode

```python
from mactoast import toast, show_success
import time

# Launch and continue immediately
process = toast("Background toast", blocking=False)
print(f"Toast launched with PID: {process.pid}")

# Launch multiple toasts simultaneously
for i in range(4):
    toast(f"Toast {i+1}", blocking=False)

# Helper functions also support non-blocking
p = show_success("Done!", blocking=False)

# Your script continues running
time.sleep(2)

# Optionally wait for specific toast
# process.wait()
```

### Click to Dismiss

```python
from mactoast import toast

# Default: click to dismiss enabled
toast("Click me!", display_duration=30)

# Disable click-to-dismiss
toast("Must wait", click_to_dismiss=False, display_duration=5)
```

### Window Levels

```python
from mactoast import toast, WindowLevel

# Normal window level
toast("Normal", window_level=WindowLevel.NORMAL)

# Floating (above normal windows)
toast("Floating", window_level=WindowLevel.FLOATING)

# Above everything
toast("Top Most", window_level=WindowLevel.SCREENSAVER)
```

### Complete Example

```python
from mactoast import toast, ToastPosition
import time

# Comprehensive toast with all features
toast(
    message="File upload complete!",
    bg="#00AA00",
    text_color="#FFFFFF",
    position=ToastPosition.TOP_RIGHT,
    width=300,
    height=100,
    font_size=16,
    corner_radius=20,
    display_duration=5.0,
    fade_in_duration=0.3,
    fade_out_duration=0.5,
    icon="checkmark.circle.fill",
    sound="confirmation1",
    click_to_dismiss=True,
    blocking=True
)
```

## ToastHUD Swift App

The ToastHUD app is a minimal native macOS application that handles toast rendering.

### Architecture

```
ToastHUD.app/
├── Contents/
│   ├── Info.plist          # App metadata
│   ├── MacOS/
│   │   └── ToastHUD        # Compiled binary
│   ├── Resources/          # Sound files
│   │   ├── beep1.wav
│   │   ├── confirmation1.wav
│   │   └── ...
│   └── _CodeSignature/     # Code signature
```

### Source Files

Located in `ToastHUD/` directory:

#### `ToastHUDApp.swift`

Main app entry point. Configures the app as an accessory (no dock icon).

```swift
@main
struct ToastHUDApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    
    var body: some Scene {
        Settings { EmptyView() }
    }
}
```

#### `AppDelegate.swift`

Application delegate that:
- Parses CLI arguments via `ToastConfig`
- Creates and positions toast window
- Handles sound playback
- Manages animations and lifecycle

**Key Methods:**
- `applicationDidFinishLaunching()`: Entry point, launches toast
- `showToast(config:)`: Creates and displays toast window
- `playSound(path:)`: Plays sound from bundle or file system
- `dismissToast(fadeOutDuration:)`: Animates dismissal and terminates

#### `ToastConfig.swift`

Configuration struct that parses CLI arguments.

**Properties:**
```swift
var message: String
var width: CGFloat = 280
var height: CGFloat = 80
var position: ToastPosition = .default
var fontSize: CGFloat = 14
var backgroundColor: NSColor = NSColor(calibratedWhite: 0.1, alpha: 0.85)
var textColor: NSColor = .white
var cornerRadius: CGFloat = 16
var displayDuration: TimeInterval = 2.5
var fadeOutDuration: TimeInterval = 0.2
var fadeInDuration: TimeInterval = 0.2
var x: CGFloat?
var y: CGFloat?
var windowLevel: String?
var icon: String?
var clickToDismiss: Bool = true
var sound: String?
```

**CLI Arguments:**
- `--width <value>`
- `--height <value>`
- `--bg <hex>`
- `--text-color <hex>`
- `--position <position>`
- `--font-size <value>`
- `--corner-radius <value>`
- `--display-duration <value>`
- `--fade-in-duration <value>`
- `--fade-out-duration <value>`
- `--x <value>`
- `--y <value>`
- `--window-level <level>`
- `--icon <symbol>`
- `--sound <name>`
- `--click-to-dismiss <true|false>`
- `--no-click-to-dismiss`
- Message (remaining arguments)

#### `ToastView.swift`

SwiftUI view that renders the toast UI.

**Components:**
- `VisualEffectView`: Blur background
- `RoundedRectangle`: Tinted overlay and border
- `HStack`: Icon + text layout
- `Image(systemName:)`: SF Symbol icon
- `Text`: Message with multiline support

**Features:**
- Tap gesture handling for click-to-dismiss
- Fixed frame sizing
- Content padding

#### `ToastPanel.swift`

`NSPanel` subclass for the toast window.

**Configuration:**
- Borderless, non-activating window
- HUD window style
- Conditional mouse event handling (click-to-dismiss)
- Transparent background
- No title bar

#### `VisualEffectView.swift`

UIViewRepresentable wrapper for `NSVisualEffectView`.

Provides native blur background with:
- `.hudWindow` material
- `.behindWindow` blending mode

### Build Configuration

The Swift app is compiled with:

```bash
swiftc -o build/ToastHUD \
    -parse-as-library \
    -framework Cocoa \
    -framework SwiftUI \
    -framework AVFoundation \
    ToastHUD/*.swift
```

**Frameworks:**
- `Cocoa`: AppKit, window management
- `SwiftUI`: Modern UI framework
- `AVFoundation`: Audio playback

## Sound System

### Overview

Sound playback is handled entirely in Swift using AVFoundation. Sounds are bundled in the app's Resources directory.

### Bundled Sounds

| Category | Files | Format |
|----------|-------|--------|
| Beep | `beep1`, `beep2`, `beep3` | `.wav` |
| Beep | `beep4`, `beep5` | `.m4a` |
| Confirmation | `confirmation1`, `confirmation2`, `confirmation3`, `confirmation5` | `.wav` |
| Confirmation | `confirmation4` | `.m4a` |
| Pop | `pop2`, `pop3` | `.wav` |
| Pop | `pop1` | `.mp3` |
| Sci-Fi | `scifi2`, `scifi3` | `.wav` |
| Sci-Fi | `scifi1` | `.m4a` |

### Supported Formats

- `.wav` - Waveform Audio File Format
- `.mp3` - MPEG Audio Layer III
- `.m4a` - MPEG-4 Audio

### Sound Resolution

The `playSound()` method in `AppDelegate.swift`:

1. **Bundled sounds**: Sound name only (e.g., `"beep1"`)
   - Looks up in `Bundle.main.path(forResource:ofType:)`
   - Automatically detects extension

2. **Custom sounds**: Absolute path (e.g., `"/path/to/sound.wav"`)
   - Loads directly from file system
   - Must be accessible when toast launches

### Adding Custom Sounds

To add sounds to the bundle:

1. Place `.wav`, `.mp3`, or `.m4a` files in `sounds/` directory
2. Copy to app bundle:
   ```bash
   cp sounds/*.wav src/mactoast/ToastHUD.app/Contents/Resources/
   ```
3. Rebuild and copy ToastHUD binary
4. Use sound name without path: `toast("Hello", sound="mysound")`

## Building from Source

### Prerequisites

- Xcode Command Line Tools
- Swift compiler (`swiftc`)
- Python 3.8+

### Build Steps

1. **Clone repository**
   ```bash
   git clone https://github.com/rafa-rrayes/mactoast.git
   cd mactoast
   ```

2. **Build Swift app**
   ```bash
   mkdir -p build
   swiftc -o build/ToastHUD \
       -parse-as-library \
       -framework Cocoa \
       -framework SwiftUI \
       -framework AVFoundation \
       ToastHUD/*.swift
   ```

3. **Copy to package**
   ```bash
   cp build/ToastHUD src/mactoast/ToastHUD.app/Contents/MacOS/ToastHUD
   ```

4. **Copy sounds (if updated)**
   ```bash
   cp sounds/* src/mactoast/ToastHUD.app/Contents/Resources/
   ```

5. **Install Python package**
   ```bash
   pip install -e .
   ```

6. **Test**
   ```bash
   python -c "import mactoast; mactoast.toast('Build test!')"
   ```

### Development Workflow

When modifying Swift code:

```bash
# Build and install
swiftc -o build/ToastHUD -parse-as-library \
    -framework Cocoa -framework SwiftUI -framework AVFoundation \
    ToastHUD/*.swift && \
cp build/ToastHUD src/mactoast/ToastHUD.app/Contents/MacOS/ToastHUD

# Test
python -c "import mactoast; mactoast.toast('Test message')"
```

When modifying Python code:
- Changes are immediate if installed with `pip install -e .`
- No rebuild needed

## Parameter Validation

Mactoast includes comprehensive parameter validation to catch configuration errors before they happen. All validation errors raise `ToastConfigError` (a subclass of `ValueError`) with descriptive messages.

### Using ToastConfigError

```python
from mactoast import toast, ToastConfigError

try:
    toast("Test", auto_size=True, width=200)
except ToastConfigError as e:
    print(f"Configuration error: {e}")
    # "Cannot specify both auto_size=True and width. Set auto_size=False to use explicit width."
```

### Dimension Validation

#### auto_size Conflicts

- ❌ Cannot use `width` with `auto_size=True`
- ❌ Cannot use `height` with `auto_size=True`
- ❌ Cannot use `min_width` or `max_width` without `auto_size=True`

```python
# ✅ Valid
toast("Hello", auto_size=True, min_width=100, max_width=400)
toast("Hello", width=300, height=100)

# ❌ Invalid
toast("Hello", auto_size=True, width=300)  # auto_size conflicts with width
toast("Hello", min_width=200)  # min_width requires auto_size=True
```

#### Value Ranges

- `width`: 50-1000 points
- `height`: 30-500 points
- `min_width`: 50-1000 points (requires `auto_size=True`)
- `max_width`: 50-1000 points (requires `auto_size=True`)
- `min_width` must be ≤ `max_width`

```python
# ❌ Invalid
toast("Hello", width=20)  # Too small
toast("Hello", auto_size=True, min_width=400, max_width=200)  # min > max
```

### Color Validation

Colors must be either:
- **Hex string**: Starting with `#`, 6 or 8 characters (RGB or RGBA)
- **Tuple**: 3 or 4 float values between 0.0 and 1.0

```python
# ✅ Valid
toast("Hello", bg="#FF0000")
toast("Hello", bg="#FF0000FF")
toast("Hello", bg=(1.0, 0.0, 0.0))
toast("Hello", bg=(1.0, 0.0, 0.0, 0.8))

# ❌ Invalid
toast("Hello", bg="FF0000")  # Missing #
toast("Hello", bg="#FF")  # Wrong length
toast("Hello", bg=(1.0, 0.0))  # Only 2 values
toast("Hello", bg=(1.5, 0.0, 0.0))  # Value out of range (must be 0.0-1.0)
```

### Position Validation

Must be one of:
- **String**: `"top-right"`, `"top-left"`, `"bottom-right"`, `"bottom-left"`, `"center"`
- **Enum**: `ToastPosition.TOP_RIGHT`, etc.
- **Tuple**: `(x, y)` coordinates as numbers

```python
# ✅ Valid
toast("Hello", position="top-right")
toast("Hello", position=ToastPosition.CENTER)
toast("Hello", position=(100, 200))

# ❌ Invalid
toast("Hello", position="middle")  # Invalid string
toast("Hello", position=(100,))  # Only 1 coordinate
```

### Window Level Validation

Must be one of: `"normal"`, `"floating"`, `"status"`, `"modal"`, `"max"`, `"screensaver"` (or corresponding `WindowLevel` enum)

```python
# ✅ Valid
toast("Hello", window_level="floating")
toast("Hello", window_level=WindowLevel.MODAL)

# ❌ Invalid
toast("Hello", window_level="super-high")  # Invalid level
```

### Duration Validation

**Value Ranges:**
- `display_duration`: 0.1-60.0 seconds
- `fade_in_duration`: 0.0-5.0 seconds
- `fade_out_duration`: 0.0-5.0 seconds

**Combined Validation:**
- `fade_in_duration + fade_out_duration` must be ≤ `display_duration`

```python
# ✅ Valid
toast("Hello", display_duration=3.0, fade_in_duration=0.3, fade_out_duration=0.3)

# ❌ Invalid
toast("Hello", display_duration=0.05)  # Too short
toast("Hello", display_duration=1.0, fade_in_duration=0.6, fade_out_duration=0.6)  # Fades exceed display
```

### Sound Validation

**Valid bundled sound names:**
- `beep1`, `beep2`, `beep3`, `beep4`, `beep5`
- `confirmation1`, `confirmation2`, `confirmation3`, `confirmation4`, `confirmation5`
- `pop1`, `pop2`, `pop3`
- `scifi1`, `scifi2`, `scifi3`
- `click1`

**Custom sound files:**
- Must be absolute path
- Must exist on filesystem
- Must have extension: `.wav`, `.mp3`, `.m4a`, `.aac`, `.aiff`, or `.caf`

```python
# ✅ Valid
toast("Hello", sound="confirmation1")
toast("Hello", sound="/path/to/custom.wav")

# ❌ Invalid
toast("Hello", sound="ding")  # Unknown sound
toast("Hello", sound="/nonexistent.wav")  # File doesn't exist
```

### Other Validations

**font_size**: 8-72 points

**corner_radius**: 0-100 points

**icon**: Must be a string (SF Symbol name)

**blocking/check**: `check=True` requires `blocking=True`

**message**: Must be a non-empty string

```python
# ✅ Valid
toast("Hello", font_size=18, corner_radius=20)
toast("Hello", icon="star.fill")
toast("Hello", blocking=True, check=True)

# ❌ Invalid
toast("Hello", font_size=100)  # Too large
toast("Hello", check=True, blocking=False)  # check requires blocking
toast("")  # Empty message
```

### Testing Validation

Run the validation test suite:

```bash
python test_validation.py
```

This runs 17 tests covering all parameter combinations and edge cases.

### Common Error Patterns

**1. Mixing auto_size with explicit dimensions**
```python
# ❌ Wrong
toast("Hello", auto_size=True, width=300)

# ✅ Correct - choose one approach
toast("Hello", auto_size=True)  # Let it calculate
toast("Hello", width=300, height=100)  # Explicit
```

**2. Using min/max_width without auto_size**
```python
# ❌ Wrong
toast("Hello", max_width=400)

# ✅ Correct
toast("Hello", auto_size=True, max_width=400)
```

**3. Fade durations too long**
```python
# ❌ Wrong - 1.5s of fades for 1s display
toast("Hello", display_duration=1.0, fade_in_duration=0.8, fade_out_duration=0.7)

# ✅ Correct
toast("Hello", display_duration=2.0, fade_in_duration=0.5, fade_out_duration=0.5)
```

**4. Invalid color formats**
```python
# ❌ Wrong
toast("Hello", bg="red")  # Color name not supported
toast("Hello", bg="FF0000")  # Missing #

# ✅ Correct
toast("Hello", bg="#FF0000")  # Hex
toast("Hello", bg=(1.0, 0.0, 0.0))  # RGB tuple
```

### Benefits of Validation

1. **Early error detection**: Catch mistakes before subprocess execution
2. **Clear error messages**: Know exactly what's wrong and how to fix it
3. **Better development experience**: IDE autocomplete + immediate feedback
4. **Prevents silent failures**: Invalid configs are caught immediately

## Troubleshooting

### Toast Not Appearing

**Issue**: No toast shows when calling `toast()`

**Solutions**:
1. Check if executable exists:
   ```python
   import os
   from mactoast._runner import _get_executable_path
   print(_get_executable_path())
   print(os.path.exists(_get_executable_path()))
   ```

2. Test the Swift app directly:
   ```bash
   /path/to/ToastHUD.app/Contents/MacOS/ToastHUD "Test message"
   ```

3. Check for errors:
   ```python
   result = toast("Test", blocking=True)
   print(result.returncode, result.stderr)
   ```

### Sound Not Playing

**Issue**: Toast appears but no sound

**Solutions**:
1. Check if sound file exists in bundle:
   ```bash
   ls src/mactoast/ToastHUD.app/Contents/Resources/
   ```

2. Test with known sound:
   ```python
   toast("Test", sound="beep1")
   ```

3. Check system volume and mute settings

4. Verify file format is supported (`.wav`, `.mp3`, `.m4a`)

### Click to Dismiss Not Working

**Issue**: Clicking toast doesn't dismiss it

**Solutions**:
1. Ensure `click_to_dismiss=True` (default)
2. Check if window level is preventing interaction:
   ```python
   toast("Test", click_to_dismiss=True, window_level="normal")
   ```

### Auto-Size Issues

**Issue**: Text cropped or size incorrect

**Solutions**:
1. Adjust constraints:
   ```python
   toast("Long message", auto_size=True, min_width=150, max_width=500)
   ```

2. Check font size:
   ```python
   toast("Test", auto_size=True, font_size=14)
   ```

3. Disable auto-size and set manual dimensions:
   ```python
   toast("Test", width=300, height=100)
   ```

### Non-Blocking Issues

**Issue**: Process not returning or script hangs

**Solutions**:
1. Ensure `blocking=False` is set:
   ```python
   p = toast("Test", blocking=False)
   print(f"PID: {p.pid}")
   ```

2. Don't call `.wait()` unless you want to block

3. Check process status:
   ```python
   print(p.poll())  # None if still running
   ```

### Import Errors

**Issue**: `ImportError` or `ModuleNotFoundError`

**Solutions**:
1. Reinstall package:
   ```bash
   pip uninstall mactoast
   pip install mactoast
   ```

2. Check Python version:
   ```bash
   python --version  # Should be 3.8+
   ```

3. Verify installation:
   ```bash
   pip show mactoast
   ```

## Advanced Topics

### Custom Toast Styles

Create reusable style configurations:

```python
from mactoast import toast

# Define custom style
my_style = {
    'bg': '#FF6B35',
    'text_color': '#FFFFFF',
    'icon': 'flame.fill',
    'sound': 'scifi1.m4a',
    'font_size': 16,
    'corner_radius': 20,
}

# Use style
toast("Custom styled!", **my_style)
```

### Multiple Toasts

Launch multiple toasts simultaneously:

```python
from mactoast import toast

# All four corners
positions = ['top-right', 'top-left', 'bottom-right', 'bottom-left']
for i, pos in enumerate(positions, 1):
    toast(f"Toast {i}", position=pos, blocking=False)
```

### Progress Notifications

Simulate progress with sequential toasts:

```python
from mactoast import toast
import time

steps = ["Starting...", "Processing...", "Almost done...", "Complete!"]
for step in steps:
    toast(step, display_duration=1.5)
    time.sleep(2)  # Actual work here
```

### Integration with Logging

Use toasts for important log events:

```python
import logging
from mactoast import show_error, show_warning

class ToastHandler(logging.Handler):
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            show_error(record.getMessage(), blocking=False)
        elif record.levelno >= logging.WARNING:
            show_warning(record.getMessage(), blocking=False)

# Setup
logger = logging.getLogger()
logger.addHandler(ToastHandler())
```

---

## Contributing

Contributions are welcome! Please see the repository for guidelines.

## License

MIT License - see LICENSE file for details.

## Links

- **GitHub**: https://github.com/rafa-rrayes/mactoast
- **PyPI**: https://pypi.org/project/mactoast/
- **SF Symbols**: https://developer.apple.com/sf-symbols/
