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
    blocking: bool = True,
    check: bool = False,
) -> Union[subprocess.CompletedProcess, subprocess.Popen]:
    """
    Show a macOS HUD toast using the bundled ToastHUD.app.

    Args:
        message: The message to display.
        width: Width of the toast in points.
        height: Height of the toast in points.
        bg: Background color (hex string or (r,g,b) tuple of 0-1 floats).
        position: Position on screen ("top-right", "center", etc) or (x, y) coordinates.
        font_size: Font size in points.
        text_color: Text color (hex string or (r,g,b) tuple of 0-1 floats).
        corner_radius: Corner radius in points.
        display_duration: How long to show the toast (seconds).
        fade_out_duration: Duration of fade out animation (seconds).
        fade_in_duration: Duration of fade in animation (seconds).
        window_level: Window level ("normal", "floating", "status", "modal", "max").
        blocking: If True, wait for the toast to close before returning.
        check: If True, raise a CalledProcessError if the toast app fails (only if blocking=True).
    """
    exe = _get_executable_path()

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

    # Message goes at the end
    args.append(str(message))

    if blocking:
        return subprocess.run(args, check=check, capture_output=True, text=True)
    
    return subprocess.Popen(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    # Simple test
    toast("Hello from mactoast!", width=300, height=100, bg="#3333FF88", position="top-right", font_size=16)