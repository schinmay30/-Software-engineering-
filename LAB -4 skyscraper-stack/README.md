# Vibe Coding Lab 4 – Skyscraper Stack

A Pygame-based Skyscraper Stack game developed as part of Vibe Coding Lab 4.

## Features

- Fixed inverted block placement logic.
- Perfect placement detection with bonus scoring.
- Width restoration after consecutive perfect placements.
- Falling off-cut debris animation with rotation.
- Dynamic block stacking and increasing movement speed.
- Current block count display.
- Persistent highest score across game sessions.
- Resizable game window.
- Game-over and restart functionality.

## Before and After

### Before

The original game contained an inverted placement condition that caused valid block overlaps to be treated incorrectly.

[▶ View Before Video](before_video.mp4)

### After

The final version includes the corrected placement logic, perfect placement bonus, debris animation, block counter, persistent high score, and resizable window.

[▶ View After Video](after_video.mp4)

## How to Run

Install Pygame:

```bash
pip install pygame