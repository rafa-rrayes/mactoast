//
//  ToastPanel.swift
//  ToastHUD
//
//  Created by Rafael Cury Rayes on 18/11/25.
//


import Cocoa

class ToastPanel: NSPanel {

    init(contentRect: NSRect, contentViewController: NSViewController, clickToDismiss: Bool = true) {
        super.init(
            contentRect: contentRect,
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )

        self.contentViewController = contentViewController

        isOpaque = false
        backgroundColor = .clear
        hasShadow = true

        // Float above normal windows but below critical stuff
        level = .screenSaver
        // Show on all spaces & don't participate in normal window cycling
        collectionBehavior = [
            .canJoinAllSpaces,
            .fullScreenAuxiliary
        ]

        // Don't vanish when other apps activate
        hidesOnDeactivate = false

        // Allow clicks only if click-to-dismiss is enabled
        ignoresMouseEvents = !clickToDismiss
    }

    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}
