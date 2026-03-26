"""
Settings screen for Rhythmix Mobile.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp, sp

from utils.config import (
    save_settings, get_setting, set_setting, WHITE
)


class SettingsScreen(Screen):
    """Screen for adjusting game settings."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        """Build the settings UI."""
        layout = BoxLayout(
            orientation='vertical',
            padding=dp(25),
            spacing=dp(20)
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
            size_hint=(0.3, 1),
            background_color=(0.4, 0.4, 0.5, 1),
            background_normal=''
        )
        back_btn.bind(on_press=self.on_back)
        header.add_widget(back_btn)
        
        title = Label(
            text='SETTINGS',
            font_size=sp(28),
            bold=True,
            size_hint=(0.7, 1)
        )
        header.add_widget(title)
        
        layout.add_widget(header)
        
        # Settings container
        settings_box = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(1, 0.7),
            padding=dp(20)
        )
        
        # Music volume
        vol_layout = BoxLayout(size_hint=(1, 0.2))
        vol_layout.add_widget(Label(
            text='Music Volume',
            font_size=sp(18),
            size_hint=(0.5, 1),
            halign='left'
        ))
        self.music_vol_btn = Button(
            text=f'{int(get_setting("music_vol", 0.85) * 100)}%',
            font_size=sp(18),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.3, 0.4, 1),
            background_normal=''
        )
        self.music_vol_btn.bind(on_press=self.cycle_music_vol)
        vol_layout.add_widget(self.music_vol_btn)
        settings_box.add_widget(vol_layout)
        
        # SFX volume
        sfx_layout = BoxLayout(size_hint=(1, 0.2))
        sfx_layout.add_widget(Label(
            text='SFX Volume',
            font_size=sp(18),
            size_hint=(0.5, 1),
            halign='left'
        ))
        self.sfx_vol_btn = Button(
            text=f'{int(get_setting("sfx_vol", 0.3) * 100)}%',
            font_size=sp(18),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.3, 0.4, 1),
            background_normal=''
        )
        self.sfx_vol_btn.bind(on_press=self.cycle_sfx_vol)
        sfx_layout.add_widget(self.sfx_vol_btn)
        settings_box.add_widget(sfx_layout)
        
        # Audio offset
        offset_layout = BoxLayout(size_hint=(1, 0.2))
        offset_layout.add_widget(Label(
            text='Audio Offset (ms)',
            font_size=sp(18),
            size_hint=(0.5, 1),
            halign='left'
        ))
        self.offset_btn = Button(
            text=f'{get_setting("audio_offset", 0)} ms',
            font_size=sp(18),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.3, 0.4, 1),
            background_normal=''
        )
        self.offset_btn.bind(on_press=self.cycle_offset)
        offset_layout.add_widget(self.offset_btn)
        settings_box.add_widget(offset_layout)
        
        # Scroll speed
        speed_layout = BoxLayout(size_hint=(1, 0.2))
        speed_layout.add_widget(Label(
            text='Scroll Speed',
            font_size=sp(18),
            size_hint=(0.5, 1),
            halign='left'
        ))
        self.speed_btn = Button(
            text=f'{get_setting("scroll_speed", 1.0):.1f}x',
            font_size=sp(18),
            size_hint=(0.5, 1),
            background_color=(0.3, 0.3, 0.4, 1),
            background_normal=''
        )
        self.speed_btn.bind(on_press=self.cycle_speed)
        speed_layout.add_widget(self.speed_btn)
        settings_box.add_widget(speed_layout)
        
        layout.add_widget(settings_box)
        
        # Save button
        save_btn = Button(
            text='SAVE SETTINGS',
            font_size=sp(22),
            bold=True,
            background_color=(0, 0.78, 1, 1),
            background_normal='',
            size_hint=(1, 0.12)
        )
        save_btn.bind(on_press=self.save)
        layout.add_widget(save_btn)
        
        # Spacer
        layout.add_widget(Label(size_hint=(1, 0.1)))
        
        self.add_widget(layout)
    
    def cycle_music_vol(self, instance):
        """Cycle through volume levels."""
        vols = [0, 0.25, 0.5, 0.75, 1.0]
        current = get_setting('music_vol', 0.85)
        idx = vols.index(current) if current in vols else 0
        new_vol = vols[(idx + 1) % len(vols)]
        set_setting('music_vol', new_vol)
        self.music_vol_btn.text = f'{int(new_vol * 100)}%'
    
    def cycle_sfx_vol(self, instance):
        """Cycle through SFX volume levels."""
        vols = [0, 0.25, 0.5, 0.75, 1.0]
        current = get_setting('sfx_vol', 0.3)
        idx = vols.index(current) if current in vols else 0
        new_vol = vols[(idx + 1) % len(vols)]
        set_setting('sfx_vol', new_vol)
        self.sfx_vol_btn.text = f'{int(new_vol * 100)}%'
    
    def cycle_offset(self, instance):
        """Cycle through audio offset values."""
        offsets = [-200, -150, -100, -50, 0, 50, 100, 150, 200]
        current = get_setting('audio_offset', 0)
        idx = offsets.index(current) if current in offsets else 4
        new_offset = offsets[(idx + 1) % len(offsets)]
        set_setting('audio_offset', new_offset)
        self.offset_btn.text = f'{new_offset} ms'
    
    def cycle_speed(self, instance):
        """Cycle through scroll speed values."""
        speeds = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
        current = get_setting('scroll_speed', 1.0)
        idx = speeds.index(current) if current in speeds else 2
        new_speed = speeds[(idx + 1) % len(speeds)]
        set_setting('scroll_speed', new_speed)
        self.speed_btn.text = f'{new_speed:.1f}x'
    
    def save(self, instance):
        """Save settings and return to menu."""
        save_settings()
        self.on_back(instance)
    
    def on_back(self, instance):
        """Return to main menu."""
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
