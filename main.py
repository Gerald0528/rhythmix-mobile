"""
Rhythmix Mobile - Main Application
Converts pygame rhythm game to Kivy for Android/iOS
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp

# Import screens
from screens.menu import MenuScreen
from screens.level_select import LevelSelectScreen
from screens.game_screen import GameScreen
from screens.results import ResultsScreen
from screens.settings import SettingsScreen

# Import utils
from utils.config import load_settings, load_scores, load_custom_songs


class RhythmixApp(App):
    """Main application class for Rhythmix rhythm game."""
    
    def build(self):
        """Build and return the app widget tree."""
        # Configure window
        Window.clearcolor = (0.047, 0.047, 0.086, 1)  # BG_COLOR
        
        # Keep screen on for mobile
        if platform == 'android':
            self._keep_screen_on()
        
        # Load data
        load_settings()
        load_scores()
        load_custom_songs()
        
        # Create screen manager
        sm = ScreenManager(transition=SlideTransition())
        
        # Add screens
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(LevelSelectScreen(name='level_select'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultsScreen(name='results'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm
    
    def _keep_screen_on(self):
        """Keep the screen awake during gameplay."""
        try:
            from android.runnable import run_on_ui_thread
            from jnius import autoclass
            
            @run_on_ui_thread
            def _enable():
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                WindowManager = autoclass('android.view.WindowManager')
                activity = PythonActivity.mActivity
                window = activity.getWindow()
                window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
            
            _enable()
        except Exception as e:
            print(f"Could not keep screen on: {e}")
    
    def on_pause(self):
        """Handle app pause - save any critical state."""
        # Notify current screen of pause
        sm = self.root
        if sm and sm.current_screen:
            if hasattr(sm.current_screen, 'on_pause'):
                sm.current_screen.on_pause()
        return True
    
    def on_resume(self):
        """Handle app resume."""
        sm = self.root
        if sm and sm.current_screen:
            if hasattr(sm.current_screen, 'on_resume'):
                sm.current_screen.on_resume()


if __name__ == '__main__':
    RhythmixApp().run()