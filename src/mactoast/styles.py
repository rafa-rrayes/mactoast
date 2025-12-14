"""Predefined toast styles for common notification types.

This module provides convenient style presets and helper functions for showing
toast notifications with common styling patterns (success, error, warning, info).
"""

from typing import Any
from mactoast._runner import toast


class ToastStyle:
    """Predefined toast styles for common notification types."""
    
    # Success: Green background with dark text
    SUCCESS = {
        'bg': (0.2, 0.8, 0.3),  # Green
        'text_color': (0.0, 0.0, 0.0),  # Black
        'icon': 'checkmark.circle.fill',
        'sound': 'confirmation1',
    }
    
    # Error: Red background with white text
    ERROR = {
        'bg': (0.9, 0.2, 0.2),  # Red
        'text_color': (1.0, 1.0, 1.0),  # White
        'icon': 'xmark.circle.fill',
        'sound': 'beep1',
    }
    
    # Warning: Orange/Yellow background with dark text
    WARNING = {
        'bg': (1.0, 0.6, 0.0),  # Orange
        'text_color': (0.0, 0.0, 0.0),  # Black
        'icon': 'exclamationmark.triangle.fill',
        'sound': 'beep1',
    }
    
    # Info: Blue background with white text
    INFO = {
        'bg': (0.2, 0.5, 0.9),  # Blue
        'text_color': (1.0, 1.0, 1.0),  # White
        'icon': 'info.circle.fill',
        'sound': 'confirmation2',
    }
    
    # Default: Dark gray background with white text
    DEFAULT = {
        'bg': (0.2, 0.2, 0.2),  # Dark gray
        'text_color': (1.0, 1.0, 1.0),  # White
    }


def show_success(message: str, **kwargs: Any):
    """
    Show a success toast notification with green styling.
    
    Args:
        message: Text to display
        **kwargs: Additional parameters to pass to toast()
    
    Example:
        >>> from mactoast import show_success
        >>> show_success("File saved successfully!")
    """
    style = ToastStyle.SUCCESS.copy()
    style.update(kwargs)
    return toast(message, **style)


def show_error(message: str, **kwargs: Any):
    """
    Show an error toast notification with red styling.
    
    Args:
        message: Text to display
        **kwargs: Additional parameters to pass to toast()
    
    Example:
        >>> from mactoast import show_error
        >>> show_error("Failed to load file")
    """
    style = ToastStyle.ERROR.copy()
    style.update(kwargs)
    return toast(message, **style)


def show_warning(message: str, **kwargs: Any):
    """
    Show a warning toast notification with orange styling.
    
    Args:
        message: Text to display
        **kwargs: Additional parameters to pass to toast()
    
    Example:
        >>> from mactoast import show_warning
        >>> show_warning("Low disk space")
    """
    style = ToastStyle.WARNING.copy()
    style.update(kwargs)
    return toast(message, **style)


def show_info(message: str, **kwargs: Any):
    """
    Show an info toast notification with blue styling.
    
    Args:
        message: Text to display
        **kwargs: Additional parameters to pass to toast()
    
    Example:
        >>> from mactoast import show_info
        >>> show_info("Update available")
    """
    style = ToastStyle.INFO.copy()
    style.update(kwargs)
    return toast(message, **style)


__all__ = [
    'ToastStyle',
    'show_success',
    'show_error',
    'show_warning',
    'show_info',
]
