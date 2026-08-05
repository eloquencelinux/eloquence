import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QTextEdit, QFileDialog, 
    QMessageBox, QToolBar, QFontComboBox, QSpinBox, QStatusBar,
    QTabWidget
)
from PyQt6.QtGui import QFont, QTextCharFormat, QAction, QIcon, QColor
from PyQt6.QtCore import Qt

class EloofficeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_filepath = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Elooffice - Eloquence Document Editor")
        self.resize(900, 600)

        # Main Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Toolbar
        self.toolbar = QToolBar("Editor Formatting")
        self.addToolBar(self.toolbar)

        # File Actions
        new_action = QAction("📄 New", self)
        new_action.triggered.connect(self.new_file)
        self.toolbar.addAction(new_action)

        open_action = QAction("📂 Open", self)
        open_action.triggered.connect(self.open_file)
        self.toolbar.addAction(open_action)

        save_action = QAction("💾 Save", self)
        save_action.triggered.connect(self.save_file)
        self.toolbar.addAction(save_action)

        self.toolbar.addSeparator()

        # Text Formatting Actions
        bold_action = QAction("<b>B</b>", self)
        bold_action.triggered.connect(self.toggle_bold)
        self.toolbar.addAction(bold_action)

        italic_action = QAction("<i>I</i>", self)
        italic_action.triggered.connect(self.toggle_italic)
        self.toolbar.addAction(italic_action)

        underline_action = QAction("<u>U</u>", self)
        underline_action.triggered.connect(self.toggle_underline)
        self.toolbar.addAction(underline_action)

        self.toolbar.addSeparator()

        # Font size picker
        self.size_picker = QSpinBox()
        self.size_picker.setRange(8, 72)
        self.size_picker.setValue(12)
        self.size_picker.valueChanged.connect(self.change_font_size)
        self.toolbar.addWidget(QLabel(" Size: "))
        self.toolbar.addWidget(self.size_picker)

        # Tab Widget (Editor vs Markdown Preview)
        self.tabs = QTabWidget()
        
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Inter", 12))
        self.editor.textChanged.connect(self.update_status)
        self.tabs.addTab(self.editor, "📝 Rich Editor")

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.tabs.addTab(self.preview, "👁 Markdown Preview")
        self.tabs.currentChanged.connect(self.tab_changed)

        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status()

        # Styling
        self.setStyleSheet("""
            QMainWindow { background-color: #17252a; }
            QToolBar { background-color: #2b2d42; border-bottom: 1px solid #3aafa9; padding: 4px; }
            QToolBar QToolButton { color: #edf2f4; font-weight: bold; margin: 0 4px; }
            QTabWidget::pane { border: 1px solid #3aafa9; background-color: #2b2d42; }
            QTabBar::tab { background-color: #17252a; color: #edf2f4; padding: 8px 16px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background-color: #3aafa9; color: #17252a; font-weight: bold; }
            QTextEdit { background-color: #2b2d42; color: #edf2f4; border: none; padding: 10px; font-size: 14px; }
            QStatusBar { background-color: #17252a; color: #a0aab2; font-size: 12px; }
        """)

    def new_file(self):
        self.editor.clear()
        self.current_filepath = None
        self.setWindowTitle("Elooffice - Untitled Document")

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open Document", "", "Text/Markdown Files (*.txt *.md *.html);;All Files (*)")
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self.editor.setPlainText(content)
                self.current_filepath = filepath
                self.setWindowTitle(f"Elooffice - {os.path.basename(filepath)}")
            except Exception as e:
                QMessageBox.critical(self, "Error Opening File", str(e))

    def save_file(self):
        if not self.current_filepath:
            filepath, _ = QFileDialog.getSaveFileName(self, "Save Document", "document.md", "Markdown (*.md);;Text (*.txt);;HTML (*.html)")
            if not filepath:
                return
            self.current_filepath = filepath

        try:
            with open(self.current_filepath, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.setWindowTitle(f"Elooffice - {os.path.basename(self.current_filepath)}")
            QMessageBox.information(self, "Saved", "Document successfully saved.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if self.editor.fontWeight() != QFont.Weight.Bold else QFont.Weight.Normal)
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(not self.editor.fontItalic())
        self.editor.mergeCurrentCharFormat(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(not self.editor.fontUnderline())
        self.editor.mergeCurrentCharFormat(fmt)

    def change_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(float(size))
        self.editor.mergeCurrentCharFormat(fmt)

    def tab_changed(self, index):
        if index == 1:
            raw_text = self.editor.toPlainText()
            self.preview.setMarkdown(raw_text)

    def update_status(self):
        text = self.editor.toPlainText()
        words = len(text.split())
        chars = len(text)
        filename = os.path.basename(self.current_filepath) if self.current_filepath else "Untitled"
        self.status_bar.showMessage(f"File: {filename}  |  Words: {words}  |  Characters: {chars}")

def main():
    app = QApplication(sys.argv)
    window = EloofficeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
