"""Mactoast - Simple toast notifications for macOS.

A lightweight library for creating elegant, customizable toast notifications
on macOS using native Cocoa APIs.

Quick Start:
    >>> from mactoast import show_toast
    >>> show_toast('Hello, World!')
    >>> show_toast('Success!', bg=(0.0, 0.8, 0.0))
"""
from ._runner import toast, ToastPosition, WindowLevel
from .styles import show_success, show_error, show_warning, show_info, ToastStyle

# Alias for backward compatibility or preference
show_toast = toast

__all__ = [
    "toast",
    "show_toast",
    "ToastPosition",
    "WindowLevel",
    "show_success",
    "show_error",
    "show_warning",
    "show_info",
    "ToastStyle",
]
