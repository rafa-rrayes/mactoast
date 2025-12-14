I DO NOT KNOW SWIFT or mac app creation. This was 100% vibe coded.

# MacToast (ToastHUD)

A lightweight, customizable toast notification tool for macOS, controllable via command line arguments.

## Usage

```bash
./ToastHUD "Your message here" [options]
```

## Options

### Positioning
| Flag | Description | Default |
|------|-------------|---------|
| `--position` | Sets the anchor position. <br>Values: `top-right`, `top-left`, `bottom-right`, `bottom-left`, `center` | `bottom-right` |
| `--x` | Overrides the X coordinate (absolute screen position). | `nil` |
| `--y` | Overrides the Y coordinate (absolute screen position). | `nil` |
| `--width` | Width of the toast in points. | `280` |
| `--height` | Height of the toast in points. | `80` |

### Appearance
| Flag | Description | Default |
|------|-------------|---------|
| `--bg` | Background color in hex format (e.g., `#FF0000` or `FF0000`). | `#1A1A1A` (approx) |
| `--text-color` | Text color in hex format. | `#FFFFFF` |
| `--font-size` | Font size of the message. | `14` |
| `--corner-radius` | Corner radius of the toast background. | `16` |
| `--icon` | SF Symbol name to display (e.g., `checkmark.circle.fill`). | `nil` |

### Interaction
| Flag | Description | Default |
|------|-------------|---------|
| Click on toast | Immediately dismisses the toast with fade-out animation. | N/A |

### Timing & Animation
| Flag | Description | Default |
|------|-------------|---------|
| `--display-duration` | How long the toast stays visible (in seconds). | `2.5` |
| `--fade-in-duration` | Duration of the fade-in animation (in seconds). | `0.2` |
| `--fade-out-duration` | Duration of the fade-out animation (in seconds). | `0.2` |

### Window Level
| Flag | Description | Default |
|------|-------------|---------|
| `--window-level` | Controls the z-index of the toast window. <br>Values: `normal`, `floating`, `status`, `modal`, `max` (or `screensaver`). <br> **Note:** The default behavior (`max`) floats above all windows, including full-screen apps. | `max` |

## Examples

**Basic Message:**
```bash
./ToastHUD "Hello World"
```

**Error Alert (Red, Top-Right):**
```bash
./ToastHUD "Critical Error!" --position top-right --bg #FF3B30 --text-color #FFFFFF
```

**Subtle Notification (Center, Transparent):**
```bash
./ToastHUD "Loading..." --position center --bg #00000088 --display-duration 1.0
```

**Always on Top (Above Screensaver):**
```bash
./ToastHUD "Wake Up!" --window-level max --font-size 24
```

**Custom Coordinate:**
```bash
./ToastHUD "Custom Spot" --x 500 --y 500
```

**With Icon:**
```bash
./ToastHUD "File Saved!" --icon checkmark.circle.fill --bg #34C759
```

**Click to Dismiss:**
Toasts can be dismissed early by clicking on them. Try with a long duration:
```bash
./ToastHUD "Click me to dismiss!" --icon hand.tap.fill --display-duration 30
```
