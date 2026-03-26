"""
Main menu screen for Rhythmix Mobile.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import ListProperty

from utils.config import BG_COLOR, WHITE


class MenuScreen(Screen):
    """Main menu with play, settings, and quit options."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the menu UI."""
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(30),
            spacing=dp(20)
        )
        
        # Spacer
        layout.add_widget(Label(size_hint=(1, 0.15)))
        
        # Title
        title = Label(
            text='RHYTHMIX',
            font_size=sp(56),
            bold=True,
            color=(1, 0.86, 0, 1),  # Gold
            size_hint=(1, 0.2)
        )
        layout.add_widget(title)
        
        # Subtitle
        subtitle = Label(
            text='Hit the beat. Feel the rhythm.',
            font_size=sp(18),
            color=(0.7, 0.7, 0.85, 1),
            size_hint=(1, 0.08)
        )
        layout.add_widget(subtitle)
        
        # Spacer
        layout.add_widget(Label(size_hint=(1, 0.1)))
        
        # Buttons container
        btn_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint=(0.8, 0.4),
            pos_hint={'center_x': 0.5}
        )
        
        # Play button
        play_btn = Button(
            text='PLAY',
            font_size=sp(26),
            bold=True,
            background_color=(0, 0.78, 1, 1),  # Cyan
            background_normal='',
            size_hint=(1, 1)
        )
        play_btn.bind(on_press=self.on_play)
        btn_layout.add_widget(play_btn)
        
        # Settings button
        settings_btn = Button(
            text='SETTINGS',
            font_size=sp(22),
            background_color=(0.5, 0.5, 0.6, 1),
            background_normal='',
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5}
        )
        settings_btn.bind(on_press=self.on_settings)
        btn_layout.add_widget(settings_btn)
        
        # Quit button
        quit_btn = Button(
            text='QUIT',
            font_size=sp(22),
            background_color=(0.8, 0.25, 0.25, 1),
            background_normal='',
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5}
        )
        quit_btn.bind(on_press=self.on_quit)
        btn_layout.add_widget(quit_btn)
        
        layout.add_widget(btn_layout)
        
        # Bottom spacer
        layout.add_widget(Label(size_hint=(1, 0.15)))
        
        self.add_widget(layout)
    
    def on_play(self, instance):
        """Navigate to level select."""
        self.manager.transition.direction = 'left'
        self.manager.current = 'level_select'
    
    def on_settings(self, instance):
        """Navigate to settings."""
        self.manager.transition.direction = 'left'
        self.manager.current = 'settings'
    
    def on_quit(self, instance):
        """Exit the app."""
        from kivy.app import App
        App.get_running_app().stop()
