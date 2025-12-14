//
//  ToastConfig.swift
//  ToastHUD
//
//  Created by Rafael Cury Rayes on 18/11/25.
//


import AppKit

enum ToastPosition: String {
    case topRight = "top-right"
    case topLeft = "top-left"
    case bottomRight = "bottom-right"
    case bottomLeft = "bottom-left"
    case center = "center"

    static let `default` = ToastPosition.bottomRight
}

struct ToastConfig {
    var message: String

    var width: CGFloat = 280
    var height: CGFloat = 80
    var position: ToastPosition = .default
    var fontSize: CGFloat = 14
    var backgroundColor: NSColor = NSColor(calibratedWhite: 0.1, alpha: 0.85)
    var textColor: NSColor = .white
    var cornerRadius: CGFloat = 16
    var displayDuration: TimeInterval = 2.5
    var fadeOutDuration: TimeInterval = 0.2
    var fadeInDuration: TimeInterval = 0.2
    var x: CGFloat?
    var y: CGFloat?
    var windowLevel: String?
    var icon: String?  // SF Symbol name (e.g., "checkmark.circle.fill")
    var clickToDismiss: Bool = true
    var sound: String?  // Path to sound file
}

extension ToastConfig {
    static func fromCommandLine() -> ToastConfig {
        var config = ToastConfig(message: "Hello from ToastHUD")
        let args = Array(CommandLine.arguments.dropFirst())

        var i = 0
        var messageParts: [String] = []

        func readValue(after index: inout Int) -> String? {
            guard index + 1 < args.count else { return nil }
            index += 1
            return args[index]
        }

        while i < args.count {
            let arg = args[i]

            if arg == "--width", let value = readValue(after: &i), let w = Double(value) {
                config.width = max(50, CGFloat(w))
            } else if arg == "--height", let value = readValue(after: &i), let h = Double(value) {
                config.height = max(30, CGFloat(h))
            } else if arg == "--font-size", let value = readValue(after: &i), let fs = Double(value) {
                config.fontSize = max(8, CGFloat(fs))
            } else if arg == "--bg", let value = readValue(after: &i) {
                if let color = NSColor.fromHexString(value) {
                    config.backgroundColor = color
                }
            } else if arg == "--position", let value = readValue(after: &i) {
                if let pos = ToastPosition(rawValue: value.lowercased()) {
                    config.position = pos
                }
            } else if arg == "--text-color", let value = readValue(after: &i) {
                if let color = NSColor.fromHexString(value) {
                    config.textColor = color
                }
            } else if arg == "--corner-radius", let value = readValue(after: &i), let cr = Double(value) {
                config.cornerRadius = max(0, CGFloat(cr))
            } else if arg == "--display-duration", let value = readValue(after: &i), let dur = Double(value) {
                config.displayDuration = max(0.1, dur)
            } else if arg == "--fade-out-duration", let value = readValue(after: &i), let dur = Double(value) {
                config.fadeOutDuration = max(0.0, dur)
            } else if arg == "--fade-in-duration", let value = readValue(after: &i), let dur = Double(value) {
                config.fadeInDuration = max(0.0, dur)
            } else if arg == "--x", let value = readValue(after: &i), let xVal = Double(value) {
                config.x = CGFloat(xVal)
            } else if arg == "--y", let value = readValue(after: &i), let yVal = Double(value) {
                config.y = CGFloat(yVal)
            } else if arg == "--window-level", let value = readValue(after: &i) {
                config.windowLevel = value
            } else if arg == "--icon", let value = readValue(after: &i) {
                config.icon = value
            } else if arg == "--click-to-dismiss", let value = readValue(after: &i) {
                config.clickToDismiss = value.lowercased() == "true" || value == "1"
            } else if arg == "--no-click-to-dismiss" {
                config.clickToDismiss = false
            } else if arg == "--sound", let value = readValue(after: &i) {
                config.sound = value
            } else if arg.hasPrefix("--") {
                // Unknown flag – ignore it (and optional value)
                // If it has a value that doesn't start with --, skip that too
                if i + 1 < args.count && !args[i + 1].hasPrefix("--") {
                    i += 1
                }
            } else {
                // Non-flag: part of the message
                messageParts.append(arg)
            }

            i += 1
        }

        if !messageParts.isEmpty {
            config.message = messageParts.joined(separator: " ")
        }

        return config
    }
}

extension NSColor {
    /// Parses "#RRGGBB", "RRGGBB", or "RRGGBBAA"
    static func fromHexString(_ hex: String) -> NSColor? {
        var string = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        if string.hasPrefix("#") {
            string.removeFirst()
        }

        guard string.count == 6 || string.count == 8,
              let value = UInt64(string, radix: 16) else {
            return nil
        }

        let r, g, b, a: CGFloat

        if string.count == 6 {
            r = CGFloat((value & 0xFF0000) >> 16) / 255.0
            g = CGFloat((value & 0x00FF00) >> 8) / 255.0
            b = CGFloat(value & 0x0000FF) / 255.0
            a = 0.85
        } else {
            r = CGFloat((value & 0xFF000000) >> 24) / 255.0
            g = CGFloat((value & 0x00FF0000) >> 16) / 255.0
            b = CGFloat((value & 0x0000FF00) >> 8) / 255.0
            a = CGFloat(value & 0x000000FF) / 255.0
        }

        return NSColor(calibratedRed: r, green: g, blue: b, alpha: a)
    }
}
