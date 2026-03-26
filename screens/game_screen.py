"""
Game screen - Main gameplay interface for Rhythmix Mobile.
Handles note rendering, touch input, scoring, and audio playback.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty, BooleanProperty

from utils.config import (
    NUM_LANES, LANE_COLORS, WHITE, COL_PERFECT, COL_GOOD, COL_OK, COL_MISS,
    PERFECT_WIN, GOOD_WIN, OK_WIN, DIFF_SPEEDS, ACTIVE_MODS,
    SONG_DURATION_MS, SONG_FILE, find_song_file, get_setting,
    update_best, _ACTIVE_SONG_ID
)


class NoteData:
    """Simple note data class."""
    def __init__(self, lane, time_ms, speed):
        self.lane = lane
        self.time_ms = time_ms
        self.speed = speed
        self.hit = False
        self.missed = False
    
    def y(self, elapsed_ms, hit_y):
        """Calculate Y position based on elapsed time."""
        return hit_y + (elapsed_ms - self.time_ms) * self.speed / 1000


class HoldNoteData:
    """Hold note data class."""
    def __init__(self, lane, time_ms, end_ms, speed):
        self.lane = lane
        self.time_ms = time_ms
        self.end_ms = end_ms
        self.speed = speed
        self.hit = False
        self.missed = False
        self.held = False
        self.released = False
        self.tail_hit = False
    
    def y(self, elapsed_ms, hit_y):
        """Calculate head Y position."""
        return hit_y + (elapsed_ms - self.time_ms) * self.speed / 1000
    
    def tail_y(self, elapsed_ms, hit_y):
        """Calculate tail Y position."""
        return hit_y + (elapsed_ms - self.end_ms) * self.speed / 1000
    
    @property
    def done(self):
        return self.missed or self.released


class GameScreen(Screen):
    """Main gameplay screen."""
    
    score = NumericProperty(0)
    combo = NumericProperty(0)
    elapsed_ms = NumericProperty(0)
    is_playing = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficulty = 'Normal'
        self.notes = []
        self.hold_notes = []
        self.max_combo = 0
        self.perfect_count = 0
        self.good_count = 0
        self.ok_count = 0
        self.miss_count = 0
        self.lane_holds = [False] * NUM_LANES
        self.sound = None
        self.hit_y = 0
        self.lane_width = 0
        
        self.build_ui()
    
    def build_ui(self):
        """Build the game UI."""
        # Main layout
        self.layout = RelativeLayout()
        
        # Game canvas for drawing notes
        self.game_canvas = Widget(size_hint=(1, 1))
        self.layout.add_widget(self.game_canvas)
        
        # Calculate dimensions
        self.lane_width = Window.width / NUM_LANES
        self.hit_y = Window.height * 0.82
        
        # Lane touch areas (invisible buttons)
        self.lane_widgets = []
        for i in range(NUM_LANES):
            lane = Button(
                background_color=LANE_COLORS[i] + (0.05,),
                background_normal='',
                size_hint=(None, 1),
                width=self.lane_width,
                pos=(i * self.lane_width, 0)
            )
            lane.bind(on_press=lambda inst, lane=i: self.on_lane_press(lane))
            lane.bind(on_release=lambda inst, lane=i: self.on_lane_release(lane))
            self.lane_widgets.append(lane)
            self.layout.add_widget(lane)
        
        # UI Overlay
        ui_overlay = FloatLayout(size_hint=(1, 1))
        
        # Score display (top right)
        self.score_label = Label(
            text='0',
            font_size=sp(32),
            bold=True,
            pos_hint={'right': 0.97, 'top': 0.97},
            size_hint=(0.25, 0.1),
            halign='right',
            valign='middle'
        )
        ui_overlay.add_widget(self.score_label)
        
        # Combo display (center, below hit line)
        self.combo_label = Label(
            text='',
            font_size=sp(44),
            bold=True,
            color=(1, 0.86, 0, 1),  # Gold
            pos_hint={'center_x': 0.5, 'y': 0.05},
            size_hint=(0.3, 0.12)
        )
        ui_overlay.add_widget(self.combo_label)
        
        # Judgment text (center)
        self.judgment_label = Label(
            text='',
            font_size=sp(26),
            bold=True,
            pos_hint={'center_x': 0.5, 'top': 0.75},
            size_hint=(0.4, 0.08)
        )
        ui_overlay.add_widget(self.judgment_label)
        
        # Progress bar (top)
        self.progress_bar = Widget(
            size_hint=(1, 0.01),
            pos_hint={'x': 0, 'top': 1}
        )
        with self.progress_bar.canvas:
            Color(0.3, 0.3, 0.4, 1)
            self.progress_bg = Rectangle(pos=(0, Window.height - dp(6)), size=(Window.width, dp(6)))
            Color(0, 0.78, 1, 1)
            self.progress_fg = Rectangle(pos=(0, Window.height - dp(6)), size=(0, dp(6)))
        ui_overlay.add_widget(self.progress_bar)
        
        # Quit button (top left)
        quit_btn = Button(
            text='✕',
            font_size=sp(20),
            size_hint=(0.08, 0.06),
            pos_hint={'x': 0.02, 'top': 0.95},
            background_color=(0.8, 0.25, 0.25, 0.8),
            background_normal=''
        )
        quit_btn.bind(on_press=self.on_quit)
        ui_overlay.add_widget(quit_btn)
        
        # Song title
        self.title_label = Label(
            text='',
            font_size=sp(14),
            color=(0.8, 0.8, 0.9, 0.7),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(0.5, 0.05)
        )
        ui_overlay.add_widget(self.title_label)
        
        self.layout.add_widget(ui_overlay)
        self.add_widget(self.layout)
        
        # Bind to window resize
        Window.bind(on_resize=self.on_window_resize)
        
        # Schedule update
        Clock.schedule_interval(self.update, 1 / 60)
    
    def on_window_resize(self, instance, width, height):
        """Handle window resize."""
        self.lane_width = width / NUM_LANES
        self.hit_y = height * 0.82
        
        # Update lane positions
        for i, lane in enumerate(self.lane_widgets):
            lane.width = self.lane_width
            lane.pos = (i * self.lane_width, 0)
        
        # Update progress bar
        self.progress_bg.pos = (0, height - dp(6))
        self.progress_bg.size = (width, dp(6))
        self.progress_fg.pos = (0, height - dp(6))
    
    def start_game(self, difficulty):
        """Initialize and start a new game."""
        from utils.config import build_beatmap, active_song
        
        self.difficulty = difficulty
        self.notes = []
        self.hold_notes = []
        self.elapsed_ms = 0
        self.is_playing = True
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.perfect_count = 0
        self.good_count = 0
        self.ok_count = 0
        self.miss_count = 0
        self.lane_holds = [False] * NUM_LANES
        
        # Set title
        song = active_song()
        self.title_label.text = f"{song['title']} - {song['artist']}"
        
        # Load beatmap
        beatmap_data = build_beatmap(difficulty)
        speed = DIFF_SPEEDS.get(difficulty, 460)
        speed *= get_setting('scroll_speed', 1.0)
        
        if ACTIVE_MODS.get('double_speed'):
            speed *= 2
        
        for data in beatmap_data:
            if 'end_ms' in data:
                self.hold_notes.append(HoldNoteData(
                    data['lane'], data['time_ms'], data['end_ms'], speed
                ))
            else:
                self.notes.append(NoteData(
                    data['lane'], data['time_ms'], speed
                ))
        
        # Load and play music
        song_path = find_song_file(SONG_FILE())
        if song_path:
            try:
                self.sound = SoundLoader.load(song_path)
                if self.sound:
                    self.sound.volume = get_setting('music_vol', 0.85)
                    self.sound.play()
            except Exception as e:
                print(f"Could not load sound: {e}")
        
        self.update_score_display()
    
    def on_lane_press(self, lane):
        """Handle lane touch/press."""
        if not self.is_playing:
            return
        
        self.lane_holds[lane] = True
        
        # Apply audio offset
        audio_offset = get_setting('audio_offset', 0)
        effective_time = self.elapsed_ms - audio_offset
        
        # Check for note hits
        hit_window = OK_WIN
        hit_y = self.hit_y
        
        # Check regular notes
        for note in self.notes:
            if note.hit or note.missed:
                continue
            if note.lane != lane:
                continue
            
            dist = abs(note.time_ms - effective_time)
            if dist <= hit_window:
                self.register_hit(dist)
                note.hit = True
                break
        
        # Check hold note heads
        for note in self.hold_notes:
            if note.hit or note.missed:
                continue
            if note.lane != lane:
                continue
            
            dist = abs(note.time_ms - effective_time)
            if dist <= hit_window:
                note.hit = True
                note.held = True
                self.register_hit(dist)
                break
        
        # Visual feedback
        self.lane_widgets[lane].background_color = LANE_COLORS[lane] + (0.35,)
    
    def on_lane_release(self, lane):
        """Handle lane release."""
        if not self.is_playing:
            return
        
        self.lane_holds[lane] = False
        
        # Check hold note releases
        audio_offset = get_setting('audio_offset', 0)
        effective_time = self.elapsed_ms - audio_offset
        
        for note in self.hold_notes:
            if not note.hit or note.released or note.missed:
                continue
            if note.lane != lane:
                continue
            
            dist = abs(note.end_ms - effective_time)
            if dist <= OK_WIN:
                note.tail_hit = True
                note.released = True
                note.held = False
                self.add_score(50)
        
        # Reset lane color
        self.lane_widgets[lane].background_color = LANE_COLORS[lane] + (0.05,)
    
    def register_hit(self, dist_ms):
        """Register a successful hit."""
        if dist_ms <= PERFECT_WIN:
            self.perfect_count += 1
            self.add_score(100)
            self.show_judgment('PERFECT', COL_PERFECT)
        elif dist_ms <= GOOD_WIN:
            self.good_count += 1
            self.add_score(50)
            self.show_judgment('GOOD', COL_GOOD)
        else:
            self.ok_count += 1
            self.add_score(25)
            self.show_judgment('OK', COL_OK)
        
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        self.update_score_display()
    
    def register_miss(self):
        """Register a miss."""
        self.miss_count += 1
        self.combo = 0
        self.show_judgment('MISS', COL_MISS)
        self.update_score_display()
    
    def add_score(self, points):
        """Add points to score with combo multiplier."""
        multiplier = 1 + (self.combo // 10) * 0.1
        self.score += int(points * multiplier)
    
    def show_judgment(self, text, color):
        """Show judgment text."""
        self.judgment_label.text = text
        self.judgment_label.color = color + (1,)
        
        # Clear after delay
        def clear_judgment(dt):
            self.judgment_label.text = ''
        
        Clock.unschedule(clear_judgment)
        Clock.schedule_once(clear_judgment, 0.4)
    
    def update_score_display(self):
        """Update the score display."""
        self.score_label.text = f'{self.score:,}'
        if self.combo > 0:
            self.combo_label.text = f'{self.combo}x'
        else:
            self.combo_label.text = ''
    
    def update(self, dt):
        """Main game update loop."""
        if not self.is_playing:
            return
        
        # Update elapsed time
        self.elapsed_ms += dt * 1000
        audio_offset = get_setting('audio_offset', 0)
        effective_time = self.elapsed_ms - audio_offset
        
        # Update progress bar
        progress = min(1.0, self.elapsed_ms / max(1, SONG_DURATION_MS()))
        self.progress_fg.size = (Window.width * progress, dp(6))
        
        # Check for missed notes
        for note in self.notes:
            if note.hit or note.missed:
                continue
            if note.time_ms < effective_time - OK_WIN:
                note.missed = True
                self.register_miss()
        
        # Check for missed hold note heads
        for note in self.hold_notes:
            if not note.hit and not note.missed:
                if note.time_ms < effective_time - OK_WIN:
                    note.missed = True
                    self.register_miss()
            
            # Auto-release hold notes that have passed
            if note.hit and note.held and not note.released:
                if effective_time > note.end_ms + OK_WIN:
                    note.released = True
                    note.held = False
        
        # Check song end
        if self.elapsed_ms >= SONG_DURATION_MS():
            self.end_game()
        
        # Redraw canvas
        self.redraw_canvas()
    
    def redraw_canvas(self):
        """Redraw the game canvas."""
        canvas = self.game_canvas.canvas
        canvas.clear()
        
        hit_y = self.hit_y
        lane_width = self.lane_width
        
        # Draw lane dividers
        with canvas:
            Color(0.3, 0.3, 0.4, 0.5)
            for i in range(NUM_LANES + 1):
                x = i * lane_width
                Line(points=[x, 0, x, Window.height], width=1)
        
        # Draw hit line
        with canvas:
            Color(*WHITE)
            Line(points=[0, hit_y, Window.width, hit_y], width=3)
            # Hit line glow
            Color(*WHITE[:3], 0.3)
            Line(points=[0, hit_y - 2, Window.width, hit_y - 2], width=6)
        
        audio_offset = get_setting('audio_offset', 0)
        effective_time = self.elapsed_ms - audio_offset
        
        # Draw regular notes
        for note in self.notes:
            if note.hit or note.missed:
                continue
            
            y = note.y(effective_time, hit_y)
            
            # Skip if off-screen
            if y < -dp(50) or y > Window.height + dp(50):
                continue
            
            # Hidden mod: fade out near hit line
            alpha = self.get_note_alpha(y, hit_y)
            if alpha <= 0:
                continue
            
            x = note.lane * lane_width + lane_width * 0.1
            w = lane_width * 0.8
            h = dp(28)
            
            with canvas:
                c = LANE_COLORS[note.lane]
                Color(c[0], c[1], c[2], alpha)
                RoundedRectangle(
                    pos=(x, y - h / 2),
                    size=(w, h),
                    radius=[dp(8)]
                )
                # Shine effect
                Color(min(1, c[0] + 0.3), min(1, c[1] + 0.3), min(1, c[2] + 0.3), alpha)
                RoundedRectangle(
                    pos=(x + dp(4), y - h / 2 + dp(3)),
                    size=(w - dp(8), dp(6)),
                    radius=[dp(3)]
                )
        
        # Draw hold notes
        for note in self.hold_notes:
            if note.missed:
                continue
            
            head_y = note.y(effective_time, hit_y)
            tail_y = note.tail_y(effective_time, hit_y)
            
            # Clamp if being held
            if note.hit and note.held and not note.released:
                tail_y = min(tail_y, hit_y - dp(15))
            
            x = note.lane * lane_width + lane_width * 0.25
            w = lane_width * 0.5
            
            # Draw body if visible
            body_top = max(-dp(50), tail_y)
            body_bot = min(Window.height + dp(50), head_y)
            
            if body_bot > body_top:
                with canvas:
                    c = LANE_COLORS[note.lane]
                    # Body
                    Color(c[0], c[1], c[2], 0.5)
                    Rectangle(pos=(x, body_top), size=(w, body_bot - body_top))
                    # Border
                    Color(c[0], c[1], c[2], 0.8)
                    Line(rectangle=(x, body_top, w, body_bot - body_top), width=1)
            
            # Draw head if not hit
            if not note.hit:
                if -dp(50) < head_y < Window.height + dp(50):
                    with canvas:
                        c = LANE_COLORS[note.lane]
                        h = dp(28)
                        x_head = note.lane * lane_width + lane_width * 0.1
                        w_head = lane_width * 0.8
                        Color(*c)
                        RoundedRectangle(
                            pos=(x_head, head_y - h / 2),
                            size=(w_head, h),
                            radius=[dp(8)]
                        )
            
            # Draw tail if not released
            if not note.released:
                ty = min(tail_y, hit_y - dp(15))
                if -dp(50) < ty < Window.height + dp(50):
                    with canvas:
                        c = LANE_COLORS[note.lane]
                        h = dp(20)
                        x_tail = note.lane * lane_width + lane_width * 0.15
                        w_tail = lane_width * 0.7
                        c_dim = (max(0, c[0] - 0.2), max(0, c[1] - 0.2), max(0, c[2] - 0.2))
                        Color(*c_dim)
                        RoundedRectangle(
                            pos=(x_tail, ty - h / 2),
                            size=(w_tail, h),
                            radius=[dp(5)]
                        )
    
    def get_note_alpha(self, y, hit_y):
        """Calculate note visibility based on mods."""
        dist = hit_y - y  # Distance from hit line
        
        if ACTIVE_MODS.get('hidden'):
            # Fade out as note approaches hit line
            fade_start = dp(200)
            fade_end = dp(80)
            if dist <= fade_end:
                return 0
            if dist >= fade_start:
                return 1
            return (dist - fade_end) / (fade_start - fade_end)
        
        if ACTIVE_MODS.get('sudden'):
            # Notes only appear close to hit line
            appear_dist = dp(150)
            fade_in = dp(60)
            if dist > appear_dist:
                return 0
            if dist <= fade_in:
                return 1
            return 1 - (dist - fade_in) / (appear_dist - fade_in)
        
        return 1
    
    def end_game(self):
        """End the game and show results."""
        self.is_playing = False
        
        if self.sound:
            self.sound.stop()
            self.sound = None
        
        # Calculate grade
        total_notes = len(self.notes) + len(self.hold_notes)
        hit_notes = self.perfect_count + self.good_count + self.ok_count
        accuracy = hit_notes / total_notes if total_notes > 0 else 0
        
        if accuracy >= 0.98:
            grade = 'S'
        elif accuracy >= 0.95:
            grade = 'A'
        elif accuracy >= 0.90:
            grade = 'B'
        elif accuracy >= 0.80:
            grade = 'C'
        else:
            grade = 'D'
        
        # Save score
        update_best(_ACTIVE_SONG_ID, self.difficulty, self.score, grade,
                    accuracy * 100, self.max_combo)
        
        # Show results
        results_screen = self.manager.get_screen('results')
        results_screen.set_results(
            self.score, grade, accuracy * 100, self.max_combo,
            self.perfect_count, self.good_count, self.ok_count, self.miss_count
        )
        
        self.manager.transition.direction = 'left'
        self.manager.current = 'results'
    
    def on_quit(self, instance):
        """Quit to menu."""
        self.is_playing = False
        
        if self.sound:
            self.sound.stop()
            self.sound = None
        
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def on_pause(self):
        """Handle app pause."""
        if self.is_playing and self.sound:
            self.sound.stop()
    
    def on_resume(self):
        """Handle app resume."""
        pass  # Could restart sound if needed
