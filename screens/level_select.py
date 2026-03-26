"""
Level select screen for choosing songs and difficulty.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, NumericProperty

from utils.config import (
    SONGS, LANE_COLORS, WHITE, GRAY,
    set_active_song, get_best, active_song
)


class LevelSelectScreen(Screen):
    """Screen for selecting song and difficulty."""
    
    difficulty = StringProperty('Normal')
    selected_index = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_index = 0
        self.difficulty = 'Normal'
        self.build_ui()
    
    def build_ui(self):
        """Build the level select UI."""
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(15),
            spacing=dp(10)
        )
        
        # Header
        header = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            spacing=dp(10)
        )
        
        back_btn = Button(
            text='← BACK',
            font_size=sp(16),
            size_hint=(0.25, 1),
            background_color=(0.4, 0.4, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        
        title = Label(
            text='SELECT SONG',
            font_size=sp(24),
            bold=True,
            size_hint=(0.5, 1)
        )
        header.add_widget(title)
        
        # Spacer for balance
        header.add_widget(Label(size_hint=(0.25, 1)))
        
        layout.add_widget(header)
        
        # Song info display
        self.info_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            padding=dp(10)
        )
        self.update_info_display()
        layout.add_widget(self.info_box)
        
        # Song list
        scroll = ScrollView(size_hint=(1, 0.45))
        self.song_list = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint=(1, None)
        )
        self.song_list.bind(
            minimum_height=self.song_list.setter('height')
        )
        
        for i, song in enumerate(SONGS):
            btn = Button(
                text=f"{song['title']}",
                font_size=sp(16),
                halign='center',
                background_color=song['color'] + (0.3,) if i == self.selected_index else (0.12, 0.12, 0.18, 1),
                background_normal='',
                size_hint=(1, None),
                height=dp(60)
            )
            btn.bind(on_press=lambda inst, idx=i: self.select_song(idx))
            self.song_list.add_widget(btn)
        
        scroll.add_widget(self.song_list)
        layout.add_widget(scroll)
        
        # Difficulty selector
        diff_layout = GridLayout(
            cols=4,
            spacing=dp(10),
            size_hint=(1, 0.12)
        )
        
        diff_colors = {
            'Easy': (0.39, 0.86, 1),     # Blue
            'Normal': (0.63, 1, 0.55),   # Green
            'Hard': (1, 0.31, 0.31),     # Red
            'Practice': (0.8, 0.8, 0.9) # Gray
        }
        
        for diff in ['Easy', 'Normal', 'Hard', 'Practice']:
            is_selected = diff == self.difficulty
            btn = Button(
                text=diff,
                font_size=sp(16),
                bold=is_selected,
                background_color=diff_colors[diff] + (1,) if is_selected else (0.25, 0.25, 0.35, 1),
                background_normal=''
            )
            btn.bind(on_press=lambda inst, d=diff: self.set_difficulty(d))
            diff_layout.add_widget(btn)
        
        layout.add_widget(diff_layout)
        
        # Start button
        start_btn = Button(
            text='START GAME',
            font_size=sp(24),
            bold=True,
            background_color=(0, 0.78, 1, 1),
            background_normal='',
            size_hint=(1, 0.12)
        )
        start_btn.bind(on_press=self.on_start)
        layout.add_widget(start_btn)
        
        self.add_widget(layout)
    
    def update_info_display(self):
        """Update the song info display."""
        self.info_box.clear_widgets()
        
        song = SONGS[self.selected_index]
        set_active_song(song['id'])
        
        # Title
        title = Label(
            text=song['title'],
            font_size=sp(22),
            bold=True,
            color=song['color'] + (1,),
            size_hint=(1, 0.4)
        )
        self.info_box.add_widget(title)
        
        # Artist
        artist = Label(
            text=f"by {song['artist']}",
            font_size=sp(14),
            color=(0.7, 0.7, 0.8, 1),
            size_hint=(1, 0.3)
        )
        self.info_box.add_widget(artist)
        
        # Best score for selected difficulty
        best = get_best(song['id'], self.difficulty)
        if best:
            best_text = f"Best: {best['grade']} | {best['score']} pts | {best['combo']}x combo"
        else:
            best_text = "No record yet"
        
        best_label = Label(
            text=best_text,
            font_size=sp(13),
            color=(0.9, 0.78, 0, 1),
            size_hint=(1, 0.3)
        )
        self.info_box.add_widget(best_label)
    
    def select_song(self, index):
        """Select a song by index."""
        self.selected_index = index
        
        # Update list button colors
        for i, btn in enumerate(self.song_list.children):
            # Reverse order because BoxLayout adds at bottom
            idx = len(SONGS) - 1 - i
            song = SONGS[idx]
            btn.background_color = song['color'] + (0.3,) if idx == index else (0.12, 0.12, 0.18, 1)
        
        self.update_info_display()
    
    def set_difficulty(self, diff):
        """Set the difficulty level."""
        self.difficulty = diff
        self.update_info_display()
        self.build_ui()  # Rebuild to update button colors
    
    def on_back(self, instance):
        """Go back to main menu."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def on_start(self, instance):
        """Start the game."""
        # Set active song
        set_active_song(SONGS[self.selected_index]['id'])
        
        # Start game
        game_screen = self.manager.get_screen('game')
        game_screen.start_game(self.difficulty)
        
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'
