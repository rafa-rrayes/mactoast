# Changelog

All notable changes to mactoast will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-14

Major feature release with icons, sounds, auto-sizing, and architecture improvements.

### Added
- **Icon Support**: Native SF Symbols integration for beautiful, crisp icons
  - All preset styles now include default icons (success, error, warning, info)
  - Custom icons via `icon` parameter using SF Symbol names
  - Automatic sizing and spacing calculations

- **Click to Dismiss**: Interactive toasts that respond to user clicks
  - Enabled by default for all toasts
  - Configurable via `click_to_dismiss` parameter
  - Allows users to dismiss long-duration notifications immediately

- **Auto-Size Feature**: Intelligent automatic dimension calculation
  - `auto_size=True` automatically calculates optimal width and height
  - Smart text wrapping only when necessary
  - Adaptive corner radius for compact toasts
  - Configurable constraints via `min_width` and `max_width` parameters
  - Icon-aware space calculations

- **Sound Effects**: Built-in notification sounds
  - 16 bundled sounds across 4 categories: beep, confirmation, pop, sci-fi
  - Multiple audio format support: `.wav`, `.mp3`, `.m4a`
  - Sounds stored in app bundle (no Python dependencies)
  - Support for custom sound files via absolute paths
  - Preset styles include default sounds
  - AVFoundation-powered playback in Swift
  - Simple API: just pass sound name or path

### Changed
- **Architecture Redesign**: Simplified Swift code, moved logic to Python
  - Python now handles all auto-size calculations
  - Swift ToastHUD app reduced to minimal rendering layer (~30% code reduction)
  - Improved maintainability and flexibility
  - Better separation of concerns

- **Default Style Updates**: Preset styles now include icons and sounds
  - `ToastStyle.SUCCESS`: Green with checkmark icon + confirmation1 sound
  - `ToastStyle.ERROR`: Red with X mark icon + beep1 sound
  - `ToastStyle.WARNING`: Orange with warning icon + beep1 sound
  - `ToastStyle.INFO`: Blue with info icon + confirmation2 sound

- **Helper Functions**: Now return process object for non-blocking support
  - `show_success()`, `show_error()`, `show_warning()`, `show_info()` can be used with `blocking=False`

### Technical Details
- Auto-size calculation uses AppKit's text measurement APIs via Python
- Adaptive corner radius: `min(16, height/2 - 2)` for compact toasts
- Text wrapping only occurs when natural width exceeds `max_width`
- Default constraints: `min_width=100`, `max_width=400`
- Sound playback uses AVFoundation in Swift
- Multi-format audio support with automatic extension detection

## [0.0.3] - Previous Release

### Features
- Customizable toast notifications for macOS
- Multiple positioning options (predefined and custom coordinates)
- Window level control for z-index management
- Non-blocking mode for asynchronous execution
- Smooth fade-in and fade-out animations
- Preset styles for common notification types
- Full color customization (background and text)
- Custom dimensions, font size, and corner radius

### Technical
- Native Swift app bundled with Python package
- Borderless, modern UI design
- HUD window style with visual effects
- Minimal dependencies

## [0.0.2] - Earlier Release

### Initial Features
- Basic toast notification system
- Color and position customization
- Timing controls

## [0.0.1] - First Release

### Added
- Initial release of mactoast
- Basic toast functionality

---

[Unreleased]: https://github.com/rafa-rrayes/mactoast/compare/v0.0.3...HEAD
[0.0.3]: https://github.com/rafa-rrayes/mactoast/releases/tag/v0.0.3
[0.0.2]: https://github.com/rafa-rrayes/mactoast/releases/tag/v0.0.2
[0.0.1]: https://github.com/rafa-rrayes/mactoast/releases/tag/v0.0.1
