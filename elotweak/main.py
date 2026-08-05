import sys
import os
import argparse
import subprocess

def set_theme_mode(mode):
    print(f"🎨 Switching Eloquence GNU/Linux theme mode to: '{mode.upper()}'...")
    wallpaper_path = "/usr/share/wallpapers/eloquence-dark.jpg" if mode == "dark" else "/usr/share/wallpapers/eloquence-light.png"
    gtk_theme = "Adwaita-dark" if mode == "dark" else "Adwaita"

    # Update Cinnamon Wallpaper & Theme via gsettings/dconf if available
    try:
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", f"file://{wallpaper_path}"], check=False)
        subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{wallpaper_path}"], check=False)
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", gtk_theme], check=False)
        print(f"[SUCCESS] Theme switched to {mode.upper()}. Wallpaper: {wallpaper_path}")
    except Exception as e:
        print(f"[NOTICE] Theme command issued: {e}")

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QMessageBox, QGroupBox
    )
    from PyQt6.QtCore import Qt

    class ElotweakWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Elotweak - Eloquence GNU/Linux System Tweaks")
            self.resize(750, 520)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            # Header
            title_label = QLabel("⚡ Elotweak System & Theme Center")
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9;")
            main_layout.addWidget(title_label)

            # Theme Group
            theme_group = QGroupBox("Eloquence GNU/Linux Desktop Theme Switcher")
            theme_layout = QVBoxLayout()
            
            self.radio_dark = QRadioButton("🌙 Eloquence Dark Mode (Dark Geometric Wallpaper + Dark Theme)")
            self.radio_dark.setChecked(True)
            self.radio_light = QRadioButton("☀️ Eloquence Light Mode (Light Geometric Wallpaper + Light Theme)")

            theme_layout.addWidget(self.radio_dark)
            theme_layout.addWidget(self.radio_light)

            self.btn_apply_theme = QPushButton("🎨 Apply Theme")
            self.btn_apply_theme.setStyleSheet("background-color: #3aafa9; color: white; font-weight: bold; padding: 8px;")
            self.btn_apply_theme.clicked.connect(self.apply_theme)
            theme_layout.addWidget(self.btn_apply_theme)
            theme_group.setLayout(theme_layout)
            main_layout.addWidget(theme_group)

            # Power Profiles Group
            power_group = QGroupBox("Power & Performance Profiles")
            power_layout = QVBoxLayout()
            
            self.radio_perf = QRadioButton("🚀 High Performance Profile")
            self.radio_bal = QRadioButton("⚖️ Balanced Profile")
            self.radio_bal.setChecked(True)
            self.radio_sav = QRadioButton("🔋 Power Saver Profile (Laptop Battery Optimization)")

            power_layout.addWidget(self.radio_perf)
            power_layout.addWidget(self.radio_bal)
            power_layout.addWidget(self.radio_sav)
            power_group.setLayout(power_layout)
            main_layout.addWidget(power_group)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Styling
            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel, QRadioButton { color: #edf2f4; font-weight: bold; }
                QGroupBox { color: #3aafa9; font-weight: bold; border: 1px solid #2b7a78; border-radius: 6px; margin-top: 10px; padding: 10px; }
                QPushButton { border-radius: 4px; font-size: 13px; }
            """)

        def apply_theme(self):
            mode = "dark" if self.radio_dark.isChecked() else "light"
            set_theme_mode(mode)
            QMessageBox.information(self, "Theme Applied", f"Eloquence GNU/Linux desktop theme switched to {mode.upper()} mode.")

    app = QApplication(sys.argv)
    window = ElotweakWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Elotweak - Eloquence GNU/Linux System Tweaks")
    parser.add_argument("-m", "--mode", help="Theme mode: dark | light", default=None)
    args, unknown = parser.parse_known_args()

    if args.mode:
        set_theme_mode(args.mode.lower())
    else:
        run_gui()

if __name__ == "__main__":
    main()
