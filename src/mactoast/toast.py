import objc
import warnings
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
    NSApp
)
from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode, NSRunLoopCommonModes, NSDate, NSObject

# Suppress PyObjC pointer warnings
warnings.filterwarnings('ignore', category=objc.ObjCPointerWarning)

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


class EmbeddedToast(NSObject):
    """
    Toast notification for embedded use in existing macOS apps.
    
    Use this mode when your Python script already has an NSApplication 
    running (e.g., rumps, PyObjC apps). The toast uses timers for 
    non-blocking animations.
    
    Example:
        import rumps
        from mactoast import EmbeddedToast
        
        class MyApp(rumps.App):
            @rumps.clicked("Show Toast")
            def show_toast(self, _):
                toast = EmbeddedToast("Hello!")
                toast.show()
        
        MyApp().run()
    """

    def initWithParams_(self, params):
        self = objc.super(EmbeddedToast, self).init()
        if not self:
            return None

        (self.message, self.width, self.height, self.bg_color, self.text_color,
         self.position, self.corner_radius, self.display_duration,
         self.fade_duration, self.font_size, self.window_level) = params

        self._toast_window = None
        self._display_timer = None
        self._fade_timer = None
        return self

    def show(self):
        """Show the toast notification (non-blocking)."""
        # Create window
        params = (
            self.message, self.width, self.height, self.bg_color,
            self.text_color, self.position, self.corner_radius,
            self.font_size, self.window_level
        )
        self._toast_window = _ToastWindow.alloc().initWithParams_(params)
        
        self._toast_window.show()
        self._toast_window.fade_in(0.3)
        
        # Schedule fade out after display duration
        # Use NSRunLoopCommonModes so timer fires even when app is busy (e.g., tracking menus)
        self._display_timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            self.display_duration,
            self,
            objc.selector(self._startFadeOut, signature=b"v@:"),
            None,
            False
        )
        NSRunLoop.currentRunLoop().addTimer_forMode_(self._display_timer, NSRunLoopCommonModes)

    def _startFadeOut(self):
        """Begin fade out animation."""
        if self._toast_window:
            self._toast_window.fade_out(self.fade_duration)
            
            # Schedule cleanup after fade completes
            # Use NSRunLoopCommonModes so timer fires even when app is busy
            self._fade_timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
                self.fade_duration,
                self,
                objc.selector(self._cleanup, signature=b"v@:"),
                None,
                False
            )
            NSRunLoop.currentRunLoop().addTimer_forMode_(self._fade_timer, NSRunLoopCommonModes)

    def _cleanup(self):
        """Clean up resources."""
        # Invalidate timers first
        if self._display_timer:
            if self._display_timer.isValid():
                self._display_timer.invalidate()
            self._display_timer = None
            
        if self._fade_timer:
            if self._fade_timer.isValid():
                self._fade_timer.invalidate()
            self._fade_timer = None
        
        # Close window safely - don't manipulate the internal window reference
        if self._toast_window:
            # Just call close() which handles everything
            self._toast_window.close()
            self._toast_window = None


class StandaloneToast(NSObject):
    """
    Toast notification for standalone Python scripts.
    
    Use this mode when your script doesn't have an NSApplication running.
    Creates and manages its own NSApplication instance. The toast will
    block until the animation completes.
    
    Example:
        from mactoast import StandaloneToast
        
        toast = StandaloneToast("Hello, World!")
        toast.show()
        print("Toast finished, continuing...")
    """
    
    def initWithParams_(self, params):
        """Initialize with parameters."""
        self = objc.super(StandaloneToast, self).init()
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
        """Show the toast notification (blocking until animation completes)."""
        # Get or create NSApplication
        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
        
        # Create toast window on main thread
        params = (
            self.message, self.width, self.height, self.bg_color,
            self.text_color, self.position, self.corner_radius,
            self.font_size, self.window_level
        )
        self._toast_window = _ToastWindow.alloc().initWithParams_(params)
        
        # Show and fade in
        self._toast_window.show()
        self._toast_window.fade_in(0.3)
        
        # Schedule display timer
        self._display_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            self.display_duration,
            self,
            objc.selector(self._startFadeOut, signature=b"v@:"),
            None,
            False
        )
        
        # Run event loop until done
        while not self._should_stop:
            NSRunLoop.currentRunLoop().runMode_beforeDate_(
                NSDefaultRunLoopMode,
                NSDate.dateWithTimeIntervalSinceNow_(0.1)
            )
    
    def _startFadeOut(self):
        """Begin fade out animation."""
        if self._toast_window:
            self._toast_window.fade_out(self.fade_duration)
            
            # Schedule cleanup
            self._fade_timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                self.fade_duration,
                self,
                objc.selector(self._cleanup, signature=b"v@:"),
                None,
                False
            )
    
    def _cleanup(self):
        """Clean up and stop event loop."""
        # Invalidate timers first
        if self._display_timer:
            if self._display_timer.isValid():
                self._display_timer.invalidate()
            self._display_timer = None
            
        if self._fade_timer:
            if self._fade_timer.isValid():
                self._fade_timer.invalidate()
            self._fade_timer = None
        
        # Close window safely
        if self._toast_window:
            self._toast_window.close()
            self._toast_window = None
            
        self._should_stop = True



def _make_embedded(
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
) -> EmbeddedToast:
    """
    Create and return an EmbeddedToast instance.
    Use for apps with existing NSApplication (e.g., rumps).
    
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
        EmbeddedToast instance (call .show() to display)
    """
    params = (
        message, width, height, bg_color, text_color, position,
        corner_radius, display_duration, fade_duration,
        font_size, window_level,
    )
    return EmbeddedToast.alloc().initWithParams_(params)


def _make_standalone(
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
) -> StandaloneToast:
    """
    Create and return a StandaloneToast instance.
    Use for standalone scripts without existing NSApplication.
    
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
        StandaloneToast instance (call .show() to display)
    """
    params = (
        message, width, height, bg_color, text_color, position,
        corner_radius, display_duration, fade_duration,
        font_size, window_level,
    )
    return StandaloneToast.alloc().initWithParams_(params)

def toast(message, **kwargs):
    app = NSApplication.sharedApplication()
    try:
        running = bool(app.isRunning())
    except Exception:
        running = bool(NSApp() and NSApp().keyWindow())
    if running:
         return _make_embedded(message, **kwargs).show()
    else:
        return _make_standalone(message, **kwargs).show()



if __name__ == "__main__":
    # Test standalone mode
    toast(
        message="Standalone Toast Test",
        bg_color=(0.0, 0.5, 1.0),
        display_duration=2.0,
    )


