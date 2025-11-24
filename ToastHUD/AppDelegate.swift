import Cocoa
import SwiftUI

class AppDelegate: NSObject, NSApplicationDelegate {

    var window: NSWindow?

    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory)
        let config = ToastConfig.fromCommandLine()
        showToast(config: config)
    }

    private func showToast(config: ToastConfig) {
        let contentView = ToastView(
            message: config.message,
            fontSize: config.fontSize,
            backgroundColor: config.backgroundColor,
            textColor: config.textColor,
            cornerRadius: config.cornerRadius,
            width: config.width,
            height: config.height
        )

        let hostingController = NSHostingController(rootView: contentView)

        let toastSize = NSSize(width: config.width, height: config.height)
        let margin: CGFloat = 32

        guard let screen = NSScreen.main ?? NSScreen.screens.first else {
            NSApp.terminate(nil)
            return
        }

        let vf = screen.visibleFrame
        var origin: CGPoint

        switch config.position {
        case .bottomRight:
            origin = CGPoint(
                x: vf.maxX - toastSize.width - margin,
                y: vf.minY + margin
            )
        case .bottomLeft:
            origin = CGPoint(
                x: vf.minX + margin,
                y: vf.minY + margin
            )
        case .topRight:
            origin = CGPoint(
                x: vf.maxX - toastSize.width - margin,
                y: vf.maxY - toastSize.height - margin
            )
        case .topLeft:
            origin = CGPoint(
                x: vf.minX + margin,
                y: vf.maxY - toastSize.height - margin
            )
        case .center:
            origin = CGPoint(
                x: vf.midX - toastSize.width / 2,
                y: vf.midY - toastSize.height / 2
            )
        }

        if let x = config.x {
            origin.x = x
        }
        if let y = config.y {
            origin.y = y
        }

        let frame = NSRect(origin: origin, size: toastSize)

        let panel = ToastPanel(
            contentRect: frame,
            contentViewController: hostingController
        )

        if let levelStr = config.windowLevel {
            switch levelStr.lowercased() {
            case "normal": panel.level = .normal
            case "floating": panel.level = .floating
            case "status": panel.level = .statusBar
            case "modal": panel.level = .modalPanel
            case "max", "screensaver": panel.level = .screenSaver
            default: panel.level = .screenSaver
            }
        }

        // Make sure the content view matches the requested size too
        hostingController.view.frame = NSRect(origin: .zero, size: toastSize)

        panel.alphaValue = 0
        panel.orderFrontRegardless()
        self.window = panel
        self.window?.makeKeyAndOrderFront(nil)
        // Fade in
        NSAnimationContext.runAnimationGroup { context in
            context.duration = config.fadeInDuration
            panel.animator().alphaValue = 1.0
        }

        DispatchQueue.main.asyncAfter(deadline: .now() + config.displayDuration) { [weak self, config] in
            self?.dismissToast(fadeOutDuration: config.fadeOutDuration)
        }
    }

    private func dismissToast(fadeOutDuration: TimeInterval) {
        guard let panel = self.window else {
            NSApp.terminate(nil)
            return
        }

        NSAnimationContext.runAnimationGroup({ context in
            context.duration = fadeOutDuration
            panel.animator().alphaValue = 0.0
        }, completionHandler: {
            panel.orderOut(nil)
            NSApp.terminate(nil)
        })
    }
}
