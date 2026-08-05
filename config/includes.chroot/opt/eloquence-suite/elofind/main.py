import sys
import os
import argparse
import fnmatch
from datetime import datetime

class FileSearchWorker:
    pass

def cli_search(query, path):
    print(f"🔍 Searching for '{query}' in '{path}'...")
    count = 0
    for dirpath, _, filenames in os.walk(path):
        for fname in filenames:
            if query.lower() in fname.lower():
                full_path = os.path.join(dirpath, fname)
                print(f"  └─ {full_path}")
                count += 1
    print(f"Found {count} matching files.")

def run_gui():
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, 
        QHBoxLayout, QPushButton, QLabel, QLineEdit, QTableWidget,
        QTableWidgetItem, QFileDialog, QHeaderView, QCheckBox, QMessageBox
    )
    from PyQt6.QtCore import Qt, QThread, pyqtSignal

    class WorkerThread(QThread):
        result_found = pyqtSignal(dict)
        finished_search = pyqtSignal(int)

        def __init__(self, root_dir, pattern, match_case=False):
            super().__init__()
            self.root_dir = root_dir
            self.pattern = pattern
            self.match_case = match_case
            self.is_cancelled = False

        def run(self):
            count = 0
            search_pattern = self.pattern if self.match_case else self.pattern.lower()

            for dirpath, _, filenames in os.walk(self.root_dir):
                if self.is_cancelled:
                    break
                for fname in filenames:
                    if self.is_cancelled:
                        break
                    check_name = fname if self.match_case else fname.lower()
                    if fnmatch.fnmatch(check_name, f"*{search_pattern}*"):
                        full_path = os.path.join(dirpath, fname)
                        try:
                            stat = os.stat(full_path)
                            size_kb = round(stat.st_size / 1024, 1)
                            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                            self.result_found.emit({
                                "name": fname,
                                "path": full_path,
                                "size": f"{size_kb} KB",
                                "modified": mod_time
                            })
                            count += 1
                        except Exception:
                            continue

            self.finished_search.emit(count)

        def cancel(self):
            self.is_cancelled = True

    class ElofindWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.worker = None
            self.init_ui()

        def init_ui(self):
            self.setWindowTitle("Elofind - Eloquence File Finder")
            self.resize(850, 550)

            central_widget = QWidget()
            main_layout = QVBoxLayout()

            search_layout = QHBoxLayout()
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Search files by name...")
            self.search_input.returnPressed.connect(self.start_search)

            self.dir_input = QLineEdit(os.path.expanduser("~"))
            self.btn_browse = QPushButton("📁 Browse")
            self.btn_browse.clicked.connect(self.browse_directory)

            self.btn_search = QPushButton("🔍 Search")
            self.btn_search.setStyleSheet("background-color: #3aafa9; color: white; font-weight: bold; padding: 6px 15px;")
            self.btn_search.clicked.connect(self.start_search)

            search_layout.addWidget(QLabel("Query:"))
            search_layout.addWidget(self.search_input)
            search_layout.addWidget(QLabel("In:"))
            search_layout.addWidget(self.dir_input)
            search_layout.addWidget(self.btn_browse)
            search_layout.addWidget(self.btn_search)
            main_layout.addLayout(search_layout)

            options_layout = QHBoxLayout()
            self.case_checkbox = QCheckBox("Case Sensitive")
            options_layout.addWidget(self.case_checkbox)
            self.status_label = QLabel("Ready")
            self.status_label.setStyleSheet("color: #a0aab2;")
            options_layout.addStretch()
            options_layout.addWidget(self.status_label)
            main_layout.addLayout(options_layout)

            self.table = QTableWidget(0, 4)
            self.table.setHorizontalHeaderLabels(["File Name", "Directory Path", "Size", "Modified Date"])
            self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            self.table.cellDoubleClicked.connect(self.open_file_location)
            main_layout.addWidget(self.table)

            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

            self.setStyleSheet("""
                QMainWindow { background-color: #17252a; }
                QLabel { color: #edf2f4; font-weight: bold; }
                QLineEdit { background-color: #2b2d42; color: #edf2f4; border: 1px solid #3aafa9; border-radius: 4px; padding: 6px; }
                QPushButton { border-radius: 4px; padding: 6px; font-weight: bold; }
                QTableWidget { background-color: #2b2d42; color: #edf2f4; gridline-color: #3aafa9; }
                QHeaderView::section { background-color: #17252a; color: #3aafa9; font-weight: bold; padding: 4px; }
                QCheckBox { color: #edf2f4; }
            """)

        def browse_directory(self):
            folder = QFileDialog.getExistingDirectory(self, "Select Directory", self.dir_input.text())
            if folder:
                self.dir_input.setText(folder)

        def start_search(self):
            query = self.search_input.text().strip()
            root_dir = self.dir_input.text().strip()

            if not query:
                QMessageBox.warning(self, "Input Error", "Please enter a search query.")
                return

            if not os.path.isdir(root_dir):
                QMessageBox.warning(self, "Directory Error", "The selected directory does not exist.")
                return

            if self.worker and self.worker.isRunning():
                self.worker.cancel()

            self.table.setRowCount(0)
            self.status_label.setText("Searching...")
            self.btn_search.setEnabled(False)

            self.worker = WorkerThread(root_dir, query, self.case_checkbox.isChecked())
            self.worker.result_found.connect(self.add_result)
            self.worker.finished_search.connect(self.search_finished)
            self.worker.start()

        def add_result(self, data):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(data["name"]))
            self.table.setItem(row, 1, QTableWidgetItem(data["path"]))
            self.table.setItem(row, 2, QTableWidgetItem(data["size"]))
            self.table.setItem(row, 3, QTableWidgetItem(data["modified"]))

        def search_finished(self, total_found):
            self.status_label.setText(f"Search complete: {total_found} files found.")
            self.btn_search.setEnabled(True)

        def open_file_location(self, row, col):
            file_path = self.table.item(row, 1).text()
            if os.path.exists(file_path):
                folder = os.path.dirname(file_path)
                if sys.platform == "darwin":
                    os.system(f'open "{folder}"')
                elif sys.platform.startswith("linux"):
                    os.system(f'xdg-open "{folder}" &')
                elif sys.platform == "win32":
                    os.startfile(folder)

    app = QApplication(sys.argv)
    window = ElofindWindow()
    window.show()
    sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="Elofind - Eloquence GNU/Linux File Search Utility")
    parser.add_argument("-q", "--query", help="Search query string", default=None)
    parser.add_argument("-p", "--path", help="Directory path to search", default=".")
    args, unknown = parser.parse_known_args()

    if args.query:
        cli_search(args.query, args.path)
    else:
        run_gui()

if __name__ == "__main__":
    main()
