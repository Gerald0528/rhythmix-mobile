# Rhythmix Mobile

A mobile rhythm game built with Kivy for Android. Touch the lanes (D, F, J, K) as notes reach the hit line to score points and build combos.

## Features

- **4-lane rhythm gameplay** - Tap or hold as notes fall
- **17 built-in songs** with generated beatmaps
- **4 difficulty levels** (Easy, Normal, Hard, Practice)
- **High score tracking** with grade system (S, A, B, C, D)
- **Audio offset adjustment** for latency calibration
- **Scroll speed customization**
- **Hold notes** - Press and release at the right time

## Project Structure

```
.
├── main.py                 # App entry point
├── buildozer.spec         # Android build configuration
├── screens/               # UI Screens
│   ├── menu.py           # Main menu
│   ├── level_select.py   # Song/difficulty selection
│   ├── game_screen.py    # Main gameplay
│   ├── results.py        # Score display
│   └── settings.py       # Options screen
├── utils/                # Utilities
│   └── config.py         # Constants, songs, persistence
├── widgets/              # Custom widgets
│   ├── lane_button.py    # Touch lane widget
│   └── note_renderer.py  # Note drawing utilities
└── assets/               # Images, audio (create this)
```

## Running on Desktop

### Prerequisites
```bash
pip install kivy kivymd
```

### Run
```bash
python main.py
```

## Building for Android

### Prerequisites
1. Install buildozer:
```bash
pip install buildozer
```

2. Install Android dependencies (Linux/WSL2):
```bash
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

3. Add your music files to `assets/songs/` folder

### Build APK
```bash
# Initialize (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build and deploy to connected device
buildozer android debug deploy run

# View logs
buildozer android logcat
```

The APK will be in `bin/` folder.

## Adding Custom Songs

1. Place MP3 files in the `assets/songs/` folder
2. Add entries to `SONGS` list in `utils/config.py`:
```python
{
    "id": "my_song",
    "title": "My Song",
    "artist": "Artist Name",
    "file": "my_song.mp3",
    "bpm": 128.0,  # or None for editor-only
    "duration": 180000,  # milliseconds
    "color": (1, 0.5, 0),  # RGB tuple
}
```

## Settings

- **Music Volume**: 0-100%
- **SFX Volume**: 0-100%
- **Audio Offset**: -200ms to +200ms (calibrate for device latency)
- **Scroll Speed**: 0.5x to 2.0x (affects note fall speed)

## Scoring

| Judgment | Timing Window | Points |
|----------|----------------|--------|
| PERFECT  | ±50ms         | 100    |
| GOOD     | ±110ms        | 50     |
| OK       | ±180ms        | 25     |
| MISS     | >180ms        | 0      |

Combo multiplier: +10% score per 10 combo

## Grades

- **S**: 98%+ accuracy
- **A**: 95%+ accuracy
- **B**: 90%+ accuracy
- **C**: 80%+ accuracy
- **D**: <80% accuracy

## Controls

- **Touch lanes**: Tap the 4 lanes at the bottom of screen
- **Hold notes**: Press when head reaches line, release when tail reaches line
- **Pause**: Back button or quit button (top-left)

## Troubleshooting

### Audio not playing
- Check file format (MP3 recommended)
- Verify file is in correct location
- Check audio volume settings

### Lag/offset issues
- Adjust "Audio Offset" in settings
- Try higher values if notes feel late
- Try lower values if notes feel early

### Build errors
- Ensure all dependencies are installed
- Use WSL2 on Windows or native Linux
- Check buildozer logs for specific errors

## License

This is a personal/educational project. Original songs belong to their respective artists.

## Credits

- Built with [Kivy](https://kivy.org/)
- Android builds via [Buildozer](https://github.com/kivy/buildozer) and [python-for-android](https://github.com/kivy/python-for-android)
