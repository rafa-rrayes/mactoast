"""
Basic usage examples for Mactoast.
Run this file to see different toast notification styles.

This example demonstrates STANDALONE mode - for standalone Python scripts
that don't have an existing NSApplication.
"""

from mactoast import toast, ToastPosition, WindowLevel, show_success, show_error
import time


def example_basic():
    """Simple toast using the convenience function."""
    print("Showing basic toast...")
    toast(
        "Hello, World!",
        bg=(0.2, 0.2, 0.2),
        text_color=(1.0, 1.0, 1.0),
        display_duration=2.0,
        position=ToastPosition.CENTER,
        window_level=WindowLevel.FLOATING)
    print("Toast completed!")
def example_colored():
    """Different colored toasts."""
    print("Showing blue toast...")
    toast(
        'Blue notification',
        bg=(0.0, 0.5, 1.0),
        text_color=(1.0, 1.0, 1.0),
        display_duration=2.0,
        position="top-right",
        window_level=WindowLevel.FLOATING

        
    )
    
    time.sleep(0.5)
    
    print("Showing green success toast...")
    show_success(
        'Success!',
        display_duration=2.0,
    )


def example_custom_timing():
    """Toast with custom display and fade timing."""
    print("Showing toast with longer display time...")
    toast(
        "Slow fade out...",
        display_duration=1.0,
        fade_out_duration=2.0,
        position=ToastPosition.BOTTOM_LEFT
    )


def example_positioned():
    """Toast at specific screen position."""
    print("Showing positioned toast...")
    toast(
        'Top right corner (custom coords)',
        position=(1200, 800),
        bg=(0.8, 0.2, 0.2),
        corner_radius=10,
        display_duration=2.0,
    )


def example_window_level():
    """Toast with specific window level."""
    print("Showing toast with max window level...")
    toast(
        "Always on top!",
        window_level=WindowLevel.MAX,
        display_duration=2.0,
        bg=(0.5, 0.0, 0.5)
    )


if __name__ == "__main__":
    print("=== Mactoast Standalone Examples ===\n")
    
    example_basic()
    time.sleep(3)
    
    example_colored()
    time.sleep(3)
    
    example_custom_timing()
    time.sleep(3)

    example_positioned()
    time.sleep(3)

    example_window_level()
    
    print("\n=== All examples completed! ===")
