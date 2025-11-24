//
//  ToastHUDApp.swift
//  ToastHUD
//
//  Created by Rafael Cury Rayes on 18/11/25.
//

import SwiftUI

@main
struct ToastHUDApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        // No main window from SwiftUI – we control windows manually via AppKit.
        Settings {
            EmptyView()
        }
    }
}
