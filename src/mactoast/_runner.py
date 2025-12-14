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


class ToastConfigError(ValueError):
    """Raised when toast configuration options are incompatible or invalid."""
    pass


def _validate_color(color: ColorType, param_name: str) -> None:
    """Validate color format."""
    if isinstance(color, str):
        if not color.startswith("#"):
            raise ToastConfigError(
                f"{param_name} must be a hex string starting with '#' "
                f"(e.g., '#FF0000') or an RGB tuple. Got: {color}"
            )
        hex_part = color[1:]
        if len(hex_part) not in (6, 8):
            raise ToastConfigError(
                f"{param_name} hex string must be 6 or 8 characters "
                f"(RGB or RGBA). Got: {color}"
            )
    elif isinstance(color, (tuple, list)):
        if len(color) not in (3, 4):
            raise ToastConfigError(
                f"{param_name} tuple must have 3 (RGB) or 4 (RGBA) values. "
                f"Got {len(color)} values"
            )
        for i, val in enumerate(color):
            if not isinstance(val, (int, float)):
                raise ToastConfigError(
                    f"{param_name}[{i}] must be a number. Got: {type(val).__name__}"
                )
            if not 0.0 <= val <= 1.0:
                raise ToastConfigError(
                    f"{param_name}[{i}] must be between 0.0 and 1.0. Got: {val}"
                )
    else:
        raise ToastConfigError(
            f"{param_name} must be a hex string or RGB(A) tuple. "
            f"Got: {type(color).__name__}"
        )


def _validate_position(position: Union[ToastPosition, str, Tuple[float, float]]) -> None:
    """Validate position format."""
    if isinstance(position, (tuple, list)):
        if len(position) != 2:
            raise ToastConfigError(
                f"position tuple must have exactly 2 values (x, y). "
                f"Got {len(position)} values"
            )
        for i, val in enumerate(position):
            if not isinstance(val, (int, float)):
                raise ToastConfigError(
                    f"position[{i}] must be a number. Got: {type(val).__name__}"
                )
    elif isinstance(position, str):
        valid_positions = [p.value for p in ToastPosition]
        if position not in valid_positions:
            raise ToastConfigError(
                f"position must be one of {valid_positions}. Got: {position}"
            )
    elif not isinstance(position, ToastPosition):
        raise ToastConfigError(
            f"position must be a ToastPosition enum, string, or (x, y) tuple. "
            f"Got: {type(position).__name__}"
        )


def _validate_window_level(level: Union[WindowLevel, str]) -> None:
    """Validate window level."""
    if isinstance(level, str):
        valid_levels = [l.value for l in WindowLevel]
        if level not in valid_levels:
            raise ToastConfigError(
                f"window_level must be one of {valid_levels}. Got: {level}"
            )
    elif not isinstance(level, WindowLevel):
        raise ToastConfigError(
            f"window_level must be a WindowLevel enum or string. "
            f"Got: {type(level).__name__}"
        )


def _validate_numeric_range(value: float, name: str, min_val: float, max_val: float) -> None:
    """Validate numeric value is within range."""
    if not isinstance(value, (int, float)):
        raise ToastConfigError(
            f"{name} must be a number. Got: {type(value).__name__}"
        )
    if not min_val <= value <= max_val:
        raise ToastConfigError(
            f"{name} must be between {min_val} and {max_val}. Got: {value}"
        )


def _validate_dimensions(
    width: Optional[float],
    height: Optional[float],
    auto_size: bool,
    min_width: Optional[float],
    max_width: Optional[float],
) -> None:
    """Validate dimension-related parameters."""
    # Check auto_size conflicts
    if auto_size:
        if width is not None:
            raise ToastConfigError(
                "Cannot specify both auto_size=True and width. "
                "Set auto_size=False to use explicit width."
            )
        if height is not None:
            raise ToastConfigError(
                "Cannot specify both auto_size=True and height. "
                "Set auto_size=False to use explicit height."
            )
    
    # Validate width/height values if provided
    if width is not None:
        _validate_numeric_range(width, "width", 50, 1000)
    if height is not None:
        _validate_numeric_range(height, "height", 30, 500)
    
    # Validate min/max width
    if min_width is not None:
        _validate_numeric_range(min_width, "min_width", 50, 1000)
    if max_width is not None:
        _validate_numeric_range(max_width, "max_width", 50, 1000)
    
    # Check min/max relationship
    if min_width is not None and max_width is not None:
        if min_width > max_width:
            raise ToastConfigError(
                f"min_width ({min_width}) cannot be greater than "
                f"max_width ({max_width})"
            )
    
    # Check if min/max are used without auto_size
    if not auto_size:
        if min_width is not None:
            raise ToastConfigError(
                "min_width only applies when auto_size=True"
            )
        if max_width is not None:
            raise ToastConfigError(
                "max_width only applies when auto_size=True"
            )


