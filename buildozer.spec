[app]
title = Rhythmix
package.name = rhythmix
package.domain = com.rhythmix.game
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,json,ttf,otf
version = 2.0.0
requirements = python3,kivy,kivymd,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WAKE_LOCK
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a
android.allow_backup = True
android.logcat_filters = *:S python:D
android.p4a_local_recipes =
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.NoTitleBar
p4a.local_recipes =
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
window_icon =

[buildozer]
log_level = 2
warn_on_root = 1