//
//  ToastPanel.swift
//  ToastHUD
//
//  Created by Rafael Cury Rayes on 18/11/25.
//


import Cocoa

class ToastPanel: NSPanel {

    init(contentRect: NSRect, contentViewController: NSViewController) {
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
        // Show on all spaces & don’t participate in normal window cycling
        collectionBehavior = [
            .canJoinAllSpaces,
            .fullScreenAuxiliary
        ]

        // Don't vanish when other apps activate
        hidesOnDeactivate = false

        // Optional: allow clicks to pass through
        ignoresMouseEvents = true
    }

    override var canBecomeKey: Bool { false }
    override var canBecomeMain: Bool { false }
}
