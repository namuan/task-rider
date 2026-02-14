# Focus Border Mode

## Overview

When a user starts a task, the main TaskRider window hides and a full-screen focus border appears around the screen with the task name displayed at the top center. This creates a distraction-free environment while keeping the user aware of their current task.

## Feature Behavior

1. **On Task Start**:
   - Main TaskRider window hides
   - Full-screen border overlay appears
   - Current task name displays at top center
   - Close button (x) appears next to task name

2. **On Close Button Click**:
   - Timer stops (via `toggle_timer()`)
   - Border overlay hides
   - Main TaskRider window reappears

3. **On Timer Pause**:
   - Border overlay hides
   - Main TaskRider window reappears

## Technical Implementation

### New File: `app/widgets/focus_border_widget.py`

A new `FocusBorderWidget` class that extends `QWidget`:

```python
class FocusBorderWidget(QWidget):
    def __init__(self, on_close_callback=None):
        # Frameless, stay-on-top, tool window
        # Translucent background for border-only appearance
```

**Key Attributes:**
- `border_color`: QColor(0, 122, 255) - Blue accent color
- `border_width`: 8 pixels - Side and bottom border thickness
- `top_border_width`: 45 pixels - Thicker top border to clear Mac notch

**Window Flags:**
- `Qt.WindowType.FramelessWindowHint` - No window decorations
- `Qt.WindowType.WindowStaysOnTopHint` - Always visible
- `Qt.WindowType.Tool` - Doesn't appear in taskbar

**Widget Attributes:**
- `Qt.WidgetAttribute.WA_TranslucentBackground` - Transparent interior
- `Qt.WidgetAttribute.WA_ShowWithoutActivating` - Doesn't steal focus

**Components:**
- `task_label`: QLabel displaying the task name (18pt bold, white text on semi-transparent black background with rounded corners and padding)
- `close_button`: QPushButton with (x) symbol, circular, hover effect
- `header_widget`: Container widget for task name and close button

**Methods:**
- `_setup_header()`: Creates the header with centered task name and close button
- `_on_close_clicked()`: Handles close button click, triggers callback
- `set_task_name(name)`: Updates the displayed task name
- `_position_header()`: Centers header at top of screen
- `paintEvent()`: Draws the border rectangle using QPainter
- `showEvent()`: Repositions header when widget shows
- `resizeEvent()`: Repositions header on resize

### Modified File: `app/controllers/overlay_controller.py`

Updated `OverlayController` to manage the focus border:

**Changes:**
- Removed old `Overlay` widget dependency
- Added `FocusBorderWidget` instance
- Connected existing signals to new behavior

**Methods:**
- `display_overlay()`: Shows focus border, hides main window
- `hide_overlay()`: Hides focus border, shows main window
- `on_focus_border_closed()`: Callback for close button, stops timer via `toggle_timer()`

## Signal Flow

```
User clicks Start
    ↓
ManageTimerController.toggle_timer()
    ↓
app_events.timer_started.emit()
    ↓
OverlayController.display_overlay()
    ↓
- Get top task from data
- Set task name on focus border
- Show focus border
- Hide main window
```

## File Structure

```
app/
├── controllers/
│   └── overlay_controller.py  (modified)
└── widgets/
    └── focus_border_widget.py  (new)
```

## Branch

`feature/focus-border-mode`

## Future Enhancements (Potential)

- Configurable border color/thickness
- Optional timer display in border
- Keyboard shortcut to toggle border
- Multi-monitor support (border on active monitor only)

### Multi-Monitor Support

The focus border now appears on all connected monitors simultaneously:

**Implementation:**
- `OverlayController` creates a `FocusBorderWidget` for each screen via `QApplication.screens()`
- `FocusBorderWidget` accepts an optional `target_screen` parameter to position on specific screens
- Monitors screen configuration changes via `QApplication.screenAdded` and `QApplication.screenRemoved` signals
- All borders display the same task name and close synchronously

**Changes to `OverlayController`:**
- Replaced single `focus_border` with `focus_borders` list
- Added `_create_focus_borders()` to initialize widgets for all screens
- Added `_handle_screen_added()` to create border for new monitors
- Added `_handle_screen_removed()` to clean up borders for removed monitors
- Updated `display_overlay()` and `hide_overlay()` to manage all borders

**Changes to `FocusBorderWidget`:**
- Added `target_screen` constructor parameter
- Uses target screen geometry instead of primary screen
- Renamed internal `screen` attribute to `_target_screen` to avoid QWidget.screen() conflict

## Recent Updates

### Multi-Monitor Support (Current)

### Task Label Background
Added semi-transparent black background (`rgba(0, 0, 0, 0.7)`) with rounded corners and padding to the task label for better visibility against any screen content.

### Mac Notch Support
Increased top border to 45 pixels to clear the Mac notch, ensuring the task name and close button appear below the notch. Side and bottom borders remain 8 pixels.

### Close Button Timer Stop
The close button now stops the timer by calling `ManageTimerController.toggle_timer()` instead of just hiding the overlay. This ensures the main window reflects the correct timer state when it reappears.

### Persistent Focus Border Across Application Switches
Implemented macOS-specific window properties to ensure the focus border remains visible when switching to other applications.

**Problem:**
On macOS, windows with `Qt.WindowType.WindowStaysOnTopHint` still get hidden when the application loses focus. This caused the focus border to disappear when switching to another app.

**Solution:**
Added `_setup_macos_window_properties()` method that configures the underlying NSWindow with special collection behaviors using the Objective-C runtime via ctypes.

**Technical Implementation:**
```python
def _setup_macos_window_properties(self):
    # Uses ctypes to call Objective-C runtime directly
    from ctypes import c_void_p, CDLL, c_bool, c_uint

    # Get the NSWindow from the Qt widget's winId
    view_id = int(self.winId())
    objc = CDLL(None)

    # Get the window from the view
    window = objc.objc_msgSend(view_id, window_sel)

    if window:
        # Prevent window from hiding on app deactivation
        objc.objc_msgSend(window, set_hides_on_deactivate_sel, False)

        # Set collection behavior to appear on all Spaces and full-screen apps
        collection_behavior = (
            NSWindowCollectionBehaviorCanJoinAllSpaces  # 1 << 0
            | NSWindowCollectionBehaviorFullScreenAuxiliary  # 1 << 8
        )
        objc.objc_msgSend(window, set_collection_behavior_sel, collection_behavior)
```

**Key macOS Window Properties Set:**
- `hidesOnDeactivate = False` - Prevents the window from being hidden when the application becomes inactive
- `collectionBehavior = CanJoinAllSpaces | FullScreenAuxiliary` - Allows the window to:
  - Appear on all macOS Spaces (virtual desktops)
  - Float above full-screen applications

**Dependencies:**
- Uses existing `pyobjc` dependency in the project
- ctypes is part of Python standard library

**Timing:**
The method is called in `showEvent()` after the widget is shown, ensuring the NSWindow exists before attempting to set its properties. A flag `_macos_properties_set` prevents redundant configuration.
