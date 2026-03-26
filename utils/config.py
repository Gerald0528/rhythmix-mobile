"""
Configuration and utilities for Rhythmix Mobile.
Contains all game constants, song data, and persistence functions.
"""

import json
import os
import random
from kivy.utils import platform


# ═══════════════════════════════════════════════════════════════════
#  GLOBAL CONFIG
# ═══════════════════════════════════════════════════════════════════

# Lanes configuration
NUM_LANES = 4
LANE_LABELS = ["D", "F", "J", "K"]
LANE_COLORS = [
    (0, 0.78, 1),      # Cyan
    (1, 0.23, 0.47),   # Pink
    (0.23, 1, 0.47),   # Green
    (1, 0.78, 0),      # Yellow
]

# Timing windows (ms)
PERFECT_WIN = 50
GOOD_WIN = 110
OK_WIN = 180

# Palette (0-1 normalized for Kivy)
BG_COLOR = (0.047, 0.047, 0.086)
PANEL_COLOR = (0.086, 0.086, 0.149)
GRID_LINE = (0.165, 0.165, 0.267)
WHITE = (1, 1, 1)
GRAY = (0.275, 0.275, 0.353)
DIM = (0.216, 0.216, 0.294)
COL_PERFECT = (1, 0.86, 0)
COL_GOOD = (0.39, 0.86, 1)
COL_OK = (0.63, 1, 0.55)
COL_MISS = (1, 0.31, 0.31)

# Difficulty speeds (pixels per second)
DIFF_SPEEDS = {"Easy": 320, "Normal": 460, "Hard": 640, "Practice": 320}

# Active song tracking
_ACTIVE_SONG_ID = None

# Mods
ACTIVE_MODS = {
    "no_fail": False,
    "double_speed": False,
    "hidden": False,
    "sudden": False,
    "mirror": False,
    "random": False,
}

# Settings
_SETTINGS = {
    "music_vol": 0.85,
    "sfx_vol": 0.30,
    "scroll_speed": 1.0,
    "audio_offset": 0,
    "practice_speed": 1.0,
}

_SCORES = {}


# ═══════════════════════════════════════════════════════════════════
#  SONG REGISTRY
# ═══════════════════════════════════════════════════════════════════

