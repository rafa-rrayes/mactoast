"""
Basic usage examples for Mactoast.
Run this file to see different toast notification styles.

This example demonstrates STANDALONE mode - for standalone Python scripts
that don't have an existing NSApplication.
"""

from mactoast import show_toast
import time


def example_basic():
    """Simple toast using the convenience function."""
    print("Showing basic toast...")
    show_toast(
        "Hello, World!",
        bg_color=(0.2, 0.2, 0.2),
        text_color=(1.0, 1.0, 1.0),
        display_duration=2.0,
        position=(800, 500)
    )
    print("Toast completed!")


def example_colored():
    """Different colored toasts."""
    print("Showing blue toast...")
    show_toast(
        'Blue notification',
        bg_color=(0.0, 0.5, 1.0),
        text_color=(1.0, 1.0, 1.0),
        display_duration=2.0,
    )
    
    time.sleep(0.5)
    
    print("Showing green success toast...")
    show_toast(
        'Success!',
        bg_color=(0.0, 0.8, 0.0),
        text_color=(0.0, 0.0, 0.0),
        display_duration=2.0,
    )


def example_custom_timing():
    """Toast with custom display and fade timing."""
    print("Showing toast with longer display time...")
    show_toast(
        'This stays longer...',
        display_duration=5.0,
        fade_duration=2.0,
    )
    print("Done!")


def example_positioned():
    """Toast at specific screen position."""
    print("Showing positioned toast...")
    show_toast(
        'Top right corner',
        position=(1200, 800),
        bg_color=(0.8, 0.2, 0.2),
        corner_radius=10,
        display_duration=2.0,
    )


if __name__ == "__main__":
    print("=== Mactoast Standalone Examples ===\n")
    
    example_basic()
    time.sleep(0.5)
    
    example_colored()
    time.sleep(0.5)
    
    example_custom_timing()
    time.sleep(0.5)
    
    example_positioned()
    
    print("\n=== All examples completed! ===")
    time.sleep(4)  # Wait to see the toast before script ends
