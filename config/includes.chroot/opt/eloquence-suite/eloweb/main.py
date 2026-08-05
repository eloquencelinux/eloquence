import sys
import os
import argparse

def create_webapp_launcher(name, url):
    print(f"🌐 Creating WebApp launcher for '{name}' -> {url}...")
    desktop_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(desktop_dir, exist_ok=True)
    file_path = os.path.join(desktop_dir, f"eloweb-{name.lower()}.desktop")

    content = f"""[Desktop Entry]
Name={name} (Eloquence WebApp)
Comment=Standalone WebApp for {url}
Exec=python3 -m eloweb.main --url "{url}"
Icon=internet-web-browser
Terminal=false
Type=Application
Categories=Network;WebBrowser;Qt;
"""
    with open(file_path, "w") as f:
        f.write(content)
    os.chmod(file_path, 0o755)
    print(f"[SUCCESS] WebApp launcher created at: {file_path}")

def run_webapp_window(url, title="Eloquence WebApp"):
    from PyQt6.QtWidgets import QApplication, QMainWindow
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtCore import QUrl

    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle(title)
    window.resize(1100, 700)

    web = QWebEngineView()
    web.load(QUrl(url))
    window.setCentralWidget(web)
    window.show()
    sys.exit(app.exec())

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QGroupBox
    )

    class ElowebWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Eloweb - Eloquence WebApp Creator")
            self.resize(700, 420)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            # Header
            title_label = QLabel("🌐 Eloweb Desktop WebApp Creator")
            title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3aafa9;")
            main_layout.addWidget(title_label)

            sub_label = QLabel("Turn any website (ChatGPT, WhatsApp, Notion, Spotify) into a standalone desktop app.")
            sub_label.setStyleSheet("color: #a0aab2; font-size: 13px; margin-bottom: 10px;")
            main_layout.addWidget(sub_label)

            # Form Group
            form_group = QGroupBox("WebApp Configuration")
            form_layout = QVBoxLayout()

            self.name_input = QLineEdit()
            self.name_input.setPlaceholderText("App Name (e.g. ChatGPT, Notion, WhatsApp)")
            
            self.url_input = QLineEdit()
            self.url_input.setPlaceholderText("Website URL (e.g. https://chatgpt.com)")

            form_layout.addWidget(QLabel("Application Name:"))
            form_layout.addWidget(self.name_input)
            form_layout.addWidget(QLabel("Website URL:"))
            form_layout.addWidget(self.url_input)

            form_group.setLayout(form_layout)
            main_layout.addWidget(form_group)

            # Buttons
            btn_layout = QHBoxLayout()
            self.btn_launch = QPushButton("▶ Launch WebApp")
            self.btn_launch.setStyleSheet("background-color: #2b7a78; color: white; padding: 10px; font-weight: bold;")
            self.btn_launch.clicked.connect(self.launch_webapp)

            self.btn_create = QPushButton("➕ Create Desktop Launcher")
            self.btn_create.setStyleSheet("background-color: #3aafa9; color: white; padding: 10px; font-weight: bold;")
            self.btn_create.clicked.connect(self.create_launcher)

            btn_layout.addWidget(self.btn_launch)
            btn_layout.addWidget(self.btn_create)
            main_layout.addLayout(btn_layout)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            # Styling
            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel { color: #edf2f4; font-weight: bold; }
                QLineEdit { background-color: #2b2d42; color: #edf2f4; border: 1px solid #3aafa9; border-radius: 4px; padding: 8px; }
                QGroupBox { color: #3aafa9; font-weight: bold; border: 1px solid #2b7a78; border-radius: 6px; margin-top: 10px; padding: 10px; }
                QPushButton { border-radius: 4px; font-size: 13px; }
            """)

        def launch_webapp(self):
            url = self.url_input.text().strip()
            name = self.name_input.text().strip() or "Eloquence WebApp"
            if not url:
                QMessageBox.warning(self, "Input Error", "Please enter a valid website URL.")
                return
            if not url.startswith("http"):
                url = "https://" + url
            run_webapp_window(url, name)

        def create_launcher(self):
            url = self.url_input.text().strip()
            name = self.name_input.text().strip()
            if not url or not name:
                QMessageBox.warning(self, "Input Error", "Please provide both App Name and Website URL.")
                return
            if not url.startswith("http"):
                url = "https://" + url
            create_webapp_launcher(name, url)
            QMessageBox.information(self, "WebApp Created", f"Standalone desktop app '{name}' created in application menu.")

    app = QApplication(sys.argv)
    window = ElowebWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Eloweb - Eloquence WebApp Creator")
    parser.add_argument("-u", "--url", help="Website URL to launch/convert", default=None)
    parser.add_argument("-n", "--name", help="WebApp name", default="Eloquence WebApp")
    args, unknown = parser.parse_known_args()

    if args.url:
        run_webapp_window(args.url, args.name)
    else:
        run_gui()

if __name__ == "__main__":
    main()
