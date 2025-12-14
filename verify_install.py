#!/usr/bin/env python3
"""
Quick verification test for mactoast package.
Run this after installing to verify everything works.
"""

import sys
import time

def test_import():
    """Test basic import."""
    print("Testing import...", end=" ")
    try:
        import mactoast
        from mactoast import toast, show_success, show_error, show_warning, show_info
        from mactoast import ToastPosition, WindowLevel
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_basic_toast():
    """Test basic toast."""
    print("Testing basic toast...", end=" ")
    try:
        import mactoast
        mactoast.toast("Basic test", display_duration=1, blocking=True)
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_with_icon():
    """Test toast with icon."""
    print("Testing icon...", end=" ")
    try:
        import mactoast
        mactoast.toast("Icon test", icon="star.fill", display_duration=1, blocking=True)
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_with_sound():
    """Test toast with sound."""
    print("Testing sound...", end=" ")
    try:
        import mactoast
        mactoast.toast("Sound test", sound="beep1", display_duration=1, blocking=True)
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_auto_size():
    """Test auto-size."""
    print("Testing auto-size...", end=" ")
    try:
        import mactoast
        mactoast.toast("Auto-size test!", auto_size=True, display_duration=1, blocking=True)
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_presets():
    """Test preset styles."""
    print("Testing presets...", end=" ")
    try:
        import mactoast
        mactoast.show_success("Success!", display_duration=1, blocking=True)
        time.sleep(0.3)
        mactoast.show_error("Error!", display_duration=1, blocking=True)
        time.sleep(0.3)
        mactoast.show_warning("Warning!", display_duration=1, blocking=True)
        time.sleep(0.3)
        mactoast.show_info("Info!", display_duration=1, blocking=True)
        print("✅")
        return True
    except Exception as e:
        print(f"❌ {e}")
        return False

def test_non_blocking():
    """Test non-blocking mode."""
    print("Testing non-blocking...", end=" ")
    try:
        import mactoast
        p = mactoast.toast("Non-blocking test", display_duration=1, blocking=False)
        if p and hasattr(p, 'pid'):
            print("✅")
            return True
        else:
            print("❌ No process returned")
            return False
    except Exception as e:
        print(f"❌ {e}")
        return False

def main():
    print("=" * 50)
    print("Mactoast Package Verification")
    print("=" * 50)
    print()
    
    tests = [
        test_import,
        test_basic_toast,
        test_with_icon,
        test_with_sound,
        test_auto_size,
        test_presets,
        test_non_blocking,
    ]
    
    results = [test() for test in tests]
    
    print()
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
