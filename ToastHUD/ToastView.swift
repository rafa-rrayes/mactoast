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

            Text(message)
                .font(.system(size: fontSize, weight: .medium))
                .multilineTextAlignment(.center)
                .padding(.horizontal, 20)
                .padding(.vertical, 12)
                .foregroundStyle(Color(nsColor: textColor))
        }
        // 👇 This is the important part: force the toast view to the requested size
        .frame(width: width, height: height)
    }
}
