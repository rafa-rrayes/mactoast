"""
Example of non-blocking toast notifications.
"""
import time
from mactoast import toast, ToastPosition

def example_non_blocking():
    print("Showing first toast (non-blocking)...")
    # This should return immediately
    process1 = toast(
        "First Toast", 
        position=(1200, 600),
        display_duration=3.0,
        blocking=False,
        corner_radius=40,
        width=150,
        height=45,
        bg=(0.2, 0.8, 0.3),  # Green
    )
    print("First toast process started.")

    print("Doing some work...")
    time.sleep(1.0)

    print("Showing second toast (non-blocking)...")
    process2 = toast(
        "Second Toast", 
        position=(1200, 500),
        display_duration=3.0,
        blocking=False,
        corner_radius=40,
        width=150,
        height=45,
        bg=(0.9, 0.2, 0.2),  # Red
    )
    print("Second toast process started.")

    print("Waiting for toasts to finish...")
    # We can wait for them if we want
    process1.wait()
    process2.wait()
    print("All toasts finished.")

if __name__ == "__main__":
    example_non_blocking()
