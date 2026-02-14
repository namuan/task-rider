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
- `border_width`: 8 pixels - Thick enough to be noticeable

**Window Flags:**
- `Qt.WindowType.FramelessWindowHint` - No window decorations
- `Qt.WindowType.WindowStaysOnTopHint` - Always visible
- `Qt.WindowType.Tool` - Doesn't appear in taskbar

**Widget Attributes:**
- `Qt.WidgetAttribute.WA_TranslucentBackground` - Transparent interior
- `Qt.WidgetAttribute.WA_ShowWithoutActivating` - Doesn't steal focus

**Components:**
- `task_label`: QLabel displaying the task name (18pt bold, white)
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
- `on_focus_border_closed()`: Callback for close button, triggers hide

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
