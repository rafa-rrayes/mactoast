import SwiftUI
import AppKit

struct ToastView: View {
    let message: String
    let fontSize: CGFloat
    let backgroundColor: NSColor
    let textColor: NSColor
    let cornerRadius: CGFloat
    let width: CGFloat
    let height: CGFloat
    let icon: String?  // SF Symbol name
    let clickToDismiss: Bool
    var onTap: (() -> Void)?  // Click-to-dismiss callback

    var body: some View {
        ZStack {
            // Blur background
            VisualEffectView(material: .hudWindow, blendingMode: .behindWindow)
                .clipShape(RoundedRectangle(cornerRadius: cornerRadius, style: .continuous))

            // Tint overlay using the provided background color
            RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                .fill(Color(nsColor: backgroundColor))

            RoundedRectangle(cornerRadius: cornerRadius, style: .continuous)
                .strokeBorder(Color.white.opacity(0.08), lineWidth: 1)

            // Content: Icon + Text
            HStack(spacing: 12) {
                if let iconName = icon, !iconName.isEmpty {
                    Image(systemName: iconName)
                        .font(.system(size: fontSize + 4, weight: .semibold))
                        .foregroundStyle(Color(nsColor: textColor))
                }
                
                Text(message)
                    .font(.system(size: fontSize, weight: .medium))
                    .foregroundStyle(Color(nsColor: textColor))
                    .multilineTextAlignment(.center)
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
        }
        .frame(width: width, height: height)
        .contentShape(Rectangle())  // Make entire area tappable
        .onTapGesture {
            if clickToDismiss {
                onTap?()
            }
        }
    }
}
