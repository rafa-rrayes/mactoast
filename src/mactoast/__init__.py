"""Mactoast - Simple toast notifications for macOS.

A lightweight library for creating elegant, customizable toast notifications
on macOS using native Cocoa APIs.

Quick Start:
    >>> from mactoast import show_toast
    >>> show_toast('Hello, World!')
    >>> show_toast('Success!', bg_color=(0.0, 0.8, 0.0))

Styled notifications:
    >>> from mactoast import show_success, show_error, show_warning, show_info
    >>> show_success('File saved!')
    >>> show_error('Operation failed!')
    >>> show_warning('Low disk space')
    >>> show_info('Update available')

For advanced use cases where you need explicit control:
    >>> from mactoast import EmbeddedToast, StandaloneToast
"""

from mactoast.toast import (
    show_toast,
    EmbeddedToast,
    StandaloneToast,
)

__version__ = "0.1.0"
__all__ = [
    "show_toast",
    "EmbeddedToast",
    "StandaloneToast",
]