import objc
from typing import Optional, Tuple
from Cocoa import (
    NSApplication,
    NSWindow,
    NSBackingStoreBuffered,
    NSMakeRect,
    NSTextField,
    NSTextAlignmentCenter,
    NSFont,
    NSColor,
    NSBorderlessWindowMask,
    NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSAnimationContext,
    NSApplicationActivationPolicyAccessory,
)
from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSRunLoopCommonModes, NSDate, NSObject


class _ToastWindow(NSObject):
    """Internal class to create and manage toast window UI."""
    
    def initWithParams_(self, params):
        """Initialize with parameters."""
        self = objc.super(_ToastWindow, self).init()
        if not self:
            return None
            
        (message, width, height, bg_color, text_color, position,
         corner_radius, font_size, window_level) = params
        
        # Create the borderless toast window
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            NSMakeRect(0, 0, width, height),
            NSBorderlessWindowMask,
            NSBackingStoreBuffered,
            False,
        )
        
        if position is None:
            self.window.center()
        else:
            x, y = position
            self.window.setFrameOrigin_((x, y))

        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setHasShadow_(True)
        self.window.setIgnoresMouseEvents_(True)
        self.window.setAlphaValue_(0.0)  # Start invisible for fade-in
        self.window.setLevel_(window_level)
        self.window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)

        # Rounded background
        content = self.window.contentView()
        content.setWantsLayer_(True)
        layer = content.layer()
        radius = corner_radius if corner_radius is not None else height / 2
        layer.setCornerRadius_(radius)
        bg = NSColor.colorWithCalibratedRed_green_blue_alpha_(*bg_color, 1.0)
        layer.setBackgroundColor_(bg.CGColor())

        # Label
        text_height = font_size * 1.5
        text_y = (height - text_height) / 2
        label = NSTextField.alloc().initWithFrame_(NSMakeRect(15, text_y, width - 30, text_height))
        label.setStringValue_(message)
        label.setBezeled_(False)
        label.setDrawsBackground_(False)
        label.setEditable_(False)
        label.setSelectable_(False)
        label.setAlignment_(NSTextAlignmentCenter)
        label.setFont_(NSFont.systemFontOfSize_(font_size))
        label.setTextColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(*text_color, 1.0))
        content.addSubview_(label)
        
        return self

    def show(self):
        """Display the window."""
        self.window.makeKeyAndOrderFront_(None)
        
    def fade_in(self, duration: float):
        """Fade in animation."""
        NSAnimationContext.beginGrouping()
        NSAnimationContext.currentContext().setDuration_(duration)
        self.window.animator().setAlphaValue_(1.0)
        NSAnimationContext.endGrouping()
        
    def fade_out(self, duration: float):
        """Fade out animation."""
        NSAnimationContext.beginGrouping()
        NSAnimationContext.currentContext().setDuration_(duration)
        self.window.animator().setAlphaValue_(0.0)
        NSAnimationContext.endGrouping()
        
    def close(self):
        """Close and cleanup the window."""
        if self.window:
            try:
                self.window.orderOut_(None)
                # Don't explicitly close, let it be garbage collected
                # self.window.close()
            except:
                pass  # Silently ignore cleanup errors
            finally:
                self.window = None
class Toast(NSObject):
    """
    Toast notification
    """
    
    def initWithParams_(self, params):
        """Initialize with parameters."""
        self = objc.super(Toast, self).init()
        if not self:
            return None
            
        (self.message, self.width, self.height, self.bg_color, self.text_color,
         self.position, self.corner_radius, self.display_duration,
         self.fade_duration, self.font_size, self.window_level) = params
        
        self._toast_window = None
        self._display_timer = None
        self._fade_timer = None
        self._should_stop = False
        return self
        
    def show(self):
        """Show the toast notification (non-blocking; assumes a running run loop)."""
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)

        params = (
            self.message, self.width, self.height, self.bg_color,
            self.text_color, self.position, self.corner_radius,
            self.font_size, self.window_level
        )
        self._toast_window = _ToastWindow.alloc().initWithParams_(params)

        # Show and fade in
        self._toast_window.show()
        self._toast_window.fade_in(0.3)

        # Schedule fade-out
        self._display_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            self.display_duration,
            self,
            objc.selector(self._startFadeOut_, signature=b"v@:@"),
            None,
            False,
        )
        # Make sure it also fires while user is interacting
        NSRunLoop.currentRunLoop().addTimer_forMode_(self._display_timer, NSRunLoopCommonModes)
    def _startFadeOut_(self, timer):
        """Begin fade out animation."""
        if self._toast_window:
            self._toast_window.fade_out(self.fade_duration)

            self._fade_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                self.fade_duration,
                self,
                objc.selector(self._cleanup_, signature=b"v@:@"),
                None,
                False,
            )
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._fade_timer, NSRunLoopCommonModes)

    def _cleanup_(self, timer):
        """Clean up and stop timers."""
        if self._display_timer and self._display_timer.isValid():
            self._display_timer.invalidate()
        self._display_timer = None

        if self._fade_timer and self._fade_timer.isValid():
            self._fade_timer.invalidate()
        self._fade_timer = None

        if self._toast_window:
            self._toast_window.close()
            self._toast_window = None

        self._should_stop = True


def make_toast(
    message: str,
    width: int = 280,
    height: int = 80,
    bg_color: Tuple[float, float, float] = (0.2, 0.2, 0.2),
    text_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    position: Optional[Tuple[int, int]] = None,
    corner_radius: Optional[float] = None,
    display_duration: float = 2.0,
    fade_duration: float = 0.5,
    font_size: float = 16.0,
    window_level: int = 3,
) -> Toast:
    """
    Create and return a Toast instance.
    
    Args:
        message: Text to display
        width: Window width in pixels
        height: Window height in pixels
        bg_color: Background color as RGB tuple (0.0-1.0)
        text_color: Text color as RGB tuple (0.0-1.0)
        position: Optional (x, y) position. None to center.
        corner_radius: Corner radius. None for pill shape.
        display_duration: How long to show (seconds)
        fade_duration: Fade out duration (seconds)
        font_size: Font size in points
        window_level: NSWindow level (3 = floating)
    
    Returns:
        Toast instance (call .show() to display)
    """
    params = (
        message, width, height, bg_color, text_color, position,
        corner_radius, display_duration, fade_duration,
        font_size, window_level,
    )
    return Toast.alloc().initWithParams_(params)


if __name__ == "__main__":
    import rumps
    class AwesomeStatusBarApp(rumps.App):
        def __init__(self):
            super(AwesomeStatusBarApp, self).__init__("Awesome App")
            self.menu = ["Preferences", "Silly button", "Say hi"]

        @rumps.clicked("Preferences")
        def prefs(self, _):
            rumps.alert("jk! no preferences available!")

        @rumps.clicked("Silly button")
        def onoff(self, sender):
            sender.state = not sender.state

        @rumps.clicked("Say hi")
        def sayhi(self, _):
            t = make_toast(
                message="Hello, World!",
                display_duration=1.0,
                fade_duration=1.0,
                width=300,
                height=100,
            )
            t.show()
    AwesomeStatusBarApp().run()