SONGS = [
    {
        "id": "abducted",
        "title": "Galactic",
        "artist": "Synthion & Sefaro",
        "file": "Abducted_by_vegtam__Geometry_Dash_2_2.mp3",
        "bpm": 174.0,
        "duration": 135500,
        "color": (0, 0.78, 1),
    },
    {
        "id": "next_to_you",
        "title": "Next to You",
        "artist": "Austin Chen",
        "file": "_next_to_you___Audio___believe_-_EP_.mp3",
        "bpm": None,
        "duration": 160000,
        "color": (1, 0.23, 0.47),
    },
    {
        "id": "brain_power",
        "title": "Brain Power",
        "artist": "NOMA",
        "file": "Brain_Power.mp3",
        "bpm": None,
        "duration": 118700,
        "color": (0.71, 0.23, 1),
    },
    {
        "id": "aleph_0",
        "title": "Aleph-0",
        "artist": "LeaF",
        "file": "Aleph-0.mp3",
        "bpm": None,
        "duration": 142400,
        "color": (1, 0.55, 0),
    },
    {
        "id": "back_on_track",
        "title": "Back on Track",
        "artist": "DJVI",
        "file": "Back_on_Track.mp3",
        "bpm": None,
        "duration": 114800,
        "color": (0, 1, 0.71),
    },
    {
        "id": "dream_flower",
        "title": "Dream Flower",
        "artist": "KLYDIX",
        "file": "Dream_Flower.mp3",
        "bpm": None,
        "duration": 165700,
        "color": (1, 0.39, 0.71),
    },
    {
        "id": "im_blue",
        "title": "I'm Blue",
        "artist": "CatStuffer",
        "file": "CatStuffer_-_I_m_blue__Trance_Version___Radio_Edit___AzxjgdRcmGQ_.mp3",
        "bpm": None,
        "duration": 107000,
        "color": (0.12, 0.56, 1),
    },
    {
        "id": "slaughter_agony",
        "title": "Slaughter Agony",
        "artist": "KzX",
        "file": "1773971798659_KzX_-_Slaughter_Agony__Ultimate_Mashup_.mp3",
        "bpm": None,
        "duration": 173600,
        "color": (0.86, 0.16, 0.16),
    },
    {
        "id": "open_window_vgh",
        "title": "Open Window vGH",
        "artist": "Jarvis9999",
        "file": "open-window-vgh-chart-preview_bpx8AcRm.mp3",
        "bpm": None,
        "duration": 65400,
        "color": (0.47, 0.86, 0.47),
    },
    {
        "id": "freedom_dive",
        "title": "Freedom Dive",
        "artist": "xi",
        "file": "1773972904721_Freedom_Dive.mp3",
        "bpm": None,
        "duration": 272700,
        "color": (0, 0.94, 0.86),
    },
    {
        "id": "nuke_powder",
        "title": "Nuke Powder",
        "artist": "MaelouX",
        "file": "1773987766197_Nuke_Powder_-_MaelouX__Thinking_space_sequel_GD_.mp3",
        "bpm": None,
        "duration": 188500,
        "color": (1, 0.47, 0),
    },
    {
        "id": "ouroboros",
        "title": "ouroboros",
        "artist": "Cranky",
        "file": "1773990689412_ouroboros__twin_stroke_at_the_end__by_Cranky.mp3",
        "bpm": None,
        "duration": 128500,
        "color": (0.63, 0.31, 1),
    },
    {
        "id": "sine_waves",
        "title": "Sine Waves",
        "artist": "Rukkus",
        "file": "1774016307305_Sine_Waves_-_Rukkus.mp3",
        "bpm": None,
        "duration": 96000,
        "color": (0, 0.78, 0.71),
    },
    {
        "id": "animation_warrior",
        "title": "Animation Warrior Theme",
        "artist": "Nighthawk22",
        "file": "1774060355890_Animation_Warrior_Theme.mp3",
        "bpm": None,
        "duration": 206700,
        "color": (1, 0.55, 0),
    },
    {
        "id": "time_leaper",
        "title": "Time Leaper",
        "artist": "Hinkik",
        "file": "1774062308530_hinkik-time-leaper.mp3",
        "bpm": None,
        "duration": 341300,
        "color": (0, 0.63, 1),
    },
    {
        "id": "classical_vip",
        "title": "Classical VIP",
        "artist": "NIGHTkilla",
        "file": "1774063677048_NIGHTkilla_-_Classical_VIP.mp3",
        "bpm": None,
        "duration": 292600,
        "color": (0.86, 0.71, 0.31),
    },
    {
        "id": "dimension",
        "title": "Dimension",
        "artist": "Creo",
        "file": "1774068311879_Creo_-_Dimension.mp3",
        "bpm": None,
        "duration": 288100,
        "color": (0.31, 0.86, 0.71),
    },
]

# Set default song
_ACTIVE_SONG_ID = SONGS[0]["id"]


def get_song(song_id: str) -> dict:
    """Get song by ID."""
    for s in SONGS:
        if s["id"] == song_id:
            return s
    return SONGS[0]


def active_song() -> dict:
    """Get currently active song."""
    return get_song(_ACTIVE_SONG_ID)


def set_active_song(song_id: str):
    """Set the active song."""
    global _ACTIVE_SONG_ID
    _ACTIVE_SONG_ID = song_id


def SONG_FILE():
    """Get active song file."""
    return active_song()["file"]


def SONG_BPM():
    """Get active song BPM."""
    return active_song()["bpm"] or 120.0


def SONG_DURATION_MS():
    """Get active song duration."""
    return active_song()["duration"]


def BEAT_MS():
    """Get milliseconds per beat."""
    return 60000 / SONG_BPM()


# ═══════════════════════════════════════════════════════════════════
#  PATHS & PERSISTENCE
# ═══════════════════════════════════════════════════════════════════

def get_app_dir():
    """Get the app directory for storing data."""
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            return app_storage_path()
        except:
            pass
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_songs_dir():
    """Get the songs directory."""
    app_dir = get_app_dir()
    songs_dir = os.path.join(app_dir, 'songs')
    if not os.path.exists(songs_dir):
        os.makedirs(songs_dir)
    return songs_dir


