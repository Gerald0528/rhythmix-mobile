"""
Note rendering utilities for the game canvas.
Handles drawing of different note types (tap, hold, mash).
"""

from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.metrics import dp

from utils.config import LANE_COLORS, WHITE


class NoteRenderer:
    """Handles rendering of notes on the game canvas."""
    
    @staticmethod
    def render_tap_note(canvas, lane, x, y, width, height, color, alpha=1.0):
        """Render a tap note."""
        with canvas:
            # Main body
            Color(color[0], color[1], color[2], alpha)
            RoundedRectangle(
                pos=(x, y - height / 2),
                size=(width, height),
                radius=[dp(8)]
            )
            # Shine effect
            Color(
                min(1, color[0] + 0.3),
                min(1, color[1] + 0.3),
                min(1, color[2] + 0.3),
                alpha
            )
            RoundedRectangle(
                pos=(x + dp(4), y - height / 2 + dp(3)),
                size=(width - dp(8), dp(6)),
                radius=[dp(3)]
            )
    
    @staticmethod
    def render_hold_body(canvas, x, y_top, y_bottom, width, color, alpha=0.5):
        """Render the body of a hold note."""
        height = y_bottom - y_top
        if height > 0:
            with canvas:
                # Main body
                Color(color[0], color[1], color[2], alpha)
                Rectangle(pos=(x, y_top), size=(width, height))
                # Border
                Color(color[0], color[1], color[2], alpha + 0.3)
                Line(rectangle=(x, y_top, width, height), width=1)
    
    @staticmethod
    def render_hold_head(canvas, lane, x, y, width, height, color, alpha=1.0):
        """Render the head of a hold note."""
        with canvas:
            Color(color[0], color[1], color[2], alpha)
            RoundedRectangle(
                pos=(x, y - height / 2),
                size=(width, height),
                radius=[dp(8)]
            )
    
    @staticmethod
    def render_hold_tail(canvas, x, y, width, height, color, alpha=1.0):
        """Render the tail of a hold note."""
        c_dim = (
            max(0, color[0] - 0.2),
            max(0, color[1] - 0.2),
            max(0, color[2] - 0.2)
        )
        with canvas:
            Color(c_dim[0], c_dim[1], c_dim[2], alpha)
            RoundedRectangle(
                pos=(x, y - height / 2),
                size=(width, height),
                radius=[dp(5)]
            )