def _validate_durations(
    display_duration: Optional[float],
    fade_in_duration: Optional[float],
    fade_out_duration: Optional[float],
) -> None:
    """Validate duration parameters."""
    if display_duration is not None:
        _validate_numeric_range(display_duration, "display_duration", 0.1, 60.0)
    
    if fade_in_duration is not None:
        _validate_numeric_range(fade_in_duration, "fade_in_duration", 0.0, 5.0)
    
    if fade_out_duration is not None:
        _validate_numeric_range(fade_out_duration, "fade_out_duration", 0.0, 5.0)
    
    # Check if fade durations are reasonable compared to display duration
    if display_duration is not None:
        total_fade = 0.0
        if fade_in_duration is not None:
            total_fade += fade_in_duration
        if fade_out_duration is not None:
            total_fade += fade_out_duration
        
        if total_fade > display_duration:
            raise ToastConfigError(
                f"Combined fade durations ({total_fade}s) exceed "
                f"display_duration ({display_duration}s). "
                "The toast will not be visible at full opacity."
            )


def _validate_sound(sound: str) -> None:
    """Validate sound parameter."""
    # If it's an absolute path, just check it exists
    if sound.startswith("/"):
        if not os.path.exists(sound):
            raise ToastConfigError(
                f"Sound file not found: {sound}"
            )
        # Check extension
        if not sound.lower().endswith(('.wav', '.mp3', '.m4a', '.aac', '.aiff', '.caf')):
            raise ToastConfigError(
                f"Sound file must be .wav, .mp3, .m4a, .aac, .aiff, or .caf. "
                f"Got: {sound}"
            )
    else:
        # It's a bundled sound name - validate it
        valid_sounds = [
            'beep1', 'beep2', 'beep3', 'beep4', 'beep5',
            'confirmation1', 'confirmation2', 'confirmation3', 'confirmation4', 'confirmation5',
            'pop1', 'pop2', 'pop3',
            'scifi1', 'scifi2', 'scifi3',
            'click1',
        ]
        if sound not in valid_sounds:
            raise ToastConfigError(
                f"Unknown sound name: {sound}. "
                f"Valid sounds: {', '.join(valid_sounds)}"
            )


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
    
    Raises:
        ToastConfigError: If parameters are invalid or incompatible.
        RuntimeError: If not running on macOS.
        FileNotFoundError: If ToastHUD.app executable is not found.
    """
    # Validate message
    if not message or not isinstance(message, str):
        raise ToastConfigError("message must be a non-empty string")
    
    # Validate dimensions and auto_size interactions
    _validate_dimensions(width, height, auto_size, min_width, max_width)
    
    # Validate colors
    if bg is not None:
        _validate_color(bg, "bg")
    if text_color is not None:
        _validate_color(text_color, "text_color")
    
    # Validate position
    if position is not None:
        _validate_position(position)
    
    # Validate window level
    if window_level is not None:
        _validate_window_level(window_level)
    
    # Validate numeric parameters
    if font_size is not None:
        _validate_numeric_range(font_size, "font_size", 8, 72)
    
    if corner_radius is not None:
        _validate_numeric_range(corner_radius, "corner_radius", 0, 100)
    
    # Validate durations
    _validate_durations(display_duration, fade_in_duration, fade_out_duration)
    
    # Validate sound
    if sound is not None:
        _validate_sound(sound)
    
    # Validate icon (basic check - just ensure it's a string)
    if icon is not None and not isinstance(icon, str):
        raise ToastConfigError(
            f"icon must be a string (SF Symbol name). Got: {type(icon).__name__}"
        )
    
    # Validate blocking/check interaction
    if check and not blocking:
        raise ToastConfigError(
            "check=True only makes sense when blocking=True. "
            "Non-blocking mode cannot check exit status."
        )
    
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