def find_song_file(filename):
    """Find a song file in various locations."""
    if not filename:
        return None
    
    paths = [
        os.path.join(get_songs_dir(), filename),
        os.path.join(get_app_dir(), filename),
        filename
    ]
    
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def load_scores():
    """Load high scores from JSON."""
    global _SCORES
    path = os.path.join(get_app_dir(), "scores.json")
    try:
        with open(path, "r") as f:
            _SCORES = json.load(f)
    except:
        _SCORES = {}


def save_scores():
    """Save high scores to JSON."""
    path = os.path.join(get_app_dir(), "scores.json")
    try:
        with open(path, "w") as f:
            json.dump(_SCORES, f, indent=2)
    except Exception as e:
        print(f"Could not save scores: {e}")


def get_best(song_id, difficulty):
    """Get best score for a song/difficulty."""
    return _SCORES.get(f"{song_id}:{difficulty}")


def update_best(song_id, difficulty, score, grade, pct, combo):
    """Update best score if higher."""
    key = f"{song_id}:{difficulty}"
    best = _SCORES.get(key)
    if best is None or score > best["score"]:
        _SCORES[key] = {
            "score": score,
            "grade": grade,
            "pct": round(pct, 2),
            "combo": combo
        }
        save_scores()
        return True
    return False


def load_settings():
    """Load settings from JSON."""
    global _SETTINGS
    path = os.path.join(get_app_dir(), "settings.json")
    try:
        with open(path, "r") as f:
            data = json.load(f)
            for k in _SETTINGS:
                if k in data:
                    _SETTINGS[k] = data[k]
    except:
        pass


def save_settings():
    """Save settings to JSON."""
    path = os.path.join(get_app_dir(), "settings.json")
    try:
        with open(path, "w") as f:
            json.dump(_SETTINGS, f, indent=2)
    except Exception as e:
        print(f"Could not save settings: {e}")


def get_setting(key, default=None):
    """Get a setting value."""
    return _SETTINGS.get(key, default)


def set_setting(key, value):
    """Set a setting value."""
    _SETTINGS[key] = value


# ═══════════════════════════════════════════════════════════════════
#  CUSTOM BEATMAPS
# ═══════════════════════════════════════════════════════════════════

_CUSTOM_BEATMAPS = {}


def _charts_path():
    """Get path to charts JSON file."""
    return os.path.join(get_app_dir(), "charts.json")


def _load_charts():
    """Load custom charts from JSON."""
    try:
        with open(_charts_path(), "r") as f:
            raw = json.load(f)
        result = {}
        for sid, notes in raw.items():
            parsed = []
            for entry in notes:
                if isinstance(entry, dict):
                    parsed.append(entry)
                else:
                    ms = float(entry[0])
                    lane = int(entry[1])
                    end = float(entry[2]) if len(entry) > 2 else None
                    parsed.append((ms, lane, end) if end is not None else (ms, lane))
            result[sid] = parsed
        return result
    except:
        return {}


def _save_charts(store):
    """Save custom charts to JSON."""
    try:
        def serialise(entry):
            if isinstance(entry, dict):
                return entry
            if len(entry) == 3:
                return [entry[0], entry[1], entry[2]]
            return [entry[0], entry[1]]
        
        with open(_charts_path(), "w") as f:
            json.dump({
                sid: [serialise(e) for e in notes]
                for sid, notes in store.items()
            }, f, indent=2)
    except Exception as e:
        print(f"Warning: could not save charts.json — {e}")


# Load charts on module init
_CUSTOM_BEATMAPS = _load_charts()


def get_custom_beatmap(song_id=None):
    """Get custom beatmap for a song."""
    sid = song_id or _ACTIVE_SONG_ID
    return _CUSTOM_BEATMAPS.get(sid)


def set_custom_beatmap(notes, song_id=None):
    """Set custom beatmap for a song."""
    sid = song_id or _ACTIVE_SONG_ID
    _CUSTOM_BEATMAPS[sid] = notes
    _save_charts(_CUSTOM_BEATMAPS)


def clear_custom_beatmap(song_id=None):
    """Clear custom beatmap for a song."""
    sid = song_id or _ACTIVE_SONG_ID
    _CUSTOM_BEATMAPS.pop(sid, None)
    _save_charts(_CUSTOM_BEATMAPS)


