"""
Lane button widget for touch input handling.
Provides a touch-responsive area for each game lane.
"""

from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


class LaneButton(Button):
    """
    Extended button widget for game lanes.
    Provides visual feedback and touch handling for gameplay.
    """
    
    def __init__(self, lane_index, color, **kwargs):
        super().__init__(**kwargs)
        self.lane_index = lane_index
        self.base_color = color
        self.is_pressed = False
        
        # Configure button appearance
        self.background_normal = ''
        self.background_color = color + (0.05,)
        
        # Add glow effect canvas instructions
        with self.canvas.before:
            self.glow_color = Color(*color, 0)
            self.glow_rect = Rectangle(pos=self.pos, size=self.size)
        
        # Bind to position/size changes
        self.bind(pos=self.update_glow)
        self.bind(size=self.update_glow)
    
    def update_glow(self, *args):
        """Update glow rectangle position and size."""
        self.glow_rect.pos = self.pos
        self.glow_rect.size = self.size
    
    def on_press(self):
        """Handle press - show glow effect."""
        self.is_pressed = True
        self.glow_color.a = 0.3
        self.background_color = self.base_color + (0.4,)
    
    def on_release(self):
        """Handle release - hide glow effect."""
        self.is_pressed = False
        self.glow_color.a = 0
        self.background_color = self.base_color + (0.05,)
    
    def flash(self, duration=0.1):
        """Flash the lane for visual feedback."""
        from kivy.animation import Animation
        
        self.glow_color.a = 0.5
        anim = Animation(a=0, duration=duration)
        anim.start(self.glow_color)
