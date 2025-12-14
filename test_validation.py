#!/usr/bin/env python3
"""Test script to verify parameter validation works correctly."""

from mactoast import toast, ToastConfigError

def test_validation(description, test_func):
    """Run a validation test and report results."""
    try:
        test_func()
        print(f"❌ {description}: Should have raised ToastConfigError")
        return False
    except ToastConfigError as e:
        print(f"✅ {description}: {e}")
        return True
    except Exception as e:
        print(f"❌ {description}: Unexpected error: {e}")
        return False

def run_tests():
    """Run all validation tests."""
    print("Testing parameter validation...\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: auto_size with width
    tests_total += 1
    if test_validation(
        "auto_size=True with width",
        lambda: toast("Test", auto_size=True, width=200)
    ):
        tests_passed += 1
    
    # Test 2: auto_size with height
    tests_total += 1
    if test_validation(
        "auto_size=True with height",
        lambda: toast("Test", auto_size=True, height=100)
    ):
        tests_passed += 1
    
    # Test 3: min_width without auto_size
    tests_total += 1
    if test_validation(
        "min_width without auto_size",
        lambda: toast("Test", min_width=150)
    ):
        tests_passed += 1
    
    # Test 4: max_width without auto_size
    tests_total += 1
    if test_validation(
        "max_width without auto_size",
        lambda: toast("Test", max_width=300)
    ):
        tests_passed += 1
    
    # Test 5: min_width > max_width
    tests_total += 1
    if test_validation(
        "min_width > max_width",
        lambda: toast("Test", auto_size=True, min_width=400, max_width=200)
    ):
        tests_passed += 1
    
    # Test 6: Invalid color format (string)
    tests_total += 1
    if test_validation(
        "Invalid color format (no #)",
        lambda: toast("Test", bg="FF0000")
    ):
        tests_passed += 1
    
    # Test 7: Invalid color tuple length
    tests_total += 1
    if test_validation(
        "Invalid color tuple length",
        lambda: toast("Test", bg=(1.0, 0.0))
    ):
        tests_passed += 1
    
    # Test 8: Color value out of range
    tests_total += 1
    if test_validation(
        "Color value out of range",
        lambda: toast("Test", bg=(1.5, 0.5, 0.5))
    ):
        tests_passed += 1
    
    # Test 9: Invalid position string
    tests_total += 1
    if test_validation(
        "Invalid position string",
        lambda: toast("Test", position="middle")
    ):
        tests_passed += 1
    
    # Test 10: Invalid window level
    tests_total += 1
    if test_validation(
        "Invalid window level",
        lambda: toast("Test", window_level="super-high")
    ):
        tests_passed += 1
    
    # Test 11: Width out of range (too small)
    tests_total += 1
    if test_validation(
        "Width too small",
        lambda: toast("Test", width=20)
    ):
        tests_passed += 1
    
    # Test 12: Font size out of range (too large)
    tests_total += 1
    if test_validation(
        "Font size too large",
        lambda: toast("Test", font_size=100)
    ):
        tests_passed += 1
    
    # Test 13: Display duration too short
    tests_total += 1
    if test_validation(
        "Display duration too short",
        lambda: toast("Test", display_duration=0.05)
    ):
        tests_passed += 1
    
    # Test 14: Fade durations exceed display duration
    tests_total += 1
    if test_validation(
        "Fade durations exceed display duration",
        lambda: toast("Test", display_duration=1.0, fade_in_duration=0.6, fade_out_duration=0.6)
    ):
        tests_passed += 1
    
    # Test 15: Invalid sound name
    tests_total += 1
    if test_validation(
        "Invalid sound name",
        lambda: toast("Test", sound="ding")
    ):
        tests_passed += 1
    
    # Test 16: check=True with blocking=False
    tests_total += 1
    if test_validation(
        "check=True with blocking=False",
        lambda: toast("Test", check=True, blocking=False)
    ):
        tests_passed += 1
    
    # Test 17: Empty message
    tests_total += 1
    if test_validation(
        "Empty message",
        lambda: toast("")
    ):
        tests_passed += 1
    
    print(f"\n{'='*60}")
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("✅ All validation tests passed!")
        return 0
    else:
        print(f"❌ {tests_total - tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(run_tests())