# ═══════════════════════════════════════════════════════════════════
#  BEATMAP GENERATION
# ═══════════════════════════════════════════════════════════════════

def build_beatmap(difficulty: str) -> list:
    """Build beatmap for current song and difficulty."""
    custom = get_custom_beatmap()
    if custom is not None:
        raw = list(custom)
    else:
        raw = _default_beatmap()

    def _entry_key(x):
        if isinstance(x, dict):
            return (x["time_ms"], x["lane"])
        return (x[0], x[1])

    seen, clean = set(), []
    for entry in sorted(raw, key=_entry_key):
        if isinstance(entry, dict):
            tm, lane = entry["time_ms"], entry["lane"]
            end_ms = entry.get("end_ms")
            ntype = entry.get("type")
        else:
            tm, lane = entry[0], entry[1]
            end_ms = entry[2] if len(entry) > 2 else None
            ntype = None
        
        if tm > SONG_DURATION_MS():
            continue
        
        key = (round(tm, 1), lane)
        if key not in seen:
            seen.add(key)
            n = {"time_ms": tm, "lane": lane}
            if end_ms is not None:
                n["end_ms"] = end_ms
            if ntype:
                n["type"] = ntype
            clean.append(n)

    # Filter by difficulty
    if difficulty == "Easy":
        out, lt = [], -9999.0
        for n in clean:
            if n["time_ms"] - lt >= BEAT_MS() * 0.9:
                out.append(n)
                lt = n["time_ms"]
        clean = out
    elif difficulty == "Normal":
        out, lt = [], -9999.0
        for n in clean:
            if n["time_ms"] - lt >= BEAT_MS() * 0.42:
                out.append(n)
                lt = n["time_ms"]
        clean = out
    
    return clean


