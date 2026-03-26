"""
Results screen for displaying game scores and grades.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty, StringProperty

from utils.config import WHITE, COL_PERFECT, COL_GOOD, COL_OK, COL_MISS


class ResultsScreen(Screen):
    """Screen displaying game results and statistics."""
    
    score = NumericProperty(0)
    grade = StringProperty('D')
    accuracy = NumericProperty(0)
    max_combo = NumericProperty(0)
    perfect_count = NumericProperty(0)
    good_count = NumericProperty(0)
    ok_count = NumericProperty(0)
    miss_count = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the results UI."""
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(15)
        )
        
        # Header
        header = Label(
            text='RESULTS',
            font_size=sp(40),
            bold=True,
            color=(1, 0.86, 0, 1),  # Gold
            size_hint=(1, 0.12)
        )
        layout.add_widget(header)
        
        # Grade display
        self.grade_label = Label(
            text=self.grade,
            font_size=sp(90),
            bold=True,
            size_hint=(1, 0.25)
        )
        layout.add_widget(self.grade_label)
        
        # Score display
        self.score_label = Label(
            text=f'{self.score}',
            font_size=sp(32),
            bold=True,
            color=WHITE + (1,),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.score_label)
        
        # Stats grid
        stats_layout = GridLayout(
            cols=2,
            spacing=(dp(20), dp(10)),
            padding=dp(20),
            size_hint=(1, 0.35)
        )
        
        # Create stat labels
        self.accuracy_label = self.create_stat_label('Accuracy', f'{self.accuracy:.1f}%')
        self.combo_label = self.create_stat_label('Max Combo', str(self.max_combo))
        self.perfect_label = self.create_stat_label('Perfect', str(self.perfect_count), COL_PERFECT)
        self.good_label = self.create_stat_label('Good', str(self.good_count), COL_GOOD)
        self.ok_label = self.create_stat_label('OK', str(self.ok_count), COL_OK)
        self.miss_label = self.create_stat_label('Miss', str(self.miss_count), COL_MISS)
        
        stats_layout.add_widget(self.accuracy_label)
        stats_layout.add_widget(self.combo_label)
        stats_layout.add_widget(self.perfect_label)
        stats_layout.add_widget(self.good_label)
        stats_layout.add_widget(self.ok_label)
        stats_layout.add_widget(self.miss_label)
        
        layout.add_widget(stats_layout)
        
        # Buttons
        btn_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(15),
            size_hint=(1, 0.12)
        )
        
        retry_btn = Button(
            text='RETRY',
            font_size=sp(20),
            bold=True,
            background_color=(0, 0.78, 1, 1),
            background_normal=''
        )
        retry_btn.bind(on_press=self.on_retry)
        btn_layout.add_widget(retry_btn)
        
        menu_btn = Button(
            text='MENU',
            font_size=sp(20),
            background_color=(0.4, 0.4, 0.5, 1),
            background_normal=''
        )
        menu_btn.bind(on_press=self.on_menu)
        btn_layout.add_widget(menu_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def create_stat_label(self, name, value, color=None):
        """Create a stat label widget."""
        text_color = color + (1,) if color else WHITE + (1,)
        return Label(
            text=f'{name}: {value}',
            font_size=sp(17),
            color=text_color,
            halign='center'
        )
    
    def set_results(self, score, grade, accuracy, max_combo,
                    perfect, good, ok, miss):
        """Set the results data."""
        self.score = score
        self.grade = grade
        self.accuracy = accuracy
        self.max_combo = max_combo
        self.perfect_count = perfect
        self.good_count = good
        self.ok_count = ok
        self.miss_count = miss
        
        # Update display
        self.update_display()
    
    def update_display(self):
        """Update the display with current values."""
        # Grade with color
        grade_colors = {
            'S': (1, 0.86, 0, 1),      # Gold
            'A': (0.39, 0.86, 1, 1),   # Blue
            'B': (0.63, 1, 0.55, 1),   # Green
            'C': (1, 0.78, 0, 1),      # Yellow
            'D': (1, 0.31, 0.31, 1),   # Red
        }
        self.grade_label.text = self.grade
        self.grade_label.color = grade_colors.get(self.grade, (1, 1, 1, 1))
        
        # Score
        self.score_label.text = f'{self.score:,}'
        
        # Stats
        self.accuracy_label.text = f'Accuracy: {self.accuracy:.1f}%'
        self.combo_label.text = f'Max Combo: {self.max_combo}'
        self.perfect_label.text = f'Perfect: {self.perfect_count}'
        self.good_label.text = f'Good: {self.good_count}'
        self.ok_label.text = f'OK: {self.ok_count}'
        self.miss_label.text = f'Miss: {self.miss_count}'
    
    def on_enter(self):
        """Called when screen is entered."""
        self.update_display()
    
    def on_retry(self, instance):
        """Retry the same song."""
        game_screen = self.manager.get_screen('game')
        game_screen.start_game(game_screen.difficulty)
        self.manager.transition.direction = 'right'
        self.manager.current = 'game'
    
    def on_menu(self, instance):
        """Return to main menu."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
