import os
import sys
import subprocess
from typing import Optional, Union, Tuple
from enum import Enum

try:
    from importlib.resources import files as resource_files
except ImportError:
    # Python < 3.9
    import importlib.resources as resource_files  # type: ignore

# Default constants
DEFAULT_WIDTH = 280
DEFAULT_HEIGHT = 80
DEFAULT_FONT_SIZE = 14
DEFAULT_CORNER_RADIUS = 16
DEFAULT_MIN_WIDTH = 100
DEFAULT_MAX_WIDTH = 400


class ToastPosition(str, Enum):
    TOP_RIGHT = "top-right"
    TOP_LEFT = "top-left"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_LEFT = "bottom-left"
    CENTER = "center"


class WindowLevel(str, Enum):
    NORMAL = "normal"
    FLOATING = "floating"
    STATUS = "status"
    MODAL = "modal"
    MAX = "max"
    SCREENSAVER = "screensaver"


ColorType = Union[str, Tuple[float, float, float], Tuple[float, float, float, float]]


def _get_executable_path() -> str:
    if sys.platform != "darwin":
        raise RuntimeError("mactoast currently only supports macOS.")

    # Locate ToastHUD.app inside this package
    base = resource_files(__package__)
    app = base / "ToastHUD.app" / "Contents" / "MacOS" / "ToastHUD"

    path = str(app)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Toast executable not found at {path}")
    return path


def _normalize_color(color: ColorType) -> str:
    """Convert a color (hex string or tuple) to a hex string."""
    if isinstance(color, str):
        return color
    
    if isinstance(color, (tuple, list)):
        # Assume 0.0-1.0 floats
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)
        if len(color) > 3:
            a = int(color[3] * 255)
            return f"#{r:02X}{g:02X}{b:02X}{a:02X}"
        else:
            return f"#{r:02X}{g:02X}{b:02X}"
            
    raise ValueError(f"Invalid color format: {color}")


def _calculate_auto_size(
    message: str,
    font_size: float,
    icon: Optional[str],
    min_width: float,
    max_width: float,
) -> Tuple[float, float, float]:
    """
    Calculate optimal width, height, and corner radius for auto-sized toast.
    Returns (width, height, corner_radius).
    """
    # Approximate character width (varies by font, but good estimate for system font)
    avg_char_width = font_size * 0.6
    
    # Calculate icon space
    icon_width = (font_size + 4 + 12) if icon else 0  # icon size + spacing
    horizontal_padding = 40  # 20 on each side
    vertical_padding = 24    # 12 top + 12 bottom
    
    # Calculate natural text width
    text_width = len(message) * avg_char_width
    total_natural_width = text_width + icon_width + horizontal_padding
    
    # Determine if wrapping is needed
    if total_natural_width <= max_width:
        # Single line - use natural width
        final_width = max(min_width, total_natural_width)
        line_height = font_size * 1.2
        final_height = line_height + vertical_padding
    else:
        # Need to wrap - use max_width and calculate height
        final_width = max_width
        available_text_width = max_width - icon_width - horizontal_padding
        chars_per_line = max(1, int(available_text_width / avg_char_width))
        num_lines = max(1, (len(message) + chars_per_line - 1) // chars_per_line)
        line_height = font_size * 1.4  # More spacing for multi-line
        final_height = (line_height * num_lines) + vertical_padding
    
    # Ensure minimum height
    final_height = max(44, final_height)
    
    # Adaptive corner radius - smaller for compact toasts
    corner_radius = min(DEFAULT_CORNER_RADIUS, final_height / 2 - 2)
    
    return (final_width, final_height, corner_radius)


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
) -> Union[subprocess.CompletedProcess, subprocess.Popen]:
    """
    Show a macOS HUD toast using the bundled ToastHUD.app.

    Args:
        message: The message to display.
        width: Width of the toast in points (ignored if auto_size=True).
        height: Height of the toast in points (ignored if auto_size=True).
        bg: Background color (hex string or (r,g,b) tuple of 0-1 floats).
        position: Position on screen ("top-right", "center", etc) or (x, y) coordinates.
        font_size: Font size in points. Default: 14.
        text_color: Text color (hex string or (r,g,b) tuple of 0-1 floats).
        corner_radius: Corner radius in points (auto-adjusted if auto_size=True).
        display_duration: How long to show the toast (seconds). Default: 2.5.
        fade_out_duration: Duration of fade out animation (seconds). Default: 0.2.
        fade_in_duration: Duration of fade in animation (seconds). Default: 0.2.
        window_level: Window level ("normal", "floating", "status", "modal", "max").
        icon: SF Symbol name (e.g., "checkmark.circle.fill", "xmark.circle.fill").
        click_to_dismiss: If True, clicking the toast dismisses it. Default: True.
        auto_size: If True, automatically size the toast based on content. Default: False.
        min_width: Minimum width when auto_size=True. Default: 100.
        max_width: Maximum width when auto_size=True. Default: 400.
        sound: Sound name ('click1', 'confirmation1', 'confirmation2') or absolute path. Default: None (no sound).
        blocking: If True, wait for the toast to close before returning.
        check: If True, raise a CalledProcessError if the toast app fails (only if blocking=True).
    """
    exe = _get_executable_path()
    
    # Use defaults
    effective_font_size = font_size if font_size is not None else DEFAULT_FONT_SIZE
    effective_min_width = min_width if min_width is not None else DEFAULT_MIN_WIDTH
    effective_max_width = max_width if max_width is not None else DEFAULT_MAX_WIDTH
    
    # Calculate size if auto_size is enabled
    if auto_size:
        calc_width, calc_height, calc_corner_radius = _calculate_auto_size(
            message=message,
            font_size=effective_font_size,
            icon=icon,
            min_width=effective_min_width,
            max_width=effective_max_width,
        )
        # Use calculated values (user can still override corner_radius)
        width = calc_width
        height = calc_height
        if corner_radius is None:
            corner_radius = calc_corner_radius

    args = [exe]

    if width is not None:
        args.extend(["--width", str(width)])
    if height is not None:
        args.extend(["--height", str(height)])
    if bg is not None:
        args.extend(["--bg", _normalize_color(bg)])
    if position is not None:
        if isinstance(position, (tuple, list)) and len(position) == 2:
            args.extend(["--x", str(position[0])])
            args.extend(["--y", str(position[1])])
        else:
            pos_str = position.value if isinstance(position, ToastPosition) else str(position)
            args.extend(["--position", pos_str])
    if font_size is not None:
        args.extend(["--font-size", str(font_size)])
    if text_color is not None:
        args.extend(["--text-color", _normalize_color(text_color)])
    if corner_radius is not None:
        args.extend(["--corner-radius", str(corner_radius)])
    if display_duration is not None:
        args.extend(["--display-duration", str(display_duration)])
    if fade_out_duration is not None:
        args.extend(["--fade-out-duration", str(fade_out_duration)])
    if fade_in_duration is not None:
        args.extend(["--fade-in-duration", str(fade_in_duration)])
    if window_level is not None:
        wl_str = window_level.value if isinstance(window_level, WindowLevel) else str(window_level)
        args.extend(["--window-level", wl_str])
    if icon is not None:
        args.extend(["--icon", str(icon)])
    if not click_to_dismiss:
        args.append("--no-click-to-dismiss")
    if sound is not None:
        args.extend(["--sound", str(sound)])

    # Message goes at the end
    args.append(str(message))

    if blocking:
        return subprocess.run(args, check=check, capture_output=True, text=True)
    
    return subprocess.Popen(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    # Simple test
    toast("Hello from mactoast!", auto_size=True, icon="star.fill")