def _default_beatmap():
    """Generate default beatmap pattern."""
    beat = BEAT_MS()
    half = beat / 2
    qtr = beat / 4
    eig = beat / 8
    raw = []

    def add(t, *ls):
        for l in ls:
            raw.append((t, l))

    # Intro
    t = beat * 4
    for lane in [0, 2, 1, 3, 2, 0, 3, 1, 0, 2, 1, 3]:
        add(t, lane)
        t += beat

    # Buildup
    t = beat * 16
    for i, lane in enumerate([0, 1, 2, 3, 2, 1, 0, 2, 1, 3, 0, 2, 3, 1, 2, 0, 1, 2, 3, 0]):
        add(t, lane)
        t += half if i >= 10 else beat

    # Drop 1
    t = beat * 35
    phrases = [
        [(0, [0]), (half, [2]), (beat, [1]), (beat + half, [3]),
         (beat * 2, [0, 2]), (beat * 2 + half, [1]), (beat * 3, [3]), (beat * 3 + half, [0, 2])],
        [(0, [1]), (qtr, [0]), (half, [2]), (half + qtr, [3]),
         (beat, [0, 1]), (beat + half, [2]), (beat * 2, [3]), (beat * 2 + qtr, [1]),
         (beat * 2 + half, [0]), (beat * 3, [2, 3]), (beat * 3 + half, [1])],
        [(0, [0, 1, 2, 3]), (half, [2]), (beat, [0, 3]), (beat + half, [1]),
         (beat * 2, [2, 3]), (beat * 2 + half, [0]), (beat * 3, [1, 3]), (beat * 3 + qtr, [0]),
         (beat * 3 + half, [2])],
        [(0, [0]), (eig, [1]), (eig * 2, [2]), (eig * 3, [3]),
         (beat, [3]), (beat + eig, [2]), (beat + eig * 2, [1]), (beat + eig * 3, [0]),
         (beat * 2, [0, 2]), (beat * 2 + half, [1, 3]), (beat * 3, [0, 1, 2, 3])],
        [(0, [2]), (half, [0]), (beat, [3]), (beat + half, [1]),
         (beat * 2, [0, 2]), (beat * 2 + qtr, [3]), (beat * 2 + half, [1]), (beat * 3, [0]),
         (beat * 3 + half, [2, 3])],
        [(0, [1, 3]), (qtr, [0]), (half, [2]), (beat, [0, 1]),
         (beat + half, [3]), (beat * 2, [2]), (beat * 2 + half, [0, 3]),
         (beat * 3, [1]), (beat * 3 + qtr, [2]), (beat * 3 + half, [0, 1, 2, 3])],
    ]
    for rep in range(16):
        for dt, ls in phrases[rep % len(phrases)]:
            add(t + dt, *ls)
        t += beat * 4

    # Break
    t = beat * 99
    for i, lane in enumerate(
            [0, 2, 1, 3, 0, 2, 3, 1, 2, 0, 3, 1, 0, 3, 2, 1, 0, 2, 1, 3, 2, 0, 1, 3, 0, 3, 1, 2]):
        add(t, lane)
        t += beat if i % 4 < 2 else half
    
    t2 = beat * 120
    rng0 = random.Random(99)
    for _ in range(12):
        ls = rng0.sample(range(4), 2)
        add(t2, *ls)
        t2 += beat

    # Drop 2
    t = beat * 145
    rng = random.Random(42)
    for _ in range(32):
        dens = [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0]
        for s in range(16):
            if dens[s]:
                n = 2 if s % 8 == 0 else 1
                add(t + eig * s, *rng.sample(range(4), n))
        t += beat * 2

    # Breakdown
    t = beat * 261
    for dt, ls in [
        (0, [0]), (half, [2]), (beat, [1]), (beat * 1.5, [3]), (beat * 2, [2]),
        (beat * 2.5, [0]), (beat * 3, [1, 3]), (beat * 3.5, [2]), (beat * 4, [0]),
        (beat * 4 + qtr, [1]), (beat * 4 + half, [2]), (beat * 4.75, [3]),
        (beat * 5, [0, 2]), (beat * 5 + half, [1]), (beat * 6, [3]),
        (beat * 6 + half, [0, 2]), (beat * 7, [1, 3]), (beat * 7 + qtr, [0]),
        (beat * 7 + half, [2]), (beat * 7.75, [1]), (beat * 8, [0]),
        (beat * 8 + half, [3]), (beat * 9, [1, 2]), (beat * 9 + half, [0]),
        (beat * 10, [3]), (beat * 10 + half, [1]), (beat * 11, [0, 2]),
        (beat * 11 + half, [3]), (beat * 12, [0, 1, 2, 3]), (beat * 12 + half, [2]),
        (beat * 13, [0]), (beat * 13 + half, [3]), (beat * 14, [1, 2]),
        (beat * 14 + half, [0]), (beat * 15, [3]), (beat * 15 + half, [1, 2]),
    ]:
        add(t + dt, *ls)

    # Final Drop
    t = beat * 319
    rng2 = random.Random(7)
    prev = []
    while t < SONG_DURATION_MS() - 1500:
        pool = [l for l in range(4) if l not in prev] or list(range(4))
        ls = rng2.sample(pool, min(rng2.choice([1, 1, 1, 2, 2, 3]), len(pool)))
        for l in ls:
            add(t, l)
        prev = ls
        t += rng2.choice([eig, eig, qtr, half])

    return raw


# ═══════════════════════════════════════════════════════════════════
#  CUSTOM SONGS
# ═══════════════════════════════════════════════════════════════════

_CUSTOM_SONGS_PATH = None


def load_custom_songs():
    """Load user-imported songs."""
    global _CUSTOM_SONGS_PATH
    _CUSTOM_SONGS_PATH = os.path.join(get_app_dir(), "custom_songs.json")
    
    try:
        with open(_CUSTOM_SONGS_PATH) as f:
            data = json.load(f)
        
        # Get built-in IDs
        built_in_ids = {s["id"] for s in SONGS}
        
        for s in data:
            if s["id"] not in built_in_ids:
                if isinstance(s.get("color"), list):
                    s["color"] = tuple(s["color"])
                SONGS.append(s)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Could not load custom songs: {e}")


def save_custom_songs():
    """Save custom songs to JSON."""
    built_in_ids = {s["id"] for s in SONGS[:17]}  # First 17 are built-in
    
    custom = []
    for s in SONGS:
        if s["id"] not in built_in_ids:
            entry = dict(s)
            if isinstance(entry.get("color"), tuple):
                entry["color"] = list(entry["color"])
            custom.append(entry)
    
    try:
        with open(_CUSTOM_SONGS_PATH, "w") as f:
            json.dump(custom, f, indent=2)
    except Exception as e:
        print(f"Could not save custom songs: {e}